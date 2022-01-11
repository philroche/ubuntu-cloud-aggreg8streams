# ubuntu-cloud-aggreg8streams
Datasette based project for populating and viewing Ubuntu cloud simplestreams data

See https://aggreg8streams.tinyviking.ie/ for example hosted datasette instance

## Example command to run datasette with sample database

python3 -m datasette serve ./simplestreams.db --port 8001 --cors --metadata ./simplestreams-datasette-metadata.json -h 0.0.0.0
