#
#  Def Parser -- Brown University
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
#   OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
#
#  By: Marina Neseem 2019
#  marina_neseem@brown.edu

# This file contains the basic functions for reading and writing various sections of DEF files

# --------------------- extract_components_section -----------------
# function: read components section of a def file to a map
# input: def file name 
# output: map
# ------------------------------------------------------------------

#!/usr/bin/env python3

def extract_components_section(file_name,components_map):
    inComponentsSection = False
    f = open (file_name,"r")
    for line in f:
        if line[0:10] == "COMPONENTS":
            inComponentsSection = True
            list_of_tokens = line.split(" ")
            numOfComponents= list_of_tokens[1]
            continue
        elif line[0:14] == "END COMPONENTS":
            inComponentsSection = False
            break

        if inComponentsSection == False or line[0] != "-":
            continue
        else:
            gate_data = {}
            list_of_tokens = line.split(" ")
            gate_name = list_of_tokens[1]
            gate_data["type"] = list_of_tokens[2]
            if "PLACED" in list_of_tokens:
                temp = list_of_tokens.index("PLACED")
                gate_data["x_location"] = list_of_tokens[temp+2]
                gate_data["y_location"] = list_of_tokens[temp+3]

            components_map[gate_name] = gate_data
    if len(components_map) != int(numOfComponents):
                print("ERROR, Number of components is not consistant")

# --------------------- save_components_section --------------------
# function: write components section to a def file
# input: map with the components section data 
# output: file
# ------------------------------------------------------------------

def save_components_section(file_name,components_map):
    f = open (file_name,"a")
    f.write("COMPONENTS %d ;\n" % len(components_map))
    for component in components_map.keys():
        f.write("- %s %s + " % (component, components_map[component]["type"]))
        if("x_location" in components_map[component].keys()):
            f.write("PLACED ( %s %s ) N ;\n" % (components_map[component]["x_location"], components_map[component]["y_location"]))
        else:
            f.write("UNPLACED ;\n")
    
    f.write("END COMPONENTS\n\n")
    f.close() 

# --------------------- extract_nets_section -----------------------
# function: read nets section of a def file to a map
# input: def file name 
# output: map
# nets_map has key net_name and value net_data
# net_data contains src and sinks
# src contains node
# sinks containes list of nodes
# node contains either (gate_name and gate_pin) if node was a gate
# or contains (pin_name) if node was a pin
# ------------------------------------------------------------------

def extract_nets_section(file_name, nets_map):
    inNetsSection = False
    f = open (file_name,"r")
    net_name = ""
    net_data = {}
    sinks = []
    new_pin = False
    for line in f:
        if line[0:4] == "NETS":
            inNetsSection = True
            tokens = line.split(" ")
            numOfNets= tokens[1]
            continue
        elif line[0:8] == "END NETS":
            inNetsSection = False
            break

        if inNetsSection == False:
            continue
        else:
            list_of_tokens = line.split(" ")

            if list_of_tokens[0] == '-':
                net_name = list_of_tokens[1]
                new_pin = True
                net_data = {}
                sinks = []
            if 1:
                for i in range(len(list_of_tokens)-1):
                    gate_name = ""
                    gate_pin = ""
                    node = {}
                    if list_of_tokens[i] == '(':
                        arg1 = list_of_tokens[i+1]
                        arg2 = list_of_tokens[i+2]
                        i = i+2
                        if arg1 == 'PIN':
                            node["pin_name"] = arg2
                        else:
                            node["gate_name"] = arg1
                            node["gate_pin"] = arg2 
                        sinks.append(node)
                        
                    if list_of_tokens[i+1] == ';\n':
                        net_data["sinks"] = sinks
                        nets_map[net_name] = net_data

# --------------------- save_nets_section -----------------
# function: write nets section to a def file
# input: map with the nets section data 
# output: file
# ------------------------------------------------------------------

