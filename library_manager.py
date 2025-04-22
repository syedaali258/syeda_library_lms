import streamlit as st
from datetime import datetime

# Initialize session state
if "books" not in st.session_state:
    st.session_state.books = []

if "current_view" not in st.session_state:
    st.session_state.current_view = "home"

# Page Config
st.set_page_config(page_title="📚 Personal Library", layout="wide")

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        color: #4B8BBE;
        font-size: 42px;
        text-align: center;
        padding: 20px;
    }
    .sub-header {
        color: #306998;
        font-size: 28px;
        padding: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar navigation
st.sidebar.title("📚 Library Navigation")
nav_option = st.sidebar.radio("Go to", ["🏠 Home", "➕ Add Book", "📖 View Library", "🔍 Search Book", "📊 Library Stats"])

# Set current view
if nav_option == "🏠 Home":
    st.session_state.current_view = "home"
elif nav_option == "➕ Add Book":
    st.session_state.current_view = "add"
elif nav_option == "📖 View Library":
    st.session_state.current_view = "view"
elif nav_option == "🔍 Search Book":
    st.session_state.current_view = "search"
elif nav_option == "📊 Library Stats":
    st.session_state.current_view = "stats"

# Home view with animation
if st.session_state.current_view == "home":
    st.markdown("<h1 class='main-header'>📚 Welcome to Your Personal Library</h1>", unsafe_allow_html=True)
    st.image("https://media.giphy.com/media/3oEduSbSGpGaRX2Vri/giphy.gif", caption="Read More, Learn More!", use_column_width=True)

# Add Book
elif st.session_state.current_view == "add":
    st.markdown("<h2 class='sub-header'>➕ Add a New Book</h2>", unsafe_allow_html=True)

    with st.form("add_book_form"):
        title = st.text_input("Title")
        author = st.text_input("Author")
        genre = st.selectbox("Genre", ["Fiction", "Non-Fiction", "Science", "History", "Biography", "Other"])
        year = st.number_input("Publication Year", min_value=1000, max_value=datetime.now().year, step=1, value=2023)
        read = st.checkbox("Mark as Read")
        submitted = st.form_submit_button("Add Book")

        if submitted:
            new_book = {
                "title": title,
                "author": author,
                "genre": genre,
                "year": year,
                "read": read
            }
            st.session_state.books.append(new_book)
            st.success("✅ Book added successfully!")

# View Library
elif st.session_state.current_view == "view":
    st.markdown("<h2 class='sub-header'>📖 Your Library</h2>", unsafe_allow_html=True)

    if st.session_state.books:
        for book in st.session_state.books:
            st.markdown(f"""
                **📘 Title:** {book['title']}  
                **✍️ Author:** {book['author']}  
                **📚 Genre:** {book['genre']}  
                **📅 Year:** {book['year']}  
                **✅ Read:** {"Yes" if book['read'] else "No"}
                ---
            """)
    else:
        st.info("No books in your library. Add some from the 'Add Book' section.")

# Search Book
elif st.session_state.current_view == "search":
    st.markdown("<h2 class='sub-header'>🔍 Search Books</h2>", unsafe_allow_html=True)
    query = st.text_input("Search by Title or Author")

    if query:
        results = [
            book for book in st.session_state.books
            if query.lower() in book['title'].lower() or query.lower() in book['author'].lower()
        ]

        if results:
            for book in results:
                st.markdown(f"""
                    **📘 Title:** {book['title']}  
                    **✍️ Author:** {book['author']}  
                    **📚 Genre:** {book['genre']}  
                    **📅 Year:** {book['year']}  
                    **✅ Read:** {"Yes" if book['read'] else "No"}
                    ---
                """)
        else:
            st.warning("No matching books found.")

# Library Stats
elif st.session_state.current_view == "stats":
    st.markdown("<h2 class='sub-header'>📊 Library Statistics</h2>", unsafe_allow_html=True)

    books = st.session_state.books
    total_books = len(books)
    read_books = len([book for book in books if book['read']])
    unread_books = total_books - read_books

    st.metric("📚 Total Books", total_books)
    st.metric("✅ Books Read", read_books)
    st.metric("📕 Unread Books", unread_books)

    # Genre Distribution
    genre_data = {}
    for book in books:
        genre = book['genre']
        genre_data[genre] = genre_data.get(genre, 0) + 1

    if genre_data:
        st.subheader("📊 Books by Genre")
        st.bar_chart(genre_data)
    else:
        st.info("No books added to show statistics.")
