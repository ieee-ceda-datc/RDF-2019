'''
    File name      : stage.py
    Author         : Jinwook Jung
    Created on     : Thu 25 Jul 2019 11:57:16 PM EDT
    Last modified  : 2020-01-06 13:27:13
    Description    : 
'''

import subprocess, os, sys, random, yaml, time
from subprocess import Popen, PIPE, CalledProcessError
from abc import ABC, abstractmethod


def run_shell_cmd(cmd, f=None):
    p = subprocess.Popen(cmd,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT,
                         shell=True)

    for line in iter(p.stdout.readline, b''):
        print(">>> {}".format(line.rstrip().decode("utf-8")))

        # FIXME
        if f is not None:
            f.write("{}\n".format(str(line.rstrip())))


class Stage(ABC):
    def __init__(self, rdf, stage_dir, prev_out_dir, user_parms, write_run_scripts=False):
        ''' Initialize the instance and populate the necessary/useful
        variables. '''
        self.rdf_path = rdf.config["rdf_path"]
        self.config = rdf.config
        self.design_dir, self.lib_dir = rdf.design_dir, rdf.lib_dir
        self.design_config, self.lib_config = rdf.design_config, rdf.lib_config

        self.stage_dir = stage_dir
        self.prev_out_dir = prev_out_dir

        self.design_name = rdf.design_config["name"]

        # Output of previous stage
        self.in_def, self.in_verilog, self.in_sdc = (None,)*3
        if prev_out_dir is not None:
            self.in_def = "{}/{}.def".format(prev_out_dir, self.design_name)
            self.in_verilog = "{}/{}.v".format(prev_out_dir, self.design_name)
            self.in_sdc = "{}/{}.sdc".format(prev_out_dir, self.design_name)
        else:
            # If this is the first stage, just use the original design file
            self.in_verilog = None
            self.in_def = None
            self.in_sdc = "{}/{}.sdc".format(self.rdf_path, self.design_name)
            self.design_verilogs = ["{}/{}".format(self.design_dir, _) \
                                    for _ in self.design_config["verilog"]]

        # Library/PDK
        self.lib_name = self.lib_config["LIBRARY_NAME"]
        self.liberty  = "{}/{}".format(self.lib_dir, self.lib_config["LIBERTY"])
        self.lef      = "{}/{}".format(self.lib_dir, self.lib_config["LEF"])
        self.tracks   = "{}/{}".format(self.lib_dir, self.lib_config["TRACKS_INFO_FILE"])

        # (TODO) User parameters
        self.user_parms = user_parms    # List of parameters (key/value pairs)

    def create_run_script_template(self):
        with open("{}/run.sh".format(self.stage_dir), 'w') as f:
            f.write("#!/bin/bash\n\n")
            f.write("export RDF_PATH=\"{}\"\n".format(self.rdf_path))
            f.write("export RDF_STAGE_DIR=\"{}\"\n".format(self.stage_dir))
            f.write("export RDF_TOOL_BIN_PATH=\"${RDF_PATH}/bin\"\n")
            f.write("\n")

    @abstractmethod
    def write_run_scripts(self):
        pass

    @abstractmethod
    def run(self):
        pass
