# -*- coding: utf-8 -*-
def strQ2B(ustring):
    rstring = ""
    for uchar in ustring:
        inside_code=ord(uchar)
        if inside_code == 12288:         
            inside_code = 32 
        elif (inside_code >= 65281 and inside_code <= 65374):
            inside_code -= 65248

        rstring += unichr(inside_code)
    return rstring

if __name__ == '__main__':
    b = strQ2B("ｍｎ123abc".decode('utf-8'))
    print b