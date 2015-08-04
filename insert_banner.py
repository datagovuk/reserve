#!/bin/python

import sys
import os.path
import re

banner_filepath = sys.argv[1]
with open(banner_filepath, 'rb') as f:
    banner_html = f.read()
banner_and_body_tag = '{0}</body>'.format(banner_html)

body_tag_re = re.compile(re.escape("</body>"), re.IGNORECASE)


html_filepaths = sys.argv[2:]

for html_filepath in html_filepaths:
    if not os.path.exists(html_filepath):
        print 'Cannot find file: %s' % html_filepath
        sys.exit(1)

    with open(html_filepath, 'rb') as f:
        content = f.read()

    if '<!-- Failover banner -->' in content:
        print 'WARN: Already has a banner - ignoring: %s' % html_filepath
        continue

    content, number_of_subs = body_tag_re.subn(banner_and_body_tag, content, re.IGNORECASE)
    if number_of_subs != 1:
        print 'ERROR: Wrong num of substitutions (%s) %s' % (number_of_subs, html_filepath)
        sys.exit(1)

    with open(html_filepath, 'wb') as f:
        f.write(content)
    print 'OK: Written %s' % html_filepath
