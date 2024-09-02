import os
import re
#directory_in_str = "E:\Git\\arkham-cards-data\i18n\pl\\return_campaigns\\rttic"
directory_in_str = "E:\Git\\arkham-cards-data\\rules\pl"
directory = os.fsencode(directory_in_str)

total_changed = 0
#dupa = os.listdir(directory)
for file in os.listdir(directory):
    filename = os.fsdecode(file)
    if filename in ('campaigns', 'cards', 'return_campaigns'):
        continue
    if filename.endswith(".po"): 
        filename = os.path.join(directory_in_str, filename)
        with open(filename, 'r', encoding='utf-8') as a:
            linijki = a.readlines()
        with open(filename, 'w', encoding='utf-8') as d:
            writelinijki = linijki[:2]
            linijki = linijki[2:]
            proceed = False
            majbi = False

            for linijka in linijki:
                outlinijka = linijka 
                if linijka.startswith("msgstr") and linijka != 'msgstr ""\n':
                    proceed = True
                elif linijka == "\n":
                    proceed = False
                    majbi = False
                
                if proceed or majbi:
                    if len(re.findall(r"[\u0300-\u036f]",linijka)) > 0:
                        #[\u0328] - combining ogonek (ą,ę)
                        outlinijka = re.sub(r"a\u0328",'ą',outlinijka)
                        outlinijka = re.sub(r"A\u0328",'Ą',outlinijka)
                        outlinijka = re.sub(r"e\u0328",'ę',outlinijka)
                        outlinijka = re.sub(r"E\u0328",'Ę',outlinijka)
                        #[\u0301] - combining acute (ć,ń,ó,ś,ź)
                        outlinijka = re.sub(r"c\u0301",'ć',outlinijka)
                        outlinijka = re.sub(r"C\u0301",'Ć',outlinijka)
                        outlinijka = re.sub(r"n\u0301",'ń',outlinijka)
                        outlinijka = re.sub(r"N\u0301",'Ń',outlinijka)
                        outlinijka = re.sub(r"o\u0301",'ó',outlinijka)
                        outlinijka = re.sub(r"O\u0301",'Ó',outlinijka)
                        outlinijka = re.sub(r"s\u0301",'ś',outlinijka)
                        outlinijka = re.sub(r"S\u0301",'Ś',outlinijka)
                        outlinijka = re.sub(r"z\u0301",'ź',outlinijka)
                        outlinijka = re.sub(r"Z\u0301",'Ź',outlinijka)
                        #[\u0307] - combining dot above (ż)
                        outlinijka = re.sub(r"z\u0307",'ż',outlinijka)
                        outlinijka = re.sub(r"Z\u0307",'Ż',outlinijka)
                
                if linijka.startswith('msgstr ""'):
                    majbi = True

                writelinijki.append(outlinijka)
            d.writelines(writelinijki)
    if filename.endswith(".json"): 
        filename = os.path.join(directory_in_str, filename)
        with open(filename, 'r', encoding='utf-8') as a:
            linijki = a.readlines()
        with open(filename, 'w', encoding='utf-8') as d:
            writelinijki = []

            for linijka in linijki:
                outlinijka = linijka 
                stripnieta = linijka.rstrip("\n").lstrip()
                #beztabow = linijka.lstrip()
                if stripnieta.startswith(('[','{','}',']','"rules"','"id"')):
                    pass
                else:
                    if len(re.findall(r"[\u0300-\u036f]",linijka)) > 0:
                        #[\u0328] - combining ogonek (ą,ę)
                        outlinijka = re.sub(r"a\u0328",'ą',outlinijka)
                        outlinijka = re.sub(r"A\u0328",'Ą',outlinijka)
                        outlinijka = re.sub(r"e\u0328",'ę',outlinijka)
                        outlinijka = re.sub(r"E\u0328",'Ę',outlinijka)
                        #[\u0301] - combining acute (ć,ń,ó,ś,ź)
                        outlinijka = re.sub(r"c\u0301",'ć',outlinijka)
                        outlinijka = re.sub(r"C\u0301",'Ć',outlinijka)
                        outlinijka = re.sub(r"n\u0301",'ń',outlinijka)
                        outlinijka = re.sub(r"N\u0301",'Ń',outlinijka)
                        outlinijka = re.sub(r"o\u0301",'ó',outlinijka)
                        outlinijka = re.sub(r"O\u0301",'Ó',outlinijka)
                        outlinijka = re.sub(r"s\u0301",'ś',outlinijka)
                        outlinijka = re.sub(r"S\u0301",'Ś',outlinijka)
                        outlinijka = re.sub(r"z\u0301",'ź',outlinijka)
                        outlinijka = re.sub(r"Z\u0301",'Ź',outlinijka)
                        #[\u0307] - combining dot above (ż)
                        outlinijka = re.sub(r"z\u0307",'ż',outlinijka)
                        outlinijka = re.sub(r"Z\u0307",'Ż',outlinijka)

                writelinijki.append(outlinijka)
            d.writelines(writelinijki)


    else:
        print(f"This '{filename}' is not .po/.json file")
