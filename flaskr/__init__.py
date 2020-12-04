import os
from zipfile import ZipFile

from flask import Flask, render_template, request, redirect, url_for

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
        series_dict = {}
        comic_series = os.listdir('flaskr/static/comics/')
        comic_series.sort()
        thumbnails = [ url_for('static', filename="{}_thumbnail.png".format(series)) for series in comic_series ]

        for i in range(len(comic_series)):
            series_dict[comic_series[i]] = thumbnails[i]
        return render_template('comics.html', series_dict=series_dict)

    """
    Shows all chapters of a certain comic
    """
    @app.route('/library/<comic_name>/')
    def comic_selection(comic_name):
        chapters = os.listdir('flaskr/static/comics/{}'.format(comic_name))
        chapters = [chapter for chapter in chapters if "cbz" not in chapter ]
        try:
            chapters.remove("thumbnail.png")
        except ValueError:
            pass
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
        chapters = os.listdir('flaskr/static/comics/{}'.format(comic_name))
        chapters = [chapter for chapter in chapters if "cbz" not in chapter]
        chapters.sort(key=num_sort)
        current_chapter_index = chapters.index(chapter)
        has_prev = False
        has_next = False
        next_chapter = None
        previous_chapter = None

        if current_chapter_index + 1 <= len(chapters) - 1:
            has_next = True
            next_chapter = chapters[current_chapter_index+1]
        if current_chapter_index - 1 >= 0:
            has_prev = True
            previous_chapter = chapters[current_chapter_index-1]
        

  


        pages = os.listdir(
            'flaskr/static/comics/{}/{}'.format(comic_name, chapter))
        pages.sort(key=num_sort)
        pages = [
            'comics/{}/{}/{}'.format(comic_name, chapter, page) for page in pages]

        context = {
            "comic_name":comic_name,
            "chapter":chapter,
            "has_prev":has_prev,
            "has_next":has_next,
            "next_chapter":next_chapter,
            "previous_chapter":previous_chapter
        }

        return render_template('chapter.html', pages=pages, context=context)

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
