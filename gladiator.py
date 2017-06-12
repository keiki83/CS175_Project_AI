import MalmoPython
import os
import sys
import time
import random
import json
import math
from sarsa import perform_trial
from collections import namedtuple


State = namedtuple('State', 'x, z, hit, mob_hit, health')
EntityInfo = namedtuple('EntityInfo', 'x, y, z, yaw, pitch, name, colour, variation, quantity, life')
EntityInfo.__new__.__defaults__ = (0, 0, 0, 0, 0, "", "", "", 1, 0)


# trial parameters
DEFAULT_NUM_TRIALS = 500
EPSILON = 0.1
AGENT = "Gladiator"
DEFAULT_MISSION = "arena2.xml"
SIDE_ATTACK = True
HEALTH_CRITICAL_LEVEL = 10.
ENABLE_ENEMY_DISTANCE_SATURATION = True
ENEMY_DISTANCE_SATURATION_LEVEL = 10
STATISTICS_OUTPUT_FILE = "statistics.txt"
QTABLE_FILENAME = "q_table.p"
MOB_TYPE = "Zombie"
MOB_START_LOCATION = [(8,64,8),(-8,64,8),(8,64,-8),(-8,64,-8)]
MOVESPEED = 1.0
ACTION_DELAY = 0.1
HEALTH_THRESHOLDS = ((20., 0), (15., 1), (10., 2), (5., 3), (0., 4))
actions = ["move " + str(MOVESPEED) , "move " + str(-1*MOVESPEED), "strafe " + str(MOVESPEED), "strafe " + str(-1*MOVESPEED), "attack 1"]
air_actions = {actions[0]:1, actions[1]:2, actions[2]:4, actions[3]:8}
# rewards
DEATH_REWARD = -50.
PROXIMITY_REWARD = 10
ENEMY_HIT_REWARD = 25
DAMAGE_REWARD = -ENEMY_HIT_REWARD / HEALTH_THRESHOLDS[-1][1] #scale penalty based on relative health
TICK_REWARD = 1
#SATURATION_REWARD = -MAX_ENEMY_PROXIMITY_REWARD



# helper functions
def checkMobHit(lifePrime):
	try:
		hit = (lifePrime < checkMobHit.life)
		checkMobHit.life = lifePrime
	except AttributeError:
		checkMobHit.life = lifePrime
		hit = False
	return hit

def checkHit(lifePrime):
	try:
		hit = (lifePrime < checkHit.life)
		checkHit.life = lifePrime
		if lifePrime <= 0:
			agent_host.sendCommand("chat I'm dead!")
	except AttributeError:
		checkHit.life = lifePrime
		hit = False
	return hit

def countMobs(entities):
	mobCount = 0
	for ent in entities:
		if ent.name == MOB_TYPE:
			mobCount += 1
	return mobCount

def findUs(entities):
	for ent in entities:
		if ent.name == MOB_TYPE:
			continue
		else:
			return ent

def lookAtNearestEntity(entities):
    us = findUs(entities)
    current_yaw = us.yaw
    closestEntity = 0
    entityDistance = sys.float_info.max
    for i,ent in enumerate(entities):
        if ent.name == MOB_TYPE:
            #check distance from us and get the lowest
            dist = math.sqrt((ent.x - us.x)*(ent.x - us.x) + (ent.z - us.z)*(ent.z - us.z))
            if(dist < entityDistance):
                closestEntity = i
                entityDistance = dist
    if closestEntity == 0:
        return 0
    best_yaw = math.degrees(math.atan2(entities[closestEntity].z - us.z, entities[closestEntity].x - us.x)) - 90
    difference = best_yaw - current_yaw;
    while difference < -180:
        difference += 360;
    while difference > 180:
        difference -= 360;
    difference /= 180.0;
    threshhold = 0.0
    if difference < threshhold and difference > 0:
    	difference = threshhold
    elif difference > -1*threshhold and difference < 0:
    	difference = -1*threshhold

    agent_host.sendCommand("turn " + str(difference))

