import re

texttosearch = '''
22/30/2020
aodshfoiawdsf
21/12/2021
'''

def extractDate(line):
    re = __import__('re')
    date  = re.findall(r'\b\d{2}[/]\d{2}[/]\d{4}\b', line)

    return date

print(extractDate(texttosearch))