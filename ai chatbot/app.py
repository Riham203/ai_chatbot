import streamlit as st
st.set_page_config(
    page_title="Streamlit demo"
)
st.header("Streamlit application")
input=st.text_input("Input",key="input")
submit=st.button("Ask a question")
if submit and input:
    st.write("Your answer comes here")