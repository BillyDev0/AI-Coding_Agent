from project_test.calculator import calcultor

while Tr:
    try:
        calculator()
        lanjut = input("Lanjut (y/n): ")
        if not lanjut or lanjut.lower() == 'n':
            brea
    except (EOFError, KeyboardInterrupt):
        print("\nProgram dihentikan.")
        break