import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Processes files and outputs \
    each site\'s articles as its own file in the site\'s directory')
    parser.add_argument('filenames', metavar='FILENAME', nargs='+', help='Filenames (or filepaths) of files to be extracted')
    parser.add_argument('-o', '--output_dir', metavar='DEST', default='.', 
                        help='Directory where directories of sites with \
                        articles will be stored. Default is current directory.')
    args = parser.parse_args()