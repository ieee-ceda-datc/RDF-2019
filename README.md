DATC Robust Design Flow 2019
===

RDF-2019 enhances the DATC RDF to span the entire RTL-to-GDS IC implementation flow, from logic synthesis to detailed routing.
The new release represents a significant revision of the previously-reported [RDF-2018 flow](https://github.com/ieee-ceda-datc/RDF-2018). 
Noteworthy *vertical* extensions include:
- **Addition of logic synthesis** starting from pure behavioral RTL Verilog RTL
- **Floorplanning** that includes initial DEF creation, I/O placement and PDN layout generation
- **Clock tree synthesis** between placement legalization and global routing

A number of *horizontal* extensions to RDF are achieved by incorporating additional tool options at each stage. 
Last, RDF-2019 provides significantly enhanced support of and interoperability with industry-standard tools and design formats (LEF/DEF, SPEF, Liberty, SDC, etc.).

RDF-2019 Cloud demonstration: [Link](http://route.ucsd.edu:8080/).


Getting Started
---

You can run it by:
```
cd bin/openroad
./install.sh
cd ../../run
python ../src/rdf.py --config test.yml --test
cd rdf.yymmdd.HHMMSS
./run.sh
```

Configuring RDF Flow
---

### Design benchmark configuration

A benchmark consists of Verilog source codes and a configuration file (YAML format).
Please refer to an example design benchmark: [Link](benchmarks/test/tv80)

Example design configuration file:

```
name:        tv80s
clock_port:  clk

verilog:     
    - tv80_alu.v
    - tv80_core.v
    - tv80_mcode.v
    - tv80_reg.v
    - tv80s.v
```

### Library configuration

Example library configuration file: [link](techlibs/nangate45/rdf_techlib.yml)


### Flow configuration

Example RDF flow configuration file in YAML format:

```
---
rdf_path: ../
job_dir: ./

design:  benchmarks/test/i2c
library: techlibs/nangate45

flow:
    - stage: synth
      tool: yosys-abc # ABC or Yosys
      user_parms: 
          max_fanout: 16
          script: resyn2
          map:    map
          
    - stage: floorplan
      tool: TritonFP 
      user_parms:
          target_utilization: 20
          aspect_ratio: 1

    - stage: global_place
      tool: RePlAce         # RePlAce, EhPlacer, ComPLx, NTUPlace
      user_parms: 
          target_density: 0.4

    - stage: detail_place
      tool: opendp
      user_parms: []

    - stage: cts
      tool: TritonCTS
      user_parms:
          target_skew: 50

    - stage: global_route
      tool: FastRoute4-lefdef
      user_parms: []

    - stage: detail_route
      tool: TritonRoute
      user_parms: []
```



Preparing Libraries
---

(TBA) Explain using ASAP7 as an example.
```
magic.tech
tracks.info
tritonCTS LUTs
gds
```

Adding Your Pont Tool Binaries
---

`./bin/<stage>/<tool_name>/`

Each tool must include runner python script, and RDF will call it: `<rdf_path>/bin/<stage>/<tool_name>/rdf_<tool_name>.py`.


Contributors
---

### Current DATC Committee members

* Jianli Chen - Fuzhou University
* Iris Hui-Ru Jiang - National Taiwan University
* Jinwook Jung - IBM Thomas J. Watson Research Center
* Andrew B. Kahng - University of California San Diego
* Victor N. Kravets - IBM Thomas J. Watson Research Center
* Yih-Lang Li - National Chiao Tung University

### Code committers

* Mingyu Woo - UCSD
* Shih-Ting Lin - NCTU

### Tool contributors

* Nima Karimpour and Laleh Behjat - University of Calgary
* Myung-Chul Kim and Igor Markov (for ComPLx)
* Shinichi Nishizawa and Hidetoshi Onodera (for NCTUcell)
* OpenROAD team

