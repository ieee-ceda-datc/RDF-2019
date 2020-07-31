################################################################################
#                       >  COPYRIGHT NOTICE  <
#
#  Copyright 2000 (c) Synopsys.
#
#
################################################################################
#
# Title        : EDA-tool callback function
#
# Project      : SDC-parser
#
# Authors      : A.Gratchev
#
# Description  : This is example of using EDA callback procedure which output
#                source of sdc-commands, based on parsed data structure
#
################################################################################

proc callback {command result} {
    upvar $result x
#    puts "Result: $command [array names x]"
    set res $command
    foreach par $sdc::procdefs($sdc::sdc_version,$command) {
        if {[lindex $par 0]==""} {
            set name [lindex $par end]
        } else {
            set name [lindex $par 0]
        }
        if {![info exists x($name)]} {
            continue
        }
        if {[string index $name 0]=="-"} {
            append res " $name"
        }
        switch -- [lindex $par 1] {
            float -
            Float -
            int -
            Int {
                append res " $x($name)"
            }
            string -
            String -
            enum -
            Enum {
                append res " \"$x($name)\""
            }
            flag -
            Flag {
            }
            list -
            List {
                if {[llength $x($name)]==1} {
                    if {[string match {\{\[*\]\}} $x($name)]} {
                        append res " [string range $x($name) 1 [expr {[string length $x($name)] - 2}]]"
                    } else {
                        append res " [list $x($name)]"
                    }
                } else {
                    append res " \[list [join $x($name)]\]"
                }
            }
            unknown -
            Unknown -
            default {
                append res " $x($name)"
            }
        }
        
    }
    if {[lsearch -exact {current_design current_instance all_clocks all_inputs all_outputs get_cells get_clocks get_libs get_lib_cells get_lib_pins get_nets get_pins get_ports} $command]==-1} {
        catch {
            set fname [::open "eda_result.sdc" a]
            puts $fname $res
            close $fname
        }
    }
    return "\{\[$res\]\}"
}

sdc::register_callback callback