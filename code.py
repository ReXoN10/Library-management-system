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

b1 = Book("Dune", "Frank Herbert", "12345")
b2 = Book("Dune", "Frank Herbert", "12346")
b1.is_checked_out = True
print(b1)
print(b1==b2)