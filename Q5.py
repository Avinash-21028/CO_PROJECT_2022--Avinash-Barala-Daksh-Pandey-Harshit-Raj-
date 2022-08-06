###########FIRST TYPE#############
print('###########FIRST TYPE#############')
size = input('Enter size of memory (eg. 16 MB): ')
mode = input('How is the memory addressed? (Enter in one word): ')
size = size.split()
n = int(size[0])
term = size[1]
if term[-1] == 'B':
    bits = n*8

if term[0] == 'K':
    bits = bits * 2**10
elif term[0] == 'M':
    bits = bits * 2**20
elif term[0] == 'G':
    bits = bits * 2**30

if mode == 'bit':
    addr_count = bits
elif mode == 'nibble':
    addr_count = bits / 4
elif mode == 'Byte' or mode == '':
    addr_count = bits / 8
elif mode == 'word':
    word_len = int(input('Enter word length of CPU (eg. 32): '))
    addr_count = bits / word_len

instr_len = int(input('Enter instruction length (eg. 32): '))
reg_len = int(input('Enter register length (eg. 7): '))
addr_bits = len(bin(int(addr_count))[2:])
opcode_len = instr_len - reg_len - addr_bits
filler_len = instr_len - opcode_len - 2*reg_len

print(f'Minimum bits needed to represent an address: {addr_bits}')
print(f'No. of bits needed to represent opcode: {opcode_len}')
print(f'No. of filler bits in instruction type 2: {filler_len}')
print(f'Maximum no. of instructions this ISA can support: {bits//instr_len}')
print(f'Maximum no. of registers this ISA can support: {2**reg_len}')

print("""
      
----------------------------------------------------   
      
      """)


###########SECOND TYPE#############
####TYPE 1:
print('###########SECOND TYPE#############')
print('####TYPE 1:')
MEM=input("Enter the memory size: ").split(" ")
MEM_0_SIZE=int(MEM[0])
if MEM[1][0]=="K":
    MEM_0_SIZE*=1024
elif MEM[1][0]=="M":
    MEM_0_SIZE*=1024*1024
elif MEM[1][0]=="G":
    MEM_0_SIZE*=1024*1024*1024
# if MEM[1][1]=="B":
#     b_multiplier=8
# else:
#     b_multiplier=1
conv_from=input("""Enter convert to which format: 
1. Bit ADDRESSABLE (1)
2. Nibble ADDRESSABLE (2)
3. Byte ADDRESSABLE (3)
4. Word ADDRESSABLE (4)
""")
if conv_from=="1":
    b_multiplier=1
elif conv_from=="2":
    b_multiplier=4
elif conv_from=="3":
    b_multiplier=8
elif conv_from=="4":
    b_multiplier=-1
# MEM_0_SIZE+=int(MEM[1][2:])*1024
OLD=bin(MEM_0_SIZE).split("b")[1]
print("The old memory size is: ",OLD)
OLD_PINS=len(OLD)-1
print("The old memory size in pins is: ",OLD_PINS)
CPU=int(input("Enter the CPU bits processor: "))
if b_multiplier==-1:
    b_multiplier=CPU
conv_to=input("""Enter convert to which format: 
1. Bit ADDRESSABLE (1)
2. Nibble ADDRESSABLE (2)
3. Byte ADDRESSABLE (3)
4. Word ADDRESSABLE (4)
""")
if conv_to=="1":
    NEW=(bin(int(MEM_0_SIZE*b_multiplier/1))).split("b")[1]
elif conv_to=="2":
    NEW=(bin(int(MEM_0_SIZE*b_multiplier/4))).split("b")[1]
elif conv_to=="3":
    NEW=(bin(int(MEM_0_SIZE*b_multiplier/8))).split("b")[1]
elif conv_to=="4":
    NEW=(bin(int(MEM_0_SIZE*b_multiplier/CPU))).split("b")[1]
    # NEW=(bin((int(MEM_0_SIZE/CPU)))).split("b")[1]-1
print("The new memory size is: ",NEW)
NEW_PINS=len(NEW)-1
print("The new memory size in pins is: ",NEW_PINS)
print("No. of Extra Pins",len(NEW)-len(OLD))
print("""
      
----------------------------------------------------   
      
      """)


####TYPE 2:
print('####TYPE 2:')
CPU=int(input("Enter the CPU bits processor: "))
PINS=int(input("Enter no of pins: "))
conv_to=input("""Enter convert to which format: 
1. Bit ADDRESSABLE (1)
2. Nibble ADDRESSABLE (2)
3. Byte ADDRESSABLE (3)
4. Word ADDRESSABLE (4)
""")
if conv_to=="1":
    # NEW=(bin(((2**PINS)*8/1)).split("b")[1])
    NEW=(2**PINS)*1/8
elif conv_to=="2":
    # NEW=(bin(((2**PINS)*8/4)).split("b")[1])
    NEW=(2**PINS)*4/8
elif conv_to=="3":
    # NEW=(bin(((2**PINS)*8/8)).split("b")[1])
    NEW=(2**PINS)*8/8
elif conv_to=="4":
    # NEW=(bin(((2**PINS)*8/CPU)).split("b")[1])
    NEW=(2**PINS)*CPU/8
    # NEW=(bin((int(MEM_0_SIZE/CPU)))).split("b")[1]-1
NEW=int(NEW)
print("The new memory size is: ",NEW,"Bytes")
NEW_PINS=len(bin(NEW).split("b")[1])-1
if NEW_PINS>=30:
    print(2**(NEW_PINS-30),"GB")
elif NEW_PINS>=20:
    print(2**(NEW_PINS-20),"MB")
elif NEW_PINS>=10:
    print(2**(NEW_PINS-10),"KB")
print((bin(NEW)).split("b")[1],"Bytes")