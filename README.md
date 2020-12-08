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
clone this repo

put your comics in `flaskr/static/comics`

If the comics directory is not there, make it.

Chapters should be stored in a directory with the comic name

ex
`flaskr/static/comics/akame_ga_kill/Chapter_{1-20}`

Soft links can also be used

If you cd into the `comics` directory and do `ln -s ~/dir/to/comics/* .`

or

`ln -s ~/dir/to/comics/comic.cbz .`

it will be linked to your static comics folder and snakereader will be able to serve the files.

run `./deploy` for "production"
or if you want to test and debug and contribute just run
`./run`