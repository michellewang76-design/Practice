import streamlit as st


st.set_page_config(
    page_title="贝儿和可儿",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': "https://aznconnect.com.au/",
        'Report a bug': "https://aznconnect.com.au/",
        'About': "# Cutest Babies Ever!"
    }
)

st.title("Michelle")
st.header("Florence")
st.subheader("Scarlett")

st.write("I love you for the sea.")
st.write("I love you to the moon.")

st.image("../Resources/Florence.jpg", width=500)
st.image("../Resources/Scarlett.jpg", width=500)

st.video("../Resources/Scarlett&Dad.mp4",width=500)

# st.audio("")