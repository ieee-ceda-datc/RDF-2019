'''
    File name      : rdf_RePlAce.py
    Author         : Jinwook Jung
    Created on     : Tue 30 Jul 2019 10:31:18 PM EDT
    Last modified  : 2020-01-06 15:22:58
    Description    : 
'''

import subprocess, os, sys, random, yaml, time
from subprocess import Popen, PIPE, CalledProcessError

# FIXME
sys.path.insert(0, '../../../src/stage.py')
from stage import *


def run(config, stage_dir, prev_out_dir, user_parms, write_run_scripts=False):
    print("-"*79)
    print("Running RePlAce...")
    print("-"*79)
    print("Job directory: {}".format(stage_dir))
    print("Previous stage outputs: {}".format(prev_out_dir))

    replace = RePlAceRunner(config, stage_dir, prev_out_dir, user_parms)
    replace.write_run_scripts()

    if not write_run_scripts:
        replace.run()

    print("Done.")
    print("")


class RePlAceRunner(Stage):
    def __init__(self, config, stage_dir, prev_out_dir, user_parms):
        super().__init__(config, stage_dir, prev_out_dir, user_parms)

        self.lef_mod = "{}/merged_padded_spacing.lef".format(self.lib_dir)

    def write_run_scripts(self):
        cmds = list()

        cmd = "${RDF_TOOL_BIN_PATH}/global_place/RePlAce/RePlAce"
        cmd += " -bmflag etc"
        # cmd += " -lef {}".format(self.lef)
        cmd += " -lef {}".format(self.lef_mod)
        cmd += " -def {}".format(self.in_def)
        cmd += " -den {}".format(float(self.user_parms["target_density"]))
        cmd += " -onlyGP"
        cmd += " -output {}".format(self.stage_dir)
        cmds.append(cmd)

        cmd = "ln -s {0}/etc/{1}/experiment000/{1}_final.def {0}/out/{1}.def" \
              .format(self.stage_dir, self.design_name)
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

    def _copy_final_output(self):
        cmd = "ln -s {0}/etc/{1}/experiment000/{1}_final.def {0}/out/{1}.def" \
              .format(self.stage_dir, self.design_name)

        run_shell_cmd(cmd)

        # Copy previous verilog file
        cmd = "ln -s {0}/{1}.v {2}/out/{1}.v" \
              .format(self.prev_out_dir, self.design_name, self.stage_dir)

        run_shell_cmd(cmd)

