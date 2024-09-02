import os
import re
import json

#TRANSLATEABLE_KEYS = (['text', 'title', 'subtext', 'name', 'description', 'confirm_text', 'scenario_name', 'full_name'])

text_keys = ['title', 'text', 'description', 'header', 'name', 'full_name', 'scenario_name', 'note', 'confirm_text']

campaigns_dir = '/Users/javnik/Documents/Git/arkham-cards-data/campaigns'
#campaigns_dir = '/Users/javnik/Documents/Git/arkham-cards-data/rules/en'

#directory_in_str = "E:\Git\\arkham-cards-data\i18n\pl\\return_campaigns\\rttic"
#directory_in_str = "E:\Git\\arkham-cards-data\\rules\pl"

directory = os.fsencode(campaigns_dir)

total_found = 0
li_of_matches = []

for direc in os.listdir(directory):
    #dodod = os.listdir(os.path.join(campaigns_dir, os.fsdecode(direc)))
    if os.fsdecode(direc) == '.DS_Store':
        continue
    direc_en = os.listdir(os.path.join(campaigns_dir, os.fsdecode(direc)))

    print(f"Entering {os.fsdecode(direc)} directory...")

    for file in direc_en:
        filename = os.fsdecode(file)
        print(f"Reading {filename}...")
        filename = os.path.join(campaigns_dir, os.fsdecode(direc), filename)
        file_now = 0
        with open(filename, 'r', encoding='utf-8') as a:
            file_content = a.readlines()
        
        for line in file_content:
            stripnieta = line.rstrip("\n").lstrip()
            if stripnieta.startswith(('[','{','}',']')):
                pass
            else:
                try:
                    leftki = stripnieta.split(":",1)[0].strip('"')
                    if leftki in text_keys:
                        all_hiddenU = re.findall(r"[\u0300-\u036f]",stripnieta)
                        #all_hiddenU = re.finditer(r"[\u0300-\u036f]",stripnieta)

                        if len(all_hiddenU) > 0:
                            for macz in re.finditer(r"[\u0300-\u036f]",stripnieta):
                                print(f"Found hidden character '{macz[0]}' (U+{format(ord(macz[0]), '04x')}) bound with character {macz.string[macz.start(0)-1:macz.start(0)]} in string sequence: '{macz.string[macz.start(0)-5:macz.end(0)+5]}'")
                                li_of_matches.append((filename,macz.string[macz.start(0)-1:macz.start(0)],macz[0],format(ord(macz[0]), '04x')))
                                total_found += 1
                except:
                    pass

print("Execution completed!")
print(f"Found {str(total_found)} issues.")
print("Writing found errors to file...")
with open("unicode_log.txt",'w+') as e:
    e.write("Log from 'campaigns_dir' file:\n")
    e.write("PATH\tCHAR BEFORE\tHIDDEN UNICODE CHAR\tUNICODE CODE OF HIDDEN CHAR\n")
    for i in li_of_matches:
        e.write(f"{i[0]}\t{i[1]}\t{i[2]}\t{i[3]}\n")
print("Log written. Thank you.")