from agent import run_agent,straming_model
from AUTH.registrasi_log import login,regist
from AUTH.jwt_auth import verif_token


def tampilan_input():
    while True:
        try:
            print("\n\n1. LOGIN\n2. REGISTRASI")
            pilihan_masuk=str(input("pilih (angka): ")).strip()
            if pilihan_masuk == '':
                continue
            if pilihan_masuk == '1':
                return login()

            elif pilihan_masuk == '2':
                return regist()

        except KeyboardInterrupt:
            print("Program dihentikan oleh pengguna melalui keyboard.")
            continue


def main():
        token=tampilan_input()
        while True:
            list_result_tools=[]
            try:
                prompt=input('masukan prompt (ketik "quit" jika sudah): ')
                if prompt == 'quit':
                    print('PROGRAM SELESAI')
                    break
                elif prompt == '':
                    continue

                result_agent,source=run_agent(token,prompt,list_result_tools)
                if result_agent == "token anda mengalami masalah":
                        print(result_agent)
                        break
                straming_model(result_agent,source)

            except KeyboardInterrupt:
                print("Program dihentikan oleh pengguna melalui keyboard.")

            except EOFError:
                print("Input tidak tersedia.")

        

if __name__=="__main__":
        main()

