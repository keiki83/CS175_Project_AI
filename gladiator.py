import MalmoPython
import os
import sys
import time
import random
import json
import math
import cPickle as pickle
from sarsa import perform_trial
# import Tkinter as tk   #for drawing gamestate on canvas
from collections import namedtuple
#State = namedtuple('State', 'air, health, x, z')
State = namedtuple('State', 'x, z')

EntityInfo = namedtuple('EntityInfo', 'x, y, z, yaw, pitch, name, colour, \
    variation, quantity, life')
EntityInfo.__new__.__defaults__ = (0, 0, 0, 0, 0, "", "", "", 1, 0)

MOVESPEED = 0.33
AGGRO_RANGE = 5
#actions = ["movenorth 1", "movesouth 1", "moveeast 1", "movewest 1", "nothing"]
actions = ["move " + str(MOVESPEED) , "move " + str(-1*MOVESPEED), "strafe " + str(MOVESPEED), "strafe " + str(-1*MOVESPEED), "attack 1"]

air_indices = {1:1, 3:2, 5:4, 7:8}
air_actions = {"movenorth 1":1, "movewest 1":2, "moveeast 1":4, "movesouth 1":8}
# define parameters here
MOB_TYPE = "Zombie"
MOB_START_LOCATION = (5.5,64,-28)
AGENT = "Gladiator"
DEFAULT_MISSION = "arena2.xml"
DEFAULT_NUM_TRIALS = 500

WALL_MOVE_PENALTY = -10.
MOVE_PENALTY = -1.

DAMAGE_PENALTY = -20.
DEATH_PENALTY = -100.

MAX_ENEMY_PROXIMITY_REWARD = 3
ENEMY_HIT_REWARD = 50
ENEMY_DEATH_REWARD = 200.

ENABLE_ENEMY_DISTANCE_SATURATION = False
ENEMY_DISTANCE_SATURATION_LEVEL = 3
ENABLE_KNOCKBACK_RESISTANCE = False
KNOCKBACK_RESIST_COMMAND = "/replaceitem entity @p slot.armor.feet leather_boots 1 0 {AttributeModifiers:{AttributeName:generic.knockbackResistance, Amount:1, Operation:0}}"
REWARD_OUTPUT_FILE = "rewards.txt"
QTABLE_FILENAME = "q_table.p"
ACTION_DELAY = 0.0
cumulative_reward = 0.
# Sarsa Related Functions

# calculateReward helper function
#def distance(playerLoc, ent):
    # helper function for reward()
    #return math.sqrt((ent.x - playerLoc[0])**2 + (ent.z - playerLoc[1])**2)

# reward is 45 for being at same location as the entity, reward is 1 for
# maximum agro range of entity Distance reward is less than 1 for distances
# greater than agro range reward is 0 if no entity detected
#def calculateReward(entities, playerLoc):
#    closestMob = Null
#    dist = float('inf')
#    for ent in entities:
#        if(closestMob == Null and ent.name != AGENT):
#            closetMob == ent
#            continue
#        if(distance(playerLoc, ent) < dist and ent.name == MOB_TYPE):
#            closestMob = ent
#            dist = distance(playerLoc, ent)
#    reward = 0
#    if(closestMob == Null):
#        return reward
#    if(distance(playerLoc, ent) == 0):
#        reward = 45
#    else:
#        reward = 45/distance(playerLoc, ent)
#    return reward


# helper function
#def isAir(s, actionIndex):
#    if(actionIndex >= 0 and actionIndex < len(s) and
#            s[actionIndex] == "air"):
#        return True
#    else:
#        return False


#def swapIndex(s, fromIndex, toIndex):
#    temp = s[toIndex]
#    s[toIndex] = s[fromIndex]
#    s[fromIndex] = s[toIndex]
#    return s


def availableActions(s_prime):
    actions_prime = actions
    #actions_prime = []
    #dim = int(math.sqrt(len(s_prime)))
    #
    # locate agent
    #agentIndex = -1
    #for i in range(0,len(s_prime)):
    #    if(s_prime[i] == AGENT):
    #        agentIndex = i
    #        break
    #offset = [-dim, dim, 1, -1]  # north, south, east, west
    #for i in range(0, len(actions)-1):
    #    if(isAir(s_prime, agentIndex + offset[i])):
    #        actions_prime.append(actions[i])
    #actions_prime.append(actions[len(actions) - 1])

    return actions_prime


#def perform(s,action):
    # perform = function which takes an action as a parameter and returns:
    #    reward, s_prime, valid actions from s_prime
    # NOTES: modify s_prime array by action
    #        do not allow a move into a non air block, penalize
    #        north = -z, south = +z inc/dec by dim
    #        east = +x, west = -x inc/dec by 1
#    reward = 0
#    s_prime = list(s)
#    actions_prime = actions
#    dim = int(math.sqrt(len(s_prime)))

    # locate agent
#    agentIndex = -1
#    for i in range(0,len(s_prime)):
#        if(s_prime[i] == AGENT):
#            agentIndex = i
#            break

    # carry out action
