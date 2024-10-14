
from array import array
from email import message
from os import read
from telnetlib import SB
import numpy as np
from BitVector import *
import time


Sbox = (
    0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76,
    0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0,
    0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15,
    0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75,
    0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84,
    0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF,
    0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8,
    0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2,
    0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73,
    0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB,
    0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79,
    0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08,
    0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A,
    0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E,
    0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF,
    0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16,
)

InvSbox = (
    0x52, 0x09, 0x6A, 0xD5, 0x30, 0x36, 0xA5, 0x38, 0xBF, 0x40, 0xA3, 0x9E, 0x81, 0xF3, 0xD7, 0xFB,
    0x7C, 0xE3, 0x39, 0x82, 0x9B, 0x2F, 0xFF, 0x87, 0x34, 0x8E, 0x43, 0x44, 0xC4, 0xDE, 0xE9, 0xCB,
    0x54, 0x7B, 0x94, 0x32, 0xA6, 0xC2, 0x23, 0x3D, 0xEE, 0x4C, 0x95, 0x0B, 0x42, 0xFA, 0xC3, 0x4E,
    0x08, 0x2E, 0xA1, 0x66, 0x28, 0xD9, 0x24, 0xB2, 0x76, 0x5B, 0xA2, 0x49, 0x6D, 0x8B, 0xD1, 0x25,
    0x72, 0xF8, 0xF6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xD4, 0xA4, 0x5C, 0xCC, 0x5D, 0x65, 0xB6, 0x92,
    0x6C, 0x70, 0x48, 0x50, 0xFD, 0xED, 0xB9, 0xDA, 0x5E, 0x15, 0x46, 0x57, 0xA7, 0x8D, 0x9D, 0x84,
    0x90, 0xD8, 0xAB, 0x00, 0x8C, 0xBC, 0xD3, 0x0A, 0xF7, 0xE4, 0x58, 0x05, 0xB8, 0xB3, 0x45, 0x06,
    0xD0, 0x2C, 0x1E, 0x8F, 0xCA, 0x3F, 0x0F, 0x02, 0xC1, 0xAF, 0xBD, 0x03, 0x01, 0x13, 0x8A, 0x6B,
    0x3A, 0x91, 0x11, 0x41, 0x4F, 0x67, 0xDC, 0xEA, 0x97, 0xF2, 0xCF, 0xCE, 0xF0, 0xB4, 0xE6, 0x73,
    0x96, 0xAC, 0x74, 0x22, 0xE7, 0xAD, 0x35, 0x85, 0xE2, 0xF9, 0x37, 0xE8, 0x1C, 0x75, 0xDF, 0x6E,
    0x47, 0xF1, 0x1A, 0x71, 0x1D, 0x29, 0xC5, 0x89, 0x6F, 0xB7, 0x62, 0x0E, 0xAA, 0x18, 0xBE, 0x1B,
    0xFC, 0x56, 0x3E, 0x4B, 0xC6, 0xD2, 0x79, 0x20, 0x9A, 0xDB, 0xC0, 0xFE, 0x78, 0xCD, 0x5A, 0xF4,
    0x1F, 0xDD, 0xA8, 0x33, 0x88, 0x07, 0xC7, 0x31, 0xB1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xEC, 0x5F,
    0x60, 0x51, 0x7F, 0xA9, 0x19, 0xB5, 0x4A, 0x0D, 0x2D, 0xE5, 0x7A, 0x9F, 0x93, 0xC9, 0x9C, 0xEF,
    0xA0, 0xE0, 0x3B, 0x4D, 0xAE, 0x2A, 0xF5, 0xB0, 0xC8, 0xEB, 0xBB, 0x3C, 0x83, 0x53, 0x99, 0x61,
    0x17, 0x2B, 0x04, 0x7E, 0xBA, 0x77, 0xD6, 0x26, 0xE1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0C, 0x7D,
)

Mixer = [
    [BitVector(hexstring="02"), BitVector(hexstring="03"), BitVector(hexstring="01"), BitVector(hexstring="01")],
    [BitVector(hexstring="01"), BitVector(hexstring="02"), BitVector(hexstring="03"), BitVector(hexstring="01")],
    [BitVector(hexstring="01"), BitVector(hexstring="01"), BitVector(hexstring="02"), BitVector(hexstring="03")],
    [BitVector(hexstring="03"), BitVector(hexstring="01"), BitVector(hexstring="01"), BitVector(hexstring="02")]
]

InvMixer = [
    [BitVector(hexstring="0E"), BitVector(hexstring="0B"), BitVector(hexstring="0D"), BitVector(hexstring="09")],
    [BitVector(hexstring="09"), BitVector(hexstring="0E"), BitVector(hexstring="0B"), BitVector(hexstring="0D")],
    [BitVector(hexstring="0D"), BitVector(hexstring="09"), BitVector(hexstring="0E"), BitVector(hexstring="0B")],
    [BitVector(hexstring="0B"), BitVector(hexstring="0D"), BitVector(hexstring="09"), BitVector(hexstring="0E")]
]

