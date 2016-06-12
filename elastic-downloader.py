#!/usr/bin/python
import requests
import sys
from clint.textui import progress

#### SET DOWNLOAD PATH ####
download_path = "/Users/mdown/Downloads/"
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
                sys.stdout.write("\r[%s%s] %.2f/%.2f" % ('=' * done, ' ' * (50-done), total_mb, dl_mb) )
                sys.stdout.flush()

# define the elastic stack & download links
def elasticsearch():
    link = 'https://download.elasticsearch.org/elasticsearch/release/org/elasticsearch/distribution/zip/elasticsearch/%s/elasticsearch-%s.zip' % (version, version)
    path = '%selasticsearch-%s.zip' % (download_path, version)
    download(link, path)

def logstash():
    link = 'https://download.elastic.co/logstash/logstash/logstash-%s.zip' % version
    path = '%slogstash-%s.zip' % (download_path, version)
    download(link, path)

# map the inputs to the function blocks
options = {
    "elasticsearch" : elasticsearch,
    "logstash": logstash
}

options[product]()
