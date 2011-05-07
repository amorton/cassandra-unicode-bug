#!/usr/bin/env python
# encoding: utf-8
"""
Test to read unicode from a 0.7 server
"""

import sys
import os

import pycassa

def main():
    client = pycassa.connect('Keyspace1')
    standard1 = pycassa.ColumnFamily(client, 'Standard1')

    uni_str = u"数時間"
    uni_str = uni_str.encode("utf-8")
    asc_str = "foo"
    
    print "Read rows"
    print asc_str, standard1.get(asc_str)
    print uni_str, standard1.get(uni_str)
    
if __name__ == '__main__':
    main()

