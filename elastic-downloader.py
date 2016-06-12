#!/usr/bin/python
import requests
import sys
from clint.textui import progress

#### SET DOWNLOAD PATH ####
download_path = "/Users/mdown/Downloads/" # Must have trailing slash
#### SET DOWNLOAD PATH ####

# remove python script name from args
args = sys.argv[1:]

# Check number of args
if len(args) > 2:
    error = 'Too many command line arguments.', str(args)
    sys.exit(error)

# Read args
product = args[0].lower()
version = args[1].lower()

print 'Product:', product.upper()
print 'Version:', version

# download funciton with progress bar
def download(link, file_name):
    with open(file_name, "wb") as f:
        print "Downloading %s from: %s" % (product, link)
        print "Saving %s to: %s" % (product, file_name)
        response = requests.get(link, stream=True)
        total_length = response.headers.get('content-length')

        if total_length is None: # no content length header
            f.write(response.content)
        else:
            dl = 0
            total_length = int(total_length)
            total_mb = float(total_length / 1024) / 1024
            for data in response.iter_content(chunk_size=1000000):
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

# define the elastic stack & download links
def elasticsearch():
    link = 'https://download.elasticsearch.org/elasticsearch/release/org/elasticsearch/distribution/zip/elasticsearch/%s/elasticsearch-%s.zip' % (version, version)
    path = '%selasticsearch-%s.zip' % (download_path, version)
    download(link, path)

def logstash():
    link = 'https://download.elastic.co/logstash/logstash/logstash-%s.zip' % version
    path = '%slogstash-%s.zip' % (download_path, version)
    download(link, path)

def kibana():
    link = url(product, version)
    path = '%skibana-%s.zip' % (download_path, version)
    download(link, path)

def packetbeat():
    link = url(product, version)
    path = '%spacketbeat-%s.zip' % (download_path, version)
    download(link, path)

def filebeat():
    link = url(product, version)
    path = '%sfilebeat-%s.zip' % (download_path, version)
    download(link, path)

def topbeat():
    link = url(product, version)
    path = '%stopbeat-%s.zip' % (download_path, version)
    download(link, path)

def winlogbeat():
    link = url(product, version)
    path = '%stopbeat-%s.zip' % (download_path, version)
    download(link, path)

def metricbeat():
    link = url(product, version)
    path = '%stopbeat-%s.zip' % (download_path, version)
    download(link, path)

# map the inputs to the function blocks
options = {
    "elasticsearch" : elasticsearch,
    "logstash": logstash,
    "kibana": kibana,
    "packetbeat": packetbeat,
    "metricbeat": metricbeat,
    "filebeat": filebeat,
    "winlogbeat": winlogbeat,
    "topbeat": topbeat
}

options[product]()
