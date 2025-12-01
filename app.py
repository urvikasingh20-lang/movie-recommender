import streamlit as st
import pandas as pd
import pickle
st.title("Movie Recommendation System")

df=pickle.load(open("mydata.pkl", "rb"))
option = st.selectbox(
    "MOVIE YOU WANT?",
    df.title,
    index=None,
    placeholder="Select contact method...",
)
similarity=pickle.load(open("similarity.pkl", "rb"))

import requests

API_KEY = st.secrets["TMDB_API_KEY"]


def fetch_poster(movie_id):
    # Call TMDB search API
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}"
    data = requests.get(url).json()

    if 'poster_path' in data and data['poster_path']:
        poster_path = data['poster_path']
        poster_url = "https://image.tmdb.org/t/p/w500" + poster_path
        return poster_url
    else:
        return "https://via.placeholder.com/500x750?text=No+Image"


def recommend(movie):
    movie_index=df[df["title"]==movie].index[0]
    distances=similarity[movie_index]
    movies_list=sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]
    recommended_movie_posters=[]
    recommended=[]
        #fetch poster from api
    for i in movies_list:
        movie_id=df.iloc[i[0]].movie_id
        recommended.append(df.iloc[i[0]].title)
        recommended_movie_posters.append(fetch_poster(movie_id))
    return recommended, recommended_movie_posters

if st.button("ReCOMMEND", type="secondary"):
    names,posters=recommend(option) # the function which will fetch the predicted movies

    cols = st.columns(5)

    for col, name, poster in zip(cols, names, posters):
        with col:
            st.text(name)
            st.image(poster)