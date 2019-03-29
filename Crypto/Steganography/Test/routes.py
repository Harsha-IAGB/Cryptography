from flask import render_template, url_for, flash, redirect, request, Flask
from Test import app, bcrypt
import secrets
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import time
from werkzeug import secure_filename
import smtplib
import imaplib
import email
import time
from PIL import Image
####################################Headers
import cryptography as cr
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA512, SHA384, SHA256, SHA, MD5
from Crypto import Random
from base64 import b64encode, b64decode
import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np
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
############################################

@app.route("/")
def compose():
    return render_template('compose.html', title='Compose')

emailId="hacchibhai44@gmail.com"
password="Hacchi44/gmail"
#######---------------------------------------###########################
def stega(message,filename):
    ####################################Getting the public Key
    f = open('publickey2.pem','r')
    publicKey = RSA.importKey(f.read())
    #print(publicKey)
    ####################################Encoding the message into bytes
    bytesOfMessage = message.encode('utf-8')
    cipher=encrypt(bytesOfMessage,publicKey)
    #print(cipher)
    ######################################Converting text into a 64x64 matrix and inserting data into image
    #############
    img=cv.imread(filename,0)
    ##############
    
    x=np.array([],dtype=int)
    get_bin = lambda x, n: format(x, 'b').zfill(n)
    for i in range(512):
        temp=get_bin(cipher[i],8)
        for j in range(8):
            x=np.append(x,int(temp[j]))
    #print(x.shape)
    x.resize(64,64)
    for i in range(64):
        for j in range(64):
            img[i][j]=img[i][j]&254
            img[i][j]=x[i][j]+img[i][j]
    print("steganised image: \n",img)
    ######################################Imagifying
    cv.imwrite("steg.png",img)
################------------------------------##################################


@app.route('/emailSent', methods=['POST', 'GET'])
def result():
    if request.method == 'POST':
        result = request.form
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(emailId, password)
        if request.method == 'POST':
            f = request.files['file']
            f.save(secure_filename(f.filename))
###################
        message=result['message']
        filename = f.filename
        stega(message,filename)
###################
        msg = MIMEMultipart()
        msg['From'] = emailId
        msg['To'] = result['to']
        msg['Subject'] = result['subject']
        body = "LOOK AND YOU SHALL FIND"#result['message']
        msg.attach(MIMEText(body, 'plain'))
        filename = "steg.png"#f.filename
        attachment = open(filename, "rb")
        p = MIMEBase('application', 'octet-stream')
        p.set_payload((attachment).read())
        encoders.encode_base64(p)
        #filename = "steg.png"
        p.add_header('Content-Disposition',"attachment; filename= %s" % filename)
        msg.attach(p)
        message = msg.as_string()
        server.sendmail(emailId, result['to'], message)
        server.quit()
    flash('Email has been succesfully sent', 'success')
    return redirect(url_for('compose'))