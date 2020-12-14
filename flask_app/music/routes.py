from flask import Blueprint, render_template, url_for, redirect, request, flash
from flask_login import current_user

from .. import client
from ..cache import cache
from .. import db
from ..forms import MusicReviewForm, SearchForm, LikedSongsForm
from ..models import User, Review, Song
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

@music.route('/search-results/<query>&<input_type>', methods=['GET'])
def query_results(query, input_type):
    try:
        results = client.get_search_results(query=query, search_type=input_type)
        return render_template('query_results.html', results=results, input_type=input_type, query=query, form = SearchForm())
    except ValueError as err:
        return render_template('query_results.html', error_msg=err, form = SearchForm())


@music.route("/music/<music_id>&<input_type>", methods=["GET", "POST"])
def music_detail(music_id, input_type):
    try:
        result = client.get_result(music_id, input_type)
    except ValueError as e:
        flash(str(e))
        return redirect(url_for("users.login"))

    review_form = MusicReviewForm()
    liked_songs_form = LikedSongsForm()
    if review_form.validate_on_submit() and current_user.is_authenticated:
        review = Review(
            commenter=current_user._get_current_object(),
            content=review_form.text.data,
            date=current_time(),
            music_id=music_id,
            input_type=input_type,
            song_title=result.name,
        )
        review.save()

        return redirect(request.path)
        
    if liked_songs_form.validate_on_submit() and current_user.is_authenticated and input_type == "Track":
        song = Song(
            user=current_user._get_current_object(),
            song=result.name,
            artist=result.artist,
            album=result.album_name
        )
        song.save()

        return redirect(request.path)

    reviews = Review.objects(music_id=music_id)
    liked_song = Song.objects(user=current_user._get_current_object(), song=result.name).first()

    return render_template(
        "music_detail.html", review_form=review_form, liked_songs_form=liked_songs_form, info=result, reviews=reviews, song=liked_song, input_type=input_type, music_id=music_id
    )


@music.route("/user/reviews/<username>")
def user_reviews(username):
    user = User.objects(username=username).first()
    reviews = Review.objects(commenter=user)

    return render_template("user_reviews.html", username=username, reviews=reviews)

@music.route("/user/liked/<username>")
def liked_songs(username):
    user = User.objects(username=username).first()
    songs = Song.objects(user=user)

    return render_template("liked_songs.html", username=username, liked_songs=songs)

@music.route("/user/liked/<username>&<song>", methods=["GET", "POST"])
def remove_liked(username, song):
    user = User.objects(username=username).first()
    song = Song.objects(user=user, song=song).first()
    song.delete()
    
    songs = Song.objects(user=user)
    
    return render_template("liked_songs.html", username=username, liked_songs=songs)
