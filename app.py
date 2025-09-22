from flask import Flask, render_template, request
import pickle

app = Flask(__name__)

# Load data
movies = pickle.load(open("movies_list.pkl", "rb"))
similarity = pickle.load(open("similarity.pkl", "rb"))

def recommend(movie):
    if movie not in movies['title'].values:
        return ["Movie not found in database!"]
    
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(
        list(enumerate(similarity[index])),
        reverse=True,
        key=lambda x: x[1]
    )
    recommended_movies = []
    for i in distances[1:6]:  # skip the first (same movie)
        recommended_movies.append(movies.iloc[i[0]].title)
    return recommended_movies

@app.route("/", methods=["GET", "POST"])
def home():
    recommendations = []
    if request.method == "POST":
        movie_name = request.form.get("movie")
        recommendations = recommend(movie_name)
    return render_template("index.html", recommendations=recommendations, movies=movies['title'].values)

if __name__ == "__main__":
    app.run(debug=True)