def save_nets_section(file_name, nets_map):
    f = open (file_name,"a")
    f.write("NETS %d ;\n" % len(nets_map))
    for net in nets_map.keys():
        f.write("- %s\n" % (net))
        for sink in nets_map[net]["sinks"]:
            if("pin_name" in sink.keys()):
                f.write(" ( PIN %s )" % sink["pin_name"])
            else:
                f.write(" ( %s %s )" % (sink["gate_name"],sink["gate_pin"]))
        f.write(" ;\n")
    f.write("END NETS\n\n")
    f.close() 

# --------------------- extract_Pins_section -----------------
# function: read Pins Locations and save them in a map with pin names as keys and locations as values
# input: def file name 
# output: map
# ------------------------------------------------------------------

def extract_Pins_section(file_name,pins_map):
    inPinsSection = False
    f = open (file_name,"r")
    net_data = {}
    pin_name = ""	
    for line in f:
        if line[0:4] == "PINS":
            inPinsSection = True
            tokens = line.split(" ")
            numOfPins= tokens[1]
            continue
        elif line[0:8] == "END PINS":
            inPinsSection = False
            break

        if inPinsSection == False:
            continue
        else:
            list_of_tokens = line.split(" ")
            if list_of_tokens[0] == '-':
                pin_name = list_of_tokens[1]
                net_data = {}

            if 'FIXED' in list_of_tokens:
                temp = list_of_tokens.index('FIXED')
                net_data['x_location'] = list_of_tokens[temp+2]
                net_data['y_location'] = list_of_tokens[temp+3]

            if 'DIRECTION' in list_of_tokens:
                temp = list_of_tokens.index('DIRECTION')
                net_data['direction'] = list_of_tokens[temp+1]

            if 'LAYER' in list_of_tokens:
                temp = list_of_tokens.index('LAYER')
                net_data['layer'] = list_of_tokens[temp+1]
                net_data['x1'] = list_of_tokens[temp+3]
                net_data['y1'] = list_of_tokens[temp+4]
                net_data['x2'] = list_of_tokens[temp+7]
                net_data['y2'] = list_of_tokens[temp+8]

            if 'PLACED' in list_of_tokens:
                temp = list_of_tokens.index('PLACED')
                net_data['x_location'] = list_of_tokens[temp+2]
                net_data['y_location'] = list_of_tokens[temp+3]

        pins_map[pin_name] = net_data

    if len(pins_map) != int(numOfPins):
        print("ERROR, Number of pins is not consistant")

# --------------------- save_pins_section --------------------
# function: write pins section to a def file
# input: map with the pins section data 
# output: file
# ------------------------------------------------------------------

def save_pins_section(file_name,pins_map):
    f = open (file_name,"a")
    f.write("PINS %d ;\n" % len(pins_map))
    for pin in pins_map.keys():
        f.write("- %s + NET %s + DIRECTION %s + USE SIGNAL \n" % (pin, pin,pins_map[pin]["direction"]))
        f.write(" + LAYER %s  ( %s %s ) ( %s %s ) " % (pins_map[pin]["layer"], pins_map[pin]["x1"], pins_map[pin]["y1"], pins_map[pin]["x2"], pins_map[pin]["y2"]))
        f.write("+ FIXED ( %s %s ) N ;\n" % (pins_map[pin]["x_location"], pins_map[pin]["y_location"]))
        #f.write(" + LAYER M2  ( -100 0 ) ( 100 1040 ) + FIXED ( 1 1 ) N ;\n")

    f.write("END PINS\n\n")
    f.close() 

# --------------------- copy_intro_section -------------------------
# function: copy the intro section of a def file
# input: file
# output: string with intro section text
# ------------------------------------------------------------------

def copy_intro_section(file_name):
    intro_section = ""
    f = open (file_name,"r")
    for line in f:
        if line[0:10] == "COMPONENTS":
            break
        intro_section = intro_section + line
    return intro_section


# --------------------- paste_intro_section -------------------------
# function: write components section to a def file
# input: string with intro section text
# output: file
# ------------------------------------------------------------------

def paste_intro_section(file_name, intro_section):
    f = open (file_name,"w+")
    f.write(intro_section)

# --------------------- copy_pins_section --------------------------
# function: copy the pins section of a def file
# input: file
# output: string with pins section text
# ------------------------------------------------------------------

