# ubuntu-cloud-aggreg8streams
[Datasette](https://datasette.io/) based project for populating and viewing Ubuntu cloud simplestreams data

See https://aggreg8streams.tinyviking.ie/ for example hosted [datasette](https://datasette.io/) instance

I built this database so that Ubuntu public cloud image data could be queryied with very specific filters and 
results returned quickly without having to download all data - as is the case with 
[Ubuntu streams data](http://cloud-images.ubuntu.com/releases/streams/v1/). It also removes the need for any library 
like boto to query cloud image data. A simple HTTP request will return what you need.

One of the huge benefits of using [datasette](https://datasette.io/) to achieve this is being able to serve results 
to queries in json or csv.

Example:

* [Find the latest Ubuntu 18.04 Bionic Minimal on AWS in the eu-west-1 region and return as json](https://aggreg8streams.tinyviking.ie/simplestreams.json?sql=select+image_id+from+cloudimage+where+label+%3D+%27release%27+and+release+%3D+%27bionic%27+and+family+%3D+%27minimal%27+and+content_id+%3D+%27com.ubuntu.cloud%3Areleased%3Aaws%27+and+crsn+%3D+%27eu-west-1%27+order+by+version_name+desc+limit+1&_shape=arrayfirst)

Any query can be bookmarked and used in your automation.

See [datasette documentation on the JSON API](https://docs.datasette.io/en/stable/json_api.html) for more details on 
how to change the format of your query results.

## Example command to run datasette with sample database

Save the current database from demo/example site locally

```
wget https://aggreg8streams.tinyviking.ie/simplestreams.db --show-progress --output-document=simplestreams.db
```

Run datasette server with this database

```
python3 -m datasette serve --immutable ./simplestreams.db --port 8001 --cors --metadata ./simplestreams-datasette-metadata.json -h 0.0.0.0
```
