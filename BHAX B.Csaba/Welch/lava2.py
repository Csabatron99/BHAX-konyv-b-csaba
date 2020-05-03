from __future__ import print_function
# ------------------------------------------------------------------------------------------------
# Copyright (c) 2016 Microsoft Corporation
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and
# associated documentation files (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge, publish, distribute,
# sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all copies or
# substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT
# NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
# ------------------------------------------------------------------------------------------------

# Tutorial sample #2: Run simple mission using raw XML

# Added modifications by Norbert Bátfai (nb4tf4i) batfai.norbert@inf.unideb.hu, mine.ly/nb4tf4i.1
# 2018.10.18, https://bhaxor.blog.hu/2018/10/18/malmo_minecraft
# 2020.02.02, NB4tf4i's Red Flowers, http://smartcity.inf.unideb.hu/~norbi/NB4tf4iRedFlowerHell
# 2020.03.02, https://github.com/nbatfai/RedFlowerHell
# 2020.03.07, "_smartSteve": nof_turn (number of turns) is replaced by the dict self.collectedFlowers
# 2020.03.11, "_bu": bottom up, s4v3: https://youtu.be/VP0kfvRYD1Y

from builtins import range
import MalmoPython
import os
import sys
import time
import random
import json
import math

if sys.version_info[0] == 2:
    sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)  # flush print output immediately
else:
    import functools
    print = functools.partial(print, flush=True)

# Create default Malmo objects:

agent_host = MalmoPython.AgentHost()
try:
    agent_host.parse( sys.argv )
except RuntimeError as e:
    print('ERROR:',e)
    print(agent_host.getUsage())
    exit(1)
if agent_host.receivedArgument("help"):
    print(agent_host.getUsage())
    exit(0)

# -- set up the mission -- #
missionXML_file='nb4tf4i_d_2.xml'
with open(missionXML_file, 'r') as f:
    print("NB4tf4i's Red Flowers (Red Flower Hell) - DEAC-Hackers Battle Royale Arena\n")
    print("NB4tf4i vörös pipacsai (Vörös Pipacs Pokol) - DEAC-Hackers Battle Royale Arena\n")
    print("The aim of this first challenge, called nb4tf4i's red flowers, is to collect as many red flowers as possible before the lava flows down the hillside.\n")
    print("Ennek az első, az nb4tf4i vörös virágai nevű kihívásnak a célja összegyűjteni annyi piros virágot, amennyit csak lehet, mielőtt a láva lefolyik a hegyoldalon.\n")
    print("Norbert Bátfai, batfai.norbert@inf.unideb.hu, https://arato.inf.unideb.hu/batfai.norbert/\n")
    print("Version history\n", "Code: ", sys.argv[0], ", series 4 v.3, bottom up, max 18 poppies. Norbert Bátfai, nbatfai@gmail.com\n")
    print("Loading mission from %s" % missionXML_file)
    mission_xml = f.read()
    my_mission = MalmoPython.MissionSpec(mission_xml, True)
    my_mission.drawBlock( 0, 0, 0, "lava")

class Hourglass:
    def __init__(self, charSet):
        self.charSet = charSet
        self.index = 0
    def cursor(self):
        self.index=(self.index+1)%len(self.charSet)
        return self.charSet[self.index]

hg = Hourglass('|/-\|')

