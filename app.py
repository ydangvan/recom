from flask import Flask, request, render_template
import pandas as pd

app = Flask(__name__)

# Placeholder for loading your movies data (Replace this with your actual code)
# For the purpose of this example, let's create a dummy movies DataFrame:
movies = pd.DataFrame({
    'movie_id': [1, 2, 3, 4, 5],
    'title': ['The Shawshank Redemption', 'The Godfather', 'The Dark Knight', 'Pulp Fiction', 'The Lord of the Rings'],
    'genre': ['Drama', 'Crime', 'Action', 'Crime', 'Fantasy']
})

# Placeholder for the cosine similarity matrix (Replace with your actual cosine similarity data)
# For demonstration, let's create a dummy similarity matrix as a pandas DataFrame:
cosine_sim_df = pd.DataFrame({
    # Your cosine similarity scores should be here
    # This is just a placeholder to simulate similarity scores
    0: [1, 0.8, 0.3, 0.4, 0.5],
    1: [0.8, 1, 0.2, 0.5, 0.6],
    2: [0.3, 0.2, 1, 0.7, 0.3],
    3: [0.4, 0.5, 0.7, 1, 0.4],
    4: [0.5, 0.6, 0.3, 0.4, 1]
}, index=[1, 2, 3, 4, 5])



@app.route('/')
def index():
    # Display the home page with form
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    user_input = request.form.get('movie_title').strip()  # Use strip() to remove any leading/trailing whitespace
    print(f"User Input Received: '{user_input}'")  # Debug print

    # Find the movie ID by matching the input title with the movies dataframe.
    matching_movies = movies[movies['title'].str.lower() == user_input.lower()]
    if matching_movies.empty:
        print(f"No matching movies found for title: '{user_input}'")  # Debug if no match is found
        return render_template('index.html', recommendations=None, error="Movie not found.", user_input=user_input)
    else:
        movie_id = matching_movies.index[0]
        print(f"Movie ID Found: {movie_id} for title: '{user_input}'")  # Debug print

    try:
        # Assuming movie_id is within the index range for the similarity matrix
        similar_scores = cosine_sim_df.loc[movie_id].sort_values(ascending=False)[1:6]  # Adjust the range as needed
        similar_movies = movies.loc[similar_scores.index]
        recommendations = similar_movies.to_dict('records')  # Converts DataFrame to a list of dicts
        return render_template('index.html', recommendations=recommendations, user_input=user_input)
    except KeyError as e:

        print(f"KeyError encountered for movie_id '{movie_id}': {e}")  # Debug print
        return render_template('index.html', recommendations=recommendations, user_input=user_input)

if __name__ == '__main__':
    app.run(debug=True)
