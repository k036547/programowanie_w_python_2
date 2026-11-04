class Logger:
    def __init__(self, name):
        self.name = name

    def __enter__(self):
        print("Start sekcji logowania")

    def __exit__(self, exc_type, exc_value, traceback):
        print("Koniec sekcji logowania")

with Logger("MyLogger") as logger:
    print("Wewnątrz sekcji logowania")