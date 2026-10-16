def calculator():
    def tambah(a, b):
        return a + b 

    def kurang(a, b):
        return a - b  

    def kali(a, b):
        return a * b

    def cek_ganjil_genap(n):
        return "Genap" if n % 2 == 0 else "Ganjil"

    print("=========================")
    print("   KALKULATOR SEDERHANA  ")
    print("=========================")
    print("1. Tambah")
    print("2. Kurang")
    print("3. Kali")
    print("4. Cek Ganjil/Genap")
    print("=========================")

    pilihan = input("Pilih operasi (1, 2, 3, atau 4): ")
    try:
        if pilihan == "4":
            n = int(input("Masukkan angka: "))
        else:
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
    elif pilihan == "4":
        print("Hasil:", cek_ganjil_genap(n))
    else:
        print("Pilihan tidak valid")