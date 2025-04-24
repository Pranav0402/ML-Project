import streamlit as st
import pickle
import pandas as pd
import requests

# Replace this with your own OMDb API key
OMDB_API_KEY = "e3a394f9"

def fetch_poster(movie_title):
    """Fetch movie poster using OMDb API"""
    url = f"http://www.omdbapi.com/?t={movie_title}&apikey={OMDB_API_KEY}"

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()

        if "Poster" in data and data["Poster"] != "N/A":
            return data["Poster"]
        else:
            return "https://via.placeholder.com/300x450?text=No+Image"
    except requests.exceptions.Timeout:
        return "https://via.placeholder.com/300x450?text=Timeout"
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching movie poster: {e}")
        return "https://via.placeholder.com/300x450?text=Error"

def recommend(movie):
    """Recommend movies based on similarity"""
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_title = movies.iloc[i[0]].title
        recommended_movies.append(movie_title)
        recommended_movies_posters.append(fetch_poster(movie_title))
    return recommended_movies, recommended_movies_posters

# Load movie data
movies_dict = pickle.load(open('movies.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

# Load similarity matrix
similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title('Movie Recommendation System')

selected_movie_name = st.selectbox(
    "Select a movie:",
    movies['title'].values
)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(names[0])
        st.image(posters[0])

    with col2:
        st.text(names[1])
        st.image(posters[1])

    with col3:
        st.text(names[2])
        st.image(posters[2])

    with col4:
        st.text(names[3])
        st.image(posters[3])

    with col5:
        st.text(names[4])
        st.image(posters[4])
