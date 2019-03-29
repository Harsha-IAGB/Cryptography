####################################Encryption
import cryptography as cr
message = "Harsha is a good boy"
####################################Headers
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA512, SHA384, SHA256, SHA, MD5
from Crypto import Random
from base64 import b64encode, b64decode
hash = "SHA-256"

def newkeys(keysize):
   random_generator = Random.new().read
   key = RSA.generate(keysize, random_generator)
   private, public = key, key.publickey()
   return public, private

def importKey(externKey):
   return RSA.importKey(externKey)

def getpublickey(priv_key):
   return priv_key.publickey()

def encrypt(message, pub_key):
   cipher = PKCS1_OAEP.new(pub_key)
   return cipher.encrypt(message)
####################################Getting the public Key
f = open('publickey2.pem','r')
publicKey = RSA.importKey(f.read())
print(publicKey)
####################################Encoding the message into bytes
bytesOfMessage = message.encode('utf-8')
#print(bytesOfMessage)
cipher=encrypt(bytesOfMessage,publicKey)
#print(type(cipher))
print(cipher)
######################################Converting text into a 64x64 matrix and inserting data into image
#############
import cv2 as cv
import matplotlib.pyplot as plt
img=cv.imread('test1.jpg',0)
#cv.imshow('image',img)
print(img.shape)
#cv.waitKey(0)
##############

import numpy as np
x=np.array([],dtype=int)
get_bin = lambda x, n: format(x, 'b').zfill(n)
for i in range(512):
    temp=get_bin(cipher[i],8)
    for j in range(8):
        x=np.append(x,int(temp[j]))
print(x.shape)
x.resize(64,64)
#print("data: ",x)
#print("image: ",img)
for i in range(64):
    for j in range(64):
        img[i][j]=img[i][j]&254
        img[i][j]=x[i][j]+img[i][j]
#np.bitwise_and
print("steganised image: \n",img)
######################################Imagifying
cv.imwrite("steg.png",img)