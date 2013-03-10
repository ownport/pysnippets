#!/usr/bin/env python
#   -*- coding: utf-8 -*-
#   
#   Gevent non-blocked iMap
#

import sys
import gevent

from gevent.pool import Pool
from gevent.queue import Queue
from gevent.queue import Empty
from gevent.greenlet import Greenlet

PY3 = sys.version_info[0] >= 3

class NonBlockingIMap(object):
    ''' NonBlockingIMap class
    '''
    def __init__(self, size=1, func=None, iterable=None):
        ''' __init__
        '''
        if size is not None and size <= 0:
            raise ValueError('size must not be negative and not equal zero: %r' % (size, ))
        self.size = size
        
        if func is None:
            raise RuntimeError('func must be assigned: %s' % (func, ))
        self.func = func

        self.greenlets_count = 0        
        self.iterable = iterable
        self.queue = Queue()

    def __iter__(self):
        ''' __iter__
        '''
        return self

    if PY3:
        __next__ = next
        del next

    def next(self):
        ''' next
        '''
        gevent.sleep()
        value = None
        if self.greenlets_count >= self.size:
            return value
        try:
            item = self.iterable.get_nowait()
            gevent.spawn(self.func, item).link(self._on_result)
            self.greenlets_count += 1
        except Empty:
            pass
            
        try:
            value = self.queue.get_nowait()
        except Empty:
            pass
            
        if not value and self.greenlets_count <= 0:
            raise StopIteration()
        return value

    def _on_result(self, greenlet):
        ''' _on_result
        '''
        self.greenlets_count -= 1
        if greenlet.successful():
            self.queue.put(greenlet.value)

def imap_nonblocking(map_size=2, func=None, iterable=None):
    ''' The same as gevent.imap_unordered() except that process is non-blocking.
    '''
    return NonBlockingIMap(size=map_size, func=func, iterable=iterable)


if __name__ == '__main__':
    def test_simple_jobs():
        ''' test: simple obs 
        '''
        def simple_job(task):
            ''' simple job
            '''
            return task

        print 'test_simple_jobs:',
        queue = Queue()
        for i in range(10):
            queue.put('msg-%d' % i)
                
        imap = imap_nonblocking(5, simple_job, queue)
        result = [r for r in imap if r is not None]
        assert result == ['msg-0','msg-1','msg-2','msg-3','msg-4',
                          'msg-5','msg-6','msg-7','msg-8','msg-9',], result
        print 'OK'

    def test_simple_urlfetch():
        ''' test: simple urlfetch
        '''
        import urllib2
        from gevent import monkey
        monkey.patch_socket()
        
        def simple_urlfetch(url):
            return "%s:%d" % (url, len(urllib2.urlopen(url).read()))

        print 'test_simple_urlfetch:',
        queue = Queue()
        queue.put('http://www.google.com')
        queue.put('http://www.yahoo.com')
        queue.put('http://www.yandex.ru')
        queue.put('http://www.wired.com')
        queue.put('http://python.org/')
        queue.put('http://www.ubuntu.com/')
        queue.put('http://www.apple.com/')
        
        imap = imap_nonblocking(3, simple_urlfetch, queue)
        result = [r for r in imap if r is not None]
        assert len(result) == 7, result
        print 'OK'
    '''
    Tests
    '''    
    test_simple_jobs()
    test_simple_urlfetch()        
        
