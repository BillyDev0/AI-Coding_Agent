from project_test.calculator import calculator

while True:
    try:
        calculator()
        lanjut = input("Lanjut (y/n): ")
        if not lanjut or lanjut.lower() == 'n':
            break
    except (EOFError, KeyboardInterrupt):
        print("\nProgram dihentikan.")
        break