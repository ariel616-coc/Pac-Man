class Book:
    def __init__(self, book_name, author):
        self.book_name = book_name
        self.author = author
        self.status = "available"
        self.borrow_name = None

    def book_borrowed(self, user_name):
        if self.status == "unavailable":
            print("book is not available")
            return False

        self.borrow_name = user_name
        self.status = "unavailable"
        return True

    def book_returned(self):
        if self.status == "available":
            print("book is not borrow")
            return False

        self.borrow_name = None
        self.status = "available"
        return True

    def print_details(self):
        print(f"name: {self.book_name}, author{self.author}")


class Reader:
    def __init__(self, user_id, user_name):
        self.user_id = user_id
        self.user_name = user_name
        self.borrowed_list = []

    def borrow_book(self, book, limit = 3):
        if len(self.borrowed_list) < limit:
            if book.book_borrowed(self.user_name):
                self.borrowed_list.append(book.book_name)
                return True
            return False
        print("you reached the limit!")
        return False

    def return_book(self, book):
        if book.book_name in self.borrowed_list:
            if book.book_returned():
                self.borrowed_list.remove(book.book_name)
                return True
            return False

        print("book is not in the borrow list")
        return False

    def print_ids(self):
        print(f"name: {self.user_name}. id: {self.user_id}")

    def print_details(self):
        self.print_ids()
        for book in self.borrowed_list:
            print(f"book name: {book.book_name}. author: {book.author}")

class Librarian(Reader):
    def __init__(self, user_id, user_name):
        super().__init__(user_id, user_name)
        self.reader_list = []

    def borrow_book(self, book, limit = 5):
        super().borrow_book(book, limit)

    def return_book(self, book):
        super().return_book(book)

    def print_details(self):
        super().print_ids()
        for reader in self.borrowed_list:
            print(f"book name: {reader.user_name}. id: {reader.user_id}")

    def add_new_reader(self, reader):
        self.reader_list.append(reader)


class ChiefLibrarian(Librarian):
    def __init__(self, user_id, user_name):
        super().__init__(user_id, user_name)
        self.librarian_list = []

    def borrow_book(self, book, limit = 7):
        super().borrow_book(book, limit)

    def return_book(self, book):
        super().return_book(book)

    def print_details(self):
        super().print_ids()
        for librarian in self.borrowed_list:
            print(f"book name: {librarian.user_name}. id: {librarian.user_id}")

    def add_new_librarian(self, librarian):
        self.librarian_list.append(librarian)


b1 = Book("Harry Potter", "J.K. Rowling")
b2 = Book("The Hobbit", "J.R.R. Tolkien")
b3 = Book("Dune", "Frank Herbert")

# Reader tests
r1 = Reader("101", "Dan")
r1.print_details()

r2 = Reader("102", "Maya")
r2.borrow_book(b1)
r2.print_details()

r3 = Reader("103", "Yosef")
r3.borrow_book(b2)
r3.borrow_book(b3)
r3.print_details()

# Librarian tests
l1 = Librarian("200", "Sarah")
l1.print_details()

l2 = Librarian("201", "David")
l2.add_new_reader(r1)
l2.add_new_reader(r2)
l2.print_details()

# Chief Librarian tests
c1 = ChiefLibrarian("300", "Noa")
c1.print_details()

c2 = ChiefLibrarian("301", "Adam")
c2.add_new_librarian(l1)
c2.add_new_librarian(l2)
c2.print_details()