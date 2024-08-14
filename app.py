import streamlit as st
import pickle
import pandas as pd
import requests


def fetch_poster(movie_id):
    response = requests.get(
        f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=f126a83943682ed47125759cc45e56a2&language=en-US"
    )
    data = response.json()
    print(data)
    return "https://image.tmdb.org/t/p/w500/"+data['poster_path'], data


def recommend(movie):
    movie_index = movies[movies["title_x"] == movie].index[0]
    si = similarity[movie_index]
    # to not lose the connection of the movies with the others
    movie_list = sorted(list(enumerate(si)), reverse=True, key=lambda x: x[1])
    recommended_movies = []
    recommended_movies_poster = []
    recommended_movies_details = []
    for i in range(1, 6):
        movie_id = movies.iloc[movie_list[i][0]].id

        recommended_movies.append(movies["title_x"][movie_list[i][0]])
        poster, details = fetch_poster(movie_id)
        recommended_movies_poster.append(poster)
        recommended_movies_details.append(details)

    return recommended_movies, recommended_movies_poster, recommended_movies_details


movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

st.markdown("""
    <style>
        .title {
            color: #E50914; /* Netflix red */
            font-size: 3em;
            font-weight: bold;
            text-align: center;
            margin-bottom: 20px;
        }
        .stApp {
            background-color: #000000; /* Netflix black background */
            color: #FFFFFF; /* Text color for readability */
        }
        .stImage {
            border-radius: 8px;
            margin-bottom: 10px;
        }
        .stMarkdown h3 {
            font-size: 1.2em;
            color: #FFFFFF; /* White text for movie titles */
            margin-top: 5px;
            margin-bottom: 5px;
            text-align: center;
        }
        .stMarkdown p {
            font-size: 0.9em;
            color: #FFFFFF; /* White text for movie details */
            margin: 2px 0;
        }
        .stMarkdown p b {
            color: #E50914; /* Netflix red for emphasis */
        }
        .stButton button {
            background-color: #E50914; /* Netflix red for buttons */
            color: white;
            border: none;
            padding: 10px 20px;
            text-align: center;
            font-size: 1em;
            margin: 4px 2px;
            border-radius: 8px;
            transition-duration: 0.4s;
        }
        .stButton button:hover {
            background-color: #FFFFFF; /* White on hover */
            color: #E50914; /* Netflix red text on hover */
            border: 2px solid #E50914; /* Border color on hover */
        }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">Movie Recommender System</div>', unsafe_allow_html=True)


selectedMovie = st.selectbox('Enter the Movie Name',
                             movies['title_x'].values)

if st.button('Recommend'):
    recommended_movie_names, recommended_movie_posters, recommended_movie_details = recommend(selectedMovie)
    cols = st.columns(5)
    for idx, col in enumerate(cols):
        with col:
            st.image(recommended_movie_posters[idx], use_column_width=True)
            st.markdown(f"<h3>{recommended_movie_names[idx]}</h3>", unsafe_allow_html=True)
            st.markdown(f"<p><b>Release Date:</b> {recommended_movie_details[idx].get('release_date', 'N/A')}</p>",
                        unsafe_allow_html=True)
            st.markdown(f"<p><b>Rating:</b> {recommended_movie_details[idx].get('vote_average', 'N/A')}</p>",
                        unsafe_allow_html=True)

# Custom CSS to enhance the styling
