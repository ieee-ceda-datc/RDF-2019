'''
    File name      : rdf_TritonCTS.py
    Author         : Jinwook Jung
    Created on     : Tue 30 Jul 2019 11:26:08 PM EDT
    Last modified  : 2020-01-06 15:30:07
    Description    : 
'''

import subprocess, os, sys, random, yaml, time
from subprocess import Popen, PIPE, CalledProcessError

# FIXME
sys.path.insert(0, '../../../src/stage.py')
from stage import *


def run(config, stage_dir, prev_out_dir, user_parms, write_run_scripts=False):
    print("-"*79)
    print("Running TritonCTS...")
    print("-"*79)
    print("Job directory: {}".format(stage_dir))
    print("Previous stage outputs: {}".format(prev_out_dir))

    triton_cts = TritonCTSRunner(config, stage_dir, prev_out_dir, user_parms)
    triton_cts.write_run_scripts()

    if not write_run_scripts:
        triton_cts.run()

    print("Done.")
    print("")


class TritonCTSRunner(Stage):
    def __init__(self, config, stage_dir, prev_out_dir, user_parms):
        super().__init__(config, stage_dir, prev_out_dir, user_parms)

    def write_run_scripts(self):
        cmds = list()

        cmd = "ln -s ${RDF_TOOL_BIN_PATH}/cts/TritonCTS/write_config.py"
        cmds.append(cmd)

        cmd = "python write_config.py \\\n"
        cmd += "  --design_name {} \\\n".format(self.design_name)
        cmd += "  --prev_out_dir {} \\\n".format(self.prev_out_dir)
        cmd += "  --lib_dir {} \\\n".format(self.lib_dir)
        cmd += "  --process {} \\\n".format(self.lib_config["PROCESS"])
        cmd += "  --clk_port {} \\\n".format(self.design_config["clock_port"])
        cmd += "  --root_buf {} \\\n".format(self.lib_config["CTS_BUF_CELL"])
        cmds.append(cmd)

        cmd = "${RDF_TOOL_BIN_PATH}/cts/TritonCTS/runTritonCTS.tcl"
        cmd += " -configFilePath={}/{}".format(self.stage_dir, "triton_cts.cfg")
        cmd += " -scriptsPath=${RDF_TOOL_BIN_PATH}/cts/TritonCTS/scripts"
        cmd += " -techFilesPath={}/{}".format(self.lib_dir, self.lib_config["CTS_TECH_DIR"])
        cmd += " -lefDefParserPath=${RDF_TOOL_BIN_PATH}/cts/TritonCTS/bin/lefdef2cts"
        cmd += " -executablePath=${RDF_TOOL_BIN_PATH}/cts/TritonCTS/bin/genHtree"
        cmd += " -legalizerPath=${RDF_TOOL_BIN_PATH}/detail_place/opendp/opendp"
        cmd += " -outputPath={}/TritonCTS".format(self.stage_dir)
        cmds.append(cmd)

        # Copy final output
        cmd = "ln -s {0}/TritonCTS/cts_final.def {0}/out/{1}.def" \
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

    def _write_config_file(self):
        # FIXME: Get width and height of the design....
        with open("{}/{}.def".format(self.prev_out_dir, self.design_name)) as f:
            lines = [l for l in (_.strip() for _ in f) if l]

        units, w_dbu, h_dbu = (None,)*3
        for l in lines:
            if l.startswith("UNITS"):
                tokens = l.split()
                units = int(tokens[3])
            elif l.startswith("DIEAREA"):
                tokens = l.split()
                w_dbu, h_dbu = int(tokens[6]), int(tokens[7])
        w, h = float(w_dbu)/units, float(h_dbu)/units

        with open("{}/triton_cts.cfg".format(self.stage_dir), 'w') as f:
            f.write("lef {}/merged_padded_spacing.lef\n".format(self.lib_dir))
            f.write("path {}/{}.def\n".format(self.prev_out_dir, self.design_name))
            f.write("verilog {}/{}.v\n".format(self.prev_out_dir, self.design_name))
            f.write("design {}/{}.v\n".format(self.prev_out_dir, self.design_name))
            f.write("target_skew {}\n".format(50))
            f.write("width {}\n".format(w))
            f.write("height {}\n".format(h))
            f.write("tech {}\n".format(self.lib_config["PROCESS"]))
            f.write("ck_port {}\n".format(self.config["design"]["clock_port"]))
            f.write("db_units {}\n".format(2000))
            f.write("root_buff {}\n".format(self.lib_config["CTS_BUF_CELL"]))
            f.write("toler {}\n".format(1000))

    def _run_triton_cts(self):
        cmd = "${RDF_TOOL_BIN_PATH}/cts/TritonCTS/runTritonCTS.tcl"
        cmd += " -configFilePath={}/{}".format(self.stage_dir, "triton_cts.cfg")
        cmd += " -scriptsPath=${RDF_TOOL_BIN_PATH}/cts/TritonCTS/scripts"
        cmd += " -techFilesPath={}/{}".format(self.lib_dir, self.lib_config["CTS_TECH_DIR"])
        cmd += " -lefDefParserPath=${RDF_TOOL_BIN_PATH}/cts/TritonCTS/bin/lefdef2cts"
        cmd += " -executablePath=${RDF_TOOL_BIN_PATH}/cts/TritonCTS/bin/genHtree"
        cmd += " -legalizerPath=${RDF_TOOL_BIN_PATH}/detail_place/opendp/opendp"
        cmd += " -outputPath={}/TritonCTS".format(self.stage_dir)

        print(cmd)

        with open("{}/out/{}.log".format(self.stage_dir, self.design_name), 'a') as f:
            run_shell_cmd(cmd, f)

    def _copy_final_output(self):
        cmd = "ln -s {0}/TritonCTS/cts_final.def {0}/out/{1}.def" \
              .format(self.stage_dir, self.design_name)

        run_shell_cmd(cmd)

        cmd = "ln -s {0}/TritonCTS/final.v {0}/out/{1}.v" \
              .format(self.stage_dir, self.design_name)

        run_shell_cmd(cmd)

