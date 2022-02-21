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

# Modify outputfolder name if necessary
def prepare_outputfolder(outputfolder):
    bad_chars = [".", "\\", "/"]
    
    for char in bad_chars:
        if char in outputfolder:
            outputfolder = outputfolder.replace(char, "")

    return outputfolder

def create_file_title(note):
    first_newline = note.find('\n')
    title = note[:first_newline].strip()

    for char in title:
        if char in (string.punctuation + " "):
            title = title.replace(char, '')
        cleaned_title = title

    return cleaned_title

# Getting notes
def create_new_file(current_working_directory, outputfolder):
    cursor.execute('SELECT * FROM notes')
    for index,entry in enumerate(cursor.fetchall()):
        if entry[8] == 0:
            note = entry[2]
            cleaned_title = create_file_title(note)

            if outputfolder:
                book_name = prepare_outputfolder(outputfolder)
            else:
                book_name = get_specific_book_name(entry)

            # Check if directory exists, and create if not
            if not os.path.isdir(os.getcwd() + f"\\{book_name}"):
                os.mkdir(book_name)
            # Check if file already exists and append if it does
            if os.path.isfile(f'{current_working_directory}\\{book_name}\\{cleaned_title}.md'):
                cleaned_title = cleaned_title + "-new"

            with open(f'{current_working_directory}\\{book_name}\\{cleaned_title}.md', 'w') as new_note:
                new_note.write(note)

def main(filepath, outputfolder=None):
    current_working_directory = os.getcwd()
    outputfolder_path = current_working_directory

    create_new_file(outputfolder_path, outputfolder)

# For Command line input
if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.stdout.write('------------\nUsage:\ndb_to_md.py <database file path> [<output folder name>]\n------------')

    else:
        connection = sqlite3.connect(sys.argv[1])
        cursor = connection.cursor()

        if len(sys.argv) == 3:
            main(sys.argv[1], sys.argv[2])
        else:
            main(sys.argv[1])

        connection.close()
