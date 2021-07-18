import streamlit as st
import pickle
import pandas as pd
import requests


movies_dict = pickle.load(open('model/movie_dict.pkl','rb'))
similarity = pickle.load(open('model/similarity.pkl','rb'))
movies = pd.DataFrame(movies_dict)

st.title("Movie recommandation system")

movie_list = movies['title'].values
movie_name = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)


def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommand(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)) , reverse=True , key= lambda x : x[1])[0:7]
    
    recommanded_movies = []
    recommanded_movies_poster = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].id
        # fetch poster from API
        recommanded_movies_poster.append(fetch_poster(movie_id))
        # fetch movie title
        recommanded_movies.append(movies.iloc[i[0]].title)
    
    return recommanded_movies,recommanded_movies_poster
    

if st.button("Recommand"):
    names , posters = recommand(movie_name)
    col1, col2, col3, col4, col5, col6 = st.beta_columns(6)
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
    with col6:
        st.text(names[5])
        st.image(posters[5])
        
        
        