#assumes there is a single mob near the agent. gets it x and z coordinates and returns the x and z coordinates relative to the agent
def extractMobState(entities):
    #res = 4
    life = 0
    for entity in [EntityInfo(**k) for k in entities]:
        if entity.name == AGENT:
            m_x = a_x = entity.x
            m_z = a_z = entity.z
        elif entity.name == MOB_TYPE:
            m_x = entity.x
            m_z = entity.z
            life = entity.life
    x = round(m_x - a_x)
    z = round(m_z - a_z)
    if ENABLE_ENEMY_DISTANCE_SATURATION:
        if abs(x) > ENEMY_DISTANCE_SATURATION_LEVEL:
            x = math.copysign(ENEMY_DISTANCE_SATURATION_LEVEL, x)
        if abs(z) > ENEMY_DISTANCE_SATURATION_LEVEL:
            z = math.copysign(ENEMY_DISTANCE_SATURATION_LEVEL, z)
    return life,x,z

def extractHealthState(health):
    for threshold,state in HEALTH_THRESHOLDS:
        if health >= threshold: return state

# this is where the rewards are counted and the state is determined
def getState():
    world_state = agent_host.getWorldState()
    while world_state.is_mission_running and len(world_state.observations) == 0:
        time.sleep(0.1)
        world_state = agent_host.getWorldState()
    if world_state.is_mission_running:
        msg = world_state.observations[-1].text
        ob = json.loads(msg)

       	#check for hit here
        health = ob[u'Life']
       	hit = checkHit(health)
        mob_life, mob_x, mob_z = extractMobState(ob[u'entities'])
        mob_hit = checkMobHit(mob_life)

        s = State(mob_x, mob_z, hit, mob_hit, extractHealthState(health))
    else:
        s = None
        ob = None
    return s, ob

def isTerminal(state):
    return (state is None) or (not world_state.is_mission_running) or (checkHit.life <= 0.)  #or (state.x == 0. and state.z == 0.)

def calculate_reward(state, s_prime, action):
    reward = 0
    if state.hit:
    	reward += DAMAGE_REWARD * state.health
    if state.mob_hit:
    	reward += ENEMY_HIT_REWARD
    #health related rewards
    if checkHit.life <= 0.:
        reward += DEATH_REWARD

    #distance related rewards
    state_distance = math.sqrt(state.x**2 + state.z**2)
    prime_distance = math.sqrt(s_prime.x**2 + s_prime.z**2)
    reward += PROXIMITY_REWARD * (prime_distance - state_distance)
#    if not (state.x == 0 and state.z == 0):
#        if abs(state.x) >= ENEMY_DISTANCE_SATURATION_LEVEL or abs(state.z) >= ENEMY_DISTANCE_SATURATION_LEVEL:
#            reward += SATURATION_REWARD
#        else:
#            reward += (MAX_ENEMY_PROXIMITY_REWARD / math.sqrt(state.x**2 + state.z**2))
#    else:
#        reward += MAX_ENEMY_PROXIMITY_REWARD

    #movement related penalties
    reward += TICK_REWARD
    #if action == "move " + str(MOVESPEED) and not hit:
    #	reward += 1
    #if action != "move " + str(MOVESPEED) and math.sqrt(state.x**2 + state.z**2) > ENEMY_DISTANCE_SATURATION_LEVEL:
    #	reward += -1

    global cumulative_reward
    cumulative_reward = cumulative_reward + reward
    return reward

def do_action(state, action):
    global ticksElapsed
    ticksElapsed = ticksElapsed + 1

    #if "strafe" in action and SIDE_ATTACK:
    #    agent_host.sendCommand("attack 1")

    s_prime, ob = getState()
    if not state is None:

        # turn towards the nearest zombie
        lookAtNearestEntity([EntityInfo(**k) for k in ob[u'entities']])

        # take action
        agent_host.sendCommand("move 0")
        agent_host.sendCommand("strafe 0")
        agent_host.sendCommand(action)

        reward = calculate_reward(state, s_prime, action)

        #automatically spawn a new mob if there is none
        if(countMobs([EntityInfo(**k) for k in ob[u'entities']]) == 0): #summon mobs if their are no more on the field
            a = ( int(random.random() * 4) % 4)
            agent_host.sendCommand("chat /summon {0} {1} {2} {3} {4}".format(MOB_TYPE, MOB_START_LOCATION[a][0], MOB_START_LOCATION[a][1], MOB_START_LOCATION[a][2], "{IsBaby:0}")) #summon mob
            global killCount
            killCount = killCount + 1
            time.sleep(0.3)



        #taunt enemy
        x = random.random()
        if x < 0.01:
        	if x < 0.0025:
        		agent_host.sendCommand("chat Are you not entertained?!")
        	elif x < 0.005:
        		agent_host.sendCommand("chat You are weak!")
        	else:
        	    agent_host.sendCommand("chat Come at me!!!")

    else:
        reward = 0
    time.sleep(ACTION_DELAY)
    return reward, s_prime, actions

