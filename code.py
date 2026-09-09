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


class BookNotAvailableError(Exception):
    pass

class BookNotFoundError(Exception):
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

lib = Library()
lib.add_book(Book("Dune", "Frank Herbert", "12345"))
lib.add_book(Book("1984", "George Orwell", "17832"))
lib.add_member(Member("Mohit", "001"))
lib.add_member(Member("Riya", "002"))
 
# print(lib.find_book("12345"))              

# print(lib.find_book("99999"))        

print(lib.find_member("001"))

print(lib.find_member("999"))