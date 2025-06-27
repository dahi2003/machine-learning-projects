
import streamlit as st
import pickle
import pandas as pd
import requests


# Function to fetch poster from TMDB API
def fetch_poster(movie_id):
    api_key = "fa985af5b516df23a0eed508887d0ee8"  # Replace with your actual TMDB API key
    response = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=fa985af5b516df23a0eed508887d0ee8&language=en-US")
    data = response.json()
    poster_path = data.get('poster_path')  # Returns None if not found
    if poster_path:
        return f"https://image.tmdb.org/t/p/w185/{poster_path}"
    return "https://via.placeholder.com/185x278?text=No+Image"  # Placeholder if no image is available


# Function to recommend movies
def recommend(movie):
    if movie not in movies['title'].values:
        st.error("Movie not found in dataset. Try another title.")
        return [], []

    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_posters = []
    for i in movie_list:
        movie_title = movies.iloc[i[0]].title
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movie_title)
        recommended_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_posters


# Load data
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Streamlit UI
st.title('Movie Recommender System')

selected_movie_name = st.selectbox('Select a movie:', movies['title'].values)

if st.button('Recommend Movies'):
    names, posters = recommend(selected_movie_name)

    if names:
        cols = st.columns(5)  # Creates 5 columns for displaying movies
        for col, name, poster in zip(cols, names, posters):
            with col:
                st.image(poster, caption=name, use_container_width=True)