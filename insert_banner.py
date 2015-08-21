#!/bin/python

"""
Inserts a banner into every .html file found in the specified directory.

Two arguments to the script are the banner.html file location, and the
folder containing the html files.
"""

import sys
import os.path
import re

with open(sys.argv[1], 'rb') as f:
    banner_html = f.read()

banner_and_body_tag = '{0}</body>'.format(banner_html)
body_tag_re = re.compile(re.escape("</body>"), re.IGNORECASE)


def insert_banner(filename):
    """ Insert the banner into the page if it is not already there """
    with open(filename, 'rb') as f:
        content = f.read()

        if '<!-- Failover banner -->' in content:
            print 'WARN: Already has a banner - ignoring: %s' % filename
            return

        content, number_of_subs = body_tag_re.subn(banner_and_body_tag, content, re.IGNORECASE)
        if number_of_subs != 1:
            print 'ERROR: Wrong num of substitutions (%s) %s' % (number_of_subs, filename)
            return

    with open(filename, 'wb') as f:
        f.write(content)

    print 'OK: Written %s' % filename


html_root = sys.argv[2]
for root, _, files in os.walk(html_root, topdown=False):
    for name in files:
        if name.endswith(".html"):
            insert_banner(os.path.join(root, name))

