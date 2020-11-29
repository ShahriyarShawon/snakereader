import os
from zipfile import ZipFile

from flask import Flask, render_template, request, redirect

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

    """
    Shows all comics in library by series
    """
    @app.route('/')
    @app.route('/library')
    @app.route('/library/')
    def library():
        comic_series = os.listdir('flaskr/static/comics/') 
        return render_template('comics.html', comic_series=comic_series)

    """
    Shows all chapters of a certain comic
    """
    @app.route('/library/<comic_name>/')
    def comic_selection(comic_name):
        chapters = os.listdir('flaskr/static/comics/{}'.format(comic_name))
        chapters = [chapter for chapter in chapters if "cbz" not in chapter]
        chapters.sort(key=num_sort)
        
        context = {
            "chapters":chapters,
            "comic_name":comic_name
        }
        return render_template('chapters.html',context=context)

    """
    Gets pages for a certain chapter of a comic
    """
    @app.route('/library/<comic_name>/<chapter>')
    def get_pages(comic_name, chapter):
        pages = os.listdir(
            'flaskr/static/comics/{}/{}'.format(comic_name, chapter))
        pages.sort(key=num_sort)
        pages = [
            'comics/{}/{}/{}'.format(comic_name, chapter, page) for page in pages]

        return render_template('chapter.html', pages=pages)

    @app.route('/library/upload', methods=['GET','POST'])
    def upload():
        if request.method == 'POST':
            supported_filetypes = [
                "cbz",
                "zip",
            ]


            folder = request.form["folder"]
            f = request.files['comic']
            final_filename = "{}/{}".format(folder, f.filename)
            

            # if the filename extension is allowed, then extract the file and delete the archive

            final_filepath = 'flaskr/static/comics/{}'.format(final_filename)
            f.save(final_filepath)


            # TODO handle extensions
            extension = final_filename[-3:]
            print("The final filename is {}".format(final_filename))
            print("The extension is {}".format(extension))
            if extension in supported_filetypes:
                with ZipFile(final_filepath) as zf:
                    zf.extractall("flaskr/static/comics/{}".format(folder))
                    os.remove(final_filepath)
 
            return redirect('/library')
        else:
            comics = os.listdir('flaskr/static/comics/')

            return render_template('upload.html', comics=comics)

    return app
