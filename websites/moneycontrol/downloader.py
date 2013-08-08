#! /usr/bin/env python

"""
script to download a given html page and store it to a given destination
"""

import os
from urllib2 import urlopen
from multiprocessing import cpu_count, Pool

ncpus = cpu_count()

def get_html(url):
    try:
        html = urlopen(url, timeout=60).read()
        return html
    except:
        print 'Not able to retrieve page for\n%s' % (url)
            
def download(url, dst):
    if url and dst:
        print 'Downloading: %s\nDestination: %s\n' % (url, dst)
        html = get_html(url)
        if html:
            f = open(dst, 'w')
            f.write(html)
    return None

def _parallel_download(url_dst):
    url, dst = url_dst
    download(url, dst)
    return None

def parallel_download(urls, dst_file_names, nthreads=32, download_if_no_file=True):
    d = dict(zip(dst_file_names, urls))
    if download_if_no_file:
        for k in d.keys():
            if os.path.exists(k):
                print '%s file exists... not downloading' % (k)
                del d[k]
                
    # return if there is nothing to download
    if not d: return None

    dst_file_names, urls = zip(*d.items())
    url_dst = zip(urls, dst_file_names)
    p = Pool(nthreads)
    p.map(_parallel_download, url_dst)

    return None

if __name__ == '__main__':
    urls = ['http://stackoverflow.com/questions/1858720/how-to-pass-items-as-args-lists-in-map',
            'http://stackoverflow.com/questions/1858720/how-to-pass-items-as-args-lists-in-map']
    dst_names = ['justhere', 'justhere1']

    #p = Pool(2)
    #p.map(parallel_download, zip(urls, dst_names))
    parallel_download(urls, dst_names)
