DiskDict is a hashtable on your hard drive. It allows you to store KAZILLIONS (!) of key/value pairs and interact with them as you would a Python dictionary, all the while never storing more than two key/value pairs in memory simultaneously. The key/value pairs can be anything that's serializable (you specify the serializer and deserializer, with repr and eval as the default). Since we're operating on the disk, big O of all operations are dependent on the host operating system's file access complexities.

>>> from disk_dict import DiskDict
>>> from numpy import array
>>> dd = DiskDict('my_disk_dict')
>>> a = array([[1,2],[3,4]])
>>> dd[a] = 'I was pointed to by ' + repr(a)
>>> dd[a]
'I was pointed to by array([[1, 2],\n       [3, 4]])'
>>> del dd[a]
>>> dd[a]
>>>

PyPI: https://pypi.python.org/pypi?name=disk_dict&:action=display

Github: https://github.com/AWNystrom/DiskDict/
