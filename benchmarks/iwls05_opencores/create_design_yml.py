import os
import glob

designs = ['ac97_ctrl', 'aes_core', 'des3_area', 'des3_perf', 'ethernet', "fpu", "i2c", "mem_ctrl", "pci", "sasc", "simple_spi", "spi", "ss_pcm", "steppermotordrive", "systemcaes", "systemcdes", "tv80", "usb_funct", "usb_phy", "vga_lcd", "wb_conmax", "wb_dma"]

for d in designs:
    os.chdir("./{}".format(d))
    print(os.getcwd())
    verilogs = glob.glob("*.v")
    with open("rdf_design.yml", 'w') as f:
        f.write("name: \n")
        f.write("clock_port: \n")
        f.write("\n")
        f.write("verilog:\n")
        for v in verilogs:
            f.write("    - {}\n".format(v))
    os.chdir("..")

