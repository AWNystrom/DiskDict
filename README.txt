DiskDict
A disk-based key/value store in Python with no dependencies. All operations are as fast as the host operating system's file access complexities. Methods have been overloaded for pretty syntax.

Example Usage
>> dd = DiskDict('my_disk_dict', default=0)
>> dd['hello']
0
>> dd['hello'] += 7
>> dd['hello']
7
>> del dd['hello']
>> dd['hello']
0

https://github.com/AWNystrom/DiskDict