class Steve:
    def __init__(self, agent_host):
        self.agent_host = agent_host

        self.x = 0
        self.y = 0
        self.z = 0
        self.yaw = 0
        self.pitch = 90

        self.forward = True
        self.backward = False
        
        self.first_turn = True
    
        self.front_of_me_idx = 0
        self.front_of_me_idxr = 0
        self.front_of_me_idxl = 0
        self.right_of_me_idx = 0
        self.left_of_me_idx = 0
        self.back_of_me_idx = 0

        self.level = False

        self.lookingat = ""

    def idle(self, delay):
        time.sleep(delay)

    
    def calcNbrIndex(self):
        if self.yaw >= 180-22.5 and self.yaw <= 180+22.5 :
            self.front_of_me_idx = 1
            self.front_of_me_idxr = 2
            self.front_of_me_idxl = 0
            self.right_of_me_idx = 5
            self.left_of_me_idx = 3
            self.back_of_me_idx = 7
        elif self.yaw >= 180+22.5 and self.yaw <= 270-22.5 :
            self.front_of_me_idx = 2
            self.front_of_me_idxr = 5
            self.front_of_me_idxl =1
            self.right_of_me_idx = 8
            self.left_of_me_idx = 0
            self.back_of_me_idx = 6
        elif self.yaw >= 270-22.5 and self.yaw <= 270+22.5 :
            self.front_of_me_idx = 5
            self.front_of_me_idxr = 8
            self.front_of_me_idxl = 2
            self.right_of_me_idx = 7
            self.left_of_me_idx = 1
            self.back_of_me_idx = 3
        elif self.yaw >= 270+22.5 and self.yaw <= 360-22.5 :
            self.front_of_me_idx = 8
            self.front_of_me_idxr = 7
            self.front_of_me_idxl = 5
            self.right_of_me_idx = 6
            self.left_of_me_idx = 2
            self.back_of_me_idx = 0
        elif self.yaw >= 360-22.5 or self.yaw <= 0+22.5 :
            self.front_of_me_idx = 7
            self.front_of_me_idxr = 6
            self.front_of_me_idxl = 8
            self.right_of_me_idx = 3
            self.left_of_me_idx = 5
            self.back_of_me_idx = 1
        elif self.yaw >= 0+22.5 and self.yaw <= 90-22.5 :
            self.front_of_me_idx = 6
            self.front_of_me_idxr = 3
            self.front_of_me_idxl = 7
            self.right_of_me_idx = 0
            self.left_of_me_idx = 8
            self.back_of_me_idx = 2
        elif self.yaw >= 90-22.5 and self.yaw <= 90+22.5 :
            self.front_of_me_idx = 3
            self.front_of_me_idxr = 0
            self.front_of_me_idxl = 6
            self.right_of_me_idx = 1
            self.left_of_me_idx = 7
            self.back_of_me_idx = 5
        elif self.yaw >= 90+22.5 and self.yaw <= 180-22.5 :
            self.front_of_me_idx = 0
            self.front_of_me_idxr = 1
            self.front_of_me_idxl = 3
            self.right_of_me_idx = 2
            self.left_of_me_idx = 6
            self.back_of_me_idx = 8
        else:
            print("There is great disturbance in the Force...")



    def whatISee(self, observations):
        self.lookingat = "NOTHING"
        if "LineOfSight" in observations:
            lineOfSight = observations["LineOfSight"]
            self.lookingat = lineOfSight["type"]

    def whatMyPos(self, observations):
        if "Yaw" in observations:
            self.yaw = int(observations["Yaw"])
        if "Pitch" in observations:
            self.pitch = int(observations["Pitch"])
        if "XPos" in observations:
            self.x = int(observations["XPos"])
        if "ZPos" in observations:
            self.z = int(observations["ZPos"])
        if "YPos" in observations:
            self.y = int(observations["YPos"])

    def run(self):
        world_state = self.agent_host.getWorldState()
        # Loop until mission ends:
        while world_state.is_mission_running:

            act = self.action(world_state)
            if not act:
                self.idle(.017)
            world_state = self.agent_host.getWorldState()


    def lavaIsClose(self, nbr):

        for i in range(18):
            if nbr[i+9] == "lava" or nbr[i+9] == "flowing_lava":      
                print("van lava kozel")   
                return True  

            else:        
                print("nincs lava kozel") 
        return False  


    def action(self, world_state):
        for error in world_state.errors:
            print("Error:", error.text)

        if world_state.number_of_observations_since_last_state == 0:
            return False

        input = world_state.observations[-1].text
        observations = json.loads(input)
        nbr = observations.get("nbr5x5", 0)
        self.whatMyPos(observations)
        print("\r    Steve's Coords: ", self.x, self.y, self.z, end='')

        self.whatISee(observations)

        self.calcNbrIndex()



        if self.level == False and self.lavaIsClose(nbr) == False and self.y < 49:
            self.agent_host.sendCommand("move 1")
            time.sleep(.3)
            if self.lavaIsClose(nbr) == False and nbr[self.front_of_me_idx+9] == "dirt":
                self.agent_host.sendCommand( "jumpmove 1" )
                time.sleep(.3)
            return True
        else:
            self.level = True

 
        if self.first_turn == True and self.level == True:
            self.agent_host.sendCommand("jumpmove -1")
            self.agent_host.sendCommand("turn 1")
            time.sleep(.1)
            self.first_turn = False


        if self.level == True and self.first_turn == False:

            if self.lavaIsClose(nbr):
                self.agent_host.sendCommand("strafe 1")
                time.sleep(.1)
                if self.backward == True:
                    self.forward = True
                    self.backward = False
                else:
                    self.forward = False
                    self.backward = True

            elif nbr[self.front_of_me_idx+9] == "dirt" :
                self.forward = False
                self.backward = True
            elif nbr[self.back_of_me_idx+9] == "dirt" :
                self.forward = True
                self.backward = False


        
            print("        THERE IS NO OBSTACLE IN FRONT OF ME", end='')

            if nbr[self.front_of_me_idx]=="dirt" and nbr[self.front_of_me_idx+9] == "air" and self.forward == True:
                self.agent_host.sendCommand( "move 1" )
                print("mek elore")
                time.sleep(.2)
            else:
                if self.backward == True:
                    self.agent_host.sendCommand("move -1")
                    time.sleep(.2)
        return True

num_repeats = 1
for ii in range(num_repeats):

    my_mission_record = MalmoPython.MissionRecordSpec()

    # Attempt to start a mission:
    max_retries = 6
    for retry in range(max_retries):
        try:
            agent_host.startMission( my_mission, my_mission_record )
            break
        except RuntimeError as e:
            if retry == max_retries - 1:
                print("Error starting mission:", e)
                exit(1)
            else:
                print("Attempting to start the mission:")
                time.sleep(2)

    # Loop until mission starts:
    print("   Waiting for the mission to start")
    world_state = agent_host.getWorldState()

    while not world_state.has_mission_begun:
        print("\r"+hg.cursor(), end="")
        time.sleep(0.15)
        world_state = agent_host.getWorldState()
        for error in world_state.errors:
            print("Error:",error.text)

    print("NB4tf4i Red Flower Hell running\n")
    steve = Steve(agent_host)
    steve.run()
    print("Number of flowers: "+ str(steve.nof_red_flower))
    time.sleep(3)

print("Mission ended")
# Mission has ended.
