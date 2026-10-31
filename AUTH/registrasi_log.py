from passlib.hash import bcrypt
from DB.setup import User,get_db
from AUTH.jwt_auth import create_token


def input_user_pw():
    username=str(input('username: ')).strip()
    password=str(input("password: ")).strip()
    return username,password

def regist():
    while True:
        username,password=input_user_pw()
        db=get_db()
        if not username or username is None:
            print("username tidak boleh kosong")
            continue
            

        if not password or password is None:
            print("username tidak boleh kosong")
        
        cek_user=db.query(User).filter(username==User.username).first()

        if cek_user:
            print("username sudah dipakai")
            continue

        hash_pw=bcrypt.hash(password)

        new_user=User(username=username,password=hash_pw)
        db.add(new_user)
        db.commit()
        db.close()

        token=create_token(username)
        print('REGISTRASI BERHASIL')

        return token

def login():
    while True:
        username,password=input_user_pw()
        db=get_db()
        if not username or username is None:
            print("username tidak boleh kosong")
            continue

        if not password or password is None:
            print("username tidak boleh kosong")
            continue
        
        cek_user=db.query(User).filter(User.username==username).first()
        
        if not cek_user:
            print("username tidak ditemukan")
            continue

        if not bcrypt.verify(password,cek_user.password):
            print("password salah")
            continue

        db.close()
        token=create_token(cek_user.username)
        print("LOGIN BERHASIL")
        
        return token


# a=input('username: ')
# b=input("password: ")
# print(login(a,b))