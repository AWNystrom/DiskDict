A disk-based key/value store in Python with no dependencies. All operations are as fast as the host operating system's file access complexities. Methods have been overloaded for pretty syntax.

>>> dd = DiskDict('my_disk_dict', default=0)
>>> dd['hello']
0
>>> dd['hello'] += 7
>> dd['hello']
7
>>> del dd['hello']
>>> dd['hello']
0

PyPI: https://pypi.python.org/pypi?name=disk_dict&version=1.0.0&:action=display

Github: https://github.com/AWNystrom/DiskDict/
