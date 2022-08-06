from sys import stdin
from matplotlib import pyplot as plt

empty = '{0:016b}'.format(0)
zeroes = '{0:08b}'.format(0)
overflow = '{0:016b}'.format(8)

Registers = {'000':empty, '001':empty, '010':empty, '011':empty, '100':empty, '101':empty, '110':empty, '111':empty}
A = {"00000", "00001", "10000", "10001", "10110", "11010", "11011", "11100"}
B = {"00010", "10010", "11000", "11001"}
C = {"10011", "10111", "11101", "11110"}
D = {"10100", "10101"}
E = {"11111", "01100", "01101", "01111"}

upper_limit_int = 2**16 - 1
upper_limit_float = (1 + 2*-1 + 2-2 + 2-3 + 2-4 + 2-5) * 2*7

def decimal(bits):
    dec = 0
    for i in range(len(bits) - 1,-1,-1):
        if bits[i] == '1':
            dec += 2**(len(bits) - 1 - i)
    return dec

def flagreset():
    Registers['111'] = empty

def float_to_decimal(Imm):
    Mantissa = 0
    for i,j in zip(range(3,8), range(-1,-6,-1)):
        Mantissa+= int(Imm[i]) * 2**j
    Xbits = Imm[:3]
    Exponent = decimal(Xbits)
    fnum = (1 + Mantissa) * 2**Exponent
    return fnum

def decimal_to_float(num):
    for i in range(8):
        m1 = num / 2**i
        if m1 >= 1 and m1 < 2:
            E = i
            break
    M = m1 - 1
    Mantissa = ''
    for i in range(5):
        M = 2*M
        if M < 1:
            Mantissa += '0'
        else:
            Mantissa += '1'
            M = M - 1
    return '{0:03b}'. format(E) + Mantissa

def movI(reg, Imm):
    Registers[reg] =  zeroes + Imm
    flagreset()

def movR(reg1, reg2):
    Registers[reg2] = Registers[reg1]
    flagreset()

def add(reg1, reg2 ,reg3):
    Sum = decimal(Registers[reg1]) + decimal(Registers[reg2])
    if Sum > upper_limit_int:
        Sum%=upper_limit_int
        Registers['111'] = overflow
    else:
        flagreset()
    Registers[reg3] = '{0:016b}'.format(Sum)

def sub(reg1, reg2, reg3):
    diff = decimal(Registers[reg1]) - decimal(Registers[reg2])
    if diff < 0:
        diff = 0
        Registers['111'] = overflow
    else:
        flagreset()
    Registers[reg3] = '{0:016b}'.format(diff)

def mul(reg1, reg2, reg3):
    Product = decimal(Registers[reg1]) * decimal(Registers[reg2])
    if Product > upper_limit_int:
        Product%=upper_limit_int
        Registers['111'] = overflow
    else:
        flagreset()
    Registers[reg3] = '{0:016b}'.format(Product)

def div(reg3, reg4):
    Quotient = decimal(Registers[reg3]) // decimal(Registers[reg4])
    Remainder = decimal(Registers[reg3]) % decimal(Registers[reg4])
    Registers['000'] = '{0:016b}'.format(Quotient)
    Registers['001'] = '{0:016b}'.format(Remainder)
    flagreset()

def RS(reg1, Imm):
    imm = decimal(Imm)
    Registers[reg1] = '{0:016b}'.format(decimal(Registers[reg1]) >> imm)
    flagreset()

def LS(reg1, Imm):
    imm = decimal(Imm)
    LS = decimal(Registers[reg1]) << imm
    if LS > upper_limit_int:
        LS%=upper_limit_int
        Registers['111'] = overflow
    else:
        flagreset()
    Registers[reg1] = '{0:016b}'.format(LS)

def AND(reg1, reg2, reg3):
    AND = decimal(Registers[reg1]) & decimal(Registers[reg2])
    Registers[reg3] = '{0:016b}'.format(AND)
    flagreset()

def OR(reg1, reg2, reg3):
    OR = decimal(Registers[reg1]) | decimal(Registers[reg2])
    Registers[reg3] = '{0:016b}'.format(OR)
    flagreset()

def NOT(reg1, reg2):
    NOT = decimal(Registers[reg1]) ^ decimal(upper_limit_int)
    Registers[reg2] = '{0:016b}'.format(NOT)
    flagreset()

def XOR(reg1, reg2, reg3):
    XOR = decimal(Registers[reg1]) ^ decimal(Registers[reg2])
    Registers[reg3] = '{0:016b}'.format(XOR)
    flagreset()

