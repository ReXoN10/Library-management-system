# Library Management System

A command-line library management system built in Python, using object-oriented design, custom exceptions, JSON persistence, and a logging context manager.

## Features

- **Book and Member management** — add books and members, track checkout status and borrowing history.
- **Checkout / return workflow** — with custom exceptions (`BookNotFoundError`, `BookNotAvailableError`, `MemberNotFoundError`) for clear, specific error handling.
- **JSON persistence** — save the entire library state to disk and reload it later. Loading correctly reconstructs shared object references, so a book referenced in a member's borrowed list and in the main catalog stays the *same* object in memory, not a duplicate.
- **Action logging** — every checkout/return attempt (success or failure) is logged with a timestamp via a custom context manager (`LibraryLogger`), writing to `library.log`.
- **Interactive CLI menu** — add books/members, check books in and out, list current state, and save/load, all through a simple terminal menu.

## Getting Started

### Requirements

- Python 3.8+ (no external dependencies — standard library only)

### Running

```bash
python3 code.py
```

You'll see a menu:

```
===== Library Menu =====
1. Add book
2. Add member
3. Checkout book
4. Return book
5. List all books
6. List all members
7. Save library
8. Load library
9. Exit
```

Saving and loading always use `library.json` in the current directory — no need to remember or type a filename.

### Example session

```
Enter choice: 1
Title: Dune
Author: Frank Herbert
ISBN: 12345
Added 'Dune'.

Enter choice: 2
Member name: Mohit
Member ID: 001
Added member 'Mohit'.

Enter choice: 3
ISBN to checkout: 12345
Member ID: 001

Enter choice: 7
Saved to library.json.
```

Next time you run the program, choose `8` to load your saved library back in.

## Project Structure

Everything currently lives in a single file, `code.py`:

- `Book`, `Member` — core data classes, with `to_dict()`/`from_dict()` for JSON serialization.
- `BookNotFoundError`, `BookNotAvailableError`, `MemberNotFoundError` — custom exceptions for specific failure cases.
- `Library` — the main class: add/find books and members, checkout/return logic, and `save_to_file()`/`load_from_file()` for persistence.
- `LibraryLogger` — a context manager (`__enter__`/`__exit__`) that wraps an action, logs whether it succeeded or failed (with a timestamp and details), and prints failures to the console without crashing the program.
- `log_action()` — a small helper combining a `Library` method call with `LibraryLogger`, so logging doesn't need a full `with` block at every call site.
- `run_cli()` — the interactive menu loop that ties everything together.

## A Design Note: Object Identity in `load_from_file()`

When loading a saved library back from JSON, a naive approach would call `Member.from_dict()` directly — but this creates a **new, separate `Book` object** for every entry in a member's borrowed-books list, disconnected from the actual `Book` object in the library's main catalog. Two objects would then represent the same physical book, and updating one (e.g. marking it returned) wouldn't be reflected in the other.

`load_from_file()` avoids this by loading all books into `Library.books` first, then manually building each `Member` and using `find_book(isbn)` to link back to the *same* `Book` object already in the catalog — instead of letting `Member.from_dict()` construct disconnected duplicates.

## Possible Improvements

- Automated tests
- Support for multiple simultaneous libraries / multiple save files