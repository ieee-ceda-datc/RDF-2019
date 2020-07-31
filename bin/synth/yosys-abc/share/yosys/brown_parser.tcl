#!/bin/sh
################################################################################
#                       >  COPYRIGHT NOTICE  <
#                    Copyright 2017 Synopsys, Inc.
#                 Authors      : A.Gratchevz, Ibna Faruque
#
#
################################################################################
#
# Title        : SDC-parser command line application
#
################################################################################\
exec tclsh "$0" "$@"

source [file join [file dirname [info script]] sdc2.1 sdcparsercore.tcl]

proc parsed_command_callback {command parsing_result} {	
	upvar $parsing_result res
	switch -- $command {
		create_clock {
			#puts "Command: $command"
			#foreach arg [array names res] {
			#	puts "  Arg $arg = $res($arg)"
			#}
			#puts ""
			parsedCreateClockCallback $res(-period) $res(port_pin_list) $res(-name) 
			return ""
		}
		set_input_delay {
			parsedSetInputDelayCallback $res(port_pin_list) $res(-clock) $res(delay_value) 
			return ""
		}
		set_max_fanout {
			parsedSetMaxFanoutCallback $res(fanout_value) $res(object_list) 
			return ""
		}
		set_max_transition {
			parsedSetMaxTransitionCallback $res(transition_value) $res(object_list)
			return ""
		}
		get_clocks -
		get_ports {
			return $res(patterns)
		}
		# 1. add more commands to support here
		# 2. go define their callbacks in the c file
		# 3. call them from here
	}
}

sdc::register_callback parsed_command_callback
