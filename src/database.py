import sqlite3
from sqlite3 import OperationalError, IntegrityError
from datetime import datetime
import os

path = "db/database.db"

if (not os.path.exists(path)): 
    with open(path, 'w') as f:
        f.write('')

connect = sqlite3.connect(path)
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
                media_url TEXT NOT NULL
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
        print("coucou", e)

def insert_project(name: str, description: str, date_creation: datetime, git: str, media: str, maintenance: bool=False, development: bool=False):
    try:
        cursor.execute("""
            INSERT INTO PROJECT (
                name, 
                description, 
                date_creation, 
                maintenance, 
                development, 
                url_github, 
                media_url
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (name, description, date_creation, maintenance, development, git, media))
    except:
        pass

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
    return [i for i in cursor.execute("SELECT * FROM PROJECT")]

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
    insert_project('puissance 4', '', datetime.now(), '', '')
    insert_project('tetris', '', datetime.now(), '', '')
    insert_technologie('python', 'language')
    insert_technologie('C++', 'language')
    insert_link(1, 1)
    insert_link(2, 2)
    insert_tag('game')
    insert_tag('web')
    insert_tags(1, 1)
    insert_tags(2, 2)

    for i in technologies_by_project(1):
        print(i)

    for i in technologies_by_project(2):
        print(i)

    print('---------')

    for i in tags_by_project(1):
        print(i)

    close()

