import sqlite3


db_path = 'pomoclicker/db.sqlite3'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS Users (
    username TEXT PRIMARY KEY,
    money INTEGER DEFAULT 0,
    clicks INTEGER DEFAULT 0,
    
    sessions30 INTEGER DEFAULT 0,
    sessions45 INTEGER DEFAULT 0,
    sessions60 INTEGER DEFAULT 0,
               
    upgradeClicks INTEGER DEFAULT 1,
    upgradeAuto INTEGER DEFAULT 0, 

    upgrade30 INTEGER DEFAULT 1,
    upgrade45 INTEGER DEFAULT 1,
    upgrade60 INTEGER DEFAULT 1
)''')

cursor.execute('SELECT username FROM Users WHERE username = ?', ("user", ))
user = cursor.fetchone()

if user == None:
    cursor.execute('''
    INSERT INTO Users (username)
    VALUES (?)''',
    ("user", ))
    conn.commit()

def setMoney(money: int) -> None:
    cursor.execute('UPDATE Users SET money = ? WHERE username = "user"', (money, ))
    conn.commit()

def getMoney() -> int:
    cursor.execute('SELECT money FROM Users WHERE username = ?', ("user", ))
    money = cursor.fetchone()
    return money[0]

def addClicks(clicks: int) -> None:
    cursor.execute(f'UPDATE Users SET "clicks" = "clicks" + {clicks}'
                   +' WHERE username = ?', ("user", ))
    conn.commit()

def getClicks() -> int:
    cursor.execute('SELECT clicks FROM Users WHERE username = ?', ("user", ))
    clicks = cursor.fetchone()
    return clicks[0]

def setClicks(clicks: int) -> None:
    cursor.execute(f'UPDATE Users SET clicks = ? WHERE username = ?', (clicks, "user", ))
    conn.commit()

def setMileAge(mode: int) -> None:
    cursor.execute(f'UPDATE Users SET "sessions{mode}" = "sessions{mode}" + 1'
                   +' WHERE username = ?', ("user", ))
    conn.commit()

def getMileAge() -> list[int]:
    cursor.execute('SELECT sessions30, sessions45, sessions60 FROM Users WHERE username = ?', ("user", ))
    mileage = cursor.fetchone()
    return mileage

def getUpgradesPomo() -> int:
    cursor.execute('SELECT upgrade30, upgrade45, upgrade60 FROM Users WHERE username = ?', ("user", ))
    upgrades = cursor.fetchone()
    return upgrades

def addUpgradePomo(minutes) -> None:
    cursor.execute(f'UPDATE Users SET "upgrade{minutes}" = "upgrade{minutes}" + 1 '
                   +'WHERE username = ?', ("user", ))
    conn.commit()

def getClickerLevel() -> int:
    cursor.execute('SELECT upgradeClicks FROM Users WHERE username = ?', ("user", ))
    level = cursor.fetchone()
    return level[0]

def addClickerLevel() -> None:
    cursor.execute(f'UPDATE Users SET upgradeClicks = upgradeClicks + 1 '
                   +'WHERE username = ?', ("user", ))
    conn.commit()

def getAutoClickerLevel() -> int:
    cursor.execute('SELECT upgradeAuto FROM Users WHERE username = ?', ("user", ))
    level = cursor.fetchone()
    return level[0]