def load_mission(fileName):
    # load mission from file
    my_mission = None
    my_mission_record = None
    with open(fileName, 'r') as f:
        print "Loading mission from %s" % fileName
        mission_xml = f.read()
        my_mission = MalmoPython.MissionSpec(mission_xml, True)
    #my_mission.forceWorldReset()    # force reset fixes back to back testing
        my_mission_record = MalmoPython.MissionRecordSpec()
    return my_mission, my_mission_record

def start_mission(agent_host, mission, mission_record):
# Attempt to start a mission:
    max_retries = 3
    for retry in range(max_retries):
    	try:
    		agent_host.startMission( mission, mission_record )
    		break
    	except RuntimeError as e:
    		if retry == max_retries - 1:
    			print "Error starting mission:",e
    			exit(1)
    		else:
    			time.sleep(2)
    # Loop until mission starts:
    print "Waiting for the mission to start ",
    world_state = agent_host.getWorldState()
    while not world_state.has_mission_begun:
    	sys.stdout.write(".")
    	time.sleep(0.1)
    	world_state = agent_host.getWorldState()
    	for error in world_state.errors:
    		print "Error:",error.text

    print
    print "Mission running ",



if __name__ == "__main__":
    # start of execution
    sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)  # flush print output immediately
    # Create default Malmo objects:
    agent_host = MalmoPython.AgentHost()
    try:
    	agent_host.parse( sys.argv )
    except RuntimeError as e:
    	print 'ERROR:',e
    	print agent_host.getUsage()
    	exit(1)
    if agent_host.receivedArgument("help"):
    	print agent_host.getUsage()
    	exit(0)
    my_mission, my_mission_record = load_mission(DEFAULT_MISSION)

    # Main loop:
    # Loop until mission ends:
    q_table = {}
    rewards = []
    cumulative_reward = 0.
    kills = []
    killCount = 0
    times = []
    ticksElapsed = 0

    start_mission(agent_host, my_mission, my_mission_record) #start mission
    world_state = agent_host.getWorldState()
    i = 0
    e = EPSILON
    while world_state.is_mission_running and i < DEFAULT_NUM_TRIALS:
    	print "epsilon: {}".format(e)
    	#summon a mob in a random corner
    	a = (int(random.random() * 4) % 4)
        agent_host.sendCommand("chat /summon {0} {1} {2} {3} {4}".format(MOB_TYPE, MOB_START_LOCATION[a][0], MOB_START_LOCATION[a][1], MOB_START_LOCATION[a][2], "{IsBaby:0}")) #summon mob
        time.sleep(0.3)

        #start of SARSA
        s,_ = getState()
        q_table = perform_trial(s, actions, do_action, isTerminal, q_table, epsilon = e)
        print "Trial {} finished.".format(i+1)
        world_state = agent_host.getWorldState()
        if world_state.is_mission_running:
            agent_host.sendCommand("quit")

        #get statistics here
        rewards.append(cumulative_reward)
        kills.append(killCount)
        times.append(ticksElapsed)
        print "Cumulative reward: {}".format(cumulative_reward)
        print "Kill count: {}".format(killCount)
        print "Actions performed: {}".format(ticksElapsed)
        cumulative_reward = 0.
        killCount = 0
        ticksElapsed = 0
        time.sleep(1)
        start_mission(agent_host, my_mission, my_mission_record) #restart mission
        world_state = agent_host.getWorldState()
        i += 1
        #e *= 0.85

    with open(STATISTICS_OUTPUT_FILE, 'w') as f:
        for r in rewards:
            f.write("{} ".format(r))
        f.write("\n")
        for k in kills:
            f.write("{} ".format(k))
        f.write("\n")
        for t in times:
        	f.write("{} ".format(t))

    # mission has ended.
    for error in world_state.errors:
        print "Error:", error.text

    print "Mission ended"
    # Mission has ended.
    time.sleep(1)  # Give mod some time.