#    if(action != "nothing"):
#        if(action == "movenorth 1"):  # -z axis (-dim)
#            actionIndex = agentIndex - dim
#            if(isAir(s_prime, actionIndex)):
#                s_prime = swapIndex(s_prime, agentIndex, actionIndex)
                # calculate reward
#                reward = 1  # place holder
#            else:
                # penalize e.g. move into zombie / move into wall
#                reward = -1  # place holder
#        if(action == "movesouth 1"):  # +z axis (+dim)
#            actionIndex = agentIndex + dim
#            if(isAir(s_prime, actionIndex)):
#                s_prime = swapIndex(s_prime, agentIndex, actionIndex)
                # calculate reward
#                reward = 1  # place holder
#            else:
                # penalize e.g. move into zombie / move into wall
#                reward = -1  # place holder
#        if(action == "moveeast 1"):  # +x axis (+1)
#            actionIndex = agentIndex + 1
#            if(isAir(s_prime, actionIndex)):
#                s_prime = swapIndex(s_prime, agentIndex, actionIndex)
                # calculate reward
#                reward = 1  # place holder
#            else:
                # penalize e.g. move into zombie / move into wall
#                reward = -1  # place holder
#        if(action == "movewest 1"):  # -x axis (-1)
#            actionIndex = agentIndex - 1
#            if(isAir(s_prime, actionIndex)):
#                s_prime = swapIndex(s_prime, agentIndex, actionIndex)
                # calculate reward
#                reward = 1  # place holder
#            else:
                # penalize e.g. move into zombie / move into wall
#                reward = -1  # place holder

    # determine available movements
#    actions_prime = availableActions(s_prime)
#    return reward, s_prime, actions_prime

# # controls maximum itterations of sarsa_trial
# def is_terminal(state):
#     return (state[0] >= state[1])

# generate the statespace for sarsa
#def generateStateSpace(grid, entities):
#    dim = math.sqrt(len(grid))
#    playerIndex = int(dim*(dim//2) + dim//2)
#    agent  = 0
#    for ent in entities:
#        if ent.name == AGENT:
#            agent = ent
#            break
#    grid[playerIndex] = agent.name
#    for ent in entities:
#        if ent.name == MOB_TYPE:
#            entIndex = int(playerIndex + dim*(ent.z-agent.z) + (ent.x - agent.x))
#            if(entIndex >= 0 or entIndex < len(grid)):
#                grid[entIndex] = ent.name
#    return grid

# get best action to take
#def getAction(q_table, state):
#    action = 0
#    value = float('-inf')
#    for key in q_table:
#        if(key[0] == repr(state) and q_table[key] > value):
#            action = key[1]
#            value = q_table[key]
#    return action


# perform action in game for agent
#def performAction(agent_host, action):
#    if (action == "nothing"):
#        return
#    else:
#        agent_host.sendCommand(action)
#    return



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
            dist = (ent.x - us.x)*(ent.x - us.x) + (ent.z - us.z)*(ent.z - us.z)
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
    threshhold = 0.02
    if difference < threshhold and difference > 0:
    	difference = threshhold
    elif difference > -1*threshhold and difference < 0:
    	difference = -1*threshhold

    agent_host.sendCommand("turn " + str(difference))

def extractAirState(grid):
    s = 0
    for k,v in air_indices.items():
        if grid[k] == u'air':
            s = s + v
    return s

def extractMobState(entities):
    life = 0
    for entity in [EntityInfo(**k) for k in entities]:
        if entity.name == AGENT:
            m_x = a_x = math.floor(entity.x)
            m_z = a_z = math.floor(entity.z)
        elif entity.name == MOB_TYPE:
            m_x = math.floor(entity.x)
            m_z = math.floor(entity.z)
            life = entity.life
    x = m_x - a_x
    z = m_z - a_z
    if ENABLE_ENEMY_DISTANCE_SATURATION:
        if abs(x) > ENEMY_DISTANCE_SATURATION_LEVEL:
            x = math.copysign(ENEMY_DISTANCE_SATURATION_LEVEL, x)
        if abs(z) > ENEMY_DISTANCE_SATURATION_LEVEL:
            z = math.copysign(ENEMY_DISTANCE_SATURATION_LEVEL, z)
    return life,x,z

def extractHealthState(life):
    return life

# this is where the rewards are counted and the state is determined
def getState():
    world_state = agent_host.getWorldState()
    while world_state.is_mission_running and len(world_state.observations) == 0:
        time.sleep(0.1)
        world_state = agent_host.getWorldState()
    if world_state.is_mission_running:
        msg = world_state.observations[-1].text
        ob = json.loads(msg)
#        airState = extractAirState(ob.get(u'floorAll',0))
       	healthState = extractHealthState(ob[u'Life'])
       	#check for hit here
       	hit = checkHit(healthState)
       	#set boolean and return it
        mob_life, mob_x, mob_z = extractMobState(ob[u'entities'])
        mob_hit = checkMobHit(mob_life)
