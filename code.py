import json
from datetime import datetime

class Book:
    def __init__(self, title, author, isbn):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.is_checked_out = False

    def to_dict(self):
        return {
            "title": self.title,
            "author": self.author,
            "isbn": self.isbn,
            "checked_out": self.is_checked_out
        }

    @classmethod
    def from_dict(cls, data):
        book = cls(data["title"], data["author"], data["isbn"])
        book.is_checked_out = data["checked_out"]
        return book

    def __str__(self):
        status = "Checked out" if self.is_checked_out else "Available"
        return f"{self.title} by {self.author} ({status})"

    def __repr__(self):
        return f"Book('{self.title}', '{self.author}', '{self.isbn}')"

    def __eq__(self, value):
        return self.isbn == value.isbn


class Member:
    def __init__(self, name, member_id):
        self.name = name
        self.member_id = member_id
        self.borrowed_books = []

    def to_dict(self):
        borrowed_dict = []
        for book in self.borrowed_books:
            borrowed_dict.append(book.to_dict())
        return {
            "name": self.name,
            "member_id": self.member_id,
            "borrowed_books": borrowed_dict
        }

    @classmethod
    def from_dict(cls, data):
        member = cls(data["name"], data["member_id"])
        for book_dict in data["borrowed_books"]:
            member.borrowed_books.append(Book.from_dict(book_dict))
        return member

    def __str__(self):
        return f"{self.name}(ID: {self.member_id})"


class BookNotFoundError(Exception):
    pass

class BookNotAvailableError(Exception):
    pass

class MemberNotFoundError(Exception):
    pass


class Library:
    def __init__(self):
        self.books = []
        self.members = []

    def add_book(self, book):
        self.books.append(book)

    def find_book(self, isbn):
        for book in self.books:
            if book.isbn == isbn:
                return book
        return None

    def add_member(self, member):
        self.members.append(member)

    def find_member(self, member_id):
        for member in self.members:
            if member.member_id == member_id:
                return member
        return None

    def checkout_book(self, isbn, member_id):
        book = self.find_book(isbn)
        if book is None:
            raise BookNotFoundError(f"Book with ISBN {isbn} not found.")

        if book.is_checked_out:
            raise BookNotAvailableError(f"{book.title} is already checked out.")

        member = self.find_member(member_id)
        if member is None:
            raise MemberNotFoundError(f"Member with ID {member_id} not found.")

        book.is_checked_out = True
        member.borrowed_books.append(book)

    def return_book(self, isbn, member_id):
        book = self.find_book(isbn)
        if book is None:
            raise BookNotFoundError(f"Book with ISBN {isbn} not found.")

        if book.is_checked_out == False:
            raise BookNotAvailableError(f"{book.title} is not checked out.")

        member = self.find_member(member_id)
        if member is None:
            raise MemberNotFoundError(f"Member with ID {member_id} not found.")

        if book not in member.borrowed_books:
            raise BookNotFoundError(f"Member with ID {member_id} did not borrow {book.title}.")

        book.is_checked_out = False
        member.borrowed_books.remove(book)

    def to_dict(self):
        books_dict=[]
        for book in self.books:
            books_dict.append(book.to_dict())

        members_dict=[]
        for member in self.members:
            members_dict.append(member.to_dict())

        return {"books":books_dict,
                "members":members_dict
        }


    def save_to_file(self,filename):
        data = self.to_dict()
        with open (filename, "w") as f:
            json.dump(data, f, indent=4)


    def load_from_file(self, filename):
        with open (filename, "r") as f:
            data = json.load(f)

        self.books=[]
        for book in data["books"]:
            self.books.append(Book.from_dict(book))

        self.members=[]
        for member in data["members"]:
            new_member = Member(member["name"], member["member_id"])
            for book_data in member["borrowed_books"]:
                isbn=book_data["isbn"]
                book=self.find_book(isbn)
                new_member.borrowed_books.append(book)
            self.members.append(new_member)


class LibraryLogger:
    def __init__(self, filename, action, **details):
        self.filename=filename
        self.action=action
        self.details=details

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, tb):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        details_str=""
        for key,value in self.details.items():
            details_str += f"{key} = {value}, "

        with open(self.filename, "a") as f:
            if exc_type is None:
                f.write(f"[{timestamp}] {self.action} - {details_str} SUCCESS.\n")
            else:
                f.write(f"[{timestamp}] {self.action} - {details_str} FAILURE: {str(exc_value)}.\n")
                print(f"Error: {exc_value}")

        return True


        

def log_action(action,filename, action_name, *args, **kwargs):
    with LibraryLogger(filename, action_name, **kwargs ) as log:
        return action(*args)


def print_menu():
    print("\n===== Library Menu =====")
    print("1. Add book")
    print("2. Add member")
    print("3. Checkout book")
    print("4. Return book")
    print("5. List all books")
    print("6. List all members")
    print("7. Save library")
    print("8. Load library")
    print("9. Exit")


LIBRARY_FILE = "library.json"


def run_cli():
    lib = Library()

    while True:
        print_menu()
        choice = input("Enter choice: ").strip()

        if choice == "1":
            title = input("Title: ").strip()
            author = input("Author: ").strip()
            isbn = input("ISBN: ").strip()
            lib.add_book(Book(title, author, isbn))
            print(f"Added '{title}'.")

        elif choice == "2":
            name = input("Member name: ").strip()
            member_id = input("Member ID: ").strip()
            lib.add_member(Member(name, member_id))
            print(f"Added member '{name}'.")

        elif choice == "3":
            isbn = input("ISBN to checkout: ").strip()
            member_id = input("Member ID: ").strip()
            log_action(lib.checkout_book, "library.log", "Checkout", isbn, member_id, isbn=isbn, member_id=member_id)

        elif choice == "4":
            isbn = input("ISBN to return: ").strip()
            member_id = input("Member ID: ").strip()
            log_action(lib.return_book, "library.log", "Return", isbn, member_id, isbn=isbn, member_id=member_id)

        elif choice == "5":
            if not lib.books:
                print("No books yet.")
            for book in lib.books:
                print(book)

        elif choice == "6":
            if not lib.members:
                print("No members yet.")
            for member in lib.members:
                print(member, [str(b) for b in member.borrowed_books])

        elif choice == "7":
            lib.save_to_file(LIBRARY_FILE)
            print(f"Saved to {LIBRARY_FILE}.")

        elif choice == "8":
            lib.load_from_file(LIBRARY_FILE)
            print(f"Loaded from {LIBRARY_FILE}.")

        elif choice == "9":
            print("Goodbye.")
            break

        else:
            print("Invalid choice, try again.")


if __name__ == "__main__":
    run_cli()