import streamlit as st
import requests
import pandas as pd
from datetime import datetime

API_BASE_URL = "http://127.0.0.1:5000"

st.set_page_config(page_title="Thumbnail Board", layout="wide", initial_sidebar_state="expanded")
st.title("🎬 YouTube Thumbnail Board")

# Initialize session state
if 'refresh' not in st.session_state:
    st.session_state.refresh = False

# Sidebar for board selection
st.sidebar.header("📌 Boards")

try:
    # Get all boards
    response = requests.get(f"{API_BASE_URL}/boards", timeout=5)
    boards = response.json() if response.status_code == 200 else []
except:
    boards = []
    st.sidebar.error("Cannot connect to backend. Start Flask app first.")

# Create new board
with st.sidebar.form("new_board"):
    board_name = st.text_input("Board Name")
    if st.form_submit_button("➕ Create Board"):
        if board_name.strip():
            try:
                requests.post(f"{API_BASE_URL}/boards", json={"name": board_name}, timeout=5)
                st.session_state.refresh = True
                st.rerun()
            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.warning("Enter a board name")

# Select board
if boards:
    board_ids = {b['name']: b['id'] for b in boards}
    selected_board_name = st.sidebar.selectbox("Select Board", list(board_ids.keys()))
    board_id = board_ids[selected_board_name]
    
    # Main content area
    st.header(f"📋 {selected_board_name}")
    
    # Add thumbnail form
    with st.form("add_thumbnail"):
        col1, col2 = st.columns(2)
        with col1:
            url = st.text_input("YouTube URL", placeholder="https://www.youtube.com/watch?v=...")
            title = st.text_input("Title", placeholder="Enter thumbnail title")
            channel = st.text_input("Channel", placeholder="Enter channel name")
        with col2:
            category = st.selectbox("Category", ["Gaming", "Tech", "Music", "Education", "Entertainment", "Other"])
            score = st.slider("Score", 0, 100, 50)
            views = st.text_input("Views", placeholder="1.2M", value="—")
        
        if st.form_submit_button("✅ Add Thumbnail"):
            if url.strip() and title.strip():
                try:
                    response = requests.post(
                        f"{API_BASE_URL}/boards/{board_id}/thumbnails",
                        json={
                            "url": url,
                            "title": title,
                            "channel": channel,
                            "category": category,
                            "score": score,
                            "views": views
                        },
                        timeout=5
                    )
                    if response.status_code == 200:
                        st.success("✅ Thumbnail added!")
                        st.rerun()
                    else:
                        st.error(response.json().get("error", "Error adding thumbnail"))
                except Exception as e:
                    st.error(f"Error: {e}")
            else:
                st.warning("URL and Title are required")
    
    # Display thumbnails
    try:
        response = requests.get(f"{API_BASE_URL}/boards/{board_id}/thumbnails", timeout=5)
        thumbnails = response.json() if response.status_code == 200 else []
    except:
        thumbnails = []
    
    if thumbnails:
        st.subheader(f"📸 Thumbnails ({len(thumbnails)})")
        
        # Filter options
        col1, col2, col3 = st.columns(3)
        with col1:
            filter_category = st.multiselect("Filter by Category", 
                                            options=list(set([t['category'] for t in thumbnails])),
                                            default=None)
        with col2:
            sort_by = st.selectbox("Sort by", ["Score (High to Low)", "Score (Low to High)", "Recently Added"])
        with col3:
            min_score = st.slider("Min Score", 0, 100, 0)
        
        # Apply filters
        filtered_thumbs = thumbnails
        if filter_category:
            filtered_thumbs = [t for t in filtered_thumbs if t['category'] in filter_category]
        filtered_thumbs = [t for t in filtered_thumbs if t['score'] >= min_score]
        
        # Sort
        if sort_by == "Score (High to Low)":
            filtered_thumbs = sorted(filtered_thumbs, key=lambda x: x['score'], reverse=True)
        elif sort_by == "Score (Low to High)":
            filtered_thumbs = sorted(filtered_thumbs, key=lambda x: x['score'])
        else:
            filtered_thumbs = sorted(filtered_thumbs, key=lambda x: x['addedAt'], reverse=True)
        
        # Display in grid
        cols = st.columns(4)
        for idx, thumb in enumerate(filtered_thumbs):
            with cols[idx % 4]:
                st.image(thumb['imageUrl'], use_container_width=True)
                st.write(f"**{thumb['title']}**")
                st.caption(f"📺 {thumb['channel']}")
                col_a, col_b, col_c = st.columns(3)
                with col_a:
                    st.metric("Score", thumb['score'])
                with col_b:
                    st.metric("Views", thumb['views'])
                with col_c:
                    st.metric("Category", thumb['category'])
                if thumb['notes']:
                    st.info(f"📝 {thumb['notes']}")
    else:
        st.info("📭 No thumbnails in this board yet. Add one above!")

else:
    st.info("👈 Create a board to get started!")
