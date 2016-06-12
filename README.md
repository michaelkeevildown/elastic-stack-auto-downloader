# Elastic Stack Auto Downloader

## What is the point of this?!

- Have you ever wanted to download an older version of **Elasticsearch** or **Kibana**?
- Have you spent more time than you should going through the **Past Releases** to find the exact version?
- Ever wanted a command line tool to do all the above?

If you have, then this is an answer to your problems! This utility will allow you to use the command line to download any version of the following products.

- Elasticsearch
- Kibana
- Logstash
- All Beats
  - Packet
  - Top
  - Metric
  - File

## How to use:

When you execute the python script **two** command line arguments have to be passed. They are as follows:

1. **Product Name** e.g. elasticsearch
2. **Version** e.g. 2.3.3 or 5.0.0-alpha3

**n.b The order in which they are passed is critical.**

To download your the specific version fo the application you can execute you the script in one of three ways:

`./elastic-downloader.py elasticsearch 2.3.3`

or

`python elastic-downloader.py elasticsearch 2.3.3`

or

`elastic-downloader elasticsearch 2.3.3`

If moved into your `$PATH`. There is a crude bash script that do this for you.

### Examples:

Here are all the commands that will download `Elasticsearch 2.3.3`, this can be replicated for all products. I am also going to chose only one of the commands above for simplicity but again this will work for all 3 different commands shown above.

##### Option 1 - Single Product
`elastic-downloader elasticsearch 2.3.3`

##### Option 2 - Multiple products same version
`elastic-downloader elasticsearch,kibana 2.3.3`

##### Option 3 - All Products for a specific version
`elastic-downloader all 2.3.3`

##### Option 4 - Multiple products but **different** versions
Stop being lazy and run the command twice..JEZZZ!


## Config:

- To set download path change the `download_path` variable in the script. The default is `~/Downloads/`.

- Add to `$PATH` for the most seamless integration so you only have to run -> `elastic-downloader elasticsearch 2.3.3`

### Limitations

- Only works for Mac as these are the only download files you can get currently

### Improvements

- [x] Remove hard coded download path
- [ ] Add Windows & Linux compatibility
- [ ] Add the ability to specify more than one product at a time in CSV e.g. kibana,elasticsearch
