import os
import re

directory_in_str = "/Users/javnik/Documents/Git/arkham-cards-data/i18n/zh/campaigns"
directory = os.fsencode(directory_in_str)

total_found = 0
li_of_matches=[]
#dupa = os.listdir(directory)
for direc in os.listdir(directory):
    if os.fsdecode(direc) in ('.DS_Store', 'campaigns', 'cards', 'return_campaigns'):
        continue
    direc_en = os.listdir(os.path.join(directory_in_str, os.fsdecode(direc)))

    print(f"Entering {os.fsdecode(direc)} directory...")

    for file in direc_en:
        filename = os.fsdecode(file)
        if filename.endswith(".po"): 
            filename = os.path.join(directory_in_str, os.fsdecode(direc), filename)
            with open(filename, 'r', encoding='utf-8') as a:
                linijki = a.readlines()
                linijki = linijki[2:]
                proceed = False
                majbi = False

                for linijka in linijki:
                    #outlinijka = linijka 
                    if linijka.startswith("msgstr") and linijka != 'msgstr ""\n':
                        proceed = True
                    elif linijka == "\n":
                        proceed = False
                        majbi = False
                    
                    if proceed or majbi:
                        all_hiddenU = re.findall(r"[\u0300-\u036f]",linijka)

                        if len(all_hiddenU) > 0:
                            for macz in re.finditer(r"[\u0300-\u036f]",linijka):
                                print(f"Found hidden character '{macz[0]}' (U+{format(ord(macz[0]), '04x')}) bound with character {macz.string[macz.start(0)-1:macz.start(0)]} in string sequence: '{macz.string[macz.start(0)-5:macz.end(0)+5]}'")
                                li_of_matches.append((filename,macz.string[macz.start(0)-1:macz.start(0)],macz[0],format(ord(macz[0]), '04x')))
                                total_found += 1

                    
                    if linijka.startswith('msgstr ""'):
                        majbi = True

                    #writelinijki.append(outlinijka)
                #d.writelines(writelinijki)

        else:
            pass
            #print(f"This '{filename}' is not .po file")

print("Execution completed!")
print(f"Found {str(total_found)} issues.")
print("Writing found errors to file...")
with open("unicode_log.txt",'w+') as e:
    e.write("Log from 'campaigns_dir' file:\n")
    e.write("PATH\tCHAR BEFORE\tHIDDEN UNICODE CHAR\tUNICODE CODE OF HIDDEN CHAR\n")
    for i in li_of_matches:
        e.write(f"{i[0]}\t{i[1]}\t{i[2]}\t{i[3]}\n")
print("Log written. Thank you.")