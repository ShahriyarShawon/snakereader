import os

from flask import Flask, render_template

from .helper import num_sort


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/')
    @app.route('/library')
    def library():
        print(os.getcwd())
        comics = os.listdir('flaskr/static/comics/')
        return render_template('comics.html', comics=comics)

    @app.route('/library/<comic_name>/<chapter>')
    def get_pages(comic_name, chapter):
        pages = os.listdir('flaskr/static/comics/{}/{}'.format(comic_name,chapter))
        pages.sort(key=num_sort)
        pages = ['comics/{}/{}/{}'.format(comic_name, chapter,page) for page in pages]


        return render_template('chapter.html',pages=pages)


    @app.route('/library/<comic_name>')
    def comic_selection(comic_name):
        chapters = os.listdir('flaskr/static/comics/{}'.format(comic_name))
        chapters = [chapter for chapter in chapters if "cbz" not in chapter]
        chapters.sort(key=num_sort)
        
        context = {
            "chapters":chapters,
            "comic_name":comic_name
        }
        return render_template('chapters.html',context=context)


    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    return app
