import re

# Read the file
with open(r'c:\ot-harjoitustyo_local\ot-harjoitustyo5\ot-harjoitustyo\src\Laihdutanyt_v2.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix all instances of font=("Arial", 11") to font=("Arial", 11)
content = re.sub(r'font=\("Arial", 11"\)', 'font=("Arial", 11)', content)

# Add missing import for uuid at the top if not already present
if 'import uuid' not in content:
    # Find the line with "from datetime import" and add uuid import after it
    content = content.replace('from datetime import date, datetime',
                             'from datetime import date, datetime\nimport uuid')

# Write back
with open(r'c:\ot-harjoitustyo_local\ot-harjoitustyo5\ot-harjoitustyo\src\Laihdutanyt_v2.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed all font typos and added uuid import!")
