
from array import array
from email import message
from telnetlib import SB
import numpy as np
from BitVector import *
from pathlib import Path
import time


k = 512

def getprime(k):
    bv = BitVector(intVal = 0)
    bv = bv.gen_random_bits(k)  
    check = bv.test_for_primality()

    while check==0:
        bv = BitVector(intVal = 0)
        bv = bv.gen_random_bits(k)  
        check = bv.test_for_primality()
    return bv

def getE(phi_n):
    phi_n = BitVector(intVal=phi_n)
    bv = BitVector(intVal = 0)
    bv = bv.gen_random_bits(phi_n.count_bits())
    gcd = bv.gcd(phi_n)
    gcd = gcd.intValue()

    while gcd!=1 or bv.intValue()==0:
        bv = BitVector(intVal = 0)
        bv = bv.gen_random_bits(phi_n.count_bits())
        gcd = bv.gcd(phi_n)
        gcd = gcd.intValue()
    return bv


# def getD1(e, phi_n):
#     de = phi_n+1
#     i = 1

#     while de%e!=0:
#         i = i+1
#         de = phi_n*i + 1
#     return int(de//e)

# d = getD(e, phi_n)

def getD(e, phi_n):
    return e.multiplicative_inverse(BitVector(intVal=phi_n))


def getKeys(k):
    p = getprime(int(k//2))
    q = getprime(int(k//2))

    while p==q:
        q = getprime(int(k//2))

    n = p.intValue()*q.intValue()
    phi_n = (p.intValue()-1)*(q.intValue()-1)

    e = getE(phi_n)
    
    d = getD(e, phi_n)

    d = d.intValue()
    e = e.intValue()

    return e, d, n



def encryptRSA(matrix, n, e):
    cmatrix = matrix.copy()
    for i in range(len(matrix)):
        cmatrix[i] = pow(matrix[i], e, n)
    return cmatrix

def decryptRSA(cmatrix, n, d):
    matrix = cmatrix.copy()
    for i in range(len(cmatrix)):
        matrix[i] = pow(cmatrix[i], d, n)
    return matrix



def convertTextToMatrix(text):
    ascii_values = []
    for character in text:
        ascii_values.append(ord(character))

    return ascii_values

def convertMatrixToText(matrix):
    text = "".join([chr(value) for value in matrix])
    return text


def encrypt(text, k):
    
    e, d, n = getKeys(k)

    dir = Path(__file__).resolve().parents[1]
    dir = dir / "Don't Open this" / 'secretFile.txt'

    with open(dir, 'w') as file:
        file.write(','.join([str(d), str(n)]))
        file.write('\n')

    matrix = convertTextToMatrix(text)
    matrix = encryptRSA(matrix, n, e)
   
    return matrix, [e, n]


def decrypt(matrix):
    dir = Path(__file__).resolve().parents[1]
    dir = dir / "Don't Open this" / 'secretFile.txt'
    with open(dir, 'r') as file:
        pk = file.read()
        pk = pk.split(",")

    matrix = decryptRSA(matrix, int(pk[1]), int(pk[0]))
    return convertMatrixToText(matrix)


def timeMeasure(text, k):
    tic = time.perf_counter()
    getKeys(k)
    toc = time.perf_counter()
    kstime = toc - tic

    tic = time.perf_counter()
    matrix, [e, n] = encrypt(text, k)
    toc = time.perf_counter()
    entime = toc - tic

    tic = time.perf_counter()
    text = decrypt(matrix)
    toc = time.perf_counter()
    detime = toc - tic
    print("k: ", k)
    print("key gen: ", kstime)
    print("Encryption: ", entime)
    print("Decryption: ", detime)



# text = "RSA implementation"

# timeMeasure(text, 16)
# timeMeasure(text, 32)
# timeMeasure(text, 64)
# timeMeasure(text, 128)






# matrix, [e, n] = encrypt("hello", 64)
# print(matrix)
# text = decrypt(matrix)
# print(text)
