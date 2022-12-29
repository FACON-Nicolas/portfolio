import sqlite3
from sqlite3 import OperationalError, IntegrityError
from datetime import datetime, date
import os

path = "db/database.db"

if (not os.path.exists(path)): 
    with open(path, 'w') as f:
        f.write('')

connect = sqlite3.connect(path, check_same_thread=False)
cursor = connect.cursor()

def create_database():
    try:
        cursor.execute("""
            CREATE TABLE PROJECT (
                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                name VARCHAR(50),
                description TEXT NOT NULL,
                date_creation DATE NOT NULL,
                maintenance BOOLEAN NOT NULL DEFAULT FALSE,
                development BOOLEAN NOT NULL DEFAULT FALSE,
                url_github TEXT NOT NULL DEFAULT 'github.com/FACON-Nicolas',
                media_url TEXT NOT NULL,
                location VARCHAR(10) NOT NULL
            )
        """)

        cursor.execute("""
            CREATE TABLE TECHNOLOGIES (
                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                name VARCHAR(50) NOT NULL,
                type VARCHAR(30) NOT NULL,
                UNIQUE (name, type)
            )
        """)

        cursor.execute("""
            CREATE TABLE LINK (
                id_project INT NOT NULL,
                id_tech INT NOT NULL,
                FOREIGN KEY (id_project) REFERENCES PROJECT (id),
                FOREIGN KEY (id_tech) REFERENCES TECHNOLOGIES (id),
                PRIMARY KEY (id_project, id_tech)
            )
        """)


        cursor.execute("""
            CREATE TABLE TAG (
                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                name VARCHAR(30)
            )
        """)

        cursor.execute("""
            CREATE TABLE TAGS (
                id_tag INT NOT NULL,
                id_project INT NOT NULL,
                FOREIGN KEY (id_tag) REFERENCES TAG (id),
                FOREIGN KEY (id_project) REFERENCES PROJECT (id),
                PRIMARY KEY (id_tag, id_project)                
            )
        """)
    except OperationalError as e:
        print(e)

