import argparse
import json
import os
def write_articles_to_dir(in_file, out_dir, filter_tags=None):
    if in_file.name.endswith('.json'):
        site_dir = os.path.join(out_dir, os.path.basename(in_file.name)[:-5])
    else:
        site_dir = os.path.join(out_dir, os.path.basename(in_file.name))
    if not os.path.exists(site_dir):
        os.mkdir(site_dir)
    js = json.load(in_file)
    for i, js_dict in enumerate(js):
        with open(os.path.join(site_dir, '%d.txt' %i, ), 'w') as f:
            if filter_tags and filter_tags(js_dict['Category']):
                f.write(js_dict['Content'][0].encode("utf-8"))



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Processes files and outputs \
    each site\'s articles as its own file in the site\'s directory')
    parser.add_argument('files', metavar='FILENAME', nargs='+', type=file, help='Filenames (or filepaths) of files to be extracted')
    parser.add_argument('-o', '--output_dir', metavar='DEST', default='.', 
                        help='Directory where directories of sites with \
                        articles will be stored. Default is current directory.')
    args = parser.parse_args()
    
    if not os.path.isdir(args.output_dir):
        if  os.path.exists(args.output_dir):
            print "%s exists but is not a directory" %args.output_dir
        else:
            os.mkdir(args.output_dir)
    for f in args.files:
        write_articles_to_dir(f, args.output_dir)
    print args.files
