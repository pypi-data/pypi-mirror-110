#!/usr/bin/env python

from bitarray import bitarray

# Customize base64
class Base64(object):

    def __init__(self, table='', padding='='):
        if table:
            self.table = table
        else:
            self.table = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
        self.padding = padding

    def encode(self, msg):
        if isinstance(msg, bytes):
            data = msg
        else:
            data = str(msg).encode('utf8')
        bit = bitarray()
        bit.frombytes(data)
        fill = (6 - len(bit)%6)
        for i in range(fill): bit.append(0)
        code = ''
        for n in range(int(len(bit)/6)):
            b = ''
            for m in bit[6*n:6*(n+1)]:
                b += '1' if m else '0'
            code += self.table[int(b,2)]
        code += self.padding * (int(fill/2))
        if isinstance(msg, bytes):
            return code.encode('utf8')
        else:
            return code

    def decode(self, code):
        if isinstance(code, bytes):
            data = code
        else:
            data = str(code).encode('utf8')
        bitcode = ''
        for n in data.strip():
            c = chr(n)
            if c == self.padding:
                bitcode = bitcode[:-2]
            else:
                p = self.table.find(c)
                bitcode += '{0:06b}'.format(p)
        msg = bitarray(bitcode).tobytes()
        if isinstance(code, bytes):
            return msg
        else:
            return msg.decode('utf8')
