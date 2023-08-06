#!python
import sys
import optparse

try:
    from html_report_line_profiler import generate_html_report_fct
except:
    sys.path.insert(0, "../")
    from html_report_line_profiler import generate_html_report_fct
#end

def main(args=None):
    parser=optparse.OptionParser()
    parser.add_option("-d", "--input-dir", help="Input directory", type=str)
    parser.add_option("-o", "--output-dir", type=str)

    args, _ = parser.parse_args() # instantiate parser

    # Attention : reprendre les deuxièmes arguments de add_option, remplace "-" par "_"
    in_dir = args.input_dir
    out_dir = args.output_dir

    if not in_dir:
        in_dir = "profile"
    #
    if not out_dir:
        out_dir = "profile_html"
    #

    generate_html_report_fct(
        the_dir=in_dir,
        out_dir=out_dir,
        build_tree=True
    )

#

if __name__=="__main__":
    main(sys.argv[1:])
