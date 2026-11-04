class SafeDivision:
    def __init__(self):
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is ZeroDivisionError:
            print("Nie można dzielić przez zero.")
            return True
        else:
            return False

    def divide(self, a, b): 
        return a / b

with SafeDivision() as sd:
    print(f"Result: {sd.divide(10, 5)}")
    print(f"Result: {sd.divide(10, 3)}")
    print(f"Result: {sd.divide(10, 0)}")