def CMP(reg1, reg2):
    if Registers[reg1] < Registers[reg2]:
        Registers['111'] = '{0:016b}'.format(4)
    elif Registers[reg1] > Registers[reg2]:
        Registers['111'] = '{0:016b}'.format(2)
    else:
        Registers['111'] = '{0:016b}'.format(1)

def movfI(reg1, Imm):
    fnum = float_to_decimal(Imm)
    Registers[reg1] = fnum
    flagreset()

def addf(reg1, reg2 ,reg3):
    Sum = float_to_decimal(Registers[reg1][8:]) + float_to_decimal(Registers[reg2][8:])
    if Sum > upper_limit_float:
        Sum = upper_limit_float
        Registers['111'] = overflow
    else:
        flagreset()
    Registers[reg3] = zeroes + decimal_to_float(Sum)

def subf(reg1, reg2, reg3):
    diff = float_to_decimal(Registers[reg1][8:]) - float_to_decimal(Registers[reg2][8:])
    if diff < 0:
        diff = 0
        Registers['111'] = overflow
    else:
        flagreset()
    Registers[reg3] = zeroes + decimal_to_float(diff)

def dump_Registers(Registers = Registers):
    for reg in Registers.keys():
        print((Registers[reg]), end = ' ')
    print()

PC = 0

hlt_found = False

Memory = stdin.readlines()

for i in range(len(Memory)):
    Memory[i] = Memory[i].rstrip('\n')
    if not(Memory[i].rstrip('\n')):
        Memory.pop(i)

Memory = Memory + (256 - len(Memory)) * [empty]

clk_cycle = 0
time = []
PC_visit = []

while True:
    clk_cycle += 1
    time.append(clk_cycle)
    print('{0:08b}'.format(PC), end=' ')
    PC_visit.append(PC)
    instr = Memory[PC]
    opcode = instr[:5]
    branch = False
    if opcode in A:
        reg1 = instr[7:10]
        reg2 = instr[10:13]
        reg3 = instr[13:]
        if opcode == "00000":
            addf(reg1, reg2, reg3)
        elif opcode == "00001":
            subf(reg1, reg2, reg3)
        elif opcode == "10000":
            add(reg1, reg2, reg3)
        elif opcode == "10001":
            sub(reg1, reg2, reg3)
        elif opcode == "10110":
            mul(reg1, reg2, reg3)
        elif opcode == "11010":
            XOR(reg1, reg2, reg3)
        elif opcode == "11011":
            OR(reg1, reg2, reg3)
        elif opcode == "11100":
            AND(reg1, reg2, reg3)
    elif opcode in B:
        reg1 = instr[5:8]
        Imm = instr[8:]
        if opcode == "00010":
            movfI(reg1, Imm)
        elif opcode == "10010":
            movI(reg1, Imm)
        elif opcode == "11000":
            RS(reg1, Imm)
        elif opcode == "11001":
            LS(reg1, Imm)
    elif opcode in C:
        reg1 = instr[10:13]
        reg2 = instr[13:]
        if opcode == "10011":
            movR(reg1, reg2)
        elif opcode == "10111":
            div(reg1, reg2)
        elif opcode == "11101":
            NOT(reg1, reg2)
        elif opcode == "11110":
            CMP(reg1, reg2)
    elif opcode in D:
        reg1 = instr[5:8]
        mem_addr = decimal(instr[8:])
        if opcode == "10100":
            Registers[reg1] = Memory[mem_addr]
        elif opcode == "10101":
            Memory[mem_addr] = Registers[reg1]
    elif opcode in E:
        mem_addr = decimal(instr[8:])
        if opcode == "11111":
            PC = mem_addr
            branch = True
        elif opcode == "01100" and decimal(Registers['111']) == 4:
            PC = mem_addr
            branch = True
        elif opcode == "01101" and decimal(Registers['111']) == 2:
            PC = mem_addr
            branch = True
        elif opcode == "01111" and decimal(Registers['111']) == 1:
            PC = mem_addr
            branch = True
        flagreset()
    elif opcode == "01010":
        hlt_found = True
    
    dump_Registers()

    if hlt_found:
        break

    if not(branch):
        PC += 1

for data in Memory:
    print(data)

plt.scatter(time, PC_visit, len(time)*[5])
plt.xlabel('Time')
plt.ylabel('PC')
plt.show()

# from sys import stdin
# # from matplotlib import pyplot as plt
# empty = '{0:016b}'.format(0)
# zeroes = '{0:08b}'.format(0)
# overflow = '{0:016b}'.format(8)

