#
#  Pins Placer -- Brown University
#
#  Copyright (C) 2019  Brown University
#
#  Permission to use, copy, modify, and/or distribute this software for any
#  purpose with or without fee is hereby granted, provided that the above
#  copyright notice and this permission notice appear in all copies.
#
#  THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
#  WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
#  MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
#  ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
#  WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
#  ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
#  OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
#
#  By: Marina Neseem 2019
#  marina_neseem@brown.edu

# ---------------------------------------------------------------------------------------
# Tool Functionaity:
# -----------------
# This Script takes a def file with unplaced pins as an input
# It places the pins uniformally around the die area
# It writes a def with the placed Pins
# ---------------------------------------------------------------------------------------

#!/usr/bin/env python3

import sys
from utils import *

# -------------------------------- Parameters

# core_width and core_height are parameters that depends on the library core dimentions

core_width = 0.2
core_height = 1.8
utilization = 0.5
units_per_micron = 2000

# ------------------------------------------

def place_pins(pins_map,dim_w,dim_h):
    io_count = len(pins_map)
    max_pins_per_side = io_count/4
    step = 200
    count = 1
    direction = 1 
    x = 0
    y = 0

    #       PINS PLACEMENT
    #       
    #        ___dir4____(dim_w,dim_h)
    #       |           |
    #       |           |
    #    dir1           dir3
    #       |           |
    #       |___________|
    #   (0,0)   dir2

    for pin in pins_map:
        if(direction == 1):
            x = 0	
            y = step * count
            count += 1
        elif(direction == 2):
            x = step * count
            y = 0
            count +=1 
        elif(direction == 3):
            x = dim_w
            y = step * count
            count +=1 
        else:
            x = step * count
            y = dim_h
            count +=1 

        if(direction == 1 and (y > dim_h - step or count > max_pins_per_side)):
            direction = 2
            count =1 
        elif(direction == 2 and (x > dim_w - step or count > max_pins_per_side)):
            direction = 3
            count =1 
        elif(direction == 3 and (y > dim_h - step or count > max_pins_per_side)):
            direction = 4
            count =1
        pins_map[pin]["x_location"] = x
        pins_map[pin]["y_location"] = y

def modify_layer_number(pins_map, layer_number):
    for pin in pins_map:
        pins_map[pin]["layer"] = "M" + layer_number

def print_Usage():
    print("USAGE: ")
    print("      python pins_placer.py -def file.def -output output.def [-layer layer_number]\n")

def execute():
    if(len(sys.argv) < 5):
        print("\nERROR: Missing or Unknown Arguments.")
        print_Usage()
        return
        
    i = 1
    layer_num = 0
    while i < len(sys.argv):
        if sys.argv[i] == "-def":
            def_file = sys.argv[i+1]
            i +=1
        elif sys.argv[i] == "-output":
            output_def = sys.argv[i+1]
            i +=1
        elif sys.argv[i] == "-layer":
            layer_num = sys.argv[i+1]
            if (str(int(layer_num)) != layer_num) or (int(layer_num) <= 0):
                print("\nERROR: -layer option should be a positive integer.")
                return
            i +=1
        else:
            print("\nERROR: Missing or Unknown Arguments.")
            print_Usage()
            return
        i += 1

    pins_map = {}

    # Copy Intro Section
    intro_section = copy_intro_section(def_file)
    components_section = copy_components_section(def_file)
    nets_section = copy_nets_section(def_file)
    exit_section = copy_exit_section(def_file)

    extract_Pins_section(def_file,pins_map)
    
    if layer_num != 0:
        modify_layer_number(pins_map,layer_num)
    
    die_area = {}
    get_die_area(def_file, die_area)
    place_pins(pins_map, die_area["width"], die_area["height"])
    
    # Write DEF
    paste_intro_section(output_def,intro_section)
    paste_components_section(output_def,components_section)
    save_pins_section(output_def,pins_map)
    paste_nets_section(output_def,nets_section)
    paste_exit_section(output_def,exit_section)

# call
execute()
