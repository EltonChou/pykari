import sqlite3

db_connect = sqlite3.connect('test.sqlite')
cursor = db_connect.cursor()
cursor.execute('''
CREATE TABLE `following` (`id` INTEGER NOT NULL UNIQUE, `name` TEXT NOT NULL, `screen_name` TEXT NOT NULL, PRIMARY KEY(`id`))
''')
