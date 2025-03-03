import sqlite3
import pathlib
import argparse
   
class Book(object):

    BOOK_TYPES = ('.epub', '.mobi', '.pdf')

    def __init__(self, id, author, title, path):
        self.id = id
        self.author = author
        self.title = title
        self.path = pathlib.Path(path)

    def __str__(self):
        return f"{self.id}\t{self.author}\t{self.title}\t{self.path}"
    
    def __repr__(self):
        return f"Book({self.id}, {self.author}, {self.title}, {self.path}"
    
    @property
    def full_path(self):
        return pathlib.Path(CALIBRE_DIR, self.path)
    
    @property
    def exists(self):    
        return self.full_path.exists()
    
    @property
    def all_files(self):
         return self.full_path.glob("*")
    
    @property
    def files(self):
        return list(f for f in self.all_files if f.suffix in self.BOOK_TYPES)

    @property
    def has_cover(self):
        return any(list([f.suffix for f in self.all_files if f.suffix == '.jpg']))

    @property
    def has_files(self):
        return len(self.files) > 0
    

#### Arguments
parser = argparse.ArgumentParser(
                    prog='calibre-checker.py',
                    description='Find missing files in your Calibre library',
                    epilog='')

#parser.add_argument("-b", "--by", help="Show problems by author or by book")
parser.add_argument("library", help="directory of the Calibre library")

parser.add_argument("missing", choices=['paths', 'files', 'status'],
                    help="choose what problem to find")

args = parser.parse_args()

CALIBRE_DIR = pathlib.Path(args.library)
CALIBRE_DB = pathlib.Path(CALIBRE_DIR, "metadata.db")


#### Check the library

# expand to a real check later
#print(CALIBRE_DB.exists())

con = sqlite3.connect(CALIBRE_DB)

cursor = con.cursor()

cursor.execute("select id, author_sort, title, path from books order by path;")
books = [Book(*b) for b in cursor.fetchall()]

def find_missing_paths():
    return [b for b in books if not b.exists]

def find_missing_files():
    return [b for b in books if not b.has_files]

if args.missing == 'paths':
    problems = find_missing_paths()
elif args.missing == 'files':
    problems = find_missing_files()
elif args.missing == 'status':
    f = find_missing_files()
    p = find_missing_paths()
    problems = [f"Missing paths: {len(p)}", f"Missing files: {len(f)}"]
else:
    problems = []

if not problems:
    print("No problems found!")
else:
    for prob in problems:
        print(prob)