Finder: File Search Tool
Overview
Finder is a Python-based application built using Tkinter for the graphical user interface (GUI). It allows users to search for files on their computer by specifying a keyword and choosing specific file types. The tool enables users to browse directories, filter files by extension, and sort search results alphabetically or by modification date. It also supports right-clicking to copy file paths.

Features
Keyword-based search: Search for files by specifying a keyword that must appear in the file names.
File type filters: Select specific file types (e.g., PDF, Word, Excel, PowerPoint, images, DWG).
Sort options: Sort search results alphabetically or by the last modified date.
Browse directories: Choose a specific directory or search across all drives.
Right-click functionality: Copy the file path of any file in the search results.
File opening: Open the selected file directly from the results list.
Requirements
To run the program, you need Python installed along with the following libraries:

Tkinter: For the graphical user interface.
pyperclip: To copy file paths to the clipboard.
You can install the required dependencies using pip:
pip install pyperclip
(Note: Tkinter is usually included with Python by default.)

How to Use
Run the Program:
Make sure you have Python installed on your system.
Save the code to a .py file (e.g., finder.py).
Run the program by executing the following in your terminal or command prompt:
python finder.py

Search for Files:
Browse Directory: Click the "Klasör Seç" button to choose a directory where you want to search for files.
Enter Keyword: Type the keyword you want to search for in the "Anahtar Kelime" field.
Select File Types: Check the file types (e.g., PDF, Word, Excel) you want to search for.
Choose Sort Order: You can choose to sort the search results alphabetically or by the last modified date.
Search: Click "Ara" to start the search.

View and Interact with Results:
File List: The search results will be displayed in a list box.
Open File: Double-click on a file in the list to open it.
Copy File Path: Right-click on a file in the list and select "Dosya Yolunu Kopyala" to copy the file path to your clipboard.

Close the Program:
Simply close the window to exit the program.

Example Use Case
Open the program and click "Klasör Seç" to choose a directory.
Enter a keyword (e.g., report) in the "Anahtar Kelime" field.
Select file types, for example, PDF and Word documents.
Choose "Alfabeye Göre" for alphabetical sorting.
Click "Ara" to search. The results will appear in the list box.
Double-click on a file to open it, or right-click to copy its path.

Known Limitations
The program currently works only on Windows for drive detection (A: to Z: drives).
Searching across all drives can take a long time depending on the number of files on your system.

License
© 2024 İsmail Çevik - All rights reserved.

Contact
For any questions or feedback, feel free to contact the author at:
Email: [ismailcevik@mail.com]

End of README
This README provides users with an understanding of the program, how to install and use it, as well as some technical details. You can adjust contact information and any other specifics that are relevant.