def insert_project(name: str, description: str, date_creation: datetime, git: str, media: str, location: str, maintenance: bool=False, development: bool=False):
    try:
        cursor.execute("""
            INSERT INTO PROJECT (
                name, 
                description, 
                date_creation, 
                maintenance, 
                development, 
                url_github, 
                media_url,
                location
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (name, description, date_creation, maintenance, development, git, media, location))
    except IntegrityError as e:
        print(e)

def insert_technologie(name, type):
    try:
        cursor.execute("""
            INSERT INTO TECHNOLOGIES (
                name,
                type
            ) VALUES (
                ?, ?
            )
        """, (name, type,))
    except IntegrityError as e:
        print(e)

def insert_link(id_project, id_tech):
    try:
        cursor.execute("INSERT INTO LINK VALUES (?, ?)", (id_project, id_tech,))
    except:
        pass

def insert_tag(name):
    try:
        cursor.execute("INSERT INTO TAG (name) VALUES (?)", (name,))
    except:
        pass

def insert_tags(id_project, id_tag):
    try:
        cursor.execute("INSERT INTO TAGS VALUES (?, ?)", (id_project, id_tag,))
    except:
        pass

def get_projects():
    return [i for i in cursor.execute("SELECT * FROM PROJECT ORDER BY date_creation DESC")]

def get_tech_by_projects(projects):
    return [
        (
            project['id'],
            [lib[1] for lib in technologies_by_project(project['id'])]
        ) for project in projects
    ]

def technologies_by_project(id_project: int):
    return [
        i for i in cursor.execute("""
            SELECT TECHNOLOGIES.*
            FROM TECHNOLOGIES JOIN LINK
            ON TECHNOLOGIES.id=LINK.id_tech
            WHERE id_project = """ + str(id_project))
    ]

def tags_by_project(id_project):
    return [
        i for i in cursor.execute(
            """
            SELECT TAG.*
            FROM TAG JOIN TAGS
            ON TAG.id=TAGS.id_tag
            WHERE id_project=""" + str(id_project))
    ]

def projects(projects):
    return [
        {
            'id': project[0],
            'name': project[1],
            'description': project[2],
            'creation_date': project[3],
            'maintenance': project[4],
            'development': project[5],
            'github': project[6],
            'media_url': project[7],
            'location': project[8]
        } for project in projects
    ]

def get_technologies():
    return [i for i in cursor.execute("SELECT * FROM TECHNOLOGIES")]

def get_link():
    return [i for i in cursor.execute("SELECT * FROM LINK")]

def close():
    connect.commit()
    cursor.close()
    connect.close()

if ('__main__' == __name__):
    create_database()
    insert_project(
        'puissance 4', 
        "This project is a connect4's (puissance 4) copy. In this game, your computer cans also play against you like a human player, good luck !", 
        date(2021, 8, 9), 
        'https://github.com/FACON-Nicolas/Puissance4', 
        'https://github.com/FACON-Nicolas/FACON-Nicolas/raw/main/resources/connect4.gif?raw=true', 
        'Personal'
    )

    insert_project(
        'tetris', 
        "This project is a Tetris' copy developed in python with the pygame library. This is my first project with a GUI implemented on the window, for pause and game over menu, a database is developed but not used.", 
        date(2021, 12, 11), 
        'https://github.com/FACON-Nicolas/Tetris', 
        'https://raw.githubusercontent.com/FACON-Nicolas/FACON-Nicolas/main/resources/tetris.gif?raw=true', 
        'Personal'
    )

    insert_project(
        'Conway\'s Game of Life (python)', 
        "This project is a conways game of life developed in python with the pygame library. This project contains a GUI implemented on the window, for the buttons (reset, last step, next step, pause / resume and random grid) management.", 
        date(2022, 1, 10), 
        'https://github.com/FACON-Nicolas/conways-life-game', 
        'https://github.com/FACON-Nicolas/FACON-Nicolas/raw/main/resources/conways-py.gif?raw=true', 
        'Personal'
    )

    insert_project(
        'Conway\'s Game of Life (C++)', 
        "This project is a conways game of life developed in C++ with the SFML library. This project is my first project in C++ and my first project with SFML library (similar to pygame in python), this conway's game of life is exactly the same as the conway's game of life developed in python.", 
        date(2022, 5, 22), 
        'https://github.com/FACON-Nicolas/conways-cpp', 
        'https://github.com/FACON-Nicolas/FACON-Nicolas/raw/main/resources/conways-cpp.gif?raw=true', 
        'Personal'
    )

    insert_project(
    'Pacman', 
    "This project is composed by a source code of pacman in C++. the project needs an implementation of A* algorithm, sound FX, and better conception. \n My pacman project is composed by a pacman played by a human, and 3 ghosts Clyde, Pinky, Blinky.", 
    date(2022, 9, 1), 
    'https://github.com/FACON-Nicolas/pacman', 
    'https://raw.githubusercontent.com/FACON-Nicolas/FACON-Nicolas/main/resources/pacman.gif?raw=true', 
    'Personal'
    )

    insert_project(
    'Sprite Sheet Splitter', 
    "This project contains the source code of a sprite sheet splitter. This sprite sheet splitter cans split a sprite sheet with N rows and N columns and a margin cans be applied from the left, the right, the top and the button of the sprite sheet.", 
    date(2022, 11, 24), 
    'https://github.com/FACON-Nicolas/sprite-sheet-splitter', 
    'https://camo.githubusercontent.com/6967796c777c7867f18c35570b5cd026c9c3d533591837a8250cb69ce93c810c/68747470733a2f2f692e6962622e636f2f564e376a4474622f7370726974652d73686565742e706e67', 
    'Personal'
    )

    insert_technologie('python', 'language')
    insert_technologie('pygame', 'framework')
    insert_technologie('pygame_gui', 'framework')
    insert_technologie('SFML', 'framework')
    insert_technologie('boost', 'framework')
    insert_technologie('Tkinter', 'framework')
    insert_technologie('PIL', 'framework')
    insert_technologie('C++', 'language')
    insert_link(1, 1)
    insert_link(1, 2)
    insert_link(2, 1)
    insert_link(2, 2)
    insert_link(2, 3)
    insert_link(3, 1)
    insert_link(3, 2)
    insert_link(3, 3)
    insert_link(4, 8)
    insert_link(4, 4)
    insert_link(5, 8)
    insert_link(5, 4)
    insert_link(6, 1)
    insert_link(6, 6)
    insert_link(6, 7)
    insert_tag('game')
    insert_tag('web')
    insert_tag('app')

    for i in technologies_by_project(1):
        print(i)

    for i in technologies_by_project(2):
        print(i)

    print('---------')

    for i in tags_by_project(1):
        print(i)

    print('---------')

    for i in cursor.execute("SELECT * FROM PROJECT"):
        print(i)

    print('---------')

    close()

