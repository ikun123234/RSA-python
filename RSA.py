'''
@Author: borgeous
@Time :2024/5/12

'''
from random import randint
import random
import math
import sys
import argparse

#将字符转化为ASCII码

def Char2Ascii(text):
    Output = []
    for i in text:
        Output.append(ord(i))
    return Output

#将ASCII码变为十六进制

def Ascii2Hex(text):
    Output = ''
    for i in text:
        Output = Output + str(hex(i)).split('x')[1]
    return Output

#将十六进制转化为十进制

def Hex2Dec(HexNum):
    DecNum = int(HexNum,16)
    return DecNum

#将十进制转化为十六进制

def Dec2Hex(DecNum):
    HexNum = hex(DecNum)
    return HexNum    

#随机产生两个大素数
def is_prime(num):
    if num < 2:
        return False
    for i in range(2, int(math.sqrt(num)) + 1):
        if num % i == 0:
            return False
    return True

def generate_prime_number(min_value):
    while True:
        num = random.randint(min_value, min_value*10)
        if is_prime(num):
            return num

def generate_key_pair_and_write_files():
    p = generate_prime_number(10**10)  # 生成大于10^10的素数p
    q = generate_prime_number(10**10)  # 生成大于10^10的素数q
    n = p * q  # 计算n
    phi_n = (p - 1) * (q - 1)  # 计算phi(n)

    # 选择与phi(n)互素且小于phi(n)的整数e
    e = random.randint(2, phi_n)
    while math.gcd(e, phi_n) != 1:
        e = random.randint(2, phi_n)

    # 计算d
    d = pow(e, -1, phi_n)

    # 将整数转换为16进制字符串
    p_hex = hex(p)[2:].upper()
    q_hex = hex(q)[2:].upper()
    n_hex = hex(n)[2:].upper()
    e_hex = hex(e)[2:].upper()
    d_hex = hex(d)[2:].upper()

    # 将结果写入文件
    with open('p.txt', 'w') as f:
        f.write(p_hex)
        print("已成功生成p，并写入p.txt\n")
        f.close()
    
    with open('q.txt', 'w') as f:
        f.write(q_hex)
        print("已成功生成q，并写入q.txt\n")
        f.close()
    
    with open('n.txt', 'w') as f:
        f.write(n_hex)
        print("已成功生成n，并写入n.txt\n")
        f.close()

    with open('e.txt', 'w') as f:
        f.write(e_hex)
        print("已成功生成e，并写入e.txt\n")
        f.close()
    
    with open('d.txt', 'w') as f:
        f.write(d_hex)
        print("已成功生成d，并写入d.txt\n")
        f.close()

    return p_hex, q_hex, n_hex, e_hex, d_hex


#快速幂算法
def FastExpMod(b,e,m):
    result = 1
    while e != 0:
        if(e&1)==1:
            result = (result*b)%m
        e >>= 1 #扩大两倍
        b=(b*b)%m
    return result 

#加密过程
def encrypt_data(plainfile,nfile,efile,cipherfile):
    print("---------数据加密---------\n")
    #读取明文
    with open(plainfile,'r') as f:    
        plaindata = f.read().strip('\n')
        print("读入的明文为：",plaindata)
        f.close()
    #转换成十进制
    dec_plain = Hex2Dec(plaindata)
    print("明文十进制为：",dec_plain)

    with open(nfile,'r') as f:
        pubkey_n = f.read().strip('\n')
        print("n为：",pubkey_n)
        f.close()
    with open(efile,'r') as f:
        pubkey_e = f.read().strip('\n')
        print("e为：",pubkey_e)
        f.close()
    dec_n = Hex2Dec(pubkey_n)
    print("n的十进制为：",dec_n)
    dec_e = Hex2Dec(pubkey_e)
    print("e的十进制为：",dec_e)

    dec_cipher = FastExpMod(dec_plain,dec_e,dec_n)
    print("dec_cipher",dec_cipher)
    #将密文转化为十六进制
    cipher = Dec2Hex(dec_cipher)
    str_cipher = str(cipher).upper()
    with open(cipherfile,'w') as f:
        f.write(str_cipher[2:])  #除去十六进制的0x头
        f.close()
    print("密文已写入成功，为：",str_cipher[2:])


def sign_data(plainfile,nfile,dfile,cipherfile):
    print("----------数据签名---------\n")
    with open(plainfile,'r') as f:    
        plaindata = f.read().strip('\n')
        print("读入的明文为：",plaindata)
        f.close()
    dec_plain = Hex2Dec(plaindata)
    print("明文十进制为：",dec_plain)

    with open(nfile,'r') as f:
        prikey_n = f.read().strip('\n')
        print("n为：",prikey_n)
        f.close()
    with open(dfile,'r') as f:
        prikey_d = f.read().strip('\n')
        print("d为：",prikey_d)
        f.close()

    dec_n = Hex2Dec(prikey_n)
    print("n的十进制为：",dec_n)
    dec_d = Hex2Dec(prikey_d)
    print("d的十进制为：",dec_d)
    sign_plain = FastExpMod(dec_plain,dec_d,dec_n)
    print("签名后十进制为：",sign_plain)
    sign_Hdata = Dec2Hex(sign_plain)
    str_sign = str(sign_Hdata).upper()
    with open(cipherfile,'w') as f:
        f.write(str_sign[2:])
        f.close()
    print("已成功签名，为：",str_sign[2:])

if __name__ =='__main__':
    parser = argparse.ArgumentParser(description='----------RSA算法实现-----------')
    parser.add_argument('option',choices=['0','1','2'],help='选择操作：0-数据加密,1-数据签名,2-随机生成p,q,公钥{e, n}和私钥{d, n}')
    parser.add_argument('-p','--plainfile',help='明文文件位置')
    parser.add_argument('-n','--nfile',help='存放n的位置')
    parser.add_argument('-e','--efile',help='数据加密过程中存放e的位置')
    parser.add_argument('-d','--dfile',help='数字签名过程中存放d的位置')
    parser.add_argument('-c','--cipherfile',help='输出文件的名称')

    args = parser.parse_args()
    option = args.option

    if(option=='0'):
        encrypt_data(args.plainfile,args.nfile,args.efile,args.cipherfile)
    elif(option == '1'):
        sign_data(args.plainfile,args.nfile,args.dfile,args.cipherfile) 
    elif(option == '2'):
        generate_key_pair_and_write_files()
    else:
        print("请输入参数0或者参数1\n")
        
