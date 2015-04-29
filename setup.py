from setuptools import setup, find_packages

setup(
    name = "disk_dict",
    packages = find_packages(),
    version = "2.2.0",
    description = "A disk-based key/value store in Python.",
    author = "Andrew Nystrom",
    author_email = "AWNystrom@gmail.com",
    url = "https://github.com/AWNystrom/DiskDict",
    keywords = ["disk", "based", "key", "value", "store", "dict", "diskdict"],
    license = "Apache 2.0",
    install_requires = ['xxhash>=0.3.2'],
    long_description=open('README.txt').read(),
    classifiers = ["Programming Language :: Python", 
    			   "Programming Language :: Python :: 2.7",
    			   "Programming Language :: Python :: 2",
    			   "License :: OSI Approved :: Apache Software License",
    			   "Operating System :: OS Independent",
    			   "Development Status :: 4 - Beta",
    			   "Intended Audience :: Developers"
    			   ]
	)
