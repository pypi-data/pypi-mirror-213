import argparse
from matrix_cloud import download_large_file, upload_large_file
from matrix_cloud.gui import run_gui


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--username")
    parser.add_argument("-p", "--password")
    parser.add_argument("-i", "--infile")
    parser.add_argument("-m", "--matrix")
    parser.add_argument("-o", "--outfile")
    parser.add_argument("-d", "--download", action='store_true')
    parser.add_argument("-g", "--gui", action='store_true')

    args = parser.parse_args()

    if args.gui:
        run_gui()
        return

    matrix_address = args.matrix if args.matrix != None else "matrix.org"

    if args.download:
        print("Downloading")
        download_large_file(args.username, args.password, args.infile,
                            matrix_address, args.outfile)

    else:
        print("Uploading")
        upload_large_file(args.username, args.password, args.infile,
                          matrix_address, args.outfile)


if __name__ == '__main__':
    main()
