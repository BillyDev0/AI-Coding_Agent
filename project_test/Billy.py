def sistem_kasir():
    print('--- Selamat Datang di Sistem Kasir ---')
    total = 0
    while True:
        nama_barang = input('Masukkan nama barang (atau ketik "selesai" untuk berhenti): ')
        if nama_barang.lower() == 'selesai':
            break
        try:
            harga = float(input(f'Masukkan harga {nama_barang}: '))
            total += harga
        except ValueError:
            print('Harga harus berupa angka.')
    print(f'Total belanja Anda adalah: Rp{total}')

if __name__ == '__main__':
    sistem_kasir()