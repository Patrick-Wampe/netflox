import requests
import json
import streamlit as st
import joblib
import pandas as pd
from sklearn.neighbors import NearestNeighbors
import streamlit_authenticator as stauth

def accueil():
    st.title("Bienvenue sur notre système de recommandation")
    st.image("https://cdn.dribbble.com/users/2351122/screenshots/14230040/comp_1_1.gif", caption="Netflix")

    df = pd.read_csv("dfPreprossFinal.csv")

    #st.dataframe(df)

    option = st.selectbox(
        "Quel film as-tu regardé ?",
        df.movie_name,
    )

    st.write("Ton choix :", option)

    st.image(json.loads(requests.get(f"https://www.omdbapi.com/?apikey=548c959e&t={option}").text)["Poster"])

    st.header("Les films que je te recommande de regarder son :")

    nbrs = NearestNeighbors(n_neighbors=6).fit(df.drop("movie_name", axis=1).values)

    #joblib.dump(nbrs, "recomodel.joblib")

    #nbrs = joblib.load("recomodel.joblib")

    ligne = df[df.movie_name == option].index[0]

    distances, indices = nbrs.kneighbors(df.drop("movie_name", axis=1).iloc[ligne, :].values.reshape(1, -1))

    listeRecommandations = df.movie_name.iloc[indices[0][1:]]

    for recommandation in listeRecommandations:
        col1, col2 = st.columns(2)
        with col1:
            try:
                #poster = requests.get(f"https://www.omdbapi.com/?apikey=548c959e&t={recommandation}").text.split('"Poster":\"')[1].split(".jpg")[0]+".jpg"
                poster = json.loads(requests.get(f"https://www.omdbapi.com/?apikey=548c959e&t={recommandation}").text)["Poster"]
                st.image(poster)
            except:
                st.image("https://www.indieactivity.com/wp-content/uploads/2022/03/File-Not-Found-Poster.png")
        with col2:
            st.subheader(f"{recommandation}", divider=True)


lesDonneesDesComptes = {'usernames': {'pjohn': {'name': 'jsmith',
    "first_name" : "Promise",
    "last_name" : "John",
   'password': '2003',
   'email': 'pJohn@gmail.com',
   'failed_login_attemps': 0, # Sera géré automatiquement
   'logged_in': False, # Sera géré automatiquement
   'role': 'utilisateur'},
  'fherry': {'name': 'fherry',
    "first_name" : "Fabien",
    "last_name" : "Herry",
   'password': '1234',
   'email': 'fherry@gmail.com',
   'failed_login_attemps': 0, # Sera géré automatiquement
   'logged_in': False, # Sera géré automatiquement
   'role': 'administrateur'}}}

authenticator = stauth.Authenticate(
    lesDonneesDesComptes,
    "cookie name",
    "cookie key",
    30
)

#def hashage(mdp):
#    return mdp.replace("a", "z").replace("2", "45")

#def dehashage(mdp):
#    return mdp.replace("z", "a").replace("45", "2")

authenticator.login()

if st.session_state['authentication_status']: # Si tout est bon
    authenticator.logout()
    st.write(f'Welcome *{st.session_state["name"]}*')
    accueil()

elif st.session_state['authentication_status'] is False:
    st.error('Username/password is incorrect')

elif st.session_state['authentication_status'] is None:
    st.warning("Merci d'indiquer votre username et mot de passe")

