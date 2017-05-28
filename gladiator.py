import MalmoPython
import os
import sys
import time
import random
import json
import math
import sarsa
#import Tkinter as tk   #for drawing gamestate on canvas
from collections import namedtuple
EntityInfo = namedtuple('EntityInfo', 'x, y, z, yaw, pitch, name, colour, variation, quantity, life')
EntityInfo.__new__.__defaults__ = (0, 0, 0, 0, 0, "", "", "", 1, 0)

actions = ["movenorth 1", "movesouth 1", "movewest 1", "moveeast 1"]

#define parameters here
MOB_TYPE = "Zombie"


#helper functions
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



#start of execution

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

#load mission from file
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


# Loop until mission ends:
while world_state.is_mission_running:
	agent_host.sendCommand("attack 1")
	world_state = agent_host.getWorldState()
	if world_state.number_of_observations_since_last_state > 0:
		#this is where the rewards are counted and the policy is updated
		current_reward = 0
		msg = world_state.observations[-1].text
		ob = json.loads(msg)

		if "Life" in ob:
			life = ob[u'Life']
			if life < current_life:
				agent_host.sendCommand("chat aaaaaaaaargh!!!")
				#do something with rewards
			current_life = life
		if "entities" in ob:
			entities = [EntityInfo(**k) for k in ob["entities"]]

		#by here we know the game state
		#Sarsa starts here

		#for ent in entities:
			#check entities

		# actions carries out here
		# turn towards the nearest zombie
		difference = lookAtNearestEntity(entities);
		agent_host.sendCommand("turn " + str(difference))

	time.sleep(0.02) #end of while loop


# mission has ended.
for error in world_state.errors:
	print "Error:",error.text

print
print "Mission ended"
# Mission has ended.
time.sleep(1) #Give mod some time.
