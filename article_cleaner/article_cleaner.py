from __future__ import division
import argparse
import json
import os
import re
import random

def write_articles_to_dir(in_file, out_dir, filter_tags=None):
    if not filter_tags:
        print 'No filter'
    js = json.load(in_file)
    for i, js_dict in enumerate(js):
        if (random.randint(0,9) == 9):
            site_dir = os.path.join(out_dir, "test")
            if in_file.name.endswith('.json'):
                site_dir = os.path.join(site_dir, os.path.basename(in_file.name)[:-5])
            else:
                site_dir = os.path.join(site_dir, os.path.basename(in_file.name))
        else:
            site_dir = os.path.join(out_dir, "train")
            if in_file.name.endswith('.json'):
                site_dir = os.path.join(site_dir, os.path.basename(in_file.name)[:-5])
            else:
                site_dir = os.path.join(site_dir, os.path.basename(in_file.name))
        if not os.path.exists(site_dir):
            os.mkdir(site_dir)
        if 'Category' in js_dict:
            cat_tags = js_dict['Category']
        elif 'Tags' in js_dict:
            cat_tags = js_dict['Tags']
        else:
            cat_tags = []
        url = js_dict['url']
        content = js_dict['Content']
        if filter_tags and filter_tags(cat_tags, url, content):
            with open(os.path.join(site_dir, '%d.txt' %i, ), 'w') as f:
                f.write(js_dict['Content'][0].encode("utf-8"))

def write_train_test_dir(in_files, classes, out_dir, percent_train=10, filter_tags=None):
    if not filter_tags:
        print 'No filter'
    print "Training percentange:", percent_train
    if percent_train < 0 or percent_train > 100 or not isinstance(percent_train, int):
        print 'bad percent_train'
        return
    for in_file, art_class in zip(in_files, classes):
        js = json.load(in_file)
        i = 0
        test_list = ([True for _ in range(percent_train *len(js) // 100)] +
            [False for _ in range(len(js) - (percent_train *len(js) // 100))])
        random.shuffle(test_list)
        for i, js_dict, is_test_file in zip(range(i, len(js)), js, test_list):
            if (is_test_file):
                site_dir = os.path.join(out_dir,  "test", art_class)
            else:
                site_dir = os.path.join(out_dir, "train", art_class)
            if not os.path.exists(site_dir):
                os.makedirs(site_dir)
            if 'Category' in js_dict:
                cat_tags = js_dict['Category']
            elif 'Tags' in js_dict:
                cat_tags = js_dict['Tags']
            else:
                cat_tags = []
            url = js_dict['url']
            content = js_dict['Content'][0]
            if filter_tags and filter_tags(cat_tags):
                with open(os.path.join(site_dir, '%d.txt' %i, ), 'w') as f:
                    f.write(filter_source_cheating(content).encode("utf-8"))
        i += len(js)

seperator = re.compile(u'([ /,-]|.html)*')
political_set = {'politics', 'election', 'politicsnews', 'world', 'worldnews',
                 'domesticnews', 'u.s.', 'us', 'news', 'world', 'national', 'nation'}
#Tags may be a list of tags or one item in a list which must be regexed into a tag list
def filter_tags(tag_list):
    for t in tag_list:
        words = re.split(seperator, t.lower())
        for w in words:
            if w in political_set:
                return True
    return False

#Cheated in the sense that I hard-coded a list of possible names
source_set = {'HuffPost', 'Post', 'NYT', 'Times',
              'CNN', 'NBC', 'LA Times', 'Boston Globe', 'Globe', 'Cracked',
              'Onion', 'Beaverton', 'Civilian'}
source_regex = re.compile('(' + '|'.join(source_set) + ')')
def filter_source_cheating(content):
    return re.sub(source_regex, "NEWSsource", content)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Processes files and outputs \
    each site\'s articles as its own file in the site\'s directory')
    parser.add_argument('files', metavar='FILENAME', nargs='+', type=file, help='Filenames (or filepaths) of files to be extracted')
    parser.add_argument('-o', '--output_dir', metavar='DEST', default='.',
                        help='Directory where directories of sites with \
                        articles will be stored. Default is current directory.')
    parser.add_argument('-f', '--filter_tags', action='store_const', const=filter_tags, default=None)
    args = parser.parse_args()

    if not os.path.isdir(args.output_dir):
        if  os.path.exists(args.output_dir):
            print "%s exists but is not a directory" %args.output_dir
        else:
            os.mkdir(args.output_dir)
    class_dict = {'huffingtonpost.json':'news',
        'bostonglobewithcategories.json':'news',
        'reuters.json':'news',
        'cracked.json':'satire',
        'nbc.json':'news',
        'onion_with_js.json':'satire',
        'latimes.json':'news',
        'cnn_attempt_2.json':'news',
        'civilian.json':'satire',
        'beaverton.json':'satire',
        'lushforlife.json': 'satire',
    }
    print 'Writing files...'
    write_train_test_dir(args.files, [class_dict[os.path.basename(f.name)] for f in args.files],
        args.output_dir, filter_tags=args.filter_tags)
