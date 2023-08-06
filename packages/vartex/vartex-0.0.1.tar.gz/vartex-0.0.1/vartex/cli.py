from vartex import VarTex
import argparse, sys


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("tex_file", help="The tex file to compile", type=str)
    parser.add_argument("--json", help="The JSON file for the variables", type=str)
    parser.add_argument("--csv", help="The CSV file for the variables", type=str)
    parser.add_argument("--build-dir", help="The build directory", type=str)

    args = parser.parse_args()

    if args.json is None and args.csv is None:
        print("Error: must specify either --json or --csv", file=sys.stderr)
        sys.exit(1)

    if args.json:
        mode = "json"
        variables_file = args.json
    else:
        mode = "csv"
        variables_file = args.csv

    vartex = VarTex(args.tex_file, variables_file, args.build_dir, mode)
    vartex.run()


if __name__ == "__main__":
    main()
