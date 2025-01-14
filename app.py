from flask import Flask, redirect, render_template, request
from src.repositories.movie_repository import get_movie_repository

app = Flask(__name__)

# Get the movie repository singleton to use throughout the application
movie_repository = get_movie_repository()


@app.get('/')
def index():
    return render_template('index.html')


@app.get('/movies')
def list_all_movies():
    # TODO: Feature 1
    movies = movie_repository.get_all_movies()
    arr = []
    for key, value in movies.items():
        arr.append({'id':key, 'title':value.title, 'director':value.director, 'rating':value.rating})
    return render_template('list_all_movies.html', list_movies_active=True, movies=arr)

@app.get('/movies/new')
def create_movies_form():
    return render_template('create_movies_form.html', create_rating_active=True)


@app.post('/movies')
def create_movie():
    # TODO: Feature 2
    # This gets the data from the form submission
    movie_title = request.form.get('title')
    movie_director = request.form.get('director')
    movie_rating = request.form.get('rating')

    # Create the movie in the database
    movie_repository.create_movie(movie_title,movie_director, movie_rating)
    # After creating the movie in the database, we redirect to the list all movies page
    return redirect('/movies')

@app.get('/movies/search')
def search_movies():
    # TODO: Feature 3
    movie_title = request.args.get('searched')

    if movie_title is None:
        found_movie = None
    else:
        found_movie = movie_repository.get_movie_by_title(movie_title)
        if found_movie is None:
            found_movie = 'Not Found'
    return render_template('search_movies.html', search_active=True, found_movie=found_movie)

@app.get('/movies/<int:movie_id>')
def get_single_movie(movie_id: int):
    # TODO: Feature 4
    movie = movie_repository.get_movie_by_id(movie_id)
    return render_template('get_single_movie.html', movie=movie)


@app.get('/movies/<int:movie_id>/edit')
def get_edit_movies_page(movie_id: int):
    movie = movie_repository.get_movie_by_id(movie_id)
    return render_template('edit_movies_form.html', movie=movie)


@app.post('/movies/<int:movie_id>')
def update_movie(movie_id: int):
    # TODO: Feature 5
    movie_title = request.form.get('title')
    movie_director = request.form.get('director')
    movie_rating = request.form.get('rating')
 
    # This line Creating the movie in the database
    movie_repository.update_movie(movie_id, movie_title,movie_director, movie_rating)
    # After updating the movie in the database, we redirect back to that single movie page
    return redirect(f'/movies/{movie_id}')


@app.post('/movies/<int:movie_id>/delete')
def delete_movie(movie_id: int):
    # TODO: Feature 6
    movie_repository.delete_movie(movie_id)
    return list_all_movies()
    
   
