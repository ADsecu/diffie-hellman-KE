import os
import sys
from utils import chilkat


def clear_screen():
    are_you_windows = os.name == "nt"
    if are_you_windows:
        os.system("cls")
    else:
        os.system("clear")
clear_screen()

Adh = chilkat.CkDh()
Bdh = chilkat.CkDh()

success = Adh.UnlockComponent("Test")
Adh.UseKnownPrime(5)

p = Adh.p()
g = Adh.get_G()
success = Bdh.SetPG(p,g)

eA = Adh.createE(256)
eB = Bdh.createE(256)
kA = Adh.findK(eB)
kB = Bdh.findK(eA)

if kA == kB:
    eq = 'A shared secret equal to B'

else:
    eq = '**Shared secret NOT EQUAL !!!!**'


crypt = chilkat.CkCrypt2()
success = crypt.UnlockComponent("Test")

crypt.put_EncodingMode("hex")
crypt.put_HashAlgorithm("md5")
sessionKey = crypt.hashStringENC(kA)
sessionm = '128-bit Season key : {}'.format(sessionKey)


#  Encrypt something...
crypt.put_CryptAlgorithm("aes")
crypt.put_KeyLength(128)
crypt.put_CipherMode("cbc")


iv = crypt.hashStringENC(sessionKey)

ivm = 'Initialization Vector: {}'.format(iv)

crypt.SetEncodedKey(sessionKey,"hex")
crypt.SetEncodedIV(iv,"hex")
print('-> {}\n--> {}'.format(sessionm, ivm))
#  Encrypt some text:
print("""

""")
crypt.put_EncodingMode("base64")

list = []

def Encrypt_text(text):
    cipherText64 = crypt.encryptStringENC(text)
    list.append(cipherText64)
    print('+ Encrypted -> '+cipherText64)



print('''
  Choose :
  [1] Encrypt text
  [2] decode text (For this Session only)
  [3] List all Encrypted texts
  [4] Exit''')
while True:

    choose = input('>> ')
    if choose == 'h':
        print("""
  Choose :
  [1] Encrypt text
  [2] decode text (For this Session only)
  [3] List all Encrypted texts
  [4] Exit
    """)
    elif choose == '1':
        choosen = input('Encrypt text >> ')
        Encrypt_text(choosen)
    elif choose == '2':
        choosen = input('decode text >> ')
        plainText = crypt.decryptStringENC(choosen)
        print(plainText)
    elif choose == '3':
        count = 1
        for i in list:
            print('{} - {}'.format(count, i))
            count = count + 1
    elif choose == '4':
        print('Good Bye')
        sys.exit()
    else:
        print('invaild number, type [h] for help or 4 for exit')
