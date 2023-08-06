# MappingOnDisk
An effort to make a map system which can be stored on hard disk/SSDs and other non voletile media.

## Installation

pip install mapdisk

## Usage

from mapDisk import mapDisk

create the hashed map file object
    md = mapDisk.MapD("HashMapName.md","path/to/file")

"HashMapName.mpd" is the name of the database file, it is created if it does not already exists and read otherwise
path/to/file is "." by default


Adding key-value pairs

md.add("key","value")

key and value are converted to string and then stored for current implementation, returns the value stored for validating written data
the same function is used to overwrite the previous data/value


Reading value

md.read(str("key))

returns the value in string format, only catch is if the value contains \x00 at the end it will be trimmed off for current implementation as a temporary fix


Deleting value

md.delete(str(key))

deletes the key-value from datafile

md.shrink()

can be called to shrink datafile if some delete operations are performed, isn't called by default after delete operation.


md.close()

It should be called at the end of data operations to close file descriptors

The above operations return None if they fail for some reason, this can be used to check for failures