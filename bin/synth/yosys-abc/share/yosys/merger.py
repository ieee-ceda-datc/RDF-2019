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

# --------------------- merge_defs ---------------------------------
# this function merges two def files where one is placed and the second is not
# it gives a modified def files which is similar to the unplaced one but modify the placements of the cells that exist in the first placed one
# Inputs: 
#		placed_components_map: map with components of the placed def
#		placed_pins_map: map with pins of the placed def
#		unplaced_components_map: map with the components of the unplaced def
#		unplaced_nets_map: map with the nets of the unplaced def
# Output:
#		merged_components_map: map with a merged def
# ------------------------------------------------------------------

#!/usr/bin/env python3

from utils import get_connected_components

def merge_defs(placed_components_map,placed_pins_map,unplaced_components_map,unplaced_nets_map,merged_components_map):
    not_done = False
    max_itter = 2
    for component in unplaced_components_map:
        if "x_location" in component:
            continue
        if component in placed_components_map.keys():
            merged_components_map[component] = unplaced_components_map[component]
            merged_components_map[component]["x_location"] = placed_components_map[component]["x_location"]
            merged_components_map[component]["y_location"] = placed_components_map[component]["y_location"]

        else:
            merged_components_map[component] = unplaced_components_map[component]
            
            gate_conn = []
            get_connected_components(component,gate_conn,unplaced_nets_map)
            x_coor_list = []
            y_coor_list = []
            
            for item in gate_conn:
                if item in placed_components_map:
                    x_coor_list.append(int(placed_components_map[item]["x_location"]))
                    y_coor_list.append(int(placed_components_map[item]["y_location"]))
                elif item in placed_pins_map:
                    x_coor_list.append(int(placed_pins_map[item]["x_location"]))
                    y_coor_list.append(int(placed_pins_map[item]["y_location"]))

            if len(x_coor_list) == 0:
                not_done = True
                print("Skipped "),
                print(component)
                continue
            min_x = min(x_coor_list)
            min_y = min(y_coor_list)

            max_x = max(x_coor_list)
            max_y = max(y_coor_list)

            merged_components_map[component]["x_location"] = int((max(x_coor_list)+min(x_coor_list))/2)
            merged_components_map[component]["y_location"] = int((max(y_coor_list)+min(y_coor_list))/2)
            
    
