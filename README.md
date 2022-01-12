# ubuntu-cloud-aggreg8streams
[Datasette](https://datasette.io/) based project for populating and viewing Ubuntu 
cloud [simplestreams](http://cloud-images.ubuntu.com/releases/streams/v1/) data

## Who maintains this project?

Although I (philroche) work for the Canonical Public Cloud team this is not a Canonical officially supported or 
maintained project. If you have any queries or issues please [create a github issue](https://github.com/philroche/ubuntu-cloud-aggreg8streams/issues/new).

## What problem is this project solving?

Ubuntu Cloud images are a very popular and are used widely in the public clouds like AWS, Azure or GCE or in other 
cloud deployments like Openstack or even locally using KVM.

Users will very often want to use the latest Ubuntu Cloud images for their chosen Ubuntu release as it means packages 
don't have to be updated and that they can be assured that the most recent images will have the current known 
security vulnerabilities already patched. Getting the details of the latest Ubuntu Cloud images is usually done 
though automation.

Canonical maintain the [simplestreams](http://cloud-images.ubuntu.com/releases/streams/v1/) datasource which is a 
machine readable listing of all current Ubuntu images across many clouds. As it is a statis JSON datasource it means 
to find the latest image you need to download all the data and parse it yourself. There is some tooling around this 
to make it easier but the overhead is quite high and adds a lot of load to the Canonical servers.

I have detailed some of these wrapper/utility tools in a couple of blog posts: 
[Ubuntu cloud images and how to find the most recent cloud image – part 1/3](https://philroche.net/2018/02/12/ubuntu-cloud-images-and-how-to-find-the-most-recent-cloud-image-part-1-of-3/) 
& [Ubuntu cloud images and how to find the most recent cloud image – part 2/3](https://philroche.net/2018/05/15/ubuntu-cloud-images-and-how-to-find-the-most-recent-cloud-image-part-2-of-3/)

Cloud providers like AWS, GCE and Azure provide ways to query their cloud to find the latest images using the 
libraries or CLI tools but this also has the overhead of installing tools and possibly configuring credentials.

All of the above adds a lot of overhead and delay to getting the data you need... enter [ubuntu-cloud-aggreg8streams](https://github.com/philroche/ubuntu-cloud-aggreg8streams).

## How is this project solving this problem?

ubuntu-cloud-aggreg8streams solves the problem of overhead by removing the need for any package or tool installation. 
A simple and quick HTTP request using WGET or CURL will return the exact data you need using the tools you already have 
installed. 

ubuntu-cloud-aggreg8streams's [update-streams.sh](https://github.com/philroche/ubuntu-cloud-aggreg8streams/blob/main/update-streams.sh) 
can be run periodically to download the parse the [simplestreams](http://cloud-images.ubuntu.com/releases/streams/v1/) 
datasources and add the entries to the ubuntu-cloud-aggreg8streams simplestreams.db SQLite database. This means the 
data is now in a queryable and filterable database.

Using the wonderful [Datasette](https://datasette.io/) project we can add a queryable and filterable readonly 
frontend to this database.

See https://aggreg8streams.tinyviking.ie/ for example hosted [datasette](https://datasette.io/) instance.

You can build and edit these queries using this [datasette](https://datasette.io/) web frontend.

[datasette](https://datasette.io/) provides a [JSON API](https://docs.datasette.io/en/stable/json_api.html) so 
you can use the filtered data in your automation.

The following will return the latest Ubuntu 18.04 Bionic Minimal on AWS in the eu-west-1 region.

```shell
curl "https://aggreg8streams.tinyviking.ie/simplestreams.json?sql=select+image_id+from+cloudimage+where+label+%3D+%27release%27+and+release+%3D+%27bionic%27+and+family+%3D+%27minimal%27+and+content_id+%3D+%27com.ubuntu.cloud%3Areleased%3Aaws%27+and+crsn+%3D+%27eu-west-1%27+order+by+version_name+desc+limit+1&_shape=arrayfirst"
```

The response payload for the above is 383 bytes and takes 39ms being served from a very old intel nuc in my network closet. 
It requires no setup of libraries, and you only download the data you need.  

You can also have CSV data returned instead using [datasette's CSV export feature](https://docs.datasette.io/en/stable/csv_export.html).

A neat benefit of the [datasette](https://datasette.io/) web frontend is that any query can be bookmarked and 
used in your automation.

## What next?

It would be nice to create [custom pages and templates](https://docs.datasette.io/en/stable/custom_templates.html) for 
easier viewing of the data in the web frontend.


## Example commands to run datasette with sample database

Save the current database from demo/example site locally

```
wget https://aggreg8streams.tinyviking.ie/simplestreams.db --show-progress --output-document=simplestreams.db
```

Run datasette server with this database

```
python3 -m datasette serve --immutable ./simplestreams.db --port 8001 --cors --metadata ./simplestreams-datasette-metadata.json -h 0.0.0.0
```
