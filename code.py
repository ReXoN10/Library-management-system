class Book:
    def __init__(self, title, author, isbn):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.is_checked_out = False

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

    def find_book(self,isbn):
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
        book=self.find_book(isbn)
        if book is None:
            raise BookNotFoundError(f"Book with ISBN {isbn} not found.")

        if book.is_checked_out:
            raise BookNotAvailableError(f"{book.title} is already checked out.")

        member=self.find_member(member_id)
        if member is None:
            raise MemberNotFoundError(f"Member with ID {member_id} not found.")

        book.is_checked_out = True
        member.borrowed_books.append(book)

    def return_book(self, isbn, member_id):
        book=self.find_book(isbn)
        if book is None:
            raise BookNotFoundError(f"Book with ISBN {isbn} not found.")
        
        if book.is_checked_out == False:
            raise BookNotAvailableError(f"{book.title} is not checked out.")

        member=self.find_member(member_id)
        if member is None:
            raise MemberNotFoundError(f"Member with ID {member_id} not found.")

        if book not in member.borrowed_books:
                raise BookNotFoundError(f"Member with ID {member_id} did not borrow {book.title}.")

        book.is_checked_out = False
        member.borrowed_books.remove(book)


def attempt(action, *args):
    try:
        result =action(*args)
        return result
    except (MemberNotFoundError, BookNotFoundError, BookNotAvailableError) as e:
        print(e)
        return None
    



lib = Library()
lib.add_book(Book("Dune", "Frank Herbert", "12345"))
lib.add_book(Book("1984", "George Orwell", "17832"))
lib.add_member(Member("Mohit", "001"))
lib.add_member(Member("Riya", "002"))


attempt(lib.checkout_book,"12345", "001")
print(lib.find_member("001").borrowed_books)  

attempt(lib.checkout_book,"12345", "002")
attempt(lib.checkout_book,"17832", "002")
print(lib.find_member("002").borrowed_books)

attempt(lib.return_book,"12345", "001")
print(lib.find_member("001").borrowed_books)