# import sqlite3

# conn = sqlite3.connect('jobs.sqlite')
# cur = conn.cursor()
# statement = '''
#     INSERT INTO Company (Name)
#     VALUES (?)
# '''
# insertion = ('aaa',)
# cur.execute(statement, insertion)
# conn.commit()

a = [78, 450, 493, 505, 535, 544, 611, 707, 768, 802, 856, 888, 1004, 1044, 1286, 1309, \
    1331, 1391, 1402, 1573, 1614, 1638, 1677, 1730, 1806, 1835, 1858, 1861, 1868, 1938, \
    1950, 1989, 2142, 2180, 2205, 2238, 2381, 2388, 2389]

print(len(a))