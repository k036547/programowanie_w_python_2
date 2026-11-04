class FileWriter:
    def __init__(self, filename):
        self.filename = filename
        self.file = None

    def __enter__(self):
        self.file = open(self.filename, 'wt', encoding='utf-8')
        print(f"Plik {self.filename} został otwarty do zapisu.")
        return self.file

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is not None:
            print(f"Błąd podczas zapisu: {exc_value}")            
        if self.file:
            self.file.close()
            print(f"Plik {self.filename} został zamknięty.")
        return False
        
with FileWriter("output.txt") as f:
    f.write("Hello, World!\n")
    x=7/0
    f.write("Hello, World2!\n")
