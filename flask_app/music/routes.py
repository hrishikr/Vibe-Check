from flask import Blueprint, render_template, url_for, redirect, request, flash
from flask_login import current_user

from .. import client
from ..cache import cache
from ..forms import MusicReviewForm, SearchForm
from ..models import User, Review
from ..utils import current_time
from ..billboard_scraper import scrape_billboard_hot_20

music = Blueprint("music", __name__)

@music.route('/', methods=['GET', 'POST'])
def index():
    form = SearchForm()
    data = scrape_billboard_hot_20()
    songs = []

    for i in data:
        query = data[i][0]
        
        if query in cache['tracks']:
            songs.append(cache['tracks'][query][0])
        else:
            results = client.get_search_results(query=data[i][0], search_type="Track")
            cache['tracks'][query] = results
            songs.append(results[0])

    if form.validate_on_submit():
        return redirect(url_for('music.query_results', query=form.search_query.data, input_type=form.input_type.data))

    return render_template('index.html', form=form, data=data, songs=songs)

@music.route('/search-results/<query>?<input_type>', methods=['GET'])
def query_results(query, input_type):
    try:
        results = client.get_search_results(query=query, search_type=input_type)
        return render_template('query_results.html', results=results, input_type=input_type, query=query, form = SearchForm())
    except ValueError as err:
        return render_template('query_results.html', error_msg=err, form = SearchForm())


@music.route("/music/<music_id>?<input_type>", methods=["GET", "POST"])
def music_detail(music_id, input_type):
    try:
        result = client.get_result(music_id, input_type)
    except ValueError as e:
        flash(str(e))
        return redirect(url_for("users.login"))

    form = MusicReviewForm()
    if form.validate_on_submit() and current_user.is_authenticated:
        review = Review(
            commenter=current_user._get_current_object(),
            content=form.text.data,
            date=current_time(),
            track_id=music_id,
            song_title=result.name,
        )
        review.save()

        return redirect(request.path)

    reviews = Review.objects(track_id=music_id)

    return render_template(
        "music_detail.html", form=form, info=result, reviews=reviews
    )


@music.route("/user/<username>")
def user_detail(username):
    user = User.objects(username=username).first()
    reviews = Review.objects(commenter=user)

    return render_template("user_detail.html", username=username, reviews=reviews)
