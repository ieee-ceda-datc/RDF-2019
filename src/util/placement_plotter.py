'''
    File name      : 300_placement_plotter.py
    Author         : Jinwook Jung (jinwookjungs@gmail.com)
    Created on     : Wed 09 Aug 2017 12:19:42 AM KST
    Last modified  : 2017-08-09 00:19:42
    Description    : Plot placement result using gnuplot.
'''
from time import gmtime, strftime


class PlaceRegion(object):
    llx = 0
    lly = 0
    urx = 987654321
    ury = 987654321


class Node(object):
    def __init__(self, name, w, h, is_fixed, llx=0, lly=0):
        self.name = name
        self.width, self.height = w, h  # Width and height
        self.llx, self.lly = llx, lly   # Placement
        self.is_fixed = is_fixed

    def draw_gnuplot(self):
        llx, lly = self.llx, self.lly
        urx = self.llx + self.width
        ury = self.lly + self.height

        box="%d %d\n%d %d\n%d %d\n%d %d\n%d %d\n\n" % \
            (llx, lly, urx, lly, urx, ury, llx, ury, llx, lly)
        return box


def parse_bookshelf_nodes(nodes, node_dict):
    with open(nodes, 'r') as f:
        # read lines without blank lines
        lines = [l for l in (line.strip() for line in f) if l]

    # Skip the first line: UCLA nodes ...
    lines_iter = iter(lines[1:])

    for l in lines_iter:
        if l.startswith('#'): continue

        tokens = l.split()
        if tokens[0] == 'NumNodes' or tokens[0] == 'NumTerminals':
            continue

        assert len(tokens) >= 3
        name, w, h = tokens[0], int(tokens[1]), int(tokens[2])

        if (len(tokens) == 4):
            is_fixed = True
            assert tokens[3] == 'terminal' or tokens[3] == 'terminal_NI'
        else:
            is_fixed = False

        node_dict[name] = Node(name, w, h, is_fixed)


def parse_bookshelf_pl(pl, node_dict):
    with open(pl, 'r') as f:
        # read lines without blank lines
        lines = [l for l in (line.strip() for line in f) if l]

    # Skip the first line: UCLA pl ...
    lines_iter = iter(lines[1:])

    for l in lines_iter:
        if l.startswith('#'): continue

        tokens = l.split()
        assert len(tokens) > 3

        name, x, y = tokens[0], int(float(tokens[1])), int(float(tokens[2]))

        n = node_dict[name]
        n.llx, n.lly = x, y


def parse_bookshelf_scl(scl):
    """ Read an scl and determine placement region """

    with open(scl, 'r') as f:
        # read lines without blank lines
        lines = [l for l in (line.strip() for line in f) if l]

    lines_iter = iter(lines[2:])    # skip the first two lines

    urx, ury = (0.0, 0.0)

    for l in lines_iter:
        if l.startswith('#'): continue
        tokens = l.split()

        if tokens[0] == 'CoreRow':
            while True:
                tokens = next(lines_iter).split()
                if tokens[0] == 'End':
                    break

                elif tokens[0] == 'Coordinate':
                    coordinate = int(tokens[2])

                elif tokens[0] == 'Height':
                    height = int(tokens[2])

                elif tokens[0] == 'Sitewidth':
                    site_width = int(tokens[2])

                elif tokens[0] == 'Sitespacing':
                    site_spacing = int(tokens[2])

                elif tokens[0] == 'SubrowOrigin':
                    subrow_origin = int(tokens[2])
                    num_sites = int(tokens[5])

            _urx = subrow_origin + num_sites*site_spacing
            _ury = coordinate + height

            urx = _urx if _urx > urx else urx
            ury = _ury if _ury > ury else ury

    PlaceRegion.urx, PlaceRegion.ury = urx, ury


def print_gnuplot_header(f_dest, png_name):
    def get_plot_size(default_size=1500):
        aspect_ratio = float(PlaceRegion.ury) / PlaceRegion.urx

        if aspect_ratio < 1.0:
            x_size = default_size
            y_size = aspect_ratio * default_size
        else:
            x_size = default_size * (1 / aspect_ratio)
            y_size = default_size

        return x_size, y_size


    x_size, y_size = get_plot_size()

    title = "placement"

    f_dest.write("reset\n")
    f_dest.write("set terminal png size %d, %d enhanced font ',16'\n" % (x_size, y_size))
    # f_dest.write("set title '%s' noenhanced\n" % (title))
    f_dest.write("set output '%s'\n\n" % (png_name))

    f_dest.write("# Define axis\n")
    f_dest.write("set style line 11 lc rgb '#101010' lt 1 lw 1.5\n")
    f_dest.write("set border 4095 back ls 11 lw 6\n")
    f_dest.write("set tics nomirror\n")
    f_dest.write("set nokey\n\n")

    f_dest.write("unset tics\n")

    f_dest.write("# Color definitions\n")
    # red, green, blue, gray
    #f_dest.write("color_list=\"#DC143C #5E9C36 #1E90FF #34495E #000000\"\n")
    #f_dest.write("color_list=\"#001848 #3090F0 #000000 \"\n")
    f_dest.write("color_list=\"#0B66FE #FF0000 #000000 \"\n")
    f_dest.write("num2col(n)=word(color_list,n)\n")

    f_dest.write("set xrange[0:%d]\n" % (PlaceRegion.urx + 0))
    f_dest.write("set yrange[0:%d]\n" % (PlaceRegion.ury + 0))
    f_dest.write("set multiplot\n\n")


def draw_nodes(f_dest, node_list, color_num, solid):
    f_dest.write("# Draw nodes\n")
    f_dest.write("set style line 1 lc rgb num2col(%d) pt 13 ps 1.5 lt 1 lw 0.5\n" % (color_num))
    f_dest.write("plot '-' with filledcurves fill solid %f border ls 1\n" % (solid))
    [f_dest.write(n.draw_gnuplot()) for n in node_list]
    f_dest.write("EOF\n")
    f_dest.write("# num_nodes: %d\n\n\n" % (len(node_list)))


def make_placement_plot(nodes, pl, scl, dest):
    # Read bookshelf files
    parse_bookshelf_scl(scl)

    node_dict = dict()
    parse_bookshelf_nodes(nodes, node_dict)
    parse_bookshelf_pl(pl, node_dict)

    # open plot file
    f_dest = open(dest + '.plt', 'w')
    png_name = dest + '.png'

    # Print plt header
    print_gnuplot_header(f_dest, png_name)

    # Draw cells
    node_list = list(node_dict.values())

    fixed_nodes = [n for n in node_list if n.is_fixed]
    regs = [n for n in node_list if n.name.startswith('l')]
    nodes = [n for n in node_list if not n.is_fixed]

    draw_nodes(f_dest, nodes, 1, 0.5);
    draw_nodes(f_dest, regs, 2, 0.33);
    draw_nodes(f_dest, fixed_nodes, 3, 0.9);

    f_dest.close()


if __name__ == '__main__':
    def parse_cl():
        import argparse
        parser = argparse.ArgumentParser(description='')
        parser.add_argument('--nodes', dest='src_nodes', required=True)
        parser.add_argument('--pl', dest='src_pl', required=True)
        parser.add_argument('--scl', dest='src_scl', required=True)
        parser.add_argument('--out', dest='out', default='out')
        return parser.parse_args()

    opt = parse_cl()
    make_placement_plot(opt.src_nodes, opt.src_pl, opt.src_scl, opt.out)

