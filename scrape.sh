#!/bin/bash

# Make sure our env var is set
if [ -z "$RESERVE_SITE" ]; then
    echo "Need to set RESERVE_SITE"
    exit 1
fi

DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

# Scrape the webpages into a specific directory
echo "+ Scraping site"
wget -P static_site -X "/search,/user,/feeds,/flag,/vote"  --adjust-extension -p --convert-links --restrict-file-names=windows -m -e robots=off  --wait .5 -x http://$RESERVE_SITE

# Call insert banner to make sure they each have a banne
echo "+ Inserting banner"
python $DIR/insert_banner.py $DIR/banner.html $DIR/static_site

# Sync with S3
echo "+ Syncing with S3"
s3cmd sync -v $DIR/static_site/$RESERVE_SITE  s3://data.gov.uk/
