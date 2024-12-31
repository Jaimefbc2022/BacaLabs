import streamlit as st

#git init
#git add .
#git commit -am "initial commit"
#git remote add origin https://github.com/Jaimefbc2022/BacaLabs.git
# git push origin master

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)



st.write("# Welcome to Baca Labs! 👋")

st.sidebar.success("Select a demo above.")

st.markdown(
    """
    Here, you'll find a collection of simple yet useful apps designed to make life a little easier.
    """
)

st.markdown(
    """
    My goal is to share tools that I’ve created and believe can help others—whether it’s solving a problem, saving time, or just simplifying a task.
    
    """
)

st.markdown(
    """
    To kick things off, I’ve built a Tax Calculator tailored for Spain and the UK, helping you quickly estimate taxes with ease. But this is just the beginning! I’ll be adding more handy apps over time, so stay tuned for updates.
    """
)
st.markdown(
    """
    Feel free to explore, try them out, and share your feedback. Let’s make this a place where practical ideas come to life! 😊
    
    """
)

