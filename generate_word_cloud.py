import sqlite3

conn = sqlite3.connect('jobs.sqlite')
state_abbr = []
num_of_job = []
cur = conn.cursor()
statement = '''
    SELECT JobSnapShot
    FROM Jobs
'''
cur.execute(statement)
results = cur.fetchall()
description = ''
for result in results:
    description += result[0].replace('\n', ' ')
# print(description)

# f = open('jobDescription.txt', 'w')
f = open('jobSnapshot.txt', 'w')
f.write(description)
f.close()