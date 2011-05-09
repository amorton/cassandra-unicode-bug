# Description

Python code to reproduce a fault moving from Cassandra 0.6 to 0.7 as described here http://www.mail-archive.com/user@cassandra.apache.org/msg12931.html

Written to work against the sample Keysapce1 keyspace. 

Code in the load/load.py using pycassa-0.3 to load two rows into a cassandra 0.6 server. Output was

```python
Insert rows 数時間 foo
Read rows
数時間 {'bar': 'baz'}
foo {'bar': 'baz'}
```

Then upgrade from 0.6.12 to 0.7.5 using the recommended approach:

1. `bin/nodetool drain`
2. migrate config with `bin/config-converter` 
3. start 0.7
4. run `bin/schematool`

Code in read/read.py then run to read the data back. Got the error below

```python
aarons-MBP-2011:read-0.7 aaron$ ./read.py 
Read rows
foo OrderedDict([('bar', 'baz')])
数時間
Traceback (most recent call last):
File "./read.py", line 25, in <module>
  main()
File "./read.py", line 22, in main
  print uni_str, standard1.get(uni_str)
File "/Users/aaron/code/scratch/unicode/read-0.7/pycassa/columnfamily.py", line 343, in get
pycassa.cassandra.ttypes.NotFoundException: NotFoundException()
```

When I step the 0.7 code, in `SSTableReader.getPosition` the code fails to compare two keys when looking for the unicode key...

```java
// search for decorated key is 
DecoratedKey(43723696825261962251520276610181237838, e695b0e69982e99693)

// index decorated key is 
DecoratedKey(17420333691542862345855860553793976250, e695b0e69982e99693)
```

# More testing 

Added `simple-test.py` which sets the unicode key, then reads back the key `???` and then reads the unicode key. This code should never work, found the following:

* v0.6.12 bin, code works
* v0.6 source head, code works when cassandra run from command line
* v0.6 source code, code fails when cassandra run inside intelli J
* v0.7.5 bin, code fails 

Expected outcome is:

    $ ./simple-test.py 
    Insert row 数時間
    数時間 1304911869357661
    Read rows
    ???
    Traceback (most recent call last):
      File "./simple-test.py", line 28, in <module>
        main()
      File "./simple-test.py", line 23, in main
        print "???", standard1.get("???")
      File "/Users/aaron/code/scratch/unicode/pycassa/columnfamily.py", line 160, in get
    cassandra.ttypes.NotFoundException: NotFoundException()
