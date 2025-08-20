import pefile
import sys
p = sys.argv[1]
pe = pefile.PE(p)
for entry in pe.DIRECTORY_ENTRY_RESOURCE.entries:
    if entry.name:
        name = entry.name.decode(errors='ignore')
    else:
        name = str(entry.id)
    print('Resource:', name)
    for sub in entry.directory.entries:
        print('  Sub:', sub.id)
