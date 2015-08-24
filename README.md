# reserve
Scripts for setting up a reserve/failover DGU instance

## Pad

http://etherpad.co-dev1.dh.bytemark.co.uk/p/static

## Configuring

You will need to tell the scrape.sh script which server to scrape. You can do this with the following (note server name, not protocol and server name):

```
export RESERVE_SITE="data.gov.uk"
```

or 

```
RESERVE_SITE="data.gov.uk" scrape.sh 
```

## Running

The scrape.sh script will:

* Use wget to download the site to ```static_site```
* Run the insert_banner script to insert the offline-warning banner
* Sync the data with the S3 bucket
