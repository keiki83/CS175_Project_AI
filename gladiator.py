import MalmoPython
import os
import sys
import time
import random
import json
import math
from sarsa import *
# import Tkinter as tk   #for drawing gamestate on canvas
from collections import namedtuple

EntityInfo = namedtuple('EntityInfo', 'x, y, z, yaw, pitch, name, colour, \
    variation, quantity, life')
EntityInfo.__new__.__defaults__ = (0, 0, 0, 0, 0, "", "", "", 1, 0)

actions = ["movenorth 1", "movesouth 1", "moveeast 1", "movewest 1", "nothing"]

# define parameters here
MOB_TYPE = "Zombie"
AGENT = "Gladiator"

# Sarsa Related Functions

# reward is 45 for being at same location as the entity, reward is 1 for
# maximum agro range of entity Distance reward is less than 1 for distances
# greater than agro range reward is 0 if no entity detected
def calculateReward(entities, playerLoc):
    closestMob = Null
    dist = float('inf')
    for ent in entities:
        if(closestMob == Null and ent.name != AGENT):
            closetMob == ent
            continue
        if(distance(playerLoc, ent) < dist and ent.name == MOB_TYPE):
            closestMob = ent
            dist = distance(playerLoc, ent)
    reward = 0
    if(closestMob == Null):
        return reward
	if(distance(playerLoc, ent) == 0):
		reward = 45
    else:
        reward = 45/distance(playerLoc, ent)
    return reward


# helper function
def isAir(s, actionIndex):
    if(actionIndex >= 0 and actionIndex < len(s_prime) and
            s[actionIndex] == "air"):
        return True
    else:
        return False


def swapIndex(s, fromIndex, toIndex):
    temp = s[toIndex]
    s[toIndex] = s[fromIndex]
    s[fromIndex] = s[toIndex]
    return s


def availableActions(s_prime):
    actions_prime = []
    dim = math.sqrt(s_prime)

    # locate agent
    agentIndex = -1
    for i in s_prime:
        if(i == AGENT):
            agentIndex = i
            break

    offset = [-dim, dim, 1, -1]  # north, south, east, west
    possibleAction = []
    for i in range(0, len(actions)):
        if(isAir(s_prime, agentIndex + offset[i])):
            possibleAction.append(actions[i]-1)
    possibleAction.append(actions[len(actions[i] - 1)])

    return possibleAction


def perform(s,action):
    # perform = function which takes an action as a parameter and returns:
    #    reward, s_prime, valid actions from s_prime
    # NOTES: modify s_prime array by action
    #        do not allow a move into a non air block, penalize
    #        north = -z, south = +z inc/dec by dim
    #        east = +x, west = -x inc/dec by 1
    reward = 0
    s_prime = s
    actions_prime = actions
    dim = math.sqrt(s_prime)

    # locate agent
    agentIndex = -1
    for i in s_prime:
        if(i == AGENT):
            agentIndex = i
            break

    # carry out action
    if(action != "nothing"):
        if(action == "movenorth 1"):  # -z axis (-dim)
            actionIndex = agentIndex - dim
            if(isAir(s_prime, actionIndex)):
                s_prime = swapIndex(s_prime, agentIndex, actionIndex)
                # calculate reward
                reward = 1  # place holder
            else:
                # penalize e.g. move into zombie / move into wall
                reward = -1  # place holder
        if(action == "movesouth 1"):  # +z axis (+dim)
            actionIndex = agentIndex + dim
            if(isAir(s_prime, actionIndex)):
                s_prime = swapIndex(s_prime, agentIndex, actionIndex)
                # calculate reward
                reward = 1  # place holder
            else:
                # penalize e.g. move into zombie / move into wall
                reward = -1  # place holder
        if(action == "moveeast 1"):  # +x axis (+1)
            actionIndex = agentIndex + 1
            if(isAir(s_prime, actionIndex)):
                s_prime = swapIndex(s_prime, agentIndex, actionIndex)
                # calculate reward
                reward = 1  # place holder
            else:
                # penalize e.g. move into zombie / move into wall
                reward = -1  # place holder
        if(action == "movewest 1"):  # -x axis (-1)
            actionIndex = agentIndex - 1
            if(isAir(s_prime, actionIndex)):
                s_prime = swapIndex(s_prime, agentIndex, actionIndex)
                # calculate reward
                reward = 1  # place holder
            else:
                # penalize e.g. move into zombie / move into wall
                reward = -1  # place holder

    # determine available movements
    actions_prime = availableActions(s_prime)

    return reward, s_prime, actions_prime

