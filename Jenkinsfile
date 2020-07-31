pipeline {
    agent any
    parameters {
        choice(
                name: 'benchmark',
                choices: ['i2c', 'tv80'],
                description: 'Choose benchmark circuit you want to try.'
              )
        choice(
                name: 'logic-synthesizer',
                choices: ['yosys-abc'],
                description: 'Choose logic synthesizer.'
              )
        choice(
                name: 'max-fanout',
                choices: ['8', '16', '32', '64'],
                description: 'Choose maximum fanout constraints for logic synthesis.'
              )
        choice(
                name: 'script',
                choices: ['resyn2', 'resyn2a', 'compress'],
                description: 'Choose ABC synthesis script.'
              )
        choice(
                name: 'map',
                choices: ['map'],
                description: 'Choose ABC technology mapping script.'
              )
        choice(
                name: 'floorplanner',
                choices: ['TritonFP'],
                description: 'Choose floorplanner.'
              )
        choice(
                name: 'target-utilization',
                choices: ['25', '50', '75'],
                description: 'Choose target utilization factor for floorplanning.'
              )
        choice(
                name: 'aspect-ratio',
                choices: ['0.5', '1', '2'],
                description: 'Enter aspect ratio for floorplanninng.'
              )
        choice(
                name: 'global-placer',
                choices: ['RePlAce', 'EhPlacer', 'ComPLx', 'NTUPlace3', 'FZUPlace'],
                description: 'Choose global placer.'
              )
        choice(
                name: 'target-density',
                choices: ['0.5', '0.7', '0.9'],
                description: 'Choose target density for global placement.'
              )
        choice(
                name: 'detail-placer',
                choices: ['opendp', 'MCHL-T'],
                description: 'Choose detail placer.'
              )
        choice(
                name: 'clock-tree-synthesizer',
                choices: ['TritonCTS'],
                description: 'Choose clock tree synthesizer.'
              )
        choice(
                name: 'target-skew',
                choices: ['25', '50', '75', '100'],
                description: 'Choose target skew.'
              )
        choice(
                name: 'global-router',
                choices: ['FastRoute4-lefdef'],
                description: 'Choose global router.'
              )
        choice(
                name: 'detail-router',
                choices: ['TritonRoute'],
                description: 'Choose detail router.'
              )
    }
    stages {
        stage('Setup') {
            steps {
                echo "Benchmark: ${params.benchmark}"
                sh '''#!/usr/bin/env bash
                      source /opt/miniconda3/etc/profile.d/conda.sh
                      conda activate
                      cd bin/openroad; ./install.sh; cd ../../
                      cd run; python ../src/rdf.py --config test.yml --test
                   '''
            }
        }
        stage('Logic Synthesis') {
            steps {
                echo 'Running logic synthesis.'
                sh '''#!/usr/bin/env bash
                      pwd
                      cd run/rdf.yymmdd.HHMMSS/synth; bash run.sh
                   '''
            }
        }
        stage('Floorplanning') {
            steps {
                echo "Running floorplanning."
                sh '''#!/usr/bin/env bash
                      pwd
                      cd run/rdf.yymmdd.HHMMSS/floorplan; bash run.sh 
                   '''
            }
        }
        stage('Global Placement') {
            steps {
                echo "Running global placement."
                sh '''#!/usr/bin/env bash
                      pwd
                      cd run/rdf.yymmdd.HHMMSS/global_place; bash run.sh 
                   '''
            }
        }
        stage('Detail Placement') {
            steps {
                echo "Running detail placement."
                sh '''#!/usr/bin/env bash
                      pwd
                      cd run/rdf.yymmdd.HHMMSS/detail_place; bash run.sh
                   '''
            }

        }
        stage('Clock Tree Synthesis') {
            steps {
                echo 'Running clock tree synthesis.'
                sh '''#!/usr/bin/env bash
                      pwd
                      source /opt/miniconda3/etc/profile.d/conda.sh
                      conda activate
                      cd run/rdf.yymmdd.HHMMSS/cts; bash run.sh
                   '''
            }
        }
        stage('Global Routing') {
            steps {
                echo 'Running global routing.'
                sh '''#!/usr/bin/env bash
                      pwd
                      cd run/rdf.yymmdd.HHMMSS/global_route; bash run.sh
                   '''
            }
        }
        stage('Detailed Routing') {
            steps {
                echo 'Running detailed routing.'
                sh '''#!/usr/bin/env bash
                      pwd
                      cd run/rdf.yymmdd.HHMMSS/detail_route; bash run.sh
                   '''
            }
        }
    }
}
