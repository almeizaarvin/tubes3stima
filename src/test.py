import re

texttosearch = '''
abcdefghijklmnopqrstuvwxyz

BABA BIBI BOBO BABIBOBO

ABCDEFGHIJKLMNOPQRSTUVWZYZ
ABC
'''

pattern = re.compile(r'\BBOBO')
matches = pattern.finditer(texttosearch)

for m in matches:
    print(m)
