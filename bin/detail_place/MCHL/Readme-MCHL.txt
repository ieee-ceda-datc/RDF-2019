This binary handles the fundamental mixed-cell-height standard-cell legalization problem, i.e., minimize the total displacement.


Use the following command to run our binary:
./MCHL -tech_lef <tech_file> -cell_lef <cell_file> -floorplan_def  <original def_file> -placed_def <placed_def_file> -def_size <size_file> [-out <output_result_file>]


An example for running our binary:
./MCHL -tech_lef ispd_2015_contest_benchmark/mgc_des_perf_1/tech.lef -cell_lef ispd_2015_contest_benchmark/mgc_des_perf_1/cells.lef -floorplan_def ispd_2015_contest_benchmark/mgc_des_perf_1/floorplan.def -placed_def ispd2016data/mgc_des_perf_1/gp_mgc_des_perf_1.def -def_size ispd2016data/mgc_des_perf_1/mgc_des_perf_1.def.size -out lg_mgc_des_perf_1.def