#		s = State(airState, healthState, mob_x, mob_z)
        s = State(mob_x, mob_z)
    else:
        s = None
        ob = None
        hit = None
        mobHit = None
    return s, ob, hit, mob_hit

def isTerminal(state):
    return (state is None) or (not world_state.is_mission_running) or (checkHit.life <= 0.)  #or (state.x == 0. and state.z == 0.)

def calculate_reward(state, s_prime, action, hit, mobHit):
    reward = 0
    if hit:
    	reward = reward + DAMAGE_PENALTY
    if mobHit:
    	reward = reward + ENEMY_HIT_REWARD
    #health related rewards
    if checkHit.life <= 0.:
        reward = reward + DEATH_PENALTY
#    elif s_prime.health < state.health:
#        reward = reward + DAMAGE_PENALTY

    #distance related rewards
    if state.x == 0. and state.z == 0:
        #mob dead
        reward = reward + ENEMY_DEATH_REWARD
    else:
        #reward closeness to mob
        reward = reward + (MAX_ENEMY_PROXIMITY_REWARD / math.sqrt(state.x**2 + state.z**2))

    #movement related penalties
    if action == "move " + str(MOVESPEED) and not hit:
    	reward += 1
    if action != "move " + str(MOVESPEED) and math.sqrt(state.x**2 + state.z**2) > AGGRO_RANGE:
    	reward += -1
#    if action != "nothing":
#        reward = reward + MOVE_PENALTY
#        if (state.air & air_actions[action]) == 0:
#            reward = reward - WALL_MOVE_PENALTY'

    global cumulative_reward
    cumulative_reward = cumulative_reward + reward
    return reward

def do_action(state, action):
#    sys.stderr.write(action + "\n")
    agent_host.sendCommand("move 0")
    agent_host.sendCommand("strafe 0")
    if action != "nothing":
        agent_host.sendCommand(action)

    s_prime, ob, hit, mobHit = getState()
    if not state is None:
        reward = calculate_reward(state, s_prime, action, hit, mobHit)

        # automatic actions carried out here
        if(countMobs([EntityInfo(**k) for k in ob[u'entities']]) == 0): #summon mobs if their are no more on the field
            agent_host.sendCommand("chat /summon {0} {1} {2} {3} {4}".format(MOB_TYPE, MOB_START_LOCATION[0], MOB_START_LOCATION[1], MOB_START_LOCATION[2], "{IsBaby:0}")) #summon mob
#            agent_host.sendCommand("chat /summon {0} {1} {2} {3} {4}".format(MOB_TYPE, MOB_START_LOCATION[0]-5, MOB_START_LOCATION[1], MOB_START_LOCATION[2]+10, "{IsBaby:0}")) #summon mob
        
        # turn towards the nearest zombie
        lookAtNearestEntity([EntityInfo(**k) for k in ob[u'entities']])
        #swing weapon
#        agent_host.sendCommand("attack 1")
        time.sleep(ACTION_DELAY)

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
        reward = -100
    valid_actions = availableActions(state)
    return reward, s_prime, valid_actions

def load_mission(fileName):
    # load mission from file
    #mission_file = './tutorial_6.xml'
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
    q_table = {} # TODO: Load from previous trials
    # Loop until mission ends:
    rewards = []
    start_mission(agent_host, my_mission, my_mission_record) #restart mission
    world_state = agent_host.getWorldState()
    i = 0
    e = 0.1
    while world_state.is_mission_running:
    	print "epsilon: {}".format(e)
        agent_host.sendCommand("chat /summon {0} {1} {2} {3} {4}".format(MOB_TYPE, MOB_START_LOCATION[0], MOB_START_LOCATION[1], MOB_START_LOCATION[2], "{IsBaby:0}")) #summon mob
#        agent_host.sendCommand("chat /summon {0} {1} {2} {3} {4}".format(MOB_TYPE, MOB_START_LOCATION[0]-5, MOB_START_LOCATION[1], MOB_START_LOCATION[2]+10, "{IsBaby:0}")) #summon mob
        if ENABLE_KNOCKBACK_RESISTANCE:
            agent_host.sendCommand("chat " + KNOCKBACK_RESIST_COMMAND) #knockback protection
        s,_,_,_ = getState()
        q_table = perform_trial(s, actions, do_action, isTerminal, q_table, epsilon = e)
        print "Trial {} finished.".format(i+1)
        world_state = agent_host.getWorldState()
        if world_state.is_mission_running:
            agent_host.sendCommand("quit")
        rewards.append(cumulative_reward)
        print cumulative_reward
        cumulative_reward = 0.
        time.sleep(1)
        start_mission(agent_host, my_mission, my_mission_record) #restart mission
        world_state = agent_host.getWorldState()
        i += 1
        e *= 0.85

    with open(REWARD_OUTPUT_FILE, 'w') as f:
        for r in rewards:
            f.write("{}\n".format(r))
    #TODO: Save q_table for further use

    # mission has ended.
    for error in world_state.errors:
        print "Error:", error.text

    print
    print "Mission ended"
    # Mission has ended.
    time.sleep(1)  # Give mod some time.
