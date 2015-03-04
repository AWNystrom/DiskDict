# DiskDict
A disk-based key/value store in Python with no dependencies. All operations are as fast as the host operating system's file access complexities. Methods have been overloaded for pretty syntax.
		
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
