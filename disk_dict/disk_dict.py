from os.path import exists
from os import mkdir, remove, makedirs
from base64 import b32encode

class DiskDict(object):
	def __init__(self, location, max_filename_len=255, default=None):
		"""
		Store key value pairs on disk. All operations are as fast as the host operating 
		system's file access complexities.
		
		--- parameters ---
		location : The directory in which all key value pairs will be stored. You
				   shouldn't plan on using this directory for anything else as it will 
				   fill up with files - one for each key that's stored.
		
		max_filename_len : The maximum number of characters the host operating system
						   allows in the name of a file.
						   
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
		self.max_filename_len = max_filename_len
		self.location = location.rstrip('/') + '/'
		self.default = default
		self.make()
		
	def make(self):
		if not exists(self.location):
			mkdir(self.location)
	
	def _get_path(self, key_):
		"""
		Returns the internal path for a key.
		"""
		key = '_' + b32encode(repr(key_)) #Prefix with _ in case empty
		path = []
		for i in xrange(0, len(key), self.max_filename_len):
			path.append(key[i:i+self.max_filename_len])
		return self.location + '/'.join(path)
		
	def get(self, key, default=None):
		if default is None:
			default = self.default
		filename = self._get_path(key)
		if exists(filename):
			fd = open(filename)
			data = fd.read()
			val = eval(data)
			return val
		else:
			return default() if hasattr(default, '__call__') else default
			
	def put(self, key, val):
		path = self._get_path(key)
		if '/' in path:
			dirs, filename = path.rsplit('/', 1)
			if not exists(dirs):
				makedirs(dirs)
			filename = dirs + '/' + filename
		else:
			filename = path
		
		fd = open(filename, 'w')
		fd.write(repr(val))
		fd.close()
	
	def __getitem__(self, key):
		return self.get(key)
	
	def __setitem__(self, key, val):
		self.put(key, val)
	
	def __contains__(self, key):
		return self.get(key) is not None
	
	def __delitem__(self, key):
		if key == '':
			return
		filename = self._get_path(key)
		if exists(filename):
			remove(filename)