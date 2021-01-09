import os
import shutil
from zipfile import ZipFile


from flask import Flask, render_template, request, redirect, url_for

from .helper import num_sort


COMICS_DIRECTORY = '/home/shahriyar/Documents/comics/'
# DO NOT CHANGE
CACHE_DIR = 'flaskr/static/cache/'

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
        comic_series = os.listdir(COMICS_DIRECTORY)
        comic_series.sort()
        # thumbnails should all the the format of {series_title}_thumbnail.png
        # and should all be placed in the root of the static directory 
        thumbnails = [ url_for('static', filename="{}_thumbnail.png".format(series)) for series in comic_series ]

        for i in range(len(comic_series)):
            series_dict[comic_series[i]] = thumbnails[i]

        return render_template('comics.html', series_dict=series_dict)

    """
    Shows all chapters of a certain comic
    """
    @app.route('/library/<comic_name>/')
    def comic_selection(comic_name):
        chapters = os.listdir('{}/{}'.format(COMICS_DIRECTORY,comic_name))
        
        chapters = [chapter.replace(".cbz","") for chapter in chapters if "cbz" in chapter ]
        try:
            chapters.remove("thumbnail.png")
        except ValueError:
            pass
        # sort by the number at the end of the chaptername
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
        chapters = os.listdir('{}/{}'.format(COMICS_DIRECTORY,comic_name))
        chapters = [chapter.replace(".cbz","") for chapter in chapters if "cbz" in chapter]
        # sort by the number at the end of the chaptername
        chapters.sort(key=num_sort)

        current_chapter_index = chapters.index(chapter)
        has_prev = False
        has_next = False
        next_chapter = None
        previous_chapter = None

        # This decides whether or not there will be a next chapter 
        # or a previous chapter button. Either neither, one, or both
        if current_chapter_index + 1 <= len(chapters) - 1:
            has_next = True
            next_chapter = chapters[current_chapter_index+1]
        if current_chapter_index - 1 >= 0:
            has_prev = True
            previous_chapter = chapters[current_chapter_index-1]

        # extracts cbz file if needed
        chapter_cache_folder = CACHE_DIR+'{}/{}'.format(comic_name, chapter)
        if not os.path.isdir(chapter_cache_folder):
            with ZipFile(COMICS_DIRECTORY+'{}/{}.cbz'.format(comic_name, chapter)) as zipped:
                zipped.extractall(CACHE_DIR+'{}'.format(comic_name))

        # Pages should be copied to the cache directory then 
        # everything else should run
        pages = os.listdir(chapter_cache_folder)

        # create a temporary cache directory that flask can serve images from
        comic_cache_dir = CACHE_DIR+'{}/'.format(comic_name)
        chapter_cache_dir = CACHE_DIR+'{}/{}'.format(comic_name, chapter)

        if not os.path.isdir(comic_cache_dir):
            os.mkdir(comic_cache_dir)
        if not os.path.isdir(chapter_cache_dir):
            os.mkdir(chapter_cache_dir)
            

        # making sure it's sorting numerically and not lexicographically
        pages.sort(key=num_sort)
        pages = [
            'cache/{}/{}/{}'.format(comic_name, chapter, page) for page in pages]

        context = {
            "comic_name":comic_name,
            "chapter":chapter,
            "has_prev":has_prev,
            "has_next":has_next,
            "next_chapter":next_chapter,
            "previous_chapter":previous_chapter
        }

        return render_template('chapter.html', pages=pages, context=context)

    # COMPLETELY NONFUNCTIONAL ATM
    # @app.route('/library/upload', methods=['GET','POST'])
    # def upload():
    #     if request.method == 'POST':
    #         # You can add supported file types here but as of Dec 4 2020, 
    #         # only directories of images actually work
    #         supported_filetypes = [
    #             "cbz",
    #             "zip",
    #         ]

    #         folder = request.form["folder"]
    #         f = request.files['comic']
    #         final_filename = "{}/{}".format(folder, f.filename)
    #         final_filepath = 'flaskr/static/comics/{}'.format(final_filename)
    #         f.save(final_filepath)

    #         extension = final_filename[-3:]
    #         print("The final filename is {}".format(final_filename))
    #         print("The extension is {}".format(extension))
    #         if extension in supported_filetypes:
    #             with ZipFile(final_filepath) as zf:
    #                 zf.extractall("flaskr/static/comics/{}".format(folder))
    #                 os.remove(final_filepath)
 
    #         return redirect('/library')
    #     else:
    #         comics = os.listdir('flaskr/static/comics/')

    #         return render_template('upload.html', comics=comics)

    return app
