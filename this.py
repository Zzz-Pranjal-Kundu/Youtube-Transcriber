import streamlit as st
import pickle
import pandas as pd
import requests # to hit APIs

movie_dict=pickle.load(open('movie_dict.pkl','rb'))
movies=pd.DataFrame(movie_dict)
similarity=pickle.load(open('similarity.pkl','rb'))


def fetch_poster(movie_id):
    response = requests.get("https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

st.title("MOVIE RECOMMENDER SYSTEM")
selected_movie_name = st.selectbox( "Select a movie: ", movies['title'].values )


#Takes a movie name as an input and returns 5 similar movie names
def recommend(movie):
    movie_idx = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_idx]
    mapping = list(enumerate(distances))  # mapping each movie score to its respective index
    entire_movie_list = sorted(mapping, reverse=True, key=lambda x: x[1])  # key=... to sort acc to the movie similarity rather than
    movies_list = entire_movie_list[1:6]

    recommended_movies=[]
    recommended_movies_posters=[]
    for i in movies_list:
        movie_id=movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        # fetching movie poster from API
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies,recommended_movies_posters


def fetch_movie_details(movie_id):
    response = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US")
    data = response.json()
    details = {
        'title': data['title'],
        'overview': data['overview'],
        'release_date': data['release_date'],
        'rating': data['vote_average'],
        'genres': ', '.join([genre['name'] for genre in data['genres']]),
        'poster_url': "https://image.tmdb.org/t/p/w500/" + data['poster_path']
    }
    return details


if st.button('Recommend'):
    names,posters = recommend(selected_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.markdown(f"<h5 style='text-align: center; font-size:14px;'>{names[0]}</h5>", unsafe_allow_html=True)
        st.image(posters[0])
    with col2:
        st.markdown(f"<h5 style='text-align: center; font-size:14px;'>{names[1]}</h5>", unsafe_allow_html=True)
        st.image(posters[1])
    with col3:
        st.markdown(f"<h5 style='text-align: center; font-size:14px;'>{names[2]}</h5>", unsafe_allow_html=True)
        st.image(posters[2])
    with col4:
        st.markdown(f"<h5 style='text-align: center; font-size:14px;'>{names[3]}</h5>", unsafe_allow_html=True)
        st.image(posters[3])
    with col5:
        st.markdown(f"<h5 style='text-align: center; font-size:14px;'>{names[4]}</h5>", unsafe_allow_html=True)
        st.image(posters[4])

