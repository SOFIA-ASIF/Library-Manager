import streamlit as st
import json
import os

# File to store the library data
LIBRARY_FILE = 'library.txt'

# Load library from file
def load_library():
    try:
        with open(LIBRARY_FILE, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

# Save library to file
def save_library(library):
    with open(LIBRARY_FILE, 'w') as file:
        json.dump(library, file, indent=4)

# Add a book
def add_book():
    st.markdown("### ➕ Add a New Book")
    with st.form("add_book_form"):
        col1, col2 = st.columns(2)
        with col1:
            title = st.text_input("📖 Title")
            author = st.text_input("✍️ Author")
        with col2:
            year = st.number_input("📅 Year", min_value=0, max_value=3000, step=1)
            genre = st.text_input("🏷️ Genre")
        read_status = st.radio("📚 Have you read this book?", ["Yes", "No"]) == "Yes"
        submitted = st.form_submit_button("Add Book ✅")
        if submitted:
            library = load_library()
            library.append({
                'title': title,
                'author': author,
                'year': year,
                'genre': genre,
                'read': read_status
            })
            save_library(library)
            st.success(f"✅ '{title}' added successfully!")

# Remove a book
def remove_book():
    st.markdown("### 🗑️ Remove a Book")
    library = load_library()
    titles = [book['title'] for book in library]
    if titles:
        book_to_remove = st.selectbox("Select a book to remove 👇", titles)
        if st.button("Remove Book ❌"):
            library = [book for book in library if book['title'] != book_to_remove]
            save_library(library)
            st.success(f"🗑️ '{book_to_remove}' removed successfully!")
    else:
        st.info("📭 No books to remove.")

# Search books
def search_books():
    st.markdown("### 🔍 Search Books")
    library = load_library()
    query = st.text_input("Search by Title or Author:")
    if query:
        matches = [
            book for book in library
            if query.lower() in book['title'].lower() or query.lower() in book['author'].lower()
        ]
        if matches:
            for book in matches:
                st.markdown(f"""
                **📖 {book['title']}**  
                _✍️ {book['author']} | 📅 {book['year']} | 🏷️ {book['genre']} | {'✅ Read' if book['read'] else '📖 Unread'}_
                """)
        else:
            st.warning("🚫 No matching books found.")

#Display Books
def display_books():
    st.subheader("All Books in Library")
    library = load_library()
    if not library:
        st.info("Library is empty.")
    else:
        for book in library:
            st.write(f"📘 {book['title']} by {book['author']} ({book['year']}) - {book['genre']} - {'✅ Read' if book['read'] else '📖 Unread'}")

# Display statistics
def display_statistics():
    st.markdown("### 📊 Your Reading Stats")
    library = load_library()
    total_books = len(library)
    read_books = sum(1 for book in library if book['read'])
    unread_books = total_books - read_books
    percentage_read = (read_books / total_books * 100) if total_books > 0 else 0

    col1, col2 = st.columns(2)
    col1.metric("📚 Total Books", total_books)
    col2.metric("✅ Books Read", read_books)

    st.progress(int(percentage_read), text=f"📈 {percentage_read:.2f}% of books read")
    if unread_books > 0:
        st.info(f"📖 {unread_books} books left to read. Keep going!")

# Main App
def main():
    st.set_page_config(page_title="Personal Library 📚", page_icon="📘", layout="centered")
    st.markdown("<h1 style='text-align: center;'>📘 Personal Library Manager</h1>", unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)

    menu = ["📖 Add Book", "🗑️ Remove Book", "🔍 Search Books", "📚 Display All Books", "📊 View Statistics"]
    choice = st.sidebar.radio("📋 Menu", menu)

    if choice == "📖 Add Book":
        add_book()
    elif choice == "🗑️ Remove Book":
        remove_book()
    elif choice == "🔍 Search Books":
        search_books()
    elif choice == "📚 Display All Books":
        display_books()
    elif choice == "📊 View Statistics":
        display_statistics()

if __name__ == "__main__":
    main()
