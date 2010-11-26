#!/usr/bin/env python
""" skier -- Keep the skier between the lines.  Watch out for jumps!

start:
    [host]$ ./skier.py

keys:
    j - move the skier to the left
    k - move the skier to the right

"""

""" 
Copyright 2003-2004 Cody Collier

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

__history__ = """
0.1 -> 05/15/2003
    -> First incarnation.  Execution.
    -> first round: print_slope, skier_position, main routine,
        generate_random, print_stats
    -> setting constants and variables
0.2 -> 05/16/2003
    -> reorganized and cleaned up 
    -> developing and testing user input methods
    -> added get_user_input_sys
    -> added get_user_input_curses
    -> added get_user_input_run
    -> add the logic for determining if skier has gone out of bounds.
0.3 -> 05/17/2003
0.3 -> 05/19/2003
    -> add limit of 80 collumns
0.4 -> 06/09/2003
    -> removed any curses references
0.5 -> 06/10/2003
    -> add the raw terminal code for getch() like functionality, based on:
    -> http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/134892
    -> fixing some bad algorithms in the display functions
0.5 -> 03/15/2004
    -> review and pick back up
    -> fixed error in the rightspace calculation

ToDo:
    -> add the raw terminal code for getch() like functionality
    -> 
    -> 

"""

import sys
import random
import time
import tty, termios, select


#-----------------------------------------------------------------------------
# calculation functions
#-----------------------------------------------------------------------------
def generate_random(choicelist):
    """
    This function generates a random choice of the items in the 
    given list.
    """
    random_choice = random.choice(choicelist)
    return random_choice

def calc_skier_position(skierposition,userinput):
    """
    """
    if userinput == "j":
        skierposition = skierposition - 1 
    if userinput == "k":
        skierposition = skierposition + 1 
    return skierposition

#-----------------------------------------------------------------------------
# display functions
#-----------------------------------------------------------------------------
def print_slopeline(padding,tree,skier,slopewidth,skierposition):
    """
    This function prints a line of the slope to the screen (stdout).
    The line includes two trees, and a skier.  Occasionally the 
    trees are not printed due to a jump.  The width of the slope is
    static for now, and the random number is used to determine how
    far from the left side of the screen the slope begins.
    0--------------t--------S----------t-------------
    """
    leftspace = skierposition - padding
    rightspace = slopewidth - leftspace
    print padding*" " + tree + leftspace*" " + skier + rightspace*" " + tree
    return 0

def print_slopeline_crash(padding,tree,skier,slopewidth,skierposition):
    """
    This function prints a line of the slope to the screen (stdout)
    that indicates the skier crashed.
    The line includes two trees, skier, and a crash.
    """

    leftspace = skierposition - padding
    rightspace = slopewidth - leftspace - 1
    print padding*" " + tree + leftspace*" " + skier + rightspace*" " + tree
    padding = padding - 1
    print padding*" " + "*" + leftspace*" " + skier + "*" + rightspace*" " + tree
    return 0

def print_stats(yards):
    """
    This function prints the final stats after a skier has crashed.
    """
    print
    print "You skied a total of", yards, "yards!"
    print "Want to take another shot?"
    print
    return 0

#-----------------------------------------------------------------------------
# user input functions
#-----------------------------------------------------------------------------
def get_user_input_sys():
    """
    Use sys.stdin to get the user's input for moving the skier.
    assist from: http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/134892
    added the select for non-blocking to the above recipe
    """
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        inputflag,null,null = select.select([fd],[],[],0.1)
        if len(inputflag) == 1:
            userinput = sys.stdin.read(1)
        else:
            userinput = null
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return userinput

def get_user_input_random():
    """
    Generate random input for auto run.
    """
    userinput = generate_random(choicelist_input)
    return userinput

##############################################################################
# Main Routine
#

#--------------------------------------
# Constants
#--------------------------------------
delay = 0   # this should rarely be changed
tree = "!"
skier = "H"
slopewidth = 31
minpadding = 0
maxpadding = 80 - slopewidth
choicelist_drift = [-2,-1,0,1,2]
choicelist_input = ["j","k"]

#--------------------------------------
# Variable Initialization
#--------------------------------------
padding = 14
skierposition = (padding + (slopewidth/2))
yards = 0

#--------------------------------------
# main logic
#--------------------------------------
#for i in xrange(150):
while 1:
    # - determine the direction of the next slope line
    drift = generate_random(choicelist_drift)
    padding = padding + drift
    if padding > maxpadding:
        padding = maxpadding
    if padding < minpadding:
        padding = minpadding

    # - get the user input
    autorun = 0
    if autorun:
        userinput = get_user_input_random()
    else:
        userinput = get_user_input_sys()
        
    #debug
    #print "user input:", userinput

    # - calculate the skier position and print
    skierposition = calc_skier_position(skierposition,userinput)
    if ((skierposition - padding) < 1) or ((skierposition - padding) > slopewidth):
        print_slopeline_crash(padding,tree,skier,slopewidth,skierposition)
        print_stats(yards)
        sys.exit(0)
    else:    
        print_slopeline(padding,tree,skier,slopewidth,skierposition)
        # - increment the yards and insert delay
        yards = yards + 1
        time.sleep(delay)

print_slopeline_crash(padding,tree,skier,slopewidth,skierposition)
print_stats(yards)
sys.exit(0)


