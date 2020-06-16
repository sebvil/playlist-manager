import time
from flask import Flask, url_for
from markupsafe import escape
from flask import request
from queries import Query

app = Flask(__name__)

@app.route('/search')
def foo():
    search = request.args.get('search')
    artist = request.args.get('artist')
    album = request.args.get('album')
    unique = request.args.get('unique') == 'True'
    print('unique=', type(unique))
    offset = 0
    limit = 50
#     if offset:
#         offset = int(offset)
#     else:
#         offset = 0

#     if limit:
#         limit = int(limit)
#     else:
#         limit = 20

    query = Query(search, album, artist, unique)
    result = []
    if not query.q:
        return {'result': result}

    query_result = query.make_query()
    query_result = list(map((lambda x: vars(x)), query_result))
    result.extend(query_result)
#         offset += 50
    return {'result' : result}



@app.route('/time')
def get_current_time(artist='', search=''):
    return { 'time': time.time() }

# @app.route('/')
# def default():
#     return {'value' :'0'}

