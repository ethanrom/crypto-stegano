import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

# 1.Hybrid (AES & RSA) Algorithm.
# To get the Secret text data for Encryption...
file_path = filedialog.askopenfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
if file_path == "":
    messagebox.showwarning(title="User Pressed Cancel", message="User Pressed Cancel")
else:
    with open(file_path, "rb") as f:
        data = f.read()
    ranka = data[:16]  # Pull odd Part (starts at 1)
    rankb = data[16:32]  # Pull even Part (starts at 17)

    data_text_AES = ranka
    data_text_RSA = rankb

# AES ENCRYPTION ...
s_box = AES.build_sbox()
key = os.urandom(16)
cipher_AES = AES.new(key, AES.MODE_ECB)
plaintext_AES = pad(data_text_AES, AES.block_size)
ciphertext_AES = cipher_AES.encrypt(plaintext_AES)

# RSA ENCRYPTION...
print('Implementation of RSA Algorithm')
p = int(input('Enter the value of p: '))
q = int(input('Enter the value of q: '))
key = RSA.generate(1024, e=65537)
public_key = key.publickey()
cipher_RSA = PKCS1_OAEP.new(public_key)
MAsg = data_text_RSA
Length_1 = len(MAsg)
cipher_RSA_text = [cipher_RSA.encrypt(bytes([MAsg[i]])) for i in range(Length_1)]
print('Cipher_RSA Text of the entered Message:')
print(cipher_RSA_text)

# Hybrid BOTH CIPHER TEXT..
Cipher_Test = ciphertext_AES + b''.join(cipher_RSA_text)
print('Cipher Text of the Original Message:')
print(Cipher_Test)

# Write cipher text to a file
with open('cipher.txt', 'wb') as f:
    f.write(Cipher_Test)