# controls maximum itterations of sarsa_trial
def is_terminal(state):
    return state[0] >= state[1]

# generate the statespace for sarsa
def generateStateSpace(grid, entities):
    dim = math.sqrt(len(grid))
    playerIndex = int(dim*(dim//2) + dim//2)
    agent  = 0
    for ent in entities:
        if ent.name == AGENT:
            agent = ent
            break
    grid[playerIndex] = agent.name
    for ent in entities:
        if ent.name == MOB_TYPE:
            entIndex = int(playerIndex + dim*(ent.z-agent.z) + (ent.x - agent.x))
            if(entIndex >= 0 or entIndex < len(grid)):
                grid[entIndex] = ent.name
    return grid

# get best action to take
def getAction(q_table, state):
    action = 0
    value = float('-inf')
    for key in Q:
        if(key[0] == state and q_table[key] > value):
            action = key[1]
            value = q_table[key]
    return action


# perform action in game for agent
def performAction(agent_host, action):
    if (action == "nothing"):
        return
    else:
        agent_host.sendCommand(action)
    return



# helper functions
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
	best_yaw = math.degrees(math.atan2(entities[closestEntity].z - us.z, entities[closestEntity].x - us.x)) - 90
	difference = best_yaw - current_yaw;
	while difference < -180:
		difference += 360;
	while difference > 180:
		difference -= 360;
	difference /= 180.0;
	return difference


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

# load mission from file
mission_file = './arena1.xml'
with open(mission_file, 'r') as f:
    print "Loading mission from %s" % mission_file
    mission_xml = f.read()
    my_mission = MalmoPython.MissionSpec(mission_xml, True)
my_mission.forceWorldReset()    # force reset fixes back to back testing
my_mission_record = MalmoPython.MissionRecordSpec()

# Attempt to start a mission:
max_retries = 3
for retry in range(max_retries):
	try:
		agent_host.startMission( my_mission, my_mission_record )
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

# Main loop:
total_reward = 0
total_commands = 0
current_yaw = 0
best_yaw = 0
current_life = 0

q_table = {}

# Loop until mission ends:
while world_state.is_mission_running:
    agent_host.sendCommand("attack 1")
    world_state = agent_host.getWorldState()
    if world_state.number_of_observations_since_last_state > 0:
        # this is where the rewards are counted and the policy is updated
        current_reward = 0
        msg = world_state.observations[-1].text
        ob = json.loads(msg)
        grid = ob.get(u'floorAll', 0)

        if "Life" in ob:
            life = ob[u'Life']
            if life < current_life:
                agent_host.sendCommand("chat aaaaaaaaargh!!!")
                # do something with rewards
            current_life = life
        if "entities" in ob:
			entities = [EntityInfo(**k) for k in ob["entities"]]

        # by here we know the game state
		# Sarsa starts here

        s = generateStateSpace(grid, entities)
        state = (0,500)
        q_table = sarsa_trial(s, actions, perform, is_terminal, state, q_table)
        performAction(agent_host, getAction(q_table, s))

        # for ent in entities:
            # check entities

        # actions carries out here
        # turn towards the nearest zombie
        difference = lookAtNearestEntity(entities)
        agent_host.sendCommand("turn " + str(difference))

	time.sleep(0.02) #end of while loop


# mission has ended.
for error in world_state.errors:
    print "Error:", error.text

print
print "Mission ended"
# Mission has ended.
time.sleep(1)  # Give mod some time.
