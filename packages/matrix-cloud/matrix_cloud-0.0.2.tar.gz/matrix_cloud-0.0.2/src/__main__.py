import argparse
from matrix_cloud import download_large_file, upload_large_file


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("username")
    parser.add_argument("password")
    parser.add_argument("file_path")
    parser.add_argument("-m", "--matrix")
    parser.add_argument("-o", "--outfile")
    parser.add_argument("-d", "--download", action='store_true')
    args = parser.parse_args()

    matrix_address = args.matrix if args.matrix != None else "matrix.org"

    if args.download:
        print("Downloading")
        download_large_file(args.username, args.password, args.file_path,
                            matrix_address, args.outfile)

    else:
        print("Uploading")
        upload_large_file(args.username, args.password, args.file_path,
                          matrix_address, args.outfile)


if __name__ == '__main__':
    main()
