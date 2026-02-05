from flask import Flask, render_template, request, redirect, url_for,flash
import random

from database import Base, engine, session
from models import Movies, Songs
from services.movie_api import get_movie_by_title, generate_movie_hints
from services.ai_service import generate_hint

app = Flask(__name__)
app.secret_key = "super_secret_game_key_123"
Base.metadata.create_all(engine)


def seed_movies_from_omdb():
    # proveri dali databasata e full
    if session.query(Movies).count() > 0:
        return


    movie_list = [
        {"title": "Inception", "img": "inception.jpg"},
        {"title": "Titanic", "img": "titanic.jpg"},
        {"title": "Gladiator", "img": "gladiator.jpg"},
        {"title": "The Matrix", "img": "the_matrix.jpg"}
    ]

    print("Seeding database with specific images...")

    for item in movie_list:
        title = item["title"]
        image_filename = item["img"]

        # 1. Dobi hints od API
        movie_data = get_movie_by_title(title)

        if movie_data and "Error" not in movie_data:
            hint_list = generate_movie_hints(movie_data)
            year_val = int(movie_data.get("Year", 2000))
        else:
            hint_list = ["A very famous movie", "Popular in its genre"]
            year_val = 2000

        #
        movie = Movies(
            title=title,
            type="movie",
            year=year_val,
            finished=False,
            points=100,
            attempts="",
            hints="|".join(hint_list),
            image_file=image_filename
        )
        session.add(movie)

    session.commit()
    print("Database seeded successfully!")


@app.get("/")
def index():
    return render_template("index.html")


@app.get("/game/movie/new")
def new_movie_game():
    # 1. site movies
    all_movies = session.query(Movies).all()

    if not all_movies:
        return "No movies found in database", 404

    # 2. random movie
    template = random.choice(all_movies)

    new_game = Movies(
        title=template.title,
        type="movie",
        year=template.year,
        finished=False,
        points=100,
        attempts="",
        hints=template.hints,
        image_file=template.image_file
    )

    # 4. Save new game
    session.add(new_game)
    session.commit()


    return redirect(url_for("play_movie", movie_id=new_game.id))


@app.route("/game/movie/<int:movie_id>", methods=['GET', 'POST'])
def play_movie(movie_id):
    movie = session.get(Movies, movie_id)


    if request.method == 'POST':
        guess = request.form.get("guess").strip().lower()

        if guess == movie.title.lower():
            movie.finished = True

        else:
            flash("Wrong, try again!", "error")
            movie.points = max(0, movie.points - 10)
            movie.add_attempts(guess)

        session.commit()

        return redirect(url_for("play_movie", movie_id=movie_id))


    return render_template("new_movie_game.html", item=movie)


@app.get("/history")
def history():
    # Samo movies dobi
    movies = session.query(Movies).filter_by(finished=True).all()

    return render_template("history.html", history=movies)


@app.route("/game/movie/<int:movie_id>/ai_hint",methods=["GET","POST"])
def ai_hint(movie_id):
    movie = session.get(Movies, movie_id)

    try:

        new_hint = generate_hint("movie", movie.get_hints())
        movie.add_hints(new_hint)
        movie.points = max(0, movie.points - 10)  #cena za koristeje na ai
        session.commit()
    except Exception as e:

        print(f"AI Error: {e}")
        movie.add_hints("AI Service currently unavailable (Check API Key)")
        session.commit()

    return redirect(url_for("play_movie", movie_id=movie_id))

@app.get("/game/movie/<int:movie_id>/details")
def movie_game_details(movie_id):
    movie = session.get(Movies, movie_id)
    return render_template("movie_details.html", movie=movie)


if __name__ == "__main__":
        print("Starting Flask app")
        seed_movies_from_omdb()
        app.run(debug=True)
