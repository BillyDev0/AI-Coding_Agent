def calculator():
    def tambah(a, b):
        return a + b 

    def kurang(a, b):
        return a - b  

    def kali(a, b):
        return a * b

    print("=========================")
    print("   KALKULATOR SEDERHANA  ")
    print("=========================")
    print("1. Tambah")
    print("2. Kurang")
    print("3. Kali")
    print("=========================")

    pilihan = input("Pilih operasi (1, 2, atau 3): ")
    try:
        a = float(input("Angka pertama: "))
        b = float(input("Angka kedua: "))
    except ValueError:
        print("Error: Input tidak valid. Harap masukkan angka.")
        return

    if pilihan == "1":
        print("Hasil:", tambah(a, b))
    elif pilihan == "2":
        print("Hasil:", kurang(a, b))
    elif pilihan == "3":
        print("Hasil:", kali(a, b))
    else:
        print("Pilihan tidak valid")