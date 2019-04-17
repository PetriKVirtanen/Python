import sqlite3

conn = sqlite3.connect('porssi.sqlite')
cur = conn.cursor()
count = 0
team = 'TAP'
#laskuri = 0
team = input('Output by team - N to bypass ')
name = input('Output by name - N to bypass ')
# https://www.sqlite.org/lang_select.html
print('---------------------------------------------')
#sqlstr = 'SELECT nimi, seura, ottelut, tulos, til FROM Pelaaja ORDER BY tulos LIMIT 20'
#for row in cur.execute(sqlstr) :
#    laskuri = laskuri + 1
#    print(laskuri,'. ',row[0], row[1], row[2], row[3], row[4])
if team != 'N' :
    print('---------------------------------------------')
    cur.execute('SELECT nimi, seura, ottelut, tulos, til FROM Pelaaja WHERE seura = ? ', (team,))
    for row in cur :
        print(row)
        count = count + 1
    print(count, 'rows.')
if name != 'N' :
    print('---------------------------------------------')
    cur.execute('SELECT nimi, seura, ottelut, tulos, til FROM Pelaaja WHERE nimi = ? ', (name,))
    for row in cur :
        print(row)
cur.close()
