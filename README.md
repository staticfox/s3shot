# S3Shot
A simple program to take screenshots and upload them to an S3 bucket.

## How to use
* git clone https://github.com/staticfox/s3shot.git
* cd s3shot
* cp example.toml config.toml
* Configure config.toml
* pyvenv .venv
* source .venv/bin/activate
* pip install -r requirements.txt
* python screenshot.py

# Requirements
For now you must have a `~/.aws/credentials` file setup. I'll probably add an option for this in a day or so.  
You must have `scrot` installed. This will probably also change in the future.

# Config options
bucket_name: The name of the S3 bucket
path: The name of the folder that this should be stored in. You can nest directories, but for now, make sure they exist. Also make sure they don't start or stop with a slash.
visibility: One of the follow:
```
'private'
 'public-read'
 'public-read-write'
 'authenticated-read'
 'aws-exec-read'
 'bucket-owner-read'
 'bucket-owner-full-control'
```
image_storage_path: Where the file will be saved (Option to not save soon^tm)
want_clipboard: Whether or not you want the public link copied to your clipboard

# How to make this a command
You can make a bash script with the following and add it to your $PATH
```
#!/bin/bash

/path/to/s3shot/.venv/bin/python /path/to/s3shot/screenshot.py
```

Make sure the script is +x, then run it
