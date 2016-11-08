import argparse
import json
import os
import re

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
            if 'Category' in js_dict:
                cat_tags = js_dict['Category']
            elif 'Tags' in js_dict:
                cat_tags = js_dict['Tags']
            else:
                cat_tags = []
            if filter_tags and filter_tags(cat_tags):
                f.write(js_dict['Content'][0].encode("utf-8"))

 
seperator = re.compile(u'[ /,]*')        
political_set = {'Politics'}
#Tags may be a list of tags or one item in a list which must be regexed into a tag list            
def filter_tags(tag_list):
    for t in tag_list:
        words = re.split(seperator, t)
        for w in words:
            if w in political_set:
                return True
    return False

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Processes files and outputs \
    each site\'s articles as its own file in the site\'s directory')
    parser.add_argument('files', metavar='FILENAME', nargs='+', type=file, help='Filenames (or filepaths) of files to be extracted')
    parser.add_argument('-o', '--output_dir', metavar='DEST', default='.', 
                        help='Directory where directories of sites with \
                        articles will be stored. Default is current directory.')
    parser.add_argument('-f', '--filter_tags', action='store_const', const=filter_tags default=None)
    args = parser.parse_args()
    print args.filter_tags
    
    if not os.path.isdir(args.output_dir):
        if  os.path.exists(args.output_dir):
            print "%s exists but is not a directory" %args.output_dir
        else:
            os.mkdir(args.output_dir)
    for f in args.files:
        write_articles_to_dir(f, args.output_dir, args.filter_tags)
    print args.files
