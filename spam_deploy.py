import streamlit as st
import pickle

# Use color and font themes
st.markdown("""
<style>
    body {
        background-color: #F0F0F0;
        font-family: Arial, sans-serif;
        color: #333;
    }
    
    h1, h2, h3 {
        color: #0071C5;
    }
    
    .btn {
        background-color: #0071C5;
        color: #FFF;
        padding: 10px 20px;
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

tfidf = pickle.load(open(r"C:/Users/KALYAN/Desktop/Projects/Projects/New folder\\feature.pkl", 'rb'))
model = pickle.load(open(r"C:/Users\KALYAN/Desktop/Projects/Projects/New folder\\model.pkl", 'rb'))

st.title("Spam Email Classifier........!")

input_mail = st.text_input("Enter the Message")

if st.button('Predict'):
    
    vector_input = tfidf.transform([input_mail])
    
    result = model.predict(vector_input)
    
    st.header("This is a " + ('Spam Mail' if result == 0 else 'Ham Mail'))

