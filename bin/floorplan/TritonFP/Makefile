# ==============================================================================
#  _____ _     ___   ___  ____  ____  _        _    _   _
# |  ___| |   / _ \ / _ \|  _ \|  _ \| |      / \  | \ | |
# | |_  | |  | | | | | | | |_) | |_) | |     / _ \ |  \| |
# |  _| | |__| |_| | |_| |  _ <|  __/| |___ / ___ \| |\  |
# |_|   |_____\___/ \___/|_| \_\_|   |_____/_/   \_\_| \_|
#
floorplan: $(RESULTS_DIR)/2_floorplan.def \
           $(RESULTS_DIR)/2_floorplan.v \
           $(RESULTS_DIR)/2_floorplan.sdc
# ==============================================================================


# STEP 1: Translate verilog to def
#-------------------------------------------------------------------------------

$(RESULTS_DIR)/2_1_floorplan.def: $(TECH_DIR)/merged.lef $(RESULTS_DIR)/1_synth.v
	@$(call BANNER, 2. FLOORPLAN)
	verilog2def \
	  -lef $(TECH_DIR)/merged.lef \
	  $(foreach file,$(LIB_FILES),-liberty $(file)) \
	  -verilog $(RESULTS_DIR)/1_synth.v \
	  -top_module $(DESIGN_NAME) \
	  -units 2000 \
	  -site $(PLACE_SITE) \
	  -die_area "$(DIE_AREA)" \
	  -core_area "$(CORE_AREA)" \
	  -tracks $(TRACKS_INFO_FILE) \
	  -def $@ \
	  2>&1 | tee $(LOG_DIR)/2_1_verilog2def.log
	sed -i 's/VERSION 5.5/VERSION 5.6/' $@
#TODO Update to use utilization

# STEP 2: IO Placement
#-------------------------------------------------------------------------------
$(RESULTS_DIR)/2_2_floorplan_io.def: $(TECH_DIR)/merged.lef $(RESULTS_DIR)/2_1_floorplan.def
	ioPlacer --input-lef $(TECH_DIR)/merged.lef \
	         --input-def $(RESULTS_DIR)/2_1_floorplan.def \
	         --output $@ \
	         --hmetal 5 \
	         --vmetal 6 \
	         --random 1 \
	         --force-spread 1 \
	         --wirelen 1 \
	         2>&1 | tee $(LOG_DIR)/2_2_ioPlacer.log

# STEP 3: Timing Driven Mixed Sized Placement
# Only run if required
#-------------------------------------------------------------------------------
$(RESULTS_DIR)/2_3_floorplan_tdms.def: $(RESULTS_DIR)/2_2_floorplan_io.def $(RESULTS_DIR)/1_synth.v $(RESULTS_DIR)/1_synth.sdc $(LIB_FILES) $(TECH_DIR)/merged_padded.lef | ./PORT9.dat ./POST9.dat ./POWV9.dat
ifeq ($(RUN_MACRO_PLACEMENT),1)
	RePlAce \
	  -bmflag etc \
	  -lef $(TECH_DIR)/merged_padded.lef \
	  -def $(RESULTS_DIR)/2_2_floorplan_io.def  \
	  -verilog $(RESULTS_DIR)/1_synth.v \
	  $(foreach file,$(LIB_FILES),-lib $(file)) \
	  -sdc $(RESULTS_DIR)/1_synth.sdc \
	  -output $(RESULTS_DIR)/td-ms-replace \
	  -t 1 \
	  -timing \
	  -resPerMicron $(RES_PER_MICRON) \
	  -capPerMicron $(CAP_PER_MICRON) \
	  -skipIP \
	  -plot \
	  -experi output \
	  -den 0.7 \
	  -onlyGP \
	  2>&1 | tee $(LOG_DIR)/2_3_TD-MS-RePlAce.log
	cp $(RESULTS_DIR)/td-ms-replace/etc/2_2_floorplan_io/output/2_2_floorplan_io_final.def $@
else
	cp $< $@
endif

# STEP 4: Macro Placement
# Only run if required
#-------------------------------------------------------------------------------
$(RESULTS_DIR)/2_4_floorplan_macro.def: $(RESULTS_DIR)/2_3_floorplan_tdms.def $(TECH_DIR)/merged_padded.lef $(RESULTS_DIR)/1_synth.v $(RESULTS_DIR)/1_synth.sdc $(IP_GLOBAL_CFG)
ifeq ($(RUN_MACRO_PLACEMENT),1)
	fplan $(foreach file,$(LIB_FILES),-lib $(file)) \
	    -verilog $(RESULTS_DIR)/1_synth.v \
	    -lef $(TECH_DIR)/merged_padded.lef \
	    -def $(RESULTS_DIR)/2_3_floorplan_tdms.def \
	    -design $(DESIGN_NAME) \
	    -sdc $(RESULTS_DIR)/1_synth.sdc \
	    -output $(DESIGN_NAME) \
	    -globalConfig $(IP_GLOBAL_CFG) \
	    -depth 3 \
	    -plot \
	    -westFix \
	    | tee $(LOG_DIR)/2_4_fplan.log
	    mv $(DESIGN_NAME)_best.def $@
else
	cp $< $@
endif

# STEP 5: PDN generation
#-------------------------------------------------------------------------------
$(RESULTS_DIR)/2_5_floorplan_pdn.def: $(RESULTS_DIR)/2_4_floorplan_macro.def
ifneq ($(PDN_CFG),)
	apply_pdn $(PDN_CFG) | tee $(LOG_DIR)/2_5_apply_pdn.log
	mv $(DESIGN_NAME)_post_T8.def $@
else
	cp $< $@
endif


# STEP 6: Tapcell and Welltie insertion
#-------------------------------------------------------------------------------
$(RESULTS_DIR)/2_6_floorplan_tapcell.def: $(TECH_DIR)/merged.lef $(RESULTS_DIR)/2_5_floorplan_pdn.def
	cp $(RESULTS_DIR)/2_5_floorplan_pdn.def $@
	tapcell -lef $(TECH_DIR)/merged.lef \
	        -def $(RESULTS_DIR)/2_5_floorplan_pdn.def \
	        -rule $(WELLTTAP_RULE) \
	        -welltap $(WELLTIE_CELL) \
	        -endcap $(ENDCAP_CELL) \
	        -rows \
	        -outdef $@ | tee $(LOG_DIR)/2_6_tapcell.log

$(RESULTS_DIR)/2_floorplan.def: $(RESULTS_DIR)/2_6_floorplan_tapcell.def
	cp $< $@

$(RESULTS_DIR)/2_floorplan.v: $(RESULTS_DIR)/1_synth.v
	cp $< $@

$(RESULTS_DIR)/2_floorplan.sdc: $(RESULTS_DIR)/1_synth.sdc
	cp $< $@


clean_floorplan:
	rm -rf $(RESULTS_DIR)/2_*floorplan*.def
	rm -rf $(RESULTS_DIR)/2_floorplan.v $(RESULTS_DIR)/2_floorplan.sdc

