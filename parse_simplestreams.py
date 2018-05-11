#!/home/philroche/.virtualenvs/streamsdatasette/bin/python3
#   Copyright (C) 2018 Canonical Ltd.
#
#   Author: Philip Roche <phil.roche@canonical.com>
#   https://launchpad.net/simplestreams
#   https://bazaar.launchpad.net/~simplestreams-dev/simplestreams/trunk/view/head:/bin/sstream-query
#   Simplestreams is free software: you can redistribute it and/or modify it
#   under the terms of the GNU Affero General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or (at your
#   option) any later version.
#
#   Simplestreams is distributed in the hope that it will be useful, but
#   WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
#   or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Affero General Public
#   License for more details.
#
#   You should have received a copy of the GNU Affero General Public License
#   along with Simplestreams.  If not, see <http://www.gnu.org/licenses/>.
from peewee import *
from simplestreams import filters
from simplestreams import mirrors
from simplestreams import util

import argparse
import errno
import signal
import sys

db = SqliteDatabase('simplestreams.db')

'''
  {
    "aliases": "14.10,u,utopic",
    "arch": "i386",
    "content_id": "com.ubuntu.cloud:released:aws-cn",
    "crsn": "cn-north-1",
    "datatype": "image-ids",
    "endpoint": "https://ec2.cn-north-1.amazonaws.com.cn",
    "format": "products:1.0",
    "id": "ami-bc71ec85",
    "item_name": "cnnn1es",
    "label": "release",
    "os": "ubuntu",
    "product_name": "com.ubuntu.cloud:server:14.10:i386",
    "pubname": "ubuntu-utopic-14.10-i386-server-20150708",
    "region": "cn-north-1",
    "release": "utopic",
    "release_codename": "Utopic Unicorn",
    "release_title": "14.10",
    "root_store": "ssd",
    "support_eol": "2015-07-23",
    "supported": "False",
    "updated": "Wed, 09 May 2018 21:17:15 +0000",
    "version": "14.10",
    "version_name": "20150708",
    "virt": "pv"
  }
'''


class CloudImage(Model):
    class Meta:
        database = db

    aliases = CharField(null=True)
    arch = CharField(null=True, index=True)
    content_id = CharField(index=True)
    crsn = CharField(null=True)
    datatype = CharField()
    endpoint = CharField(null=True)
    format = CharField()
    image_id = CharField(null=True, index=True)
    item_name = CharField(index=True)
    label = CharField(null=True)
    os = CharField(null=True, index=True)
    product_name = CharField(index=True)
    pubname = CharField(null=True, index=True)
    region = CharField(null=True, index=True)
    release = CharField(null=True, index=True)
    release_codename = CharField(null=True, index=True)
    release_title = CharField(null=True, index=True)
    root_store = CharField(null=True)
    support_eol = DateField(null=True)
    supported = BooleanField(null=True, index=True)
    updated = DateTimeField(index=True)
    version = CharField(null=True)
    version_name = CharField(null=True)
    virt = CharField(null=True)
    ftype = CharField(null=True, index=True)
    path = CharField(null=True)
    item_url = CharField(null=True)
    size = BigIntegerField(null=True)
    md5 = CharField(null=True)
    sha256 = CharField(null=True)


def warn(msg):
    sys.stderr.write("WARN: %s" % msg)


class FilterMirror(mirrors.BasicMirrorWriter):
    def __init__(self, config=None):
        super(FilterMirror, self).__init__(config=config)
        if config is None:
            config = {}
        self.config = config
        self.entries = []

    def load_products(self, path=None, content_id=None):
        return {'content_id': content_id, 'products': {}}

    def insert_item(self, data, src, target, pedigree, contentsource):
        # src and target are top level products:1.0
        # data is src['products'][ped[0]]['versions'][ped[1]]['items'][ped[2]]
        # contentsource is a ContentSource if 'path' exists in data or None
        data = util.products_exdata(src, pedigree)
        if 'path' in data:
            data.update({'item_url': contentsource.url})
        data["image_id"] = data.get("id", None)
        if "id" in data:
            del data["id"]
        self.entries.append(data)


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('mirror_url')

    cmdargs = parser.parse_args()

    (mirror_url, path) = util.path_from_mirror_url(cmdargs.mirror_url, None)

    initial_path = path

    def policy(content, path):
        if initial_path.endswith('sjson'):
            return util.read_signed(content,
                                    keyring=None,
                                    checked=True)
        else:
            return content

    smirror = mirrors.UrlMirrorReader(mirror_url, policy=policy)

    cfg = {}#'max_items': 1

    tmirror = FilterMirror(config=cfg)
    try:
        tmirror.sync(smirror, path)
        db.connect()
        db.create_tables([CloudImage])
        for cloud_image_entry in tmirror.entries:
            print(cloud_image_entry)
            CloudImage.create(**cloud_image_entry)
    except IOError as e:
        if e.errno == errno.EPIPE:
            sys.exit(0x80 | signal.SIGPIPE)
        raise


if __name__ == '__main__':
    main()

# vi: ts=4 expandtab syntax=python
