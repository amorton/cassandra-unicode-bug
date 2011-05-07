# Description

Python code to reproduce a fault moving from Cassandra 0.6 to 0.7 as described here http://www.mail-archive.com/user@cassandra.apache.org/msg12931.html

Written to work against the sample Keysapce1 keyspace. 

Code in the load/load.py using pycassa-0.3 to load two rows into a cassandra 0.6 server. Output was

  Insert rows 数時間 foo
  Read rows
  数時間 {'bar': 'baz'}
  foo {'bar': 'baz'}
  
Then upgrade from 0.6.12 to 0.7.5 using the recommended approach:

1. `bin/nodetool drain`
2. migrate config with `bin/config-converter` 
3. start 0.7
4. run `bin/schematool`

Code in read/read.py then run to read the data back. Got the error below

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