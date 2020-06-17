import sqlite3
import os

db_abs_path = os.path.dirname(os.path.realpath(__file__))
db_path = os.path.join(db_abs_path, 'alegrosz.db')

conn = sqlite3.connect(db_path)
c = conn.cursor()

c.execute("DROP TABLE IF EXISTS items")
c.execute("DROP TABLE IF EXISTS categories")
c.execute("DROP TABLE IF EXISTS subcategories")
c.execute("DROP TABLE IF EXISTS comments")

c.execute("""CREATE TABLE categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT
)""")

c.execute("""CREATE TABLE subcategories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    category_id INTEGER,
    FOREIGN KEY (category_id) REFERENCES categories (id)
)""")

c.execute("""CREATE TABLE items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    description TEXT,
    price REAL,
    image TEXT,
    category_id INTEGER,
    subcategory_id INTEGER,
    FOREIGN KEY (category_id) REFERENCES categories (id),
    FOREIGN KEY (subcategory_id) REFERENCES subcategories (id)
)""")

c.execute("""CREATE TABLE comments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content TEXT,
    item_id INTEGER,
    FOREIGN KEY (item_id) REFERENCES items (id)
)""")

categories = [
    ("Food",),
    ("Garden",),
    ("Toys",),
]

c.executemany("INSERT INTO categories (name) VALUES (?)", categories)

subcategories = [
    ("Fruit", 1),
    ("Meat", 1),
    ("Eatable", 1),
    ("Shovel", 2),
    ("Chainsaw", 2),
    ("Cars", 3),
    ("Lego", 3),
    ("Kinetic sand", 3),
]

c.executemany("INSERT INTO subcategories (name, category_id) VALUES (?, ?)", subcategories)

items = [
    ("Bananas", "1kg of fresh bananas", 6.50, "", 1, 1),
    ("Police station", "most popular lego set", 199.99, "", 3, 7),
    ("Bat", "Fresh china street food", 20, "", 1, 3),
    ("HotWheels Truck", "Good for sand racing truck", 29.99, "", 3, 6),
]

c.executemany(
    "INSERT INTO items (title, description, price, image, category_id, subcategory_id) VALUES (?, ?, ?, ?, ?, ?)",
    items)

conn.commit()
conn.close()

print('Database is created and initialized.')
