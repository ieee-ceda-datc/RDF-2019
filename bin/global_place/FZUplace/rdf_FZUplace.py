'''
    File name      : rdf_FZUplace.py
    Author         : Jinwook Jung
    Created on     : Wed 14 Aug 2019 12:08:23 AM EDT
    Last modified  : 2020-03-30 22:54:26
    Description    : 
'''

import subprocess, os, sys, random, yaml, time
from subprocess import Popen, PIPE, CalledProcessError

# FIXME
sys.path.insert(0, '../../../src/stage.py')
from stage import *


def run(config, stage_dir, prev_out_dir, user_parms, write_run_scripts):
    print("-"*79)
    print("Running FZUplace...")
    print("-"*79)
    print("Job directory: {}".format(stage_dir))
    print("Previous stage outputs: {}".format(prev_out_dir))

    fzu = FZUplaceRunner(config, stage_dir, prev_out_dir, user_parms)
    fzu.write_run_scripts()
    if not write_run_scripts:
        fzu.run()

    print("Done.")
    print("")


class FZUplaceRunner(Stage):
    def __init__(self, config, stage_dir, prev_out_dir, user_parms):
        super().__init__(config, stage_dir, prev_out_dir, user_parms)

        self.lef_mod = "{}/merged_padded_spacing.lef".format(self.lib_dir)

        # FIXME
        self.bookshelf = "bookshelf.aux"

    def write_run_scripts(self):
        cmds = list()
        # FZUplace assumes bookshelf is stored at the directory under run directory.
        cmd = "mkdir {}/bookshelf".format(self.stage_dir)

        cmds.append(cmd)

        # Write bookshelf
        cmd = "cd {}/bookshelf && {}/src/util/bookshelf_writer".format(self.stage_dir, self.rdf_path)
        cmd += " --lef {}".format(self.lef_mod)
        cmd += " --def {}".format(self.in_def)
        cmd += " --bookshelf bookshelf"

        cmds.append(cmd)

        # Run
        cmd = "cd {} && {}/bin/global_place/FZUplace/FZUplace".format(self.stage_dir, self.rdf_path)
        cmd += " -aux bookshelf/{}".format(self.bookshelf)
        if "target_density" in self.user_parms.keys():
            cmd += " -util {}".format(float(self.user_parms["target_density"]))
        cmd += " -nolegal -nodetail"

        cmds.append(cmd)

        # Write DEF
        cmd = "cd {} && {}/src/util/place_updater".format(self.stage_dir, self.rdf_path)
        cmd += " --lef {}".format(self.lef_mod)
        cmd += " --def {}".format(self.in_def)
        cmd += " --pl {}/output/bookshelf/bookshelf.pl".format(self.stage_dir)

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
        print("Hello FZUplace...")

        self._write_bookshelf()

        self._run_fzu_place()

        self._write_def()

        self._copy_final_output()

    def _write_bookshelf(self):
        # FZUplace assumes bookshelf is stored at the directory under run directory.
        os.mkdir("{}/bookshelf".format(self.stage_dir))

        cmd = "cd {}/bookshelf && {}/src/util/lefdef_util/bookshelf_writer/bookshelf_writer".format(self.stage_dir, self.rdf_path)
        cmd += " --lef {}".format(self.lef_mod)
        cmd += " --def {}".format(self.in_def)
        cmd += " --bookshelf bookshelf"

        print(cmd)

        with open("{}/out/{}.log".format(self.stage_dir, self.design_name), 'a') as f:
            f.write("\n")
            f.write("# Command: {}\n".format(cmd))
            f.write("\n")
            run_shell_cmd(cmd, f)

    def _run_fzu_place(self):
        cmd = "cd {} && {}/bin/global_place/FZUplace/FZUplace".format(self.stage_dir, self.rdf_path)
        cmd += " -aux bookshelf/{}".format(self.bookshelf)
        if "target_density" in self.user_parms.keys():
            cmd += " -util {}".format(float(self.user_parms["target_density"]))
        cmd += " -nolegal -nodetail"

        print(cmd)

        with open("{}/out/{}.log".format(self.stage_dir, self.design_name), 'a') as f:
            f.write("\n")
            f.write("# Command: {}\n".format(cmd))
            f.write("\n")
            run_shell_cmd(cmd, f)

    def _write_def(self):
        cmd = "cd {} && {}/src/util/lefdef_util/place_updater/place_updater".format(self.stage_dir, self.rdf_path)
        cmd += " --lef {}".format(self.lef_mod)
        cmd += " --def {}".format(self.in_def)
        cmd += " --pl {}/output/bookshelf/bookshelf.pl".format(self.stage_dir)

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

