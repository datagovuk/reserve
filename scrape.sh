#!/bin/bash

# Make sure our env var is set
if [ -z "$RESERVE_SITE" ]; then
    echo "Need to set RESERVE_SITE"
    exit 1
fi

DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

# Scrape the webpages into a specific directory
echo "+ Scraping site"
#wget -P static_site -X "/data/resource_cache*,/data/search*,/api/*,/search*,/user*,/feeds*,/flag*,/vote*"  --adjust-extension -p --convert-links --restrict-file-names=windows -m -e robots=off  --wait .5 -x http://$RESERVE_SITE
wget -P static_site --reject "user*,search@*" -X "/data/resource_cache*,/data/search*,/api/*,/search*,/user*,/feeds*,/flag*,/vote*"  --adjust-extension -p --convert-links --restrict-file-names=windows -m -e robots=off  --wait .5 -x http://$RESERVE_SITE

# Mod the HTML to insert a banner and fix search etc
echo "+ Inserting banner"
python $DIR/html_modder.py $DIR/banner.html $DIR/static_site --search-simple-google

# Sync with S3
echo "+ Syncing with S3"
cd $DIR/static_site/$RESERVE_SITE
s3cmd put -r . s3://data.gov.uk/


