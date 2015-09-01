#!/usr/bin/env python

import sys
import os.path
import os
import re
import argparse
from running_stats import Stats

parser = argparse.ArgumentParser()
parser.add_argument('banner_filepath', help='Banner HTML')
parser.add_argument('html_filepath',  help='Folder containing HTML files to be modified')
parser.add_argument('--search-simple-google', action="store_true", help='Just insert simple google search')
args = parser.parse_args()

all_mods = not args.search_simple_google

if all_mods:
    with open(getattr(args, 'banner-filepath'), 'rb') as f:
        banner_html = f.read()
    banner_and_body_tag = '{0}</body>'.format(banner_html)
    body_tag_re = re.compile(re.escape("</body>"), re.IGNORECASE)

def mod_filepaths(html_filepath, args):
    stats = Stats()
    are_errors = False

    with open(html_filepath, 'rb') as f:
        content = f.read()

    if all_mods:
        # Banner
        if '<!-- Failover banner -->' in content:
            print stats.add('WARN: Already has a banner - ignoring', html_filepath)
        else:
            content, number_of_subs = body_tag_re.subn(banner_and_body_tag, content, re.IGNORECASE)
            if number_of_subs == 1:
                print stats.add('Banner added', html_filepath)
            else:
                print stats.add('ERROR: Wrong num of banner substitutions', '%s (%s)' % (html_filepath, number_of_subs))
                are_errors = True

    if all_mods or args.search_simple_google:
        # Search simple google
        if '<!-- Simple Google form -->' in content:
            print stats.add('WARN: Already has google simple form - ignoring', html_filepath)
        else:
            content, number_of_subs = search_form_re.subn(simple_google_form_html, content)
            try:
                if number_of_subs == 2:
                    print stats.add('Main search box on data search page substituted', html_filepath)
                elif number_of_subs == 1:
                    print stats.add('Corner search box substituted', html_filepath)
                elif number_of_subs == 0:
                    print stats.add('ERROR: Wrong num of corner search (simple google form) substitutions', '%s (%s)' % (html_filepath, number_of_subs))
                    are_errors = True
            except:
                # Not interesed in utf8 errors atm
                pass

            content, number_of_subs = search_hint_re.subn('Search site via Google', content)

    with open(html_filepath, 'wb') as f:
        f.write(content)
    print 'OK: Written %s' % html_filepath

    print stats

    #if are_errors:
        #sys.exit(1)

simple_google_form_html = r'''
<!-- Simple Google form -->
<form \1action="http://google.co.uk/search"\2>
      <input type="hidden" name="q" value="site:data.gov.uk" />
'''

#search_form_main = '{0}</body>'.format(banner_html)
# Search form in the corner of the page:
#   <form action="search.html" class="input-group input-group-sm">
# Search form on the data search page:
#   <form class="form-search" action="search.html" method="GET">
search_form_re = re.compile(r'<form ([^>]*)action="(?:search.html|\/data\/search)"([^>]*)>')
search_hint_re = re.compile('Search for data\.\.\.')

print args
for root, _, files in os.walk(args.html_filepath, topdown=False):
    for name in files:
        if name.endswith(".html"):
            mod_filepaths(os.path.join(root, name), args)


