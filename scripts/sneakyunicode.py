import pathlib as pl
import polib as po
from collections.abc import Generator,Iterator
import sys
#import time
import re
import argparse


class HiddenUnicodeError():
    def __init__(self, triggered_combination, unicode_found, filename, filelocation=None) -> None:
        self.triggered_combination = triggered_combination
        self.unicode_found = unicode_found
        self.filename = filename
        self.filelocation = filelocation
    
    def __str__(self) -> str:
        if self.filelocation != None:
            return f"HiddenUnicodeError:\n\tFound hidden unicode character ({self.unicode_found}) in letter combination >> {self.triggered_combination} << inside {self.filename} file around: {self.filelocation}.\nMore about this unicode character here: https://www.compart.com/en/unicode/{self.unicode_found}"
        else:
            return f"HiddenUnicodeError:\n\tFound hidden unicode character ({self.unicode_found}) in letter combination >> {self.triggered_combination} << inside {self.filename} file.\nMore about this unicode character here: https://www.compart.com/en/unicode/{self.unicode_found}"

class HiddenUnicodeWarning(HiddenUnicodeError):
    def __init__(self, triggered_combination, unicode_found, filename, filelocation=None) -> None:
        HiddenUnicodeError.__init__(self, triggered_combination, unicode_found, filename, filelocation)

    def __str__(self) -> str:
        if self.filelocation != None:
            return f"HiddenUnicodeWarning:\n\tFound hidden unicode character ({self.unicode_found}) in letter combination >> {self.triggered_combination} << inside {self.filename} file around: {self.filelocation}.\nPlease check if this is correct, more about this unicode character here: https://www.compart.com/en/unicode/{self.unicode_found}"
        else:
            return f"HiddenUnicodeWarning:\n\tFound hidden unicode character ({self.unicode_found}) in letter combination >> {self.triggered_combination} << inside {self.filename} file.\nPlease check if this is correct, more about this unicode character here: https://www.compart.com/en/unicode/{self.unicode_found}"

def find_hidden_unicodes_in_po_files() -> Iterator:
    cwd = pl.Path.cwd().joinpath('i18n')

    # move through all files in dirs
    for po_file in cwd.rglob("*.po"):
        po2read = po.pofile(po_file, encoding="UTF-8")
        curr_i18_folder = po_file.parts[po_file.parts.index("i18n")+1]

        for msg in po2read:
            if msg.translated():
                hidden_unicode_pattern = re.compile(r"[\u0300-\u036f]")
                # Combining Diacritical Marks Unicode Block
                # https://www.compart.com/en/unicode/block/U+0300
                hiddenU_DM = re.findall(hidden_unicode_pattern,msg.msgstr)

                filename = f"[{curr_i18_folder}]:{po_file.parent.name}/{po_file.stem}{po_file.suffix}"
                filelocation = f"translation of msg_id #{str(msg.linenum)}"

                if len(hiddenU_DM) > 0:
                    for macz in re.finditer(hidden_unicode_pattern,msg.msgstr):
                        # do not warn for certain langs
                        if curr_i18_folder == "ru":
                            # do not warn about U+0301
                            unicode_p = f"U+{format(ord(macz[0]), '04x')}"
                            if unicode_p != "U+0301":
                                yield HiddenUnicodeWarning(macz.string[macz.start(0)-1:macz.start(0)+1],f"U+{format(ord(macz[0]), '04x')}",filename,filelocation)
                        else:
                            yield HiddenUnicodeError(macz.string[macz.start(0)-1:macz.start(0)+1],f"U+{format(ord(macz[0]), '04x')}",filename,filelocation)

def find_hidden_unicodes_in_jsons() -> Iterator:
    # finds only parts of json with text
    match_pattern = re.compile(r"\"text\": (\".+\")|\"title\": (\".+\")|\"name\": (\".+\")|\"description\": (\".+\")|\"confirm_text\": (\".+\")|\"scenario_name\": (\".+\")|\"full_name\": (\".+\")|\"note\": (\".+\")|\"header\": (\".+\")")
    hidden_unicode_pattern = re.compile(r"[\u0300-\u036f]")
    # check only .jsons in following folders:
    interesting_parts = ['campaigns', 'return_campaigns', 'rules', 'wip']

    for part in interesting_parts:
        cwd = pl.Path.cwd().joinpath(part)

        for jsonfile in cwd.rglob("*.json"):
            with open(jsonfile, 'r', encoding="UTF-8") as jf:
                json_content = jf.read()
            
            for content_found in re.finditer(match_pattern,json_content):
                if len(re.findall(hidden_unicode_pattern, content_found.group(0))) > 0:
                    for hidden_char in re.finditer(hidden_unicode_pattern,content_found.group(0)):
                        filelocation = f"(...){hidden_char.string[hidden_char.start(0)-12:hidden_char.start(0)+1] if hidden_char.start(0) > 12 else hidden_char.string[hidden_char.start(0)-10:hidden_char.start(0)+1]}"

                        if "ru" in jsonfile.parts:
                            yield HiddenUnicodeWarning(hidden_char.string[hidden_char.start(0)-1:hidden_char.start(0)+1],f"U+{format(ord(hidden_char[0]), '04x')}",jsonfile,filelocation)
                        else:
                            yield HiddenUnicodeError(hidden_char.string[hidden_char.start(0)-1:hidden_char.start(0)+1],f"U+{format(ord(hidden_char[0]), '04x')}",jsonfile,filelocation)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="sneakyunicode",
        description="Validates translations and original texts against hidden unicode characters.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("-m", default="all", choices=["i18n", "jsons", "all"], metavar="mode", help="Mode of operation - one of: (default: %(default)s)\n  i18n  - scans through translated msgstr in .po files of each locale\n  jsons - scans through subset of original english .jsons along with rules in every locale\n  all   - uses both above options")
    args = parser.parse_args()
    
    #start_time = time.time()
    num_warnings = 0
    num_errors = 0

    if args.m in ("i18n", "all"):
        for error in find_hidden_unicodes_in_po_files():
            print(error)
            if type(error) == HiddenUnicodeWarning:
                num_warnings += 1
            elif type(error) == HiddenUnicodeError:
                num_errors += 1
    if args.m in ("jsons", "all"):
        for error in find_hidden_unicodes_in_jsons():
            print(error)
            if type(error) == HiddenUnicodeWarning:
                num_warnings += 1
            elif type(error) == HiddenUnicodeError:
                num_errors += 1

    #execution_time = time.time() - start_time
    print(f"Found {num_errors} errors and {num_warnings} warnings!")
    #print("Execution time in seconds: " + str(execution_time))

    if num_errors > 0:
        sys.exit(1)