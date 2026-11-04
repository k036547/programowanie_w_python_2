class FileWriter:
    def __init__(self, filename):
        self.filename = filename
        self.file = None

    def __enter__(self):
        self.file = open(self.filename, 'wt')
        print(f"Plik {self.filename} został otwarty do zapisu.")
        return self.file
    
    def __exit__(self, exc_type, exc_value, traceback):
        if self.file:
            self.file.close()
            print(f"Plik {self.filename} został zamknięty.")
        else:
            print("Plik nie został zamknięty bo nie został wcześniej otwarty lub wystąpił błąd podczas otwierania.")

with FileWriter("output.txt") as f:
    f.write("Hello, World!\n")