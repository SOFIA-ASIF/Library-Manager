import json

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
        json.dump(library, file)

# Add a book
def add_book(library):
    title = input('Enter the book title: ')
    author = input('Enter the author: ')
    year = int(input('Enter the publication year: '))
    genre = input('Enter the genre: ')
    read_status = input('Have you read this book? (yes/no): ').lower() == 'yes'
    library.append({
        'title': title,
        'author': author,
        'year': year,
        'genre': genre,
        'read': read_status
    })
    print('Book added successfully!')

# Remove a book
def remove_book(library):
    title = input('Enter the title of the book to remove: ')
    for book in library:
        if book['title'].lower() == title.lower():
            library.remove(book)
            print('Book removed successfully!')
            return
    print('Book not found.')

# Search for a book
def search_books(library):
    search_type = int(input('Search by: \n1. Title \n2. Author \nEnter your choice: '))
    query = input('Enter your search query: ')
    matches = [book for book in library if query.lower() in book['title'].lower() or query.lower() in book['author'].lower()]
    if matches:
        for book in matches:
            print(f"{book['title']} by {book['author']} ({book['year']}) - {book['genre']} - {'Read' if book['read'] else 'Unread'}")
    else:
        print('No matching books found.')

# Display all books
def display_books(library):
    if not library:
        print('Library is empty.')
        return
    for book in library:
        print(f"{book['title']} by {book['author']} ({book['year']}) - {book['genre']} - {'Read' if book['read'] else 'Unread'}")

# Display statistics
def display_statistics(library):
    total_books = len(library)
    read_books = sum(1 for book in library if book['read'])
    percentage_read = (read_books / total_books * 100) if total_books > 0 else 0
    print(f'Total books: {total_books}')
    print(f'Percentage read: {percentage_read:.2f}%')

# Main menu
def menu():
    library = load_library()
    while True:
        print('\nPersonal Library Manager')
        print('1. Add a book')
        print('2. Remove a book')
        print('3. Search for a book')
        print('4. Display all books')
        print('5. Display statistics')
        print('6. Exit')
        choice = input('Enter your choice: ')
        if choice == '1':
            add_book(library)
        elif choice == '2':
            remove_book(library)
        elif choice == '3':
            search_books(library)
        elif choice == '4':
            display_books(library)
        elif choice == '5':
            display_statistics(library)
        elif choice == '6':
            save_library(library)
            print('Library saved to file. Goodbye!')
            break
        else:
            print('Invalid choice. Please try again.')

# Run the program
menu()
