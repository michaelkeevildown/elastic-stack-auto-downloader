#!/usr/bin/python
import csv
import os
import requests
import sys
import warnings
from clint.textui import progress



#### SET DOWNLOAD PATH ####
download_path = "~/Downloads/"
#### SET DOWNLOAD PATH ####


# call all functions to download products
def trigger(product):
    try:
        options[product]()
    except Exception as e:
        print "## Invalid product: %s -- Please try again!" % product

# download funciton with progress bar
def download(link, file_name):
    with open(file_name, "wb") as f:
        print "\nDownloading %s from: %s" % (product, link)
        print "Saving %s to: %s" % (product, file_name)
        response = requests.get(link, stream=True)
        total_length = response.headers.get('content-length')

        if response.status_code != 200:
            print 'HTTP Status Code: %s' % response.status_code
            print '#### Invalid version: %s ####' % version
        else:
            if total_length is None: # no content length header
                f.write(response.content)
            else:
                dl = 0
                total_length = int(total_length)
                total_mb = float(total_length / 1024) / 1024
                print 'Total download size: %.2fMB' % total_mb
                for data in response.iter_content(chunk_size=1000):
                    dl += len(data)
                    f.write(data)
                    done = int(50 * dl / total_length)
                    dl_mb = float(dl / 1024) / 1024
                    sys.stdout.write("\r[%s%s] %.2fMB/%.2fMB" % ('=' * done, ' ' * (50-done), total_mb, dl_mb) )
                    sys.stdout.flush()

# dynamicly change URL for version less and version 5.x
def url(product, version):
    split_version = version.split(".")
    first_char = int(split_version[0])
    if product != "kibana":
        product_type = "beats"
    else:
        product_type = "kibana"

    if first_char >= 5:
        link = 'https://download.elastic.co/%s/%s/%s-%s-darwin-x64.tar.gz' % (product_type, product, product, version)
    else:
        link = 'https://download.elastic.co/%s/%s/%s-%s-darwin.tar.gz' % (product_type, product, product, version)
    return link

# override global product variable
def global_product(new_product):
    global product
    product = new_product

# define the elastic stack & download links
def elasticsearch():
    link = 'https://download.elasticsearch.org/elasticsearch/release/org/elasticsearch/distribution/zip/elasticsearch/%s/elasticsearch-%s.zip' % (version, version)
    path = '%selasticsearch-%s.zip' % (download_path, version)
    global_product('elasticsearch')
    download(link, path)

def logstash():
    link = 'https://download.elastic.co/logstash/logstash/logstash-%s.zip' % version
    path = '%slogstash-%s.zip' % (download_path, version)
    global_product('logstash')
    download(link, path)

def kibana():
    link = url(product, version)
    path = '%skibana-%s.zip' % (download_path, version)
    global_product('kibana')
    download(link, path)

def packetbeat():
    link = url(product, version)
    path = '%spacketbeat-%s.zip' % (download_path, version)
    global_product('packetbeat')
    download(link, path)

def filebeat():
    link = url(product, version)
    path = '%sfilebeat-%s.zip' % (download_path, version)
    global_product('filebeat')
    download(link, path)

def topbeat():
    # this has been added as topbeat will be merged into metricbeat from 5.x onwards
    split_version = version.split(".")
    first_char = int(split_version[0])
    if first_char < 5:
        link = url(product, version)
        path = '%stopbeat-%s.zip' % (download_path, version)
        global_product('topbeat')
        download(link, path)
    else:
        print 'Topbeat has been merged with Metricbeat from relase 5.x and onwards'

def metricbeat():
    link = url(product, version)
    path = '%stopbeat-%s.zip' % (download_path, version)
    global_product('metricbeat')
    download(link, path)

def all():
    global_product('elasticsearch')
    elasticsearch()
    global_product('kibana')
    kibana()
    global_product('packetbeat')
    packetbeat()
    global_product('filebeat')
    filebeat()
    global_product('metricbeat')
    metricbeat()
    global_product('topbeat')
    topbeat()


# map the inputs to the function blocks
options = {
    "elasticsearch" : elasticsearch,
    "logstash": logstash,
    "kibana": kibana,
    "packetbeat": packetbeat,
    "metricbeat": metricbeat,
    "filebeat": filebeat,
    "topbeat": topbeat,
    "all": all
}

## Setup ##
# ensure download path has trailing slash
if download_path.endswith('/') == False:
    download_path = '%s/' % download_path

# expand users local directory
download_path = os.path.expanduser(download_path)

# remove python script name from args
args = sys.argv[1:]

# Check number of args
if len(args) > 2:
    error = 'Too many command line arguments.', str(args)
    sys.exit(error)

# Read args
global_product(args[0].lower())
version = args[1].lower()

print '\n############################'
print 'Product(s):', product.upper()
print 'Version:', version.upper()
print '############################'
## Setup ##

## Start ##
# parse product argument to see if it is a list
if ',' not in product:
    trigger(product)
else:
    product_array = product.split(',')
    for single_product in product_array:
        trigger(single_product)
## Start ##
