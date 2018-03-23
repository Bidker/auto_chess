#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
import sqlalchemy #przerobić na alchemy

connection = sqlite3.connect('chess.db')

connection.row_factory = sqlite3.Row

cursor = connection.cursor()

cursor.executescript("""
    DROP TABLE IF EXISTS ksiega_otwarc;
    CREATE TABLE IF NOT EXISTS ksiega_otwarc (
        id INTEGER PRIMARY KEY ASC,
        nazwa varchar(50) NOT NULL,
        nazwa_kontry varchar(50) NOT NULL
    )""")

cursor.executescript("""
    DROP TABLE IF EXISTS ruchy_otwarc;
    CREATE TABLE IF NOT EXISTS ruchy_otwarc (
        id INTEGER PRIMARY KEY ASC,
        pole varchar(50) NOT NULL,
        bierka varchar(50) NOT NULL,
        id_otwarcia INTEGER NOT NULL,
        FOREIGN KEY(id_otwarcia) REFERENCES ksiega_otwarc(id)
    )""")
