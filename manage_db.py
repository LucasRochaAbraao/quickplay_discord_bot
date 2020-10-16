import os
import pathlib
import sqlite3
import datetime
from dotenv import load_dotenv

load_dotenv()
DB = os.getenv('DISCORD_DB')

#current dir + db file
CURR_PATH = pathlib.Path(__file__).parent.absolute()
DB_PATH = os.path.join(CURR_PATH, DB)

def db_connect(db_path=DB_PATH):
    try:
        sqliteConnection = sqlite3.connect(db_path)
        print(f"Conectado ao db SQLite3: {DB}")
    except sqlite3.Error as error:
        print(f"Erro ao se conectar com o SQLite3: {error}")
    return sqliteConnection

def create_tables(conn):
    # ISO8601 string date format: YYYY-MM-DD HH:MM:SS.SSS
    cur = conn.cursor()
    
    evento_sql = """
CREATE TABLE IF NOT EXISTS eventos (
    evento_id INTEGER PRIMARY KEY,
    data timestamp NOT NULL,
    jogo text NOT NULL,
    equipe text NOT NULL,
    jogador text NOT NULL)"""

    ranking_sql = """
CREATE TABLE IF NOT EXISTS ranking (
    equipe text NOT NULL,
    jogador text NOT NULL,
    FOREIGN KEY (equipe)
    REFERENCES eventos (equipe)
        ON UPDATE CASCADE
        ON DELETE CASCADE)"""
    
    membro_discord = """
CREATE TABLE IF NOT EXISTS membros_discord (
    membro_id
    cor
    moedas
    piadas
    conselhos
    equipe
    -> stats

)"""
    
    cur.execute("PRAGMA foreign_keys=off;")
    cur.execute(evento_sql)
    cur.execute(ranking_sql)
    cur.execute("COMMIT;")
    cur.execute("PRAGMA foreign_keys=on;")
    print("tabelas criadas.")

if __name__ == '__main__':
    conn = db_connect(DB_PATH)
    create_tables(conn)
    conn.commit()



"""
--
-- salespeople
--
CREATE TABLE salespeople (
    id INTEGER PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    commission_rate REAL NOT NULL
);

-- customers
--
CREATE TABLE customers (
    id INTEGER PRIMARY KEY,
    company_name TEXT NOT NULL,
    street_address TEXT NOT NULL,
    city TEXT NOT NULL,
    state TEXT NOT NULL,
    zip TEXT NOT NULL
);

-- orders
--
CREATE TABLE orders (
    id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    salesperson_id INTEGER,
    FOREIGN KEY(customer_id) REFERENCES customers(id),
    FOREIGN KEY(salesperson_id) REFERENCES salespeople(id)
);

--
-- salespeople sample data
--
INSERT INTO salespeople VALUES (null, 'Fred', 'Flinstone', 10.0);
INSERT INTO salespeople VALUES (null, 'Barney', 'Rubble', 10.0);

--
-- customers sample data
--
INSERT INTO customers VALUES (null, 'ACME, INC.', '101 Main Street', 'Anchorage', 'AK', '99501');
INSERT INTO customers VALUES (null, 'FOOBAR', '200 Foo Way', 'Louisville', 'KY', '40207');

--
-- orders sample data
--
INSERT INTO orders VALUES (null, 1, 1);
INSERT INTO orders VALUES (null, 2, 2);

"""