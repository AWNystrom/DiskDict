from os.path import exists, expanduser, realpath
from os import mkdir, remove, rename, walk
from xxhash import xxh64
from base64 import b64encode, b64decode


class DiskDict(object):
    def __init__(self, location,
                 serializer=repr,
                 deserializer=eval,
                 default=None):
        """
                Store key value pairs on disk. All operations are as fast as the host operating 
                system's file access complexities.

                --- parameters ---
                location : The directory in which all key value pairs will be stored. You
                           shouldn't plan on using this directory for anything else as it will 
                           fill up with files - one for each key that's stored.

                serializer : A value associated with a key is serialized so that it can be written
                             to disk. This callable determines how the value is serialized. Good
                             options could be repr, cPickle.dumps, or ujson.dumps, depending on
                             your task.
		
		deserializer : This is the inverse of serializer. E.g. if serializer is repr, this
                               should be eval. If serializer was cPickle.dumps, this should be
                               cPickle.loads, etc.
						   
		default : The value returned when a key is not present. Think default as in 
                          collections.defaultdict. If default is a callable, its __call__ method
                          will be called.

                --- methods ---
                get : Returns the value associated with the specified key.

                put : Associates a key with a value.

                Note: bracket operators have been overloaded.

                Example usage:

                >> dd = DiskDict('my_disk_dict', default=0)
                >> dd['hello']
                0
                >> dd['hello'] += 7
                >> dd['hello']
                7
                >> del dd['hello']
                >> dd['hello']
                0
               """
        self.serializer = serializer
        self.deserializer = deserializer
        self.location = realpath(expanduser(location.rstrip('/'))) + '/'
        self.default = default
        if not exists(self.location):
            mkdir(self.location)

    def get(self, key, default=None):
        if default is None:
            default = self.default

        serialized_key = self.serializer(key)
        key_hash = xxh64(serialized_key).hexdigest()
        hash_file = self.location + key_hash

        if not exists(hash_file):
            return default() if hasattr(default, '__call__') else default

        for line in open(hash_file):
            b64_key, b64_val = line.split('\t')
            key_from_line = self.deserializer(b64decode(b64_key))
            if key == key_from_line:
                return self.deserializer(b64decode(b64_val))
        return default() if hasattr(default, '__call__') else default

    def put(self, key, val):
        serialized_key = self.serializer(key)
        key_hash = xxh64(serialized_key).hexdigest()
        hash_file = self.location + key_hash
        remove_key = False

        if exists(hash_file):
            for line in open(hash_file):
                b64_key, b64_val = line.split('\t')
                key_from_line = self.deserializer(b64decode(b64_key))
                if key == key_from_line:
                    deserialized_val = self.deserializer(b64decode(b64_val))
                    if val == deserialized_val:
                        #The key is already points to the proper value.
                        return
                    remove_key = True
                    #The key is in the dict, but points to an old value. Make a copy of the
                    #file but without the line for this key, then replace the old hash file
                    #with it.

            if remove_key:
                self.__delitem__(key)

        #Now just append the key,val pair to the hash file
        fd = open(hash_file, 'a')
        fd.write(b64encode(self.serializer(key)))
        fd.write('\t')
        fd.write(b64encode(self.serializer(val)))
        fd.write('\n')
        fd.close()

    def __getitem__(self, key):
        return self.get(key)

    def __setitem__(self, key, val):
        self.put(key, val)

    def __contains__(self, key):
        serialized_key = self.serializer(key)
        key_hash = xxh64(serialized_key).hexdigest()
        hash_file = self.location + key_hash

        if not exists(hash_file):
            return False

        for line in open(hash_file):
            b64_key, b64_val = line.split('\t')
            key_from_line = self.deserializer(b64decode(b64_key))
            if key == key_from_line:
                return True

        return False

    def __delitem__(self, key):
        serialized_key = self.serializer(key)
        key_hash = xxh64(serialized_key).hexdigest()
        hash_file = self.location + key_hash
        if not exists(hash_file):
            #Our work here is done.
            return
        copied_filename = hash_file + '~'
        copied_file = open(copied_filename, 'w')
        found = False

        for line_count, line in enumerate(open(hash_file)):
            b64_key, b64_val = line.split('\t')
            key_from_line = self.deserializer(b64decode(b64_key))
            if not found and key == key_from_line:
                found = True
                continue
            copied_file.write(line)
            
        copied_file.close()
        rename(copied_filename, hash_file)

        if line_count == 0 and found:
            #If we removed the last element, remove the hash file.
            remove(hash_file)
            
        if not found:
            raise KeyError
    
    def iterkeys(self):
        deserializer = self.deserializer
        for root, dirs, files in walk(self.location):
            for hash_filename in files:
                for line in open(root + hash_filename):
	                b64_key, _ = line.split('\t')
	                yield deserializer(b64decode(b64_key))
	
    def iteritems(self):
        deserializer = self.deserializer
        for root, dirs, files in walk(self.location):
            for hash_filename in files:
                for line in open(root + hash_filename):
                    b64_key, b64_val = line.split('\t')
                    yield (deserializer(b64decode(b64_key)), 
                           deserializer(b64decode(b64_val)))
	                       
    def itervalues(self):
        deserializer = self.deserializer
        for root, dirs, files in walk(self.location):
            for hash_filename in files:
                for line in open(root + hash_filename):
                    _, b64_val = line.split('\t')
                    yield deserializer(b64decode(b64_val))
    
    def keys(self):
        return [k for k in self.iterkeys()]
    
    def values(self):
        return [v for v in self.itervalues()]
    
    def items(self):
        return [p for p in self.iteritems()]