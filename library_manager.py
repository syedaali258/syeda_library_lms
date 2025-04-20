
import streamlit as st
import pandas as pd
import json
import os
import datetime
import time
import random
import plotly.express as px
import plotly.graph_objects as go
from streamlit_lottie import st_lottie
import requests

# Page Configuration
st.set_page_config(
    page_title="Personal Library Management",
    page_icon="🕮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS Styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem !important;
        color:#1E3A8A;
        font-weight:700;
        text-align: center;
    }
    .sub-header {
        font-size:1.8rem !important;
        color:#3B82F6;
        font-weight: 600;
        margin-top: 1rem;
        margin-bottom: 1rem;
    }
    .success-message {
        padding: 1rem;
        background-color: #FEF3C7;
        border-left: 5px solid #F59E0B;
        border-radius: 0.375rem;
    }
    .book-card {
        background-color: #F3F4F6;
        border-radius: 0.5rem;
        padding: 1rem;
        margin-bottom: 1rem;
        border-left: 5px solid #3B82F6;
    }
    .read-badge {
        background-color: #10B981;
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 1rem;
        font-size: 0.875rem;
        font-weight: 600;
    }
    .unread-badge {
        background-color: #F87171;
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 1rem;
        font-size: 0.875rem;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# Load Lottie animation
def load_lottieurl(url):
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None

# Session States
if 'library' not in st.session_state:
    st.session_state.library = []
if 'search_results' not in st.session_state:
    st.session_state.search_results = []
if 'book_added' not in st.session_state:
    st.session_state.book_added = False
if 'book_removed' not in st.session_state:
    st.session_state.book_removed = False
if 'current_view' not in st.session_state:
    st.session_state.current_view = "library"

# Load Library from File
def load_library():
    if os.path.exists('library.json'):
        with open('library.json', 'r') as file:
            st.session_state.library = json.load(file)

# Save Library to File
import os

def load_library():
    if os.path.exists("library.json"):
        with open("library.json", "r") as file:
            try:
                st.session_state.library = json.load(file)
            except json.JSONDecodeError:
                st.session_state.library = []  
    else:
        st.session_state.library = []  

# Add Book
def add_book(title, author, publication_year, genre, read_status):
    book = {
        'title': title,
        'author': author,
        'publication_year': publication_year,
        'genre': genre,
        'read_status': read_status,
        'added_date': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    st.session_state.library.append(book)
    save_library()
    st.session_state.book_added = True
    time.sleep(0.5)

# Remove Book
def remove_book(index):
    if 0 <= index < len(st.session_state.library):
        del st.session_state.library[index]
        save_library()
        st.session_state.book_removed = True
        return True
    return False

# Search Books
def search_books(search_term, search_by):
    search_term = search_term.lower()
    results = []
    for book in st.session_state.library:
        if search_by == "Title" and search_term in book['title'].lower():
            results.append(book)
        elif search_by == "Author" and search_term in book['author'].lower():
            results.append(book)
        elif search_by == "Genre" and search_term in book['genre'].lower():
            results.append(book)
    st.session_state.search_results = results

# Library Stats
def get_library_stats():
    total_books = len(st.session_state.library)
    read_books = sum(1 for book in st.session_state.library if book['read_status'])
    percent_read = (read_books / total_books * 100) if total_books > 0 else 0

    genres = {}
    authors = {}
    decades = {}

    for book in st.session_state.library:
        genre = book['genre']
        author = book['author']
        decade = (book['publication_year'] // 10) * 10

        genres[genre] = genres.get(genre, 0) + 1
        authors[author] = authors.get(author, 0) + 1
        decades[decade] = decades.get(decade, 0) + 1

    return {
        'total_books': total_books,
        'read_books': read_books,
        'percent_read': percent_read,
        'genres': dict(sorted(genres.items(), key=lambda x: x[1], reverse=True)),
        'authors': dict(sorted(authors.items(), key=lambda x: x[1], reverse=True)),
        'decades': dict(sorted(decades.items(), key=lambda x: x[0]))
    }

# Create Visualizations
def create_visualizations(stats):
    if stats['total_books'] > 0:
        fig_read_status = go.Figure(data=[go.Pie(
            labels=['Read', 'Unread'],
            values=[stats['read_books'], stats['total_books'] - stats['read_books']],
            hole=0.4,
            marker_colors=['#10B981', '#F87171']
        )])
        fig_read_status.update_layout(title="Read vs Unread Books", height=400)
        st.plotly_chart(fig_read_status, use_container_width=True)

    if stats['genres']:
        df_genres = pd.DataFrame({
            'Genre': list(stats['genres'].keys()),
            'Count': list(stats['genres'].values())
        })
        fig_genres = px.bar(df_genres, x='Genre', y='Count', color='Count', color_continuous_scale='Blues')
        fig_genres.update_layout(title='Books by Genre', height=400)
        st.plotly_chart(fig_genres, use_container_width=True)

    if stats['decades']:
        df_decades = pd.DataFrame({
            'Decade': [f"{k}s" for k in stats['decades'].keys()],
            'Count': list(stats['decades'].values())
        })
        fig_decades = px.line(df_decades, x='Decade', y='Count', markers=True)
        fig_decades.update_layout(title='Books by Publication Decade', height=400)
        st.plotly_chart(fig_decades, use_container_width=True)

# Sidebar & Main Logic
load_library()
lottie_book = load_lottieurl("https://assets9.lottiefiles.com/temp/1f20_akAfIn.json")

st.sidebar.markdown("<h1 style='text-align: center;'>Navigation</h1>", unsafe_allow_html=True)
if lottie_book:
    st.sidebar_lottie = st_lottie(lottie_book, height=200)

nav_options = st.sidebar.radio("Choose an option:", ["View Library", "Add Book", "Search Books", "Library Statistics"])

st.session_state.current_view = nav_options.lower().replace(" ", "_")

st.markdown("<h1 class='main-header'>Personal Library Manager</h1>", unsafe_allow_html=True)

# View: Add Book
if st.session_state.current_view == "add_book":
    st.markdown("<h2 class='sub-header'>Add a New Book</h2>", unsafe_allow_html=True)
    with st.form("add_form_book"):
        col1, col2 = st.columns(2)
        with col1:
            title = st.text_input("Book Title", max_chars=100)
            author = st.text_input("Author", max_chars=100)
            publication_year = st.number_input("Publication Year", min_value=1000, max_value=datetime.datetime.now().year, step=1, value=2023)
        with col2:
            genre = st.selectbox("Genre", ["Fiction", "Non-Fiction", "Science", "Technology", "Romance", "Poetry", "Self-Help", "Art", "Religion", "History", "Other"])
            read_status = st.radio("Read Status", ["Read", "Unread"], horizontal=True)
        submit = st.form_submit_button("Add Book")
        if submit and title and author:
            add_book(title, author, publication_year, genre, read_status == "Read")

    if st.session_state.book_added:
        st.markdown("<div class='success-message'>Book added successfully!</div>", unsafe_allow_html=True)
        st.balloons()
        st.session_state.book_added = False

# View: Library
elif st.session_state.current_view == "view_library":
    st.markdown("<h2 class='sub-header'>Your Library</h2>", unsafe_allow_html=True)
    if not st.session_state.library:
        st.warning("Your library is empty. Add some books to get started!")
    else:
        for i, book in enumerate(st.session_state.library):
            st.markdown(f"""
                <div class='book-card'>
                    <h3>{book['title']}</h3>
                    <p><strong>Author:</strong> {book['author']}</p>
                    <p><strong>Year:</strong> {book['publication_year']}</p>
                    <p><strong>Genre:</strong> {book['genre']}</p>
                    <p><span class='{ 'read-badge' if book['read_status'] else 'unread-badge' }'>
                    {"Read" if book['read_status'] else "Unread"}</span></p>
                </div>
            """, unsafe_allow_html=True)
            col1, col2 = st.columns([1, 1])
            with col1:
                if st.button("Remove", key=f"remove_{i}"):
                    if remove_book(i):
                        st.rerun()
            with col2:
                toggle_label = "Mark as Unread" if book['read_status'] else "Mark as Read"
                if st.button(toggle_label, key=f"toggle_{i}"):
                    st.session_state.library[i]['read_status'] = not book['read_status']
                    save_library()
                    st.rerun()

# View: Search Books
elif st.session_state.current_view == "search_books":
    st.markdown("<h2 class='sub-header'>Search Books</h2>", unsafe_allow_html=True)
    search_by = st.selectbox("Search by:", ["Title", "Author", "Genre"])
    search_term = st.text_input("Enter search term:")
    if st.button("Search"):
        if search_term:
            with st.spinner("Searching..."):
                time.sleep(0.5)
                search_books(search_term, search_by)

    if st.session_state.search_results:
        st.success(f"Found {len(st.session_state.search_results)} matching book(s).")
        for book in st.session_state.search_results:
            st.markdown(f"""
                <div class='book-card'>
                    <h3>{book['title']}</h3>
                    <p><strong>Author:</strong> {book['author']}</p>
                    <p><strong>Year:</strong> {book['publication_year']}</p>
                    <p><strong>Genre:</strong> {book['genre']}</p>
                    <p><span class='{ 'read-badge' if book['read_status'] else 'unread-badge' }'>
                    {"Read" if book['read_status'] else "Unread"}</span></p>
                </div>
            """, unsafe_allow_html=True)
    elif search_term:
        st.warning("No books found matching your search.")

# View: Statistics
elif st.session_state.current_view == "library_statistics":
    st.markdown("<h2 class='sub-header'>Library Statistics</h2>", unsafe_allow_html=True)
    if not st.session_state.library:
        st.warning("Your library is empty. Add some books to see stats.")
    else:
        stats = get_library_stats()
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Books", stats['total_books'])
        with col2:
            st.metric("Books Read", stats['read_books'])
        with col3:
            st.metric("Percentage Read", f"{stats['percent_read']:.1f}%")

        create_visualizations(stats)

        if stats['authors']:
            st.markdown("### Top Authors")
            top_authors = dict(list(stats['authors'].items())[:5])
            for author, count in top_authors.items():
                st.markdown(f"**{author}**: {count} book{'s' if count > 1 else ''}")

st.markdown("---")
st.markdown("© 2025 SYEDA BUSHRA ALI — Personal Library Manager", unsafe_allow_html=True)
