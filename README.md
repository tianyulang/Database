Design Document
a general overview:
A general overview of your system with a small user guide: We use the data from
City of Edmonton's Open Data initiative and get some criminal information. Our
program is to implement SQLite search in a host programming language, python.
This program can allow users to enter the number of function to finish certain
search as they want. We import pandas, sqlite3, Folium and matplotlib to help us
analyze data easier.
a detailed design:
At the beginning, the program will required user to type in the database name (includes
the .db Tail segment), then the program will work on this specific database.
In the initial interface, there are five choices: first four choices are functions from 1 to 4 and
the last choice is exit. Unless you choose to exit, it will always go back to the initial interface
after finishing each function.
