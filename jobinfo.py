#!/usr/bin/env python3

"""
Extract job info from WARC files’ warcinfo record
"""

import sys, json, os
from datetime import datetime
from warcio.archiveiterator import ArchiveIterator

if __name__ == '__main__':
    json.dump ({'version': 2, 'generated': datetime.utcnow ().isoformat ()}, sys.stdout)
    sys.stdout.write ('\n')
    sys.stdout.flush ()

    for l in sys.stdin:
        l = l.strip ()
        with open (l, 'rb') as fd:
            for record in ArchiveIterator (fd):
                if record.rec_type == 'warcinfo':
                    warcinfo = json.load (record.raw_stream)
                    try:
                        chromebot = warcinfo['extra']['chromebot']
                    except KeyError:
                        break
                    jid = chromebot['jobid']
                    params = {'recursive': chromebot['recursive'], 'concurrency': chromebot['concurrency']}
                    j = {'id': jid,
                        'user': chromebot['user'],
                        'queued': chromebot['queued'],
                        'retrieved': record.rec_headers['WARC-Date'],
                        'warcsize': os.path.getsize (l),
                        'url': warcinfo['parameters']['url'],
                        'seedurl': chromebot['url'],
                        'parameters': params}

                    json.dump (j, sys.stdout)
                    sys.stdout.write ('\n')
                    sys.stdout.flush ()

                    # don’t process more than the first warcinfo
                    break

