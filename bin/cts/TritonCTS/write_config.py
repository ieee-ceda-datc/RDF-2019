'''
    File name      : write_config.py
    Author         : Jinwook Jung
    Created on     : Fri 01 Nov 2019 11:56:10 PM EDT
    Last modified  : 2019-11-01 23:56:20
    Description    : 
'''

def write_config(prev_out_dir, design_name, lib_dir, process, clk_port, root_buf):
    # FIXME: Get width and height of the design....
    with open("{}/{}.def".format(prev_out_dir, design_name)) as f:
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

    with open("./triton_cts.cfg",'w') as f:
        f.write("lef {}/merged_padded_spacing.lef\n".format(lib_dir))
        f.write("path {}/{}.def\n".format(prev_out_dir, design_name))
        f.write("verilog {}/{}.v\n".format(prev_out_dir, design_name))
        f.write("design {}/{}.v\n".format(prev_out_dir, design_name))
        f.write("target_skew {}\n".format(50))
        f.write("width {}\n".format(w))
        f.write("height {}\n".format(h))
        f.write("tech {}\n".format(process))
        f.write("ck_port {}\n".format(clk_port))
        f.write("db_units {}\n".format(2000))
        f.write("root_buff {}\n".format(root_buf))
        f.write("toler {}\n".format(1000))

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--design_name", action="store", required=True)
    parser.add_argument("--prev_out_dir", action="store", required=True)
    parser.add_argument("--lib_dir", action="store", required=True)
    parser.add_argument("--process", action="store", required=True)
    parser.add_argument("--clk_port", action="store", required=True)
    parser.add_argument("--root_buf", action="store", required=True)
    args, _ = parser.parse_known_args()

    write_config(args.prev_out_dir,
                 args.design_name,
                 args.lib_dir,
                 args.process,
                 args.clk_port,
                 args.root_buf)

