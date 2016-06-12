# Auto Elastic Stack Downloader

## Intro
This python script will automatically download any of the Elastic Stack products with only two command line params:

1. **Product Name** e.g. elasticsearch
2. **Version** e.g. 2.3.3 or 5.0.0-alpha3

To run, download the python script and run the following command:

`./elastic-downloader.py elasticsearch 2.3.3`

or

`python elastic-downloader.py elasticsearch 2.3.3`

## Config

- To set download path change the `download_path` variable in the script.
- Add to `$PATH` for the most seamless integration

### Limitations

- Only works for Mac as these are the only download files you can get currently

### Improvements

- Remove hard coded download path
- Add Windows & Linux compatibility
