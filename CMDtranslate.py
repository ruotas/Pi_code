#!/usr/bin/env python3
# coding:utf-8


import serial
import time
import binascii


import threading
import subprocess
import eventlet


action_list = ['0']


RES_PACKAGE_HEAD = [0xFF, 0xFF]


# 取反运算
def bit_not_op(v,bit_size):
    bit16_not_val = 0
    for i in range(0,bit_size):
        if ((v >> i)&0x1) == 0 :
            bit16_not_val |= (1 << i)
    return (bit16_not_val)

# 和校验结果
def check_sum(package):
    sum_result = 0
    for hex_data in package:
        sum_result += hex_data
        
    sum_result = sum_result % 256
    
    not_result = bit_not_op(sum_result,8)
    # print(not_result)

    return not_result    # 校验结果


# 写命令 三个字节  30 31 32
def cmd_write(ser,param1,param2,param3):
    if param1 == 0:
        print("value error!!")
        return
    else:
        id_byte =   [0x01]
        total_len = [1 + 2 + 1 +2]
        inst_byte = [0x03]

        reg_addr_byte = [0x1e]
        reg_data_byte = [param1,param2,param3]
        pac_list = id_byte + total_len +inst_byte +reg_addr_byte +reg_data_byte
        print("dec list:",pac_list)
        res_hex = map(lambda x: hex(x),pac_list)
        print("hex list:",list(res_hex))

        check_sum_reslut = check_sum(pac_list)
        print("check_sum_reslut",check_sum_reslut)
        res = RES_PACKAGE_HEAD + pac_list + [check_sum_reslut]
        print(res)

    ser.write(res)
    print("send ok")





# 读CMDstatus
def read_CMDstatus( ser):
    
    id_byte = [0x01]
    total_len = [1 + 2 + 1 ]
    inst_byte = [0x02]

    pac_param_byte = [0x1f,0x01]
    pac_check_sum = [0xd8]


    res = RES_PACKAGE_HEAD + id_byte + total_len + inst_byte + pac_param_byte + pac_check_sum

    # res_hex = map(lambda x: hex(x), res)
    # print(list(res_hex))
    ser.write(res)


if __name__ == '__main__':
  
    with serial.Serial('/dev/ttyAMA0', 115200) as ser:
        while True:
            data1,data2,data3 = input("please input CMD(dec)>>data1 data2 data3:").split()      # CMD CMD_status param1
            cmd_write(ser,int(data1),int(data2),int(data3))