RCon = [
    [0x01, 0x00, 0x00, 0x00],
    [0x02, 0x00, 0x00, 0x00],
    [0x04, 0x00, 0x00, 0x00],
    [0x08, 0x00, 0x00, 0x00],
    [0x10, 0x00, 0x00, 0x00],
    [0x20, 0x00, 0x00, 0x00],
    [0x40, 0x00, 0x00, 0x00],
    [0x80, 0x00, 0x00, 0x00],
    [0x1B, 0x00, 0x00, 0x00],
    [0x36, 0x00, 0x00, 0x00]
]

def subBytes(matrix):
    for i in range(4):
        for j in range(4):
            matrix[i][j] = Sbox[matrix[i][j]]


def inverseSubBytes(matrix):
    for i in range(4):
        for j in range(4):
            matrix[i][j] = InvSbox[matrix[i][j]]


def shiftRows(matrix):
    tempMatrix = matrix.copy()
    for i in range(4):
        matrix[1][i] = tempMatrix[1][(i+1)%4]
        matrix[2][i] = tempMatrix[2][(i+2)%4]
        matrix[3][i] = tempMatrix[3][(i+3)%4]


def InvShiftRows(matrix):
    tempMatrix = matrix.copy()
    for i in range(4):
        matrix[1][i] = tempMatrix[1][(i-1)%4]
        matrix[2][i] = tempMatrix[2][(i-2)%4]
        matrix[3][i] = tempMatrix[3][(i-3)%4]


def mixCollumn(matrix):
    ans = [[0 for x in range(4)] for y in range(4)] 
    for i in range(4):
        for j in range(4):
            for k in range(4):
                AES_modulus = BitVector(bitstring='100011011')
                bv1 = BitVector(intVal= matrix[k][j], size=8)
                val = Mixer[i][k].gf_multiply_modular(bv1, AES_modulus, 8) 
                ans[i][j] = ans[i][j]^val.intValue()
    return ans

def invMixCollumn(matrix):
    ans = [[0 for x in range(4)] for y in range(4)] 
    for i in range(4):
        for j in range(4):
            for k in range(4):
                AES_modulus = BitVector(bitstring='100011011')
                bv1 = BitVector(intVal= matrix[k][j], size=8)
                val = InvMixer[i][k].gf_multiply_modular(bv1, AES_modulus, 8) 
                ans[i][j] = ans[i][j]^val.intValue()
    return ans

def addRoundKey(matrix, keyMatrix):
    for i in range(4):
        for j in range(4):
            matrix[i][j] = matrix[i][j] ^ keyMatrix[i][j]


def XORWords(X, Y):
    ans = X.copy()
    for i in range(4):
        ans[i] = X[i]^Y[i]
    return ans


def expandKeys(keyMatrix):
    temp = keyMatrix.copy()
    temp = np.transpose(temp)
    total = temp.copy()
    # print(total)
    
    for i in range(10):
        w3 = total[-1].copy()
       
        w3temp =total[-1].copy()
        #rotate w3
        for j in range(4):
            w3[(j-1)%4] = w3temp[j]
        
       
        #subbyte w3
        for j in range(4):
            w3[j] = Sbox[w3[j]]
        # W0 xor W3 = W4

        w0 = total[i*4].copy()
        w4 = XORWords(w0, w3)
        w4 = XORWords(w4, RCon[i])

        total = np.vstack([total,w4])

        for j in range(1, 4):
            w5 = XORWords(total[-1] , total[i*4+j])
            total = np.vstack([total,w5])
    
    return total


    
def encrypt128(message, totalkeys, keyMatrix):
    matrix = convertTextToMatrix(message)
    

    addRoundKey(matrix, keyMatrix)

    for i in range(9):
        subBytes(matrix)
        
        shiftRows(matrix)
        matrix = mixCollumn(matrix)
        matrix = np.asanyarray(matrix)
        addRoundKey(matrix, np.transpose(totalkeys[(i+1)*4: (i+1)*4+4]))
        
    
    subBytes(matrix)
    shiftRows(matrix)
    addRoundKey(matrix, np.transpose(totalkeys[len(totalkeys)-4:len(totalkeys)]))

    return convertMatrixToText(matrix)

def decrypt128(message, totalkeys):
    matrix = convertTextToMatrix(message)
    # keyMatrix = convertTextToMatrix(key)

    # totalkeys = expandKeys(keyMatrix)

    addRoundKey(matrix, np.transpose(totalkeys[len(totalkeys)-4:len(totalkeys)]))
    InvShiftRows(matrix)
    inverseSubBytes(matrix)

    for i in range(9, 0, -1):
        addRoundKey(matrix, np.transpose(totalkeys[(i)*4: (i)*4+4]))
        matrix = invMixCollumn(matrix)
        matrix = np.asanyarray(matrix)
        InvShiftRows(matrix)
        inverseSubBytes(matrix)

    addRoundKey(matrix, np.transpose(totalkeys[0 : 4]))

    return convertMatrixToText(matrix)

