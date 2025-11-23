/* =========================================================
   Lab Assignment 3 - Portfolio Website
   Author: Anupriya Agarwal
   ========================================================= */


import csv

class Book:
    def _init_(self, title, author, isbn):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.status = "available"  # Default status

    def _str_(self):
        return f"Title: {self.title}, Author: {self.author}, ISBN: {self.isbn}, Status: {self.status}"

    def to_dict(self):
        return {
            "title": self.title,
            "author": self.author,
            "isbn": self.isbn,
            "status": self.status
        }

    def issue(self):
        if self.status == "available":
            self.status = "issued"
            return True
        else:
            return False

    def return_book(self):
        if self.status == "issued":
            self.status = "available"
            return True
        else:
            return False

    def is_available(self):
        return self.status == "available"

class LibraryInventory:
    def _init_(self, filename="library.csv"):
        self.books = []
        self.filename = filename
        self.load_books()

    def add_book(self, book):
        # Check if ISBN is unique
        if any(b.isbn == book.isbn for b in self.books):
            return False
        self.books.append(book)
        self.save_books()
        return True

    def search_by_title(self, title):
        results = [book for book in self.books if title.lower() in book.title.lower()]
        return results

    def search_by_isbn(self, isbn):
        results = [book for book in self.books if book.isbn == isbn]
        return results

    def display_all(self):
        if not self.books:
            print("No books in the inventory.")
        else:
            for book in self.books:
                print(book)

    def save_books(self):
        try:
            with open(self.filename, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['title', 'author', 'isbn', 'status'])  # Header
                for book in self.books:
                    writer.writerow([book.title, book.author, book.isbn, book.status])
        except Exception as e:
            print(f"Error saving books: {e}")
        finally:
            pass  # No specific cleanup needed

    def load_books(self):
        try:
            with open(self.filename, 'r', newline='') as f:
                reader = csv.reader(f)
                header = next(reader, None)  # Skip header if present
                self.books = []
                for row in reader:
                    if len(row) == 4:  # Ensure row has 4 columns
                        title, author, isbn, status = row
                        book = Book(title, author, isbn)
                        book.status = status  # Set status from file
                        self.books.append(book)
                    else:
                        print(f"Skipping invalid row: {row}")
        except FileNotFoundError:
            # File does not exist, start with empty inventory
            self.books = []
        except Exception as e:
            print(f"Error loading books: {e}. Starting with empty inventory.")
            self.books = []
        finally:
            pass  # No specific cleanup needed

def main():
    inventory = LibraryInventory()

    while True:
        print("\nLibrary Management System")
        print("1. Add Book")
        print("2. Issue Book")
        print("3. Return Book")
        print("4. View All Books")
        print("5. Search Book")
        print("6. Exit")

        try:
            choice = int(input("Enter your choice (1-6): "))
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 6.")
            continue

        if choice == 1:
            # Add Book
            title = input("Enter book title: ").strip()
            if not title:
                print("Title cannot be empty.")
                continue
            author = input("Enter book author: ").strip()
            if not author:
                print("Author cannot be empty.")
                continue
            isbn = input("Enter book ISBN: ").strip()
            if not isbn:
                print("ISBN cannot be empty.")
                continue
            book = Book(title, author, isbn)
            if inventory.add_book(book):
                print("Book added successfully.")
            else:
                print("Failed to add book. ISBN might already exist.")

        elif choice == 2:
            # Issue Book
            isbn = input("Enter ISBN of the book to issue: ").strip()
            if not isbn:
                print("ISBN cannot be empty.")
                continue
            results = inventory.search_by_isbn(isbn)
            if not results:
                print("Book not found.")
            elif results[0].issue():
                print("Book issued successfully.")
            else:
                print("Book is already issued.")

        elif choice == 3:
            # Return Book
            isbn = input("Enter ISBN of the book to return: ").strip()
            if not isbn:
                print("ISBN cannot be empty.")
                continue
            results = inventory.search_by_isbn(isbn)
            if not results:
                print("Book not found.")
            elif results[0].return_book():
                print("Book returned successfully.")
            else:
                print("Book was not issued.")

        elif choice == 4:
            # View All Books
            inventory.display_all()

        elif choice == 5:
            # Search Book
            print("Search by:")
            print("1. Title")
            print("2. ISBN")
            try:
                search_choice = int(input("Enter choice (1-2): "))
            except ValueError:
                print("Invalid input.")
                continue
            if search_choice == 1:
                title = input("Enter title to search: ").strip()
                if not title:
                    print("Title cannot be empty.")
                    continue
                results = inventory.search_by_title(title)
                if results:
                    for book in results:
                        print(book)
                else:
                    print("No books found with that title.")
            elif search_choice == 2:
                isbn = input("Enter ISBN to search: ").strip()
                if not isbn:
                    print("ISBN cannot be empty.")
                    continue
                results = inventory.search_by_isbn(isbn)
                if results:
                    print(results[0])
                else:
                    print("No book found with that ISBN.")
            else:
                print("Invalid choice.")

        elif choice == 6:
            # Exit
            print("Exiting the system.")
            break

        else:
            print("Invalid choice. Please select 1-6.")

if _name_ == "_main_":
    main()