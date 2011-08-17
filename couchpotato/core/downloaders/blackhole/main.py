from __future__ import with_statement
from couchpotato.core.downloaders.base import Downloader
from couchpotato.core.helpers.encoding import toSafeString
from couchpotato.core.logger import CPLog
from inspect import isfunction
import os
import traceback
import urllib

log = CPLog(__name__)

class Blackhole(Downloader):

    type = ['nzb', 'torrent']

    def download(self, data = {}, movie = {}):

        if self.isDisabled() or not self.isCorrectType(data.get('type')):
            return

        directory = self.conf('directory')

        if not directory or not os.path.isdir(directory):
            log.error('No directory set for blackhole %s download.' % data.get('type'))
        else:
            cp_tag = '.cp(' + movie['library'].get('identifier') + ')' if movie['library'].get('identifier') else ''
            fullPath = os.path.join(directory, '%s%s.%s' % (toSafeString(data.get('name')), cp_tag , data.get('type')))

            try:
                if not os.path.isfile(fullPath):
                    log.info('Downloading %s to %s.' % (data.get('type'), fullPath))
                    if isfunction(data.get('download')):
                        file = data.get('download')()
                        if not file:
                            log.debug('Failed download file: %s' % data.get('name'))
                            return False
                    else:
                        file = urllib.urlopen(data.get('url')).read()

                    with open(fullPath, 'wb') as f:
                        f.write(file)

                    return True
                else:
                    log.info('File %s already exists.' % fullPath)
                    return True
            except:
                log.error('Failed to download to blackhole %s' % traceback.format_exc())
                pass

        return False
