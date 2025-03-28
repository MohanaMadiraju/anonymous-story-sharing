import streamlit as st
import pandas as pd
import random
from datetime import datetime

# Generate Random Anonymous Username
def generate_username():
    adjectives = ['Quiet', 'Happy', 'Bold', 'Gentle', 'Brave']
    nouns = ['Tiger', 'Sky', 'River', 'Leaf', 'Stone']
    return f"{random.choice(adjectives)}{random.choice(nouns)}{random.randint(100, 999)}"

# Initialize Session State
if "username" not in st.session_state:
    st.session_state.username = None
    st.session_state.logged_in = False

# Data Storage using CSV
DATA_FILE = "stories.csv"
if not st.session_state.logged_in and not st.session_state.username:
    if not st.button("Generate Your Anonymous Username"):
        st.stop()
    st.session_state.username = generate_username()
    st.success(f"Welcome! Your anonymous username is **{st.session_state.username}**")
    st.session_state.logged_in = True

# Tabs for Navigation
tab1, tab2 = st.tabs(["Write a Story", "Read Stories"])

# Story Submission Tab
with tab1:
    st.subheader("Share Your Story Anonymously")
    story = st.text_area("What's on your mind today?", height=300)

    if st.button("Submit Story"):
        if not story.strip():
            st.warning("Please write something before submitting.")
        else:
            # Save Story to CSV
            data = pd.DataFrame([[st.session_state.username, story, datetime.now()]], columns=["Username", "Story", "Date"])
            data.to_csv(DATA_FILE, mode='a', header=not pd.io.common.file_exists(DATA_FILE), index=False)
            st.success("Your story has been shared anonymously!")

# Story Feed Tab
with tab2:
    st.subheader("Read Anonymous Stories")
    if pd.io.common.file_exists(DATA_FILE):
        stories = pd.read_csv(DATA_FILE)
        for _, row in stories.iterrows():
            st.write(f"📝 **{row['Username']}** | 🕰 {row['Date']}")
            st.write(f"> {row['Story']}")
            st.markdown("---")
    else:
        st.info("No stories yet. Be the first to share your thoughts.")
