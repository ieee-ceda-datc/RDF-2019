This binary handles the mixed-cell-height legalization problem with technology and region constraints, i.e., consider the technology constraints (pin-short, pin-access, edge spacing, etc) and fence region constraint, and minimize the total displacement and wirelength. 

The binary need the following arguments:
(1) tech_lef : specifies the tech.lef input file
(2) cell_lef : specifies the cell.lef input file
(3) input_def: specifies the input DEF file (that is a global placement solution)
(4) cpu      : specifies the number of parallel threads to use
(5) placement_constraints : specifies the placement.constraints file
(6) output_def: specifies the output DEF file (that is a legal solution)


Use the following command to run our binary:
./MCHL_T-tech_lef tech.lef -cell_lef cell.lef -input_def placed.def -cpu 1 -placement_constraints placement.constraints -output_def lg.def


An example for running our binary:
./MCHL_T -tech_lef benchmarks/des_perf_b_md1/tech.lef -cell_lef benchmarks/des_perf_b_md1/cells_modified.lef -input_def benchmarks/des_perf_b_md1/placed.def -cpu 1 -placement_constraints benchmarks/des_perf_b_md1/placement.constraints -output_def des_perf_b_md1_lg.def
