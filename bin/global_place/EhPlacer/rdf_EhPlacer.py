'''
    File name      : rdf_EhPlacer.py
    Author         : Jinwook Jung
    Created on     : Thu 08 Aug 2019 09:58:40 PM EDT
    Last modified  : 2020-04-30 21:57:00
    Description    : 
'''

import subprocess, os, sys, random, yaml, time
from subprocess import Popen, PIPE, CalledProcessError

# FIXME
sys.path.insert(0, '../../../src/stage.py')
from stage import *


def run(config, stage_dir, prev_out_dir, user_parms, write_run_scripts=False):
    print("-"*79)
    print("Running EhPlacer...")
    print("-"*79)
    print("Job directory: {}".format(stage_dir))
    print("Previous stage outputs: {}".format(prev_out_dir))

    ehplacer = EhPlacerRunner(config, stage_dir, prev_out_dir, user_parms)
    ehplacer.write_run_scripts()
    if not write_run_scripts:
        ehplacer.run()

    print("Done.")
    print("")


class EhPlacerRunner(Stage):
    def __init__(self, config, stage_dir, prev_out_dir, user_parms):
        super().__init__(config, stage_dir, prev_out_dir, user_parms)

        self.lef_mod = "{}/merged_padded_spacing.lef".format(self.lib_dir)

    def write_run_scripts(self):
        # Create constraint file
        # FIXME: Check the existence of each user parm and its value range.
        const_file = "{}/placement_constraints".format(self.stage_dir)
        with open(const_file, 'w') as f:
            if "target_density" in self.user_parms.keys():
                target_util = 100 * float(self.user_parms["target_density"])
            else:
                target_util = 90

            f.write("maximum_utilization={}%\n".format(target_util))

        cmds = list()

        cmd = "cd {} && {}/bin/global_place/EhPlacer/bin/EhPlacer".format(self.stage_dir, self.rdf_path)
        # FIXME: Do we need to use merged_padded_spacing.lef here?
        cmd += " -tech_lef {}".format(self.lef_mod)
        cmd += " -cell_lef {}".format(self.lef_mod)
        cmd += " -floorplan_def {}".format(self.in_def)
        cmd += " -placement_constraints {}".format(const_file)
        cmd += " -cpu 8"
        cmd += " -output {}/out.def".format(self.stage_dir)
        cmds.append(cmd)

        self.create_run_script_template()
        with open("{}/run.sh".format(self.stage_dir), 'a') as f:
            [f.write("{}\n".format(_)) for _ in cmds]

#        with open("{}/out/{}.log".format(self.stage_dir, self.design_name), 'a') as f:
#            f.write("\n")
#            f.write("# Command: {}\n".format(cmd))
#            f.write("\n")
#            run_shell_cmd(cmd, f)
#
#        self._copy_final_output()

    def run(self):
        pass

    def _copy_final_output(self):
        cmd = "ln -s {0}/out.def {0}/out/{1}.def" \
              .format(self.stage_dir, self.design_name)

        run_shell_cmd(cmd)

        # Copy previous verilog file
        cmd = "ln -s {0}/{1}.v {2}/out/{1}.v" \
              .format(self.prev_out_dir, self.design_name, self.stage_dir)

        run_shell_cmd(cmd)

