'''
    File name      : rdf_NTUplace3.py
    Author         : Jinwook Jung
    Created on     : Wed 14 Aug 2019 12:20:30 AM EDT
    Last modified  : 2020-04-30 22:59:12
    Description    : 
'''

import subprocess, os, sys, random, yaml, time
from subprocess import Popen, PIPE, CalledProcessError

# FIXME
sys.path.insert(0, '../../../src/stage.py')
from stage import *


def run(config, job_dir, prev_out_dir, user_parms):
    print("-"*79)
    print("Running NTUplace...")
    print("-"*79)
    print("Job directory: {}".format(job_dir))
    print("Previous stage outputs: {}".format(prev_out_dir))

    ntu = NTUplaceRunner(config, job_dir, prev_out_dir, user_parms)
    ntu.run()

    print("Done.")
    print("")


class NTUplaceRunner(Stage):
    def __init__(self, config, job_dir, prev_out_dir, user_parms):
        super().__init__(config, job_dir, prev_out_dir, user_parms)

        self.lef_mod = "{}/merged_padded_spacing.lef".format(self.lib_dir)

        # FIXME
        self.bookshelf = "out.aux"

    def run(self):
        print("Hello NTUplace...")

        self._write_bookshelf()

        self._run_ntu_place()

        self._write_def()

        self._copy_final_output()

    def _write_bookshelf(self):
        cmd = "cd {} && {}/src/util/lefdef_util/bookshelf_writer/bookshelf_writer".format(self.job_dir, self.rdf_path)
        cmd += " --lef {}".format(self.lef_mod)
        cmd += " --def {}".format(self.in_def)

        print(cmd)

        with open("{}/out/{}.log".format(self.job_dir, self.design_name), 'a') as f:
            f.write("\n")
            f.write("# Command: {}\n".format(cmd))
            f.write("\n")
            run_shell_cmd(cmd, f)

    def _run_ntu_place(self):
        cmd = "cd {} && {}/bin/global_place/NTUplace3/ntuplace3".format(self.job_dir, self.rdf_path)
        cmd += " -aux {}".format(self.bookshelf)
        if "target_density" in self.user_parms.keys():
            cmd += " -util {}".format(float(self.user_parms["target_density"]))

        print(cmd)

        with open("{}/out/{}.log".format(self.job_dir, self.design_name), 'a') as f:
            f.write("\n")
            f.write("# Command: {}\n".format(cmd))
            f.write("\n")
            run_shell_cmd(cmd, f)

    def _write_def(self):
        cmd = "cd {} && {}/src/util/lefdef_util/place_updater/place_updater".format(self.job_dir, self.rdf_path)
        cmd += " --lef {}".format(self.lef_mod)
        cmd += " --def {}".format(self.in_def)
        cmd += " --pl {}/out.ntup.pl".format(self.job_dir)

        print(cmd)

        with open("{}/out/{}.log".format(self.job_dir, self.design_name), 'a') as f:
            f.write("\n")
            f.write("# Command: {}\n".format(cmd))
            f.write("\n")
            run_shell_cmd(cmd, f)

    def _copy_final_output(self):
        cmd = "ln -s {0}/out.def {0}/out/{1}.def" \
              .format(self.job_dir, self.design_name)

        run_shell_cmd(cmd)

        # Copy previous verilog file
        cmd = "ln -s {0}/{1}.v {2}/out/{1}.v" \
              .format(self.prev_out_dir, self.design_name, self.job_dir)

        run_shell_cmd(cmd)

