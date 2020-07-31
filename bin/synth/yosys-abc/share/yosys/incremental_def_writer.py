#
# Incremental Def Writer -- Brown University
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
# ------------------
# This tool is an Incremental Def Writer, It takes Two Def files and Merge them while retaining the placement data found in the placed one.
# Inputs:
#	1. DEF file with all the components Placed
#	2. The new DEF file with the modified/added components which are all unplaced
# Output:
#   DEF file with all components including Modified/Added ones from the second def files, 
#	with all components placed in the locations from the first placed DEF if found,
#	else the component is placed in the centroid of its fanins and fanouts
# ---------------------------------------------------------------------------------------

#!/usr/bin/env python3

import sys
from utils import *
from merger import *

def print_Usage():
    print("USAGE: ")
    print("      python incremental_def_writer.py -placed file1.def -unplaced file2.def -output output.def\n")

def execute():
    if(len(sys.argv) != 7):
        print("\nERROR: Missing or Unknown Arguments.")
        print_Usage()
        return
        
    i = 1
    while i < 7:
        if sys.argv[i] == "incremental_def_writer.py":
            continue
        elif sys.argv[i] == "-placed":
            placed_def = sys.argv[i+1]
            i +=1
        elif sys.argv[i] == "-unplaced":
            unplaced_def = sys.argv[i+1]
            i +=1
        elif sys.argv[i] == "-output":
            output_def = sys.argv[i+1]
            i +=1
        else:
            print("\nERROR: Missing or Unknown Arguments.")
            print_Usage()
            return
        i += 1

    placed_components_map = {}
    unplaced_components_map = {}
    unplaced_nets_map = {}
    merged_components_map = {}
    placed_pins_map = {}

    # Extract Data from unplaced DEF

    # Copy Intro Section
    intro_section = copy_intro_section(placed_def)

    # Extract Components Section data into data structures
    extract_components_section(unplaced_def,unplaced_components_map)

    # Extract some data from Pins Sections into data structures and copy it as well
    extract_Pins_section(unplaced_def,placed_pins_map)
    pins_section = copy_pins_section(unplaced_def)

    # Extract Nets Sections data into data structures
    extract_nets_section(unplaced_def,unplaced_nets_map)
    nets_section = copy_nets_section(unplaced_def)
    # Copy Exit Section
    exit_section = copy_exit_section(unplaced_def)

    # Extract Components from placed DEF
    extract_components_section(placed_def,placed_components_map)


    # Merge the 2 Defs:
    merge_defs(placed_components_map,placed_pins_map,unplaced_components_map,unplaced_nets_map,merged_components_map)


    # Write DEF
    paste_intro_section(output_def,intro_section)
    save_components_section(output_def,merged_components_map)
    paste_pins_section(output_def,pins_section)
    paste_nets_section(output_def,nets_section)
    paste_exit_section(output_def,exit_section)
    print("SUCCESSFULLY WRITE DEF FILE INTO "),
    print(output_def)

# call
execute()
