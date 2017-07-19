"""
    Generates a table in sqlite3 that contains every password possible given
    a combination of letters, numbers, and certain special characters.

    abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+:;<>?/.,'"{}-\|
"""
import sqlite3
import string
import itertools
import hashlib

restart_at_iteration = 0

conn = sqlite3.connect('pws.db')
c = conn.cursor()

# If the table already exists, get the current count and we'll use that to skip to
# the same counter position when restarting
try:
    c.execute('SELECT COUNT(PW) FROM pws')
    row = c.fetchone()
    restart_at_iteration = None if not row[0] else row[0]
except (sqlite3.OperationalError, IndexError):
    restart_at_iteration = None

if restart_at_iteration is None:
    c.execute('DROP TABLE IF EXISTS pws')
    conn.commit()
    c.execute('CREATE TABLE IF NOT EXISTS pws (PW TEXT, md5 TEXT, sha1 TEXT, sha256 TEXT)')
    conn.commit()

# Add any extra characters you wish here, or remove any you don't care for.
letters = '{}{}{}'.format(string.ascii_letters, string.digits, '!@#$%^&*()_+:;<>?/.,\'"{}-\\|')

insert_query = 'INSERT INTO pws (PW, md5, sha1, sha256) VALUES (?,?,?,?)'

total_counter = 0
for i in range(len(letters)):

    keywords = itertools.product(letters, repeat=i)

    counter = 0
    inserts = []

    for k in keywords:
        counter += 1

        # We still need the counter to count properly so just skip the iteration
        if isinstance(restart_at_iteration, int) and counter <= restart_at_iteration:
            continue

        pw = ''.join(k).encode('utf-8')
        inserts.append((
            pw,
            hashlib.md5(pw).hexdigest(),
            hashlib.sha1(pw).hexdigest(),
            hashlib.sha256(pw).hexdigest()
        ))

        # Only commit to the database every 1 millionth iteration
        if counter % 1000000 == 0:
            print('\tCommitting', i, counter, pw)
            c.executemany(insert_query, inserts)
            conn.commit()
            inserts = []
            print('\t\tFinished Committing', i, counter, pw)

    # Ensure any left over inserts are commited before moving on.
    if inserts:
        c.executemany(insert_query, inserts)

    conn.commit()
    total_counter += counter
    print('\tFinished {}, Inserted: {}, Total Processed: {}'.format(i, counter, total_counter))
