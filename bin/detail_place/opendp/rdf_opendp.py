'''
    File name      : rdf_OpenDP.py
    Author         : Jinwook Jung
    Created on     : Tue 30 Jul 2019 10:31:18 PM EDT
    Last modified  : 2019-08-08 21:29:24
    Description    : 
'''

import subprocess, os, sys, random, yaml, time
from subprocess import Popen, PIPE, CalledProcessError

# FIXME
sys.path.insert(0, '../../../src/stage.py')
from stage import *


def run(config, stage_dir, prev_out_dir, user_parms, write_run_scripts=False):
    print("-"*79)
    print("Running OpenDP...")
    print("-"*79)
    print("Job directory: {}".format(stage_dir))
    print("Previous stage outputs: {}".format(prev_out_dir))

    opendp = OpenDPRunner(config, stage_dir, prev_out_dir, user_parms)
    opendp.write_run_scripts()

    if not write_run_scripts:
        opendp.run()

    print("Done.")
    print("")


class OpenDPRunner(Stage):
    def __init__(self, config, stage_dir, prev_out_dir, user_parms):
        super().__init__(config, stage_dir, prev_out_dir, user_parms)

        self.lef_mod = "{}/merged_padded_spacing.lef".format(self.lib_dir)

    def write_run_scripts(self):
        cmds = list()

        cmd = "${RDF_TOOL_BIN_PATH}/detail_place/opendp/opendp"
        #cmd += " -lef {}".format(self.lef)
        cmd += " -lef {}".format(self.lef_mod)
        cmd += " -def {}".format(self.in_def)
        cmd += " -cpu 4"
        cmd += " -output_def {}/out/{}.def".format(self.stage_dir, self.design_name)
        cmds.append(cmd)

        # Copy previous verilog file
        cmd = "ln -s {0}/{1}.v {2}/out/{1}.v" \
              .format(self.prev_out_dir, self.design_name, self.stage_dir)
        cmds.append(cmd)

        self.create_run_script_template()
        with open("{}/run.sh".format(self.stage_dir), 'a') as f:
            [f.write("{}\n".format(_)) for _ in cmds]

    def run(self):
        pass

