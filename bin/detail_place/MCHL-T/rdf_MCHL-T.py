'''
    File name      : rdf_MCHL-T.py
    Author         : Jinwook Jung
    Created on     : Thu 08 Aug 2019 11:37:01 PM EDT
    Last modified  : 2019-08-08 23:40:06
    Description    : 
'''

import subprocess, os, sys, random, yaml, time
from subprocess import Popen, PIPE, CalledProcessError

# FIXME
sys.path.insert(0, '../../../src/stage.py')
from stage import *


def run(config, job_dir, prev_out_dir, user_parms):
    print("-"*79)
    print("Running MCHL...")
    print("-"*79)
    print("Job directory: {}".format(job_dir))
    print("Previous stage outputs: {}".format(prev_out_dir))

    mchl = MCHLRunner(config, job_dir, prev_out_dir, user_parms)
    mchl.run()

    print("Done.")
    print("")


class MCHLRunner(Stage):
    def __init__(self, config, job_dir, prev_out_dir, user_parms):
        super().__init__(config, job_dir, prev_out_dir, user_parms)

        self.lef_mod = "{}/merged_padded_spacing.lef".format(self.lib_dir)
        self.tech_lef = "{}/{}".format(self.lib_dir, self.lib_config["TECHLEF"])
        self.cell_lef = "{}/{}".format(self.lib_dir, self.lib_config["CELLLEF"])

    def run(self):
        print("Hello MCHL...")

        cmd = "{}/bin/detail_place/MCHL-T/MCHL-T".format(self.rdf_path)
        #cmd += " -lef {}".format(self.lef)
        cmd += " -tech_lef {}".format(self.tech_lef)
        cmd += " -cell_lef {}".format(self.cell_lef)
        cmd += " -input_def {}".format(self.in_def)
        cmd += " -cpu 4"
        cmd += " -output_def {}/out/{}.def".format(self.job_dir, self.design_name)

        print(cmd)

        with open("{}/out/{}.log".format(self.job_dir, self.design_name), 'a') as f:
            f.write("\n")
            f.write("# Command: {}\n".format(cmd))
            f.write("\n")
            run_shell_cmd(cmd, f)

        # Copy previous verilog file
        cmd = "ln -s {0}/{1}.v {2}/out/{1}.v" \
              .format(self.prev_out_dir, self.design_name, self.job_dir)

        run_shell_cmd(cmd)

