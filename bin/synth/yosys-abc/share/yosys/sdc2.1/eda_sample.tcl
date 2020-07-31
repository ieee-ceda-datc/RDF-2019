#!/bin/sh
#
# This is a simple example of EDA application
#
# It contains  
#
# - EDA callback procedure "callback_simple_example"
# - main program (register callback and parse file)
#
# The callback procedure
#   - prints parameter values for SDC commands
#     - create_clock
#     - set_input_delay
#   - returns parameter values for SDC Object Access Functions
#     (here without searching in Design Data Base)
#     - get_clocks
#     - get_ports
#
#\
exec tclsh "$0" "$@"

# include parser engine

source [file join [file dirname [info script]] sdcparsercore.tcl]

# callback procedure

proc callback_simple_example {command parsing_result} {
   
    # put reference to data structure after parsing

    upvar $parsing_result res

    # Switch on command type

    switch -- $command {


        create_clock -
        set_input_delay  { 
            puts "Command: $command"
            foreach arg [array names res] {
                puts "  Argument $arg = $res($arg)"
            }
            puts ""
            return ""
        }


        get_clocks -
        get_ports {
            return $res(patterns)
        }

        default {
        }
    }
}

# main program

sdc::register_callback callback_simple_example

sdc::parse_file [lindex $argv 0]