'''
    File name      : rdf.py
    Author         : Jinwook Jung (jinwookjung@ibm.com)
    Created on     : Thu 25 Jul 2019 11:33:57 PM EDT
    Last modified  : 2020-04-30 16:31:44
    Description    : 
'''

import subprocess
import os
import sys
import random
import yaml
import time
import importlib

from os import path
from datetime import datetime
from uuid import uuid4
from shutil import copyfile


class RDF(object):
    ''' Main class of RDF.
    '''
    def __init__(self, config_yml):
        self.config_yml = config_yml
        self.config = None

        self.flow = None

        self.design_dir = None
        self.design_config = None

        self.lib_dir = None
        self.lib_config = None

    def process_config(self):
        ''' Process user config file and populate necessary values.
        '''

        print("(I) Process config file...\n")

        with open(config_yml) as f:
            self.config = yaml.safe_load(f)

        # FIXME: Get the RDF installation directory from user config file.
        src_dir = path.dirname(path.realpath(__file__))
        self.config["rdf_path"] = path.dirname(src_dir)

        for k,v in self.config.items():
            if k == 'job_dir':
                # FIXME: Need to get the job directory form user config file.
                cur_dir = os.getcwd()
                self.config["job_dir"]  = "{}/{}".format(cur_dir, job_id)

            elif k == "design":
                self.design_dir = "{}/{}".format(self.config["rdf_path"], v)
                with open("{}/rdf_design.yml".format(self.design_dir)) as f:
                    self.design_config = yaml.safe_load(f)
                    print("Design: {}".format(self.design_config["name"]))

            elif k == "library":
                self.lib_dir = "{}/{}".format(self.config["rdf_path"], v)
                self.lib_config = None
                with open("{}/rdf_techlib.yml".format(self.lib_dir)) as f:
                    self.lib_config = yaml.safe_load(f)

            elif k == "flow":
                self.flow = v

            else:
                print("(W) Invalid: {}={}".format(k,v))

    def write_run_scripts(self):
        ''' Write run script for each stage.
        '''

        # Copy the current config file.
        copyfile(self.config_yml, "{}/rdf.yml".format(self.config["job_dir"]))
        prev_out_dir = None

        for stage in self.flow:
            stage_name, tool = stage["stage"], stage["tool"]
            user_parms = stage["user_parms"]

            print("Current stage: {}".format(stage_name))
            if stage_name not in \
                    ("synth", "floorplan", "global_place", "detail_place", \
                     "cts", "global_route", "detail_route"):
                print("(W) Not supported yet... skip")
                continue

            print("Create run directory:")
            stage_dir = "{}/{}".format(self.config["job_dir"], stage_name)
            out_dir = "{}/out".format(stage_dir)
            os.makedirs(stage_dir)
            os.makedirs(out_dir)

            runpy = "{0}/{1}/{2}/{3}/rdf_{3}".format(self.config["rdf_path"], "bin", stage_name, tool)
            print("Run python script: {}.py".format(runpy))

            # FIXME: Temporarily modify system path...
            sys.path.insert(0, path.dirname(runpy))
            module = importlib.import_module("rdf_{}".format(tool))

            module.run(self, stage_dir, prev_out_dir, user_parms, write_run_scripts=True)
            prev_out_dir = out_dir

            print("Done: {}.".format(stage_name))
            print("")

        with open("{}/run.sh".format(self.config["job_dir"]), 'w') as f:
            f.write("#!/bin/bash\n\n")
            f.write("export RDF_JOB_DIR=\"{}\"\n".format(self.config["job_dir"]))

            for stage in self.flow:
                stage_name = stage["stage"]
                print(stage_name)
                if stage_name not in \
                        ("synth", "floorplan", "global_place", "detail_place", \
                         "cts", "global_route", "detail_route"):
                    print("(W) Not supported yet... skip")
                    continue

                f.write("cd ${{RDF_JOB_DIR}}/{}; bash run.sh\n".format(stage_name))


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", action="store", required=True)
    parser.add_argument("--run", action="store_true")
    parser.add_argument("--test", action="store_true")
    parser.add_argument("--job_id", action="store")
    args, _ = parser.parse_known_args()

    config_yml = args.config

    if args.test:
        job_id = "rdf.yymmdd.HHMMSS"
    elif args.job_id is not None:
        job_id = args.job_id
    else:
        job_id = "rdf.{}".format(datetime.now().strftime('%y%m%d.%H%M%S'))

    print("Job ID: {}".format(job_id))

    # Create a job directory with the current job id
    if args.test:
        import shutil
        shutil.rmtree(job_id, ignore_errors=True)
    os.mkdir(job_id)

    rdf = RDF(config_yml)
    rdf.process_config()
    rdf.write_run_scripts()

    if args.run:
        rdf.run()

