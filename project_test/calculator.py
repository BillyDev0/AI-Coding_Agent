def calculator():
    def tambah(a, b):
        return a + b

    def kurang(a, b):
        return a - b

    def kali(a, b):
        return a * b

    def bagi(a, b):
        return a / b

    print("Calculator")
    print("1. Tambah")
    print("2. Kurang")
    print("3. Kali")
    print("4. Bagi")

    pilihan = input("Pilih operasi: ")
    a = float(input("Angka pertama: "))
    b = float(input("Angka kedua: "))

    if pilihan == "1":
        print("Hasil:", tambah(a, b))
    elif pilihan == "2":
        print("Hasil:", kurang(a, b))
    elif pilihan == "3":
        print("Hasil:", kali(a, b))
    elif pilihan == "4":
        print("Hasil:", bagi(a, b))
    else:
        print("Pilihan tidak valid")