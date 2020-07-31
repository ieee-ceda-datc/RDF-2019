'''
    File name      : rdf_FastRoute4-lefdef.py
    Author         : Jinwook Jung
    Created on     : Tue 30 Jul 2019 11:26:08 PM EDT
    Last modified  : 2020-01-06 15:30:47
    Description    : 
'''

import subprocess, os, sys, random, yaml, time
from subprocess import Popen, PIPE, CalledProcessError

# FIXME
sys.path.insert(0, '../../../src/stage.py')
from stage import *


def run(config, stage_dir, prev_out_dir, user_parms, write_run_scripts=False):
    print("-"*79)
    print("Running FastRoute4-lefdef...")
    print("-"*79)
    print("Job directory: {}".format(stage_dir))
    print("Previous stage outputs: {}".format(prev_out_dir))

    fastroute = FastRouteRunner(config, stage_dir, prev_out_dir, user_parms)
    fastroute.write_run_scripts()

    if not write_run_scripts:
        fastroute.run()

    print("Done.")
    print("")


class FastRouteRunner(Stage):
    def __init__(self, config, stage_dir, prev_out_dir, user_parms):
        super().__init__(config, stage_dir, prev_out_dir, user_parms)

    def write_run_scripts(self):
        self._write_rsyn_script()

        # Write run script
        cmds = list()

        for flute_file in ("PORT9.dat", "POST9.dat", "POWV9.dat"):
            cmd = "ln -s ${{RDF_TOOL_BIN_PATH}}/global_route/FastRoute4-lefdef/{} {}" \
                .format(flute_file, self.stage_dir)
            cmds.append(cmd)

        cmd = "cd {};".format(self.stage_dir)
        cmd += "${RDF_TOOL_BIN_PATH}/global_route/FastRoute4-lefdef/FRlefdef"
        cmd += " --no-gui"
        cmd += " --script fastroute.rsyn".format(self.stage_dir)
        cmds.append(cmd)

        # Copy previous DEF
        cmd = "ln -s {0}/{1}.def {2}/out/{1}.def" \
              .format(self.prev_out_dir, self.design_name, self.stage_dir)
        cmds.append(cmd)

        # Copy previous Verilog
        cmd = "ln -s {0}/{1}.v {2}/out/{1}.v" \
              .format(self.prev_out_dir, self.design_name, self.stage_dir)
        cmds.append(cmd)

        # Copy output route guide.
        cmd = "ln -s {0}/route.guide {0}/out/{1}.guide" \
              .format(self.stage_dir, self.design_name)
        cmds.append(cmd)

        self.create_run_script_template()
        with open("{}/run.sh".format(self.stage_dir), 'a') as f:
            [f.write("{}\n".format(_)) for _ in cmds]


    def run(self):
        print("Hello FastRoute4-lefdef...")

        self._write_rsyn_script()

        self._run_fastroute()

        self._copy_final_output()

    def _write_rsyn_script(self):
        with open("{}/fastroute.rsyn".format(self.stage_dir), 'w') as f:
            f.write("open \"generic\" {\n")
            #f.write("  \"lefFiles\" : \"{}\",\n".format(self.lef))
            f.write("  \"lefFiles\" : \"{}/merged_padded_spacing.lef\",\n".format(self.lib_dir))
            f.write("  \"defFiles\" : \"{}/{}.def\"\n".format(self.prev_out_dir, self.design_name))
            f.write("};\n")
            f.write("\n")
            f.write("run \"rsyn.fastRoute\" {\"outfile\" : \"route.guide\"};\n")
            f.write("\n")
            f.write("# outfile: string. indicate the name of the generated guides file\n")
            f.write("# adjustment: float. indicate the percentage reduction of each edge\n")
            f.write("# maxRoutingLayer: integer. indicate the max routing layer available for FastRoute\n")

    def _run_fastroute(self):
        for flute_file in ("PORT9.dat", "POST9.dat", "POWV9.dat"):
            cmd = "ln -s ${{RDF_TOOL_BIN_PATH}}/global_route/FastRoute4-lefdef/{} {}" \
                .format(flute_file, self.stage_dir)

            print(cmd)

            with open("{}/out/{}.log".format(self.stage_dir, self.design_name), 'a') as f:
                f.write("\n")
                f.write("# Command: {}\n".format(cmd))
                f.write("\n")
                run_shell_cmd(cmd, f)

        cmd = "cd {};".format(self.stage_dir)
        cmd += "${RDF_TOOL_BIN_PATH}/global_route/FastRoute4-lefdef/FRlefdef"
        cmd += " --no-gui"
        cmd += " --script fastroute.rsyn".format(self.stage_dir)

        print(cmd)

        with open("{}/out/{}.log".format(self.stage_dir, self.design_name), 'a') as f:
            f.write("\n")
            f.write("# Command: {}\n".format(cmd))
            f.write("\n")
            run_shell_cmd(cmd, f)

    def _copy_final_output(self):
        # Copy previous DEF
        cmd = "ln -s {0}/{1}.def {2}/out/{1}.def" \
              .format(self.prev_out_dir, self.design_name, self.stage_dir)

        run_shell_cmd(cmd)

        # Copy previous Verilog
        cmd = "ln -s {0}/{1}.v {2}/out/{1}.v" \
              .format(self.prev_out_dir, self.design_name, self.stage_dir)

        run_shell_cmd(cmd)

        # Copy output route guide.
        cmd = "ln -s {0}/route.guide {0}/out/{1}.guide" \
              .format(self.stage_dir, self.design_name)

        run_shell_cmd(cmd)

