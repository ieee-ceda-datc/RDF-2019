yosys -import

# Don't change these unless you know what you are doing
set stat_ext    "_stat.rep"
set gl_ext      "_gl.v"
set abc_script  "+read_constr,ac97_ctrl.sdc;strash;ifraig;retime,-D,{D},-M,6;strash;dch,-f;map,-p,-M,1,{D},-f;topo;dnsize;buffer,-p;upsize;"

# Reading blackbox implementation of standard cells (treated as blackboxes)
read_verilog NangateOpenCellLibrary.blackbox.v
read_verilog ../../../../benchmarks/iwls2005/IWLS_benchmarks_2005_V_1.0/opencores/rtl/tv80/tv80_alu.v
read_verilog ../../../../benchmarks/iwls2005/IWLS_benchmarks_2005_V_1.0/opencores/rtl/tv80/tv80_core.v
read_verilog ../../../../benchmarks/iwls2005/IWLS_benchmarks_2005_V_1.0/opencores/rtl/tv80/tv80_mcode.v
read_verilog ../../../../benchmarks/iwls2005/IWLS_benchmarks_2005_V_1.0/opencores/rtl/tv80/tv80_reg.v
read_verilog ../../../../benchmarks/iwls2005/IWLS_benchmarks_2005_V_1.0/opencores/rtl/tv80/tv80s.v

# generic synthesis
synth  -top tv80s -flatten
opt_clean -purge

# mapping for Registers
dfflibmap -liberty nangate45.lib

# TODO: Not sure why we have to set these seeing as we are passing sdc?
# mapping for technology
abc -D [expr 50 * 1000] \
    -constr tv80.sdc \
    -liberty nangate45.lib \
    -script $abc_script

# Splitting nets resolves unwanted compound assign statements ( assign {..} = {..})
splitnets -ports; opt
hilomap -hicell {*}LOGIC1_X1 Z -locell {*}LOGIC0_X1 Z

opt_clean -purge

# cleanup
clean
opt_clean -purge

# reports
tee -o synth_check.txt check
tee -o synth_stat.txt stat -liberty nangate45.lib

# write synthesized design
write_verilog -noattr -noexpr -nohex -nodec synth.yosys.v
