from __future__ import print_function
from future import standard_library
standard_library.install_aliases()
from builtins import object
import re
import os
import urllib.request, urllib.error, urllib.parse
import logging
from datetime import datetime
from ontologyutils.ou_settings import OUConfig

__author__ = 'gautierk'

class HPOActions(object):
    DOWNLOAD='download'

class HPODownloader(object):

    def __init__(self):
        pass

    def download(self):
        now = datetime.utcnow()
        today = datetime.strptime("{:%Y-%m-%d}".format(datetime.now()), '%Y-%m-%d')

        for dir in [OUConfig.HPO_DIRECTORY, OUConfig.HPO_OBO_DIRECTORY, OUConfig.HPO_ANNOTATIONS_DIRECTORY]:
            if not os.path.exists(dir):
                os.makedirs(dir)

        for url in OUConfig.HPO_URIS:
            directory = OUConfig.HPO_ANNOTATIONS_DIRECTORY
            filename = re.match("^.+/([^/]+)$", url).groups()[0]
            logging.debug(url)
            #match = re.match("^.+/([^/]+)$", url)
            if re.match(OUConfig.HPO_OBO_MATCH, url):
                directory = OUConfig.HPO_OBO_DIRECTORY
            elif re.match(OUConfig.HPO_ANNOTATIONS_MATCH, url):
                directory = OUConfig.HPO_ANNOTATIONS_DIRECTORY

            logging.debug(filename)
            # get a new version of HPO
            req = urllib.request.Request(url)

            try:
                response = urllib.request.urlopen(req)

                # Open our local file for writing
                local_file = open('%s/%s'%(directory, filename), "wb")
                #Write to our local file
                local_file.write(response.read())
                local_file.close()

                logging.info("downloaded %s"%filename)

            #handle errors
            except urllib.error.HTTPError as e:
                logging.error("HTTP Error:",e.code , url)
            except urllib.error.URLError as e:
                logging.error("URL Error:",e.reason , url)