def convertTextToMatrix(text):
    ascii_values = []
    for character in text:
        ascii_values.append(ord(character))

    matrix = [list(ascii_values[i:i+4]) for i in range(0, len(ascii_values), 4)]
    matrix = np.asarray(matrix)
    matrix = np.transpose(matrix)
    return matrix

def convertMatrixToText(matrix):
    matrix = np.transpose(matrix)
    matrix = matrix.flatten()
    # print(matrix)
    text = "".join([chr(value) for value in matrix])
    return text

def readFile(filename):
    with open(filename, "rb") as nfile:
        f = nfile.read()
        b = bytearray(f)
        return b

def writeFile(filename, text):
    barray = bytearray()
    barray.extend(map(ord, text))
    
    with open(filename, "wb") as binary_file:
        # Write bytes to file
        for i in range(len(barray)):
            binary_file.write(barray[i].to_bytes(1,"big"))


def encryptFile(filename, key):
    key = pad(key)
    keyMatrix = convertTextToMatrix(key)

    totalkeys = expandKeys(keyMatrix)

    b = readFile(filename)
    entext = ""
    r = int(len(b)//16)+1
    for i in range(r):
        matrix = b[i*16: i*16+16]
        text = "".join([chr(value) for value in matrix])
        if(len(text)<16):
            text = pad(text)
        # print(text)
        text1 = encrypt128(text, totalkeys, keyMatrix)
        entext+=text1
        # print(entext)
    return entext

def decryptFile(entext, key):
    detext = ""
    r = len(entext)//16
    key = pad(key)
    keyMatrix = convertTextToMatrix(key)

    totalkeys = expandKeys(keyMatrix)

    for i in range(int(r)):
        text = entext[i*16: i*16+16]
        text = decrypt128(text, totalkeys)
        detext+=text
    return detext


def pad(text):
    if(len(text)<16):
        text+=" "*(16-len(text))
    elif len(text)>16:
        text = text[0:16]
    return text

def encryptString(text, key):
    key = pad(key)
    keyMatrix = convertTextToMatrix(key)

    totalkeys = expandKeys(keyMatrix)

    entext = ""
    r = int(len(text)//16)+1
    for i in range(r):
        t = text[i*16: i*16+16]
        t = pad(t)
        # print(text)
        text1 = encrypt128(t, totalkeys, keyMatrix)
        entext+=text1
        # print(entext)
    return entext

def decryptString(entext, key):
    key = pad(key)
    keyMatrix = convertTextToMatrix(key)

    totalkeys = expandKeys(keyMatrix)
    detext = ""
    r = len(entext)//16
    for i in range(int(r)):
        text = entext[i*16: i*16+16]
        text = decrypt128(text, totalkeys)
        detext+=text
    return detext


def stringToHex(text):
    return text.encode("utf_8").hex()


# if __name__ == '__main__':
    # print("begins")
    # np.set_printoptions(formatter={'int':hex})
    # key = "Thats my sing Fu"
    # mes = "Two One five Two"
    # text = encrypt128(mes, key)
    # print(text)

    # text2 = decrypt128(text, key)
    # print(text2)

    # entext = encryptFile("icon.png", key)
    # print(entext)
    # detext = decryptFile(entext, key)
    # print(detext)

    # writeFile("icon1.png", detext)

    # msg = "no no no no la la la la la la la la la "
    # entext = encryptString(msg, key)
    # detext = decryptString(entext, key)
    # print(detext)

    

    # offline spec

    # print("Plain Text: ")
    # pt = str(input())

    # padsize = 16 - len(pt)%16

    # print("Key: ")
    # key = str(input())

    # keyy = pad(key)
    # keyMatrix = convertTextToMatrix(keyy)

    # tic = time.perf_counter()
    # totalkeys = expandKeys(keyMatrix)
    # toc = time.perf_counter()
    # kstime = toc - tic


    # tic = time.perf_counter()
    # entext = encryptString(pt, key)
    # toc = time.perf_counter()
    # entime = toc - tic - kstime

    # tic = time.perf_counter()
    # detext = decryptString(entext, key)
    # toc = time.perf_counter()
    # dctime = toc - tic - kstime

    # print("Plain Text:")
    # print(pt, "[in ASCII]")
    # print(stringToHex(pt), "[in Hex]")

    # print("Key:")
    # print(key, "[in ASCII]")
    # print(stringToHex(key), "[in Hex]")

    # print("Cipher Text:")
    # print(entext, "[in ASCII]")
    # print(stringToHex(entext), "[in Hex]")
    
    # detext = detext[:-padsize]
    # print("Deciphered Text:")
    # print(detext, "[in ASCII]")
    # print(stringToHex(detext), "[in Hex]")

    # print("Execution Time")
    # print("Key Scheduling: ", kstime, "seconds")
    # print("Encryption Time: ", entime, "seconds")
    # print("Decryption Time: ", dctime, "seconds")

    