# Registers = {'000':empty, '001':empty, '010':empty, '011':empty, '100':empty, '101':empty, '110':empty, '111':empty}
# A = {"00000", "00001", "10000", "10001", "10110", "11010", "11011", "11100"}
# B = {"00010", "10010", "11000", "11001"}
# C = {"10011", "10111", "11101", "11110"}
# D = {"10100", "10101"}
# E = {"11111", "01100", "01101", "01111"}

# upper_limit_int = 2**16 - 1
# upper_limit_float = (1 + 2*-1 + 2-2 + 2-3 + 2-4 + 2-5) * 2*7

# def decimal(bits):
#     dec = 0
#     for i in range(len(bits) - 1,-1,-1):
#         if bits[i] == '1':
#             dec += 2**(len(bits) - 1 - i)
#     return dec

# def flagreset():
#     Registers['111'] = empty

# def float_to_decimal(Imm):
#     Mantissa = 0
#     for i,j in zip(range(3,8), range(-1,-6,-1)):
#         Mantissa+= int(Imm[i]) * 2**j
#     Xbits = Imm[:3]
#     Exponent = decimal(Xbits)
#     fnum = (1 + Mantissa) * 2**Exponent
#     return fnum

# def decimal_to_float(num):
#     for i in range(8):
#         m1 = num / 2**i
#         if m1 >= 1 and m1 < 2:
#             E = i
#             break
#     M = m1 - 1
#     Mantissa = ''
#     for i in range(5):
#         M = 2*M
#         if M < 1:
#             Mantissa += '0'
#         else:
#             Mantissa += '1'
#             M = M - 1
#     return '{0:03b}'. format(E) + Mantissa

# def movI(reg, Imm):
#     Registers[reg] =  zeroes + Imm
#     flagreset()

# def movR(reg1, reg2):
#     Registers[reg2] = Registers[reg1]
#     flagreset()

# def add(reg1, reg2 ,reg3):
#     Sum = decimal(Registers[reg1]) + decimal(Registers[reg2])
#     if Sum > upper_limit_int:
#         Sum%=upper_limit_int
#         Registers['111'] = overflow
#     else:
#         flagreset()
#     Registers[reg3] = '{0:016b}'.format(Sum)

# def sub(reg1, reg2, reg3):
#     diff = decimal(Registers[reg1]) - decimal(Registers[reg2])
#     if diff < 0:
#         diff = 0
#         Registers['111'] = overflow
#     else:
#         flagreset()
#     Registers[reg3] = '{0:016b}'.format(diff)

# def mul(reg1, reg2, reg3):
#     Product = decimal(Registers[reg1]) * decimal(Registers[reg2])
#     if Product > upper_limit_int:
#         Product%=upper_limit_int
#         Registers['111'] = overflow
#     else:
#         flagreset()
#     Registers[reg3] = '{0:016b}'.format(Product)

# def div(reg3, reg4):
#     Quotient = decimal(Registers[reg3]) // decimal(Registers[reg4])
#     Remainder = decimal(Registers[reg3]) % decimal(Registers[reg4])
#     Registers['000'] = '{0:016b}'.format(Quotient)
#     Registers['001'] = '{0:016b}'.format(Remainder)
#     flagreset()

# def RS(reg1, Imm):
#     imm = decimal(Imm)
#     Registers[reg1] = '{0:016b}'.format(decimal(Registers[reg1]) >> imm)
#     flagreset()

# def LS(reg1, Imm):
#     imm = decimal(Imm)
#     LS = decimal(Registers[reg1]) << imm
#     if LS > upper_limit_int:
#         LS%=upper_limit_int
#         Registers['111'] = overflow
#     else:
#         flagreset()
#     Registers[reg1] = '{0:016b}'.format(LS)

# def AND(reg1, reg2, reg3):
#     AND = decimal(Registers[reg1]) & decimal(Registers[reg2])
#     Registers[reg3] = '{0:016b}'.format(AND)
#     flagreset()

# def OR(reg1, reg2, reg3):
#     OR = decimal(Registers[reg1]) | decimal(Registers[reg2])
#     Registers[reg3] = '{0:016b}'.format(OR)
#     flagreset()

# def NOT(reg1, reg2):
#     NOT = decimal(Registers[reg1]) ^ decimal(upper_limit_int)
#     Registers[reg2] = '{0:016b}'.format(NOT)
#     flagreset()

# def XOR(reg1, reg2, reg3):
#     XOR = decimal(Registers[reg1]) ^ decimal(Registers[reg2])
#     Registers[reg3] = '{0:016b}'.format(XOR)
#     flagreset()

