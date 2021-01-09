# SnakeReader
A self hosted comic book written in python/flask

## What's Supported?
Currently only supports having directories of images.

Try not to have spaces in the names of anything, it's a nuisance to deal with.


## Requirements
- python3
- flask
- gunicorn

## Installation
Clone this repo

Change `COMICS_DIRECTORY` to the directory your comics are in.

MAKE SURE YOUR DIRECTORY HAS A TRAILING `/`

Your directory should only contain subdirectories named after
each series that you have. In those subdirectories there 
should be .cbz files that hold each chapter. 

NOTE:
- Only cbz is supported right now
- make sure to have the right permissions on your comic directory
- I am in the process of making everything more forgiving and less strict. 


run `./deploy` for "production"
or if you want to test and debug and contribute just run
`./run`