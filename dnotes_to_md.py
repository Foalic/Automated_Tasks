#! /usr/bin/env python3

import sqlite3
import os
import sys
import string

def make_dict_of_books():
    cursor.execute('SELECT * FROM books')
    books_dict = dict()
    for book in cursor.fetchall():
        if book[4] == 0:
            book_name = book[1]
            book_uuid = book[0]
            books_dict[book_uuid] = book_name
    return books_dict

def get_specific_book_name(entry):
    book_uuid = entry[1]
    books_dict = make_dict_of_books()
    for uuid,book in books_dict.items():
        if uuid == book_uuid:
            book_name = book
            return book_name

def create_file_title(note):
    first_newline = note.find('\n')
    title = note[:first_newline].strip()
    for char in string.punctuation:
        if char in title:
            title = title.replace(char, '_')
    cleaned_title = title.replace(' ', '_')
    return cleaned_title

# Getting notes
def create_new_file(current_working_directory):
    cursor.execute('SELECT * FROM notes')
    for index,entry in enumerate(cursor.fetchall()):
        if entry[8] == 0:
            note = entry[2]
            cleaned_title = create_file_title(note)
            book_name = get_specific_book_name(entry)
            if not os.path.isdir(os.getcwd() + f"\\{book_name}"):
                os.mkdir(book_name)

            with open(f'{current_working_directory}\\{book_name}\\{cleaned_title}.md', 'w') as new_note:
                new_note.write(note)

def main(filepath, outputfolder=None):
    global cursor
    current_working_directory = os.getcwd()
    if outputfolder is not None:
        outputfolder_path = current_working_directory + '\\' + outputfolder
    else:
        outputfolder_path = current_working_directory

    connection = sqlite3.connect(filepath)
    cursor = connection.cursor()

    create_new_file(outputfolder_path)

    connection.close()

# For Command line input
if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.stdout.write('------------\nUsage:\ndb_to_md.py <database file path> [<output folder name>]\n------------')
        print(sys.argv)

    else:
        if len(sys.argv) == 3:
            main(sys.argv[1], sys.argv[2])
        else:
            main(sys.argv[1])
