'''
    File name      : rdf_ComPLx.py
    Author         : Jinwook Jung
    Created on     : Tue 13 Aug 2019 11:52:53 PM EDT
    Last modified  : 2020-03-30 22:54:24
    Description    : 
'''

import subprocess, os, sys, random, yaml, time
from subprocess import Popen, PIPE, CalledProcessError

# FIXME
sys.path.insert(0, '../../../src/stage.py')
from stage import *


def run(config, stage_dir, prev_out_dir, user_parms, write_run_scripts):
    print("-"*79)
    print("Running ComPLx...")
    print("-"*79)
    print("Job directory: {}".format(stage_dir))
    print("Previous stage outputs: {}".format(prev_out_dir))

    complx = ComPLxRunner(config, stage_dir, prev_out_dir, user_parms)
    complx.write_run_scripts()
    if not write_run_scripts:
        complx.run()

    print("Done.")
    print("")


class ComPLxRunner(Stage):
    def __init__(self, config, stage_dir, prev_out_dir, user_parms):
        super().__init__(config, stage_dir, prev_out_dir, user_parms)

        self.lef_mod = "{}/merged_padded_spacing.lef".format(self.lib_dir)

        # FIXME
        self.bookshelf = "out.aux"

    def write_run_scripts(self):
        cmds = list()

        # Write bookshelf
        cmd = "cd {} && {}/src/util/bookshelf_writer".format(self.stage_dir, self.rdf_path)
        cmd += " --lef {}".format(self.lef_mod)
        cmd += " --def {}".format(self.in_def)

        cmds.append(cmd)

        # Run
        cmd = "cd {} && {}/bin/global_place/ComPLx/ComPLx.exe".format(self.stage_dir, self.rdf_path)
        cmd += " -f {}".format(self.bookshelf)
        if "target_density" in self.user_parms.keys():
            cmd += " -ut {}".format(float(self.user_parms["target_density"]))

        cmds.append(cmd)

        # Write DEF
        cmd = "cd {} && {}/src/util/place_updater".format(self.stage_dir, self.rdf_path)
        cmd += " --lef {}".format(self.lef_mod)
        cmd += " --def {}".format(self.in_def)
        cmd += " --pl {}/out-ComPLx.pl".format(self.stage_dir)

        cmds.append(cmd)

        # Copy
        cmd = "ln -s {0}/out.def {0}/out/{1}.def" \
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
        print("Hello ComPLx...")

        self._write_bookshelf()

        self._run_complx()

        self._write_def()

        self._copy_final_output()

    def _write_bookshelf(self):
        cmd = "cd {} && {}/bin/global_place/ComPLx/bookshelf_writer".format(self.stage_dir, self.rdf_path)
        cmd += " --lef {}".format(self.lef_mod)
        cmd += " --def {}".format(self.in_def)

        print(cmd)

        with open("{}/out/{}.log".format(self.stage_dir, self.design_name), 'a') as f:
            f.write("\n")
            f.write("# Command: {}\n".format(cmd))
            f.write("\n")
            run_shell_cmd(cmd, f)

    def _run_complx(self):
        cmd = "cd {} && {}/bin/global_place/ComPLx/ComPLx.exe".format(self.stage_dir, self.rdf_path)
        cmd += " -f {}".format(self.bookshelf)
        if "target_density" in self.user_parms.keys():
            cmd += " -ut {}".format(float(self.user_parms["target_density"]))

        print(cmd)

        with open("{}/out/{}.log".format(self.stage_dir, self.design_name), 'a') as f:
            f.write("\n")
            f.write("# Command: {}\n".format(cmd))
            f.write("\n")
            run_shell_cmd(cmd, f)

    def _write_def(self):
        cmd = "cd {} && {}/bin/global_place/ComPLx/place_updater".format(self.stage_dir, self.rdf_path)
        cmd += " --lef {}".format(self.lef_mod)
        cmd += " --def {}".format(self.in_def)
        cmd += " --pl {}/out-ComPLx.pl".format(self.stage_dir)

        print(cmd)

        with open("{}/out/{}.log".format(self.stage_dir, self.design_name), 'a') as f:
            f.write("\n")
            f.write("# Command: {}\n".format(cmd))
            f.write("\n")
            run_shell_cmd(cmd, f)

    def _copy_final_output(self):
        cmd = "ln -s {0}/out.def {0}/out/{1}.def" \
              .format(self.stage_dir, self.design_name)

        run_shell_cmd(cmd)

        # Copy previous verilog file
        cmd = "ln -s {0}/{1}.v {2}/out/{1}.v" \
              .format(self.prev_out_dir, self.design_name, self.stage_dir)

        run_shell_cmd(cmd)

