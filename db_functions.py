import sqlite3

def connectToDb():
    con = sqlite3.connect('ratio.db')
    cur = con.cursor()

    # cur.execute('CREATE TABLE IF NOT EXISTS Statistics(UserID INT PRIMARY KEY, Win INT, Loss INT, Find INT);')
    # cur.execute('CREATE TABLE IF NOT EXISTS FoundRatio(MentionID INT, Tweet1ID INT, Tweet2ID INT, LikeDifference INT);')

    return con, cur

def addStatistics(userID, win, loss, found, cur, con):
    cur.execute(f'INSERT INTO Statistics (UserID, Win, Loss, Find) VALUES ({userID}, {win}, {loss}, {found});')
    con.commit()

def checkIfExists(ID, table, cur, what):
    res = cur.execute(f'SELECT * FROM {table} WHERE {what} = {ID}')
    if res:
        return True
    return False

def incrementStat(userID, stat, cur):
    res = cur.execute(f'SELECT {stat} FROM Statistics WHERE userID = {userID};')
    value = res.fetchone()[0] + 1
    cur.execute(f'UPDATE Statistics SET {stat} = {value} WHERE UserID = {userID};')

def getStats(userID, cur):
    res = cur.execute(f'SELECT Win, Loss, Find FROM Statistics WHERE userID = {userID};')
    stats = res.fetchall()[0]
    return stats[0], stats[1], stats[2]
