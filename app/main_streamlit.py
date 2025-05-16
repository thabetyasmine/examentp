import streamlit as st
import requests

API_BASE_URL = "http://127.0.0.1:8000"

st.title("🎬 Movie Explorer")

# Initialiser la session
if 'movie' not in st.session_state:
    st.session_state.movie = None
if 'summary' not in st.session_state:
    st.session_state.summary = None

# Bouton pour afficher un film aléatoire
if st.button("🎲 Show Random Movie"):
    try:
        response = requests.get(f"{API_BASE_URL}/movies/random/")
        if response.status_code == 200:
            st.session_state.movie = response.json()
            st.session_state.summary = None  # Réinitialise le résumé
        else:
            st.error("No movie found or API error.")
    except Exception as e:
        st.error(f"Error: {e}")

# Afficher les détails du film
if st.session_state.movie:
    movie = st.session_state.movie
    st.header(f"{movie['title']} ({movie['year']})")
    st.write(f"🎬 Directed by: **{movie['director']}**")
    st.subheader("Actors:")
    for actor in movie['actors']:
        st.write(f"🎭 {actor['actor_name']}")

    # Bouton pour obtenir le résumé
    if st.button("🧠 Get Summary"):
        try:
            payload = {"movie_id": movie['id']}
            response = requests.post(f"{API_BASE_URL}/generate_summary/", json=payload)
            if response.status_code == 200:
                st.session_state.summary = response.json()['summary_text']
            else:
                st.error("Failed to generate summary.")
        except Exception as e:
            st.error(f"Error: {e}")

# Afficher le résumé
if st.session_state.summary:
    st.subheader("📃 Summary")
    st.info(st.session_state.summary)
import streamlit as st
import requests

API_BASE_URL = "http://127.0.0.1:8000"

st.title("🎬 Movie Explorer")

# Initialiser la session
if 'movie' not in st.session_state:
    st.session_state.movie = None
if 'summary' not in st.session_state:
    st.session_state.summary = None

# Bouton pour afficher un film aléatoire
if st.button("🎲 Show Random Movie"):
    try:
        response = requests.get(f"{API_BASE_URL}/movies/random/")
        if response.status_code == 200:
            st.session_state.movie = response.json()
            st.session_state.summary = None  # Réinitialise le résumé
        else:
            st.error("No movie found or API error.")
    except Exception as e:
        st.error(f"Error: {e}")

# Afficher les détails du film
if st.session_state.movie:
    movie = st.session_state.movie
    st.header(f"{movie['title']} ({movie['year']})")
    st.write(f"🎬 Directed by: **{movie['director']}**")
    st.subheader("Actors:")
    for actor in movie['actors']:
        st.write(f"🎭 {actor['actor_name']}")

    # Bouton pour obtenir le résumé
    if st.button("🧠 Get Summary"):
        try:
            payload = {"movie_id": movie['id']}
            response = requests.post(f"{API_BASE_URL}/generate_summary/", json=payload)
            if response.status_code == 200:
                st.session_state.summary = response.json()['summary_text']
            else:
                st.error("Failed to generate summary.")
        except Exception as e:
            st.error(f"Error: {e}")

# Afficher le résumé
if st.session_state.summary:
    st.subheader("📃 Summary")
    st.info(st.session_state.summary)