def copy_pins_section(file_name):
    pins_section = ""
    inPinsSection = False
    f = open (file_name,"r")
    for line in f:
        if line[0:4] == "PINS":
            inPinsSection = True
            
        elif line[0:8] == "END PINS":
            inPinsSection = False
            pins_section = pins_section + line + "\n"
            break

        if inPinsSection == False:
            continue
        else:
            pins_section = pins_section + line
    return pins_section

# --------------------- paste_pins_section --------------------------
# function: write pins section to a def file
# input: string with pins section text
# output: file
# ------------------------------------------------------------------

def paste_pins_section(file_name, pins_section):
    f = open (file_name,"a")
    f.write(pins_section)


# --------------------- copy_nets_section --------------------------
# function: copy the nets section of a def file
# input: file
# output: string with nets section text
# ------------------------------------------------------------------

def copy_nets_section(file_name):
    nets_section = ""
    inNetsSection = False
    f = open (file_name,"r")
    for line in f:
        if line[0:4] == "NETS":
            inNetsSection = True
        elif line[0:8] == "END NETS":
            inNetsSection = False
            nets_section = nets_section + line + "\n"
            break

        if inNetsSection == False:
            continue
        else:
            nets_section = nets_section + line
    return nets_section

# --------------------- paste_nets_section --------------------------
# function: write nets section to a def file
# input: string with nets section text
# output: file
# ------------------------------------------------------------------

def paste_nets_section(file_name, nets_section):
    f = open (file_name,"a")
    f.write(nets_section)

# --------------------- copy_components_section --------------------------
# function: copy the components section of a def file
# input: file
# output: string with nets section text
# ------------------------------------------------------------------

def copy_components_section(file_name):
    components_section = ""
    inComponentsSection = False
    f = open (file_name,"r")
    for line in f:
        if line[0:10] == "COMPONENTS":
            inComponentsSection = True

        elif line[0:14] == "END COMPONENTS":
            inComponentsSection = False
            components_section = components_section + line + "\n"
            break

        if inComponentsSection == False:
            continue
        else:
            components_section = components_section + line
    return components_section

# --------------------- paste_nets_section --------------------------
# function: write nets section to a def file
# input: string with nets section text
# output: file
# ------------------------------------------------------------------

def paste_components_section(file_name, components_section):
    f = open (file_name,"a")
    f.write(components_section)

# --------------------- copy_exit_section --------------------------
# function: copy the exit section of a def file
# input: file
# output: string with exit section text
# ------------------------------------------------------------------

def copy_exit_section(file_name):
    exit_section = ""
    inExitSection = False
    f = open (file_name,"r")
    for line in f:
        if line[0:8] == "END NETS":
            inExitSection = True
            continue
        if inExitSection == True:
            exit_section = exit_section + line
    return exit_section


# --------------------- paste_exit_section --------------------------
# function: write exit section to a def file
# input: string with exit section text
# output: file
# ------------------------------------------------------------------
def paste_exit_section(file_name, exit_section):
    f = open (file_name,"a")
    f.write(exit_section)

def get_connected_components(gate,conn_list,nets_map):
    for net in nets_map:
        for sink in nets_map[net]["sinks"]:
            if "gate_name" in sink and gate == sink["gate_name"] and 'Z' == sink["gate_pin"]:
                for sink in nets_map[net]["sinks"]:
                    if "gate_name" in sink and gate != sink["gate_name"]:
                        conn_list.append(sink["gate_name"])
                    elif "pin_name" in sink:
                        conn_list.append(sink["pin_name"])
            elif "gate_name" in sink and gate == sink["gate_name"]:
                for sink in nets_map[net]["sinks"]:
                    if "pin_name" in sink:
                        conn_list.append(sink["pin_name"])
    #print("Gate "),
    #print(gate),
    #print(" is connected to "),
    #print(conn_list)


def get_die_area(file_name, die_area):
    f = open (file_name,"r")
    for line in f:
        if line[0:7] == "DIEAREA":
            list_of_tokens = line.split(" ")
            die_area["width"] = int(list_of_tokens[6])
            die_area["height"] = int(list_of_tokens[7])

