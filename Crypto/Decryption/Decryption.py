############################Headers
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
######################################Reading the image
import numpy as np
from PIL import Image
img = Image.open('steg.png')
x = np.array(img)
#print(x)
#######################################Getting private Key
fi=open('privatekey2.pem','r')
privateKey = RSA.importKey(fi.read())
#print(privateKey)
######################################Decoding the image into data

import numpy as np
decr=np.array(img)
decr.resize(4096,)
#print(decr)
for x in range(4096):
    decr[x]=decr[x]&1
token=bytearray([])
for ex in range(512):
    bok=""
    for why in range(8):
        bok=bok+str(decr[8*ex+why])
    bokk=int(bok,2)
    #tempArr=bokk.to_bytes(1,byteorder='big')
    token.append(bokk)
token = bytes(token)
#print(token)
######################################Decryption
def decrypt(ciphertext, priv_key):
   cipher = PKCS1_OAEP.new(priv_key)
   return cipher.decrypt(ciphertext)

def sign(message, priv_key, hashAlg = "SHA-256"):
   global hash
   hash = hashAlg
   signer = PKCS1_v1_5.new(priv_key)
   
   if (hash == "SHA-512"):
      digest = SHA512.new()
   elif (hash == "SHA-384"):
      digest = SHA384.new()
   elif (hash == "SHA-256"):
      digest = SHA256.new()
   elif (hash == "SHA-1"):
      digest = SHA.new()
   else:
      digest = MD5.new()
   digest.update(message)
   return signer.sign(digest)

def verify(message, signature, pub_key):
   signer = PKCS1_v1_5.new(pub_key)
   if (hash == "SHA-512"):
      digest = SHA512.new()
   elif (hash == "SHA-384"):
      digest = SHA384.new()
   elif (hash == "SHA-256"):
      digest = SHA256.new()
   elif (hash == "SHA-1"):
      digest = SHA.new()
   else:
      digest = MD5.new()
   digest.update(message)
   return signer.verify(digest, signature)

print("Harsha says: ",end="")
print(decrypt(token,privateKey))
############################################