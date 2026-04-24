import sys

with open('my_schema.sql', 'r', encoding='utf-8') as f:
    sql = f.read()

sql = sql.replace('CREATE TABLE', 'CREATE TABLE IF NOT EXISTS')
# Remove CREATE TABLE sqlite_sequence if it exists since it's an internal table
sql = '\n'.join([line for line in sql.split('\n') if not 'sqlite_sequence' in line])

with open('database.py', 'r', encoding='utf-8') as f:
    content = f.read()

start_marker = "    c.executescript('''"
start_idx = content.find(start_marker) + len(start_marker)
end_idx = content.find("''')", start_idx)

new_content = content[:start_idx] + '\n' + sql + '\n    ' + content[end_idx:]

with open('database.py', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("database.py updated")
