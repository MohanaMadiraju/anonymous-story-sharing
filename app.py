import streamlit as st
import pandas as pd
import random
from datetime import datetime
import os

# --- Config ---
DATA_FILE = "stories.csv"
COMMENT_FILE = "comments.csv"
LIKE_FILE = "likes.csv"

# --- Generate Username ---
def generate_username():
    adjectives = ['Quiet', 'Happy', 'Bold', 'Gentle', 'Brave']
    nouns = ['Tiger', 'Sky', 'River', 'Leaf', 'Stone']
    return f"{random.choice(adjectives)}{random.choice(nouns)}{random.randint(100, 999)}"

# --- Init Session ---
if "username" not in st.session_state:
    st.session_state.username = generate_username()
    st.session_state.logged_in = True

# --- Styling ---
st.markdown("""
<style>
    .main {background-color: #f9f9f9;}
    .stTextArea textarea {font-size: 16px;}
    .story-box {padding: 20px; background: #fff; border-radius: 10px; box-shadow: 0 0 10px #ddd; margin-bottom: 20px;}
    .comment-box {margin-left: 20px; font-size: 15px; color: #555;}
</style>
""", unsafe_allow_html=True)

st.title("🕊️ Anonymous Story Sharing")

# --- Tabs ---
tab1, tab2 = st.tabs(["📝 Write a Story", "📖 Read Stories"])

# --- Story Writing ---
with tab1:
    st.subheader("Your thoughts, your space.")
    story = st.text_area("What's on your mind today?", height=300)
    if st.button("Submit Story"):
        if story.strip():
            story_id = 1
            if os.path.exists(DATA_FILE):
                existing = pd.read_csv(DATA_FILE)
                if not existing.empty:
                    story_id = existing["StoryID"].max() + 1
            new_story = pd.DataFrame([[story_id, st.session_state.username, story, datetime.now()]],
                                     columns=["StoryID", "Username", "Story", "Date"])
            new_story.to_csv(DATA_FILE, mode='a', header=not os.path.exists(DATA_FILE), index=False)
            st.success("Story shared anonymously!")
        else:
            st.warning("Please write something before submitting.")

# --- Story Feed ---
with tab2:
    st.subheader("✨ Latest Stories")

    if os.path.exists(DATA_FILE) and os.path.getsize(DATA_FILE) > 0:
        stories = pd.read_csv(DATA_FILE)
        if not stories.empty:
            comments_df = pd.read_csv(COMMENT_FILE) if os.path.exists(COMMENT_FILE) else pd.DataFrame(columns=["StoryID", "Username", "Comment", "Date"])
            likes_df = pd.read_csv(LIKE_FILE) if os.path.exists(LIKE_FILE) else pd.DataFrame(columns=["StoryID", "Likes"])

            for _, story in stories.sort_values(by='Date', ascending=False).iterrows():
                with st.container():
                    st.markdown(f"""<div class='story-box'>
                    <b>Anonymous:</b> {story['Username']}<br>
                    <i>🕰 {story['Date']}</i><br><br>
                    {story['Story']}
                    </div>""", unsafe_allow_html=True)

                    # --- Likes ---
                    story_id = story["StoryID"]
                    likes = int(likes_df[likes_df["StoryID"] == story_id]["Likes"].values[0]) if story_id in likes_df["StoryID"].values else 0
                    if st.button(f"👍 {likes} Like(s)", key=f"like_{story_id}"):
                        if story_id in likes_df["StoryID"].values:
                            likes_df.loc[likes_df["StoryID"] == story_id, "Likes"] += 1
                        else:
                            likes_df = pd.concat([likes_df, pd.DataFrame([[story_id, 1]], columns=["StoryID", "Likes"])])
                        likes_df.to_csv(LIKE_FILE, index=False)

                    # --- Comments ---
                    st.markdown("💬 **Comments:**", unsafe_allow_html=True)
                    story_comments = comments_df[comments_df["StoryID"] == story_id]
                    for _, c in story_comments.iterrows():
                        st.markdown(f"<div class='comment-box'>🗨️ {c['Username']}: {c['Comment']}</div>", unsafe_allow_html=True)

                    comment_text = st.text_input("Write a comment...", key=f"comment_input_{story_id}")
                    if st.button("Submit Comment", key=f"comment_btn_{story_id}"):
                        new_comment = pd.DataFrame([[story_id, st.session_state.username, comment_text, datetime.now()]],
                                                   columns=["StoryID", "Username", "Comment", "Date"])
                        new_comment.to_csv(COMMENT_FILE, mode='a', header=not os.path.exists(COMMENT_FILE), index=False)
                        st.experimental_rerun()

        else:
            st.info("No stories posted yet. Be the first!")
    else:
        st.info("No stories posted yet. Be the first!")