# def CMP(reg1, reg2):
#     if Registers[reg1] < Registers[reg2]:
#         Registers['111'] = '{0:016b}'.format(4)
#     elif Registers[reg1] > Registers[reg2]:
#         Registers['111'] = '{0:016b}'.format(2)
#     else:
#         Registers['111'] = '{0:016b}'.format(1)

# def movfI(reg1, Imm):
#     fnum = float_to_decimal(Imm)
#     Registers[reg1] = fnum
#     flagreset()

# def addf(reg1, reg2 ,reg3):
#     Sum = float_to_decimal(Registers[reg1][8:]) + float_to_decimal(Registers[reg2][8:])
#     if Sum > upper_limit_float:
#         Sum = upper_limit_float
#         Registers['111'] = overflow
#     else:
#         flagreset()
#     Registers[reg3] = zeroes + decimal_to_float(Sum)

# def subf(reg1, reg2, reg3):
#     diff = float_to_decimal(Registers[reg1][8:]) - float_to_decimal(Registers[reg2][8:])
#     if diff < 0:
#         diff = 0
#         Registers['111'] = overflow
#     else:
#         flagreset()
#     Registers[reg3] = zeroes + decimal_to_float(diff)

# def dump_Registers(Registers = Registers):
#     for reg in Registers.keys():
#         print((Registers[reg]), end = ' ')
#     print()

# PC = 0

# hlt_found = False

# Memory = stdin.readlines()

# for i in range(len(Memory)):
#     Memory[i] = Memory[i].rstrip('\n')
#     if not(Memory[i].rstrip('\n')):
#         Memory.pop(i)

# Memory = Memory + (256 - len(Memory)) * [empty]

# clk_cycle = 0
# time = []
# PC_visit = []

# while True:
#     clk_cycle += 1
#     time.append(clk_cycle)
#     print('{0:08b}'.format(PC), end=' ')
#     PC_visit.append(PC)
#     instr = Memory[PC]
#     opcode = instr[:5]
#     branch = False
#     if opcode in A:
#         reg1 = instr[7:10]
#         reg2 = instr[10:13]
#         reg3 = instr[13:]
#         if opcode == "00000":
#             addf(reg1, reg2, reg3)
#         elif opcode == "00001":
#             subf(reg1, reg2, reg3)
#         elif opcode == "10000":
#             add(reg1, reg2, reg3)
#         elif opcode == "10001":
#             sub(reg1, reg2, reg3)
#         elif opcode == "10110":
#             mul(reg1, reg2, reg3)
#         elif opcode == "11010":
#             XOR(reg1, reg2, reg3)
#         elif opcode == "11011":
#             OR(reg1, reg2, reg3)
#         elif opcode == "11100":
#             AND(reg1, reg2, reg3)
#     elif opcode in B:
#         reg1 = instr[5:8]
#         Imm = instr[8:]
#         if opcode == "00010":
#             movfI(reg1, Imm)
#         elif opcode == "10010":
#             movI(reg1, Imm)
#         elif opcode == "11000":
#             RS(reg1, Imm)
#         elif opcode == "11001":
#             LS(reg1, Imm)
#     elif opcode in C:
#         reg1 = instr[10:13]
#         reg2 = instr[13:]
#         if opcode == "10011":
#             movR(reg1, reg2)
#         elif opcode == "10111":
#             div(reg1, reg2)
#         elif opcode == "11101":
#             NOT(reg1, reg2)
#         elif opcode == "11110":
#             CMP(reg1, reg2)
#     elif opcode in D:
#         reg1 = instr[5:8]
#         mem_addr = decimal(instr[8:])
#         if opcode == "10100":
#             Registers[reg1] = Memory[mem_addr]
#         elif opcode == "10101":
#             Memory[mem_addr] = Registers[reg1]
#     elif opcode in E:
#         mem_addr = decimal(instr[8:])
#         if opcode == "11111":
#             PC = mem_addr
#             branch = True
#         elif opcode == "01100" and decimal(Registers['111']) == 4:
#             PC = mem_addr
#             branch = True
#         elif opcode == "01101" and decimal(Registers['111']) == 2:
#             PC = mem_addr
#             branch = True
#         elif opcode == "01111" and decimal(Registers['111']) == 1:
#             PC = mem_addr
#             branch = True
#         flagreset()
#     elif opcode == "01010":
#         hlt_found = True
    
#     dump_Registers()

#     if hlt_found:
#         break

#     if not(branch):
#         PC += 1

# for data in Memory:
#     print(data)

# # plt.scatter(time, PC_visit, len(time)*[5])
# # plt.xlabel('Time')
# # plt.ylabel('PC')
# # plt.show()