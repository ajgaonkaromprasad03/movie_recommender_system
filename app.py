import streamlit as st
import pickle
import pandas as pd
import requests
movies_dict = pickle.load(open('movie_dict.pkl','rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl','rb'))

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?language=en-US"
    headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJkYWYwODIyMzhhMmYxMDJlNGRjYzA2MjA2ZTg5YWIzMyIsIm5iZiI6MTc0Nzc3MDU3Ny4xOTYsInN1YiI6IjY4MmNkY2QxYTc4OGY3OGQ4ODY0OTNkOSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.CuyqpU2MsCwn6kg5bK05uG8lAl9UZmxkCB2NS-7SKno"
    }
    response = requests.get(url, headers=headers)
    data = response.json()
    return  "https://image.tmdb.org/t/p/w500/" + data['poster_path']
fetch_poster(20)

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)),reverse =True, key = lambda x:x[1])[1:6]

    recommended_movies = []
    recommended_poster = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_poster.append(fetch_poster(movie_id))
    return recommended_movies,recommended_poster

st.title('Movie Recommender System')
selected_movie_name = st.selectbox(
    'type below for recommendation', movies['title'].values)

if st.button('Recommended'):
    names, posters = recommend(selected_movie_name)

    col1, col2, col3,col4,col5 = st.columns(5)
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






