#!/usr/bin/env python
# encoding: utf-8
"""
Simple Test to load unicode into a Cassandra v0.6 server
"""

import sys
import os

import pycassa

def main():
    client = pycassa.connect()
    standard1 = pycassa.ColumnFamily(client, 'Keyspace1', 'Standard1')

    uni_str = u"数時間"
    uni_str = uni_str.encode("utf-8")
    
    print "Insert row", uni_str
    print uni_str, standard1.insert(uni_str, {"bar" : "baz"})

    print "Read rows"
    print "???", standard1.get("???")
    print uni_str, standard1.get(uni_str)

    
if __name__ == '__main__':
    main()

