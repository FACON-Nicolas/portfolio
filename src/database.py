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
        cursor.execute(""" CREATE TABLE PROJECT (
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

        cursor.execute(""" CREATE TABLE TECHNOLOGIES (
                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                name VARCHAR(50) NOT NULL,
                type VARCHAR(30) NOT NULL,
                media_url TEXT NOT NULL,
                learn_more TEXT NOT NULL,
                UNIQUE (name, type)
            )
        """)

        cursor.execute(""" CREATE TABLE LINK (
                id_project INT NOT NULL,
                id_tech INT NOT NULL,
                FOREIGN KEY (id_project) REFERENCES PROJECT (id),
                FOREIGN KEY (id_tech) REFERENCES TECHNOLOGIES (id),
                PRIMARY KEY (id_project, id_tech)
            )
        """)

        cursor.execute(""" CREATE TABLE SKILL (
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            name VARCHAR(30) NOT NULL
        )
        """)

        cursor.execute(""" CREATE TABLE LINK_SKILL(
            id_skill INTEGER NOT NULL,
            id_tech INTEGER NOT NULL,
            PRIMARY KEY (id_skill, id_tech)
        )
        """)


        cursor.execute(""" CREATE TABLE TAG (
                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                name VARCHAR(30)
            )
        """)

        cursor.execute(""" CREATE TABLE TAGS (
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
        cursor.execute(""" INSERT INTO PROJECT (
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

def insert_technologie(name, type, media_url, doc_url):
    try:
        cursor.execute(""" INSERT INTO TECHNOLOGIES (
                name,
                type, 
                media_url,
                learn_more
            ) VALUES (
                ?, ?, ?, ?
            )
        """, (name, type, media_url, doc_url, ))
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

def insert_skill(name: str):
    try:
        cursor.execute('INSERT INTO SKILL (name) VALUES (?)', (name, ))
    except:
        pass

def techs_by_skills(id_skill):
    return [
        i for i in cursor.execute("""SELECT TECHNOLOGIES.*
            FROM TECHNOLOGIES JOIN LINK_SKILL
            ON TECHNOLOGIES.id=LINK_SKILL.id_tech
            WHERE LINK_SKILL.id_skill = """ + str(id_skill))
    ]

def insert_link_skill(id_skill, id_tech):
    try:
        cursor.execute("INSERT INTO LINK_SKILL VALUES (?, ?)", (id_skill, id_tech,))
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
        i for i in cursor.execute(""" SELECT TECHNOLOGIES.*
            FROM TECHNOLOGIES JOIN LINK
            ON TECHNOLOGIES.id=LINK.id_tech
            WHERE id_project = """ + str(id_project))
    ]

def tags_by_project(id_project):
    return [
        i for i in cursor.execute(
            """ SELECT TAG.*
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

def tech_by_skill(id_skill):
    return [
        {
            'id': tech[0],
            'name': tech[1],
            'type': tech[2],
            'media': tech[3],
            'doc': tech[4],
            'id_skill': id_skill
        } for tech in techs_by_skills(id_skill)
    ]

def skills():
    return [
        {
            'id': skill[0],
            'name': skill[1]
        } for skill in cursor.execute("SELECT * FROM SKILL")
    ]

def techs(skills):
    return [
        tech_by_skill(skill['id'])
        for skill in skills
    ]

def get_technologies():
    return [i for i in cursor.execute("SELECT * FROM TECHNOLOGIES")]

def get_link():
    return [i for i in cursor.execute("SELECT * FROM LINK")]

def close():
    connect.commit()
    cursor.close()
    connect.close()
