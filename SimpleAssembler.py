# CO PROJECT

# AVINASH BARALA 2021028
# DAKSH PANDEY 2021036
# HARSHIT RAJ 2021051

from itertools import count
import sys
from sys import stdin

# do we have to print code of label file?
# stdin=open("input.txt",'r')
# sys.stdout=open("Output.txt",'w')
def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False
def incr_len(num):
    x = num[::-1]
    while len(x) < 8:
        x += '0'
    num = x[::-1]
    # print(num)
    return num
    
try:

    A={"addf":"00000","subf":"00001","add":"10000", "sub":"10001", "mul":"10110", "xor":"11010", "or":"11011", "and":"11100"}
    B={"mov":"10010", "rs":"11000", "ls":"11001", "movf":"00010"}
    C={"mov":"10011", "div":"10111", "not":"11101", "cmp":"11110"}
    D={"ld":"10100", "st":"10101"}
    E={"jmp":"11111", "jlt":"01100", "jgt":"01101", "je":"01111"}
    F={"hlt":"0101000000000000"}
    label_dict={}
    var_dict={}

    Register={"R0":"000", "R1":"001", "R2":"010", "R3":"011", "R4":"100", "R5":"101", "R6":"110", "FLAGS":"111"}

    def bit_extend(num):
        # print(num)
        binum=bin(num)
        # print(binum)
        return "0"*(10-len(binum)) + binum[2:]

    instr_list=stdin.readlines()
    
    label_lst=[]
    labls=[]
    vars={}
    var_lst=[]
    ct_line_no=0 
    statement_no=0
    ct_hlt=0
    empt_line=0
    var_line=0
    label_line=0
    ct_labels=0
    hlt_flag=False
    address=0
    var_address=0
    
    for i in instr_list:
        statement_no+=1
        ct_line_no+=1
        address+=1
        
            
        # if (i!="\n" or i=="") and ct_hlt==1:
        if (i.isascii())==False and ct_hlt==1:
            assert ct_hlt!=1 , f"## More statement written after 1 hlt , hlt Error at line_no {ct_line_no} and statement_no {statement_no} ##"
            
        # print(f"{i}")
        temp=i.split()
        # print(temp)
        # print(len(temp))
        if len(temp)==0:
            empt_line  += 1
            statement_no-=1
            var_address-=1
            address-=1
            ct_line_no+=1
            continue
        
        if i=="hlt\n" or i=="hlt" or temp==['hlt']:
            hlt_flag=True
            ct_hlt+=1
            if (ct_hlt>1):
                print(f"More than 1 hlt , ## hlt Error at line_no {ct_line_no} and statement_no {statement_no} ##")
                raise AssertionError
            
        if i.startswith("hlt"):
            if temp!=['hlt']:
                assert temp==['hlt'] , f"## hlt statement Token Error in line at line_no {ct_line_no} statement_no {statement_no} ## "
        if temp[0]=="var":
            address-=1
            
        if temp[0][-1]==":" and temp[1]=="hlt":
            ct_hlt+=1
            hlt_flag=True
            
            
        # print( instr_list[statement_no])
        # print(f"{instr_list[statement_no-1]}")
        # # if instr_list[statement_no-1]=='\n' or instr_list[statement_no-1]=='':
        # #     empt_line+=1
        # if i=="\n" or instr_list[statement_no-1]==['\n'] or temp==['\n']:
        #     empt_line+=1
        #     statement_no-=1
        # print(f"{var_address}")
        if temp[0][-1]==":":
            label_dict[temp[0][:-1]]=statement_no-var_line-1
            # print(f"{temp[0]} : {statement_no-var_line-1}")
            label_line+=1
            ct_labels+=1
            # print(f"{var_address}")
        if i.startswith("var"):
            var_address+=1
            var_line+=1
            assert len(i.split())==2 , f" ## var Token Error in line_no {ct_line_no} and statement_no {statement_no} ##"
            assert statement_no<=var_line , f"var not declared at top ## var Token Error in line_no {ct_line_no} and statement_no {statement_no} ##"
            if i.split()[1] not in var_lst:
                var_lst.append(i.split()[1])
                var_dict[i.split()[1]]=var_address
                # print(f"{i.split()[1]} {var_address}")
            else:
                print(f"var {i.split()[1]} already declared above , ## Error at line_no {ct_line_no} and statement_no {statement_no} ##")
                raise AssertionError
             
            if temp[1] in A or temp[1] in B or temp[1] in C or temp[1] in D or temp[1] in E or temp[1] in F or temp[1] in Register:
                print(f" ## var Token Error in line_no {ct_line_no} and statement_no {statement_no} ##")
                raise AssertionError
            
    for i in var_dict:
        var_dict[i]+=statement_no-var_line-1
        # print(f"{i} {var_dict[i]}")
    # for i in label_dict:
        # print(f"{i} {label_dict[i]}")
    if hlt_flag==False:
        print(f"## No hlt given at end of code , error after line_no {ct_line_no} and statement_no {statement_no} ##")
        raise AssertionError
    # print(len(instr_list))
    # print(empt_line)
    
    if ct_labels==0:
        code_size=len(instr_list)-(empt_line+var_line) 
    else:
        code_size=len(instr_list)-(empt_line+var_line+label_line)
    
    if code_size>256:
        print("No of instructions exceed 256 statements ## var line is considered as instructions")
        raise AssertionError
    

    
    ct_line_no=0
    statement_no=0
    var_name=""
    out=""

    for Instr in instr_list:
        ct_line_no+=1
        if Instr=="\n":
            continue
        instr=Instr.split()
        if instr==[]:
            continue
        statement_no+=1
        if instr=="":
            break
        if (instr[0] not in A.keys()) and (instr[0] not in B.keys()) and (instr[0] not in C.keys()) and (instr[0] not in D.keys()) and (instr[0] not in E.keys()) and instr[0]!="var" and instr[0]!="hlt" and instr[0][-1]!=":":
            print(f"## {instr[0]} statement Token Error in line at line_no {ct_line_no} statement_no {statement_no} ## ")
            raise AssertionError
        ################
        if instr[0][-1]==":":
            if instr[0][0:-1] in label_lst :
                print (f"label {instr[0][0:-1]} is already given above , Error in line at line_no {ct_line_no} statement_no {statement_no} ##")
                raise AssertionError
            elif len(instr)<=1:
                print (f"label {instr[0][0:-1]} Token Error in line at line_no {ct_line_no} statement_no {statement_no} ##")
                raise AssertionError
            else:
                pass
        
        ###############
        if instr[0][-1]==":":
            if instr[0][:-1] in A or instr[0][:-1] in B or instr[0][:-1] in C or instr[0][:-1] in D or instr[0][:-1] in E or instr[0][:-1] in F or instr[0][:-1] in Register:
                print(f"## {instr[0]} statement Token Error in line at line_no {ct_line_no} statement_no {statement_no} ## ")
                raise AssertionError
            if instr[0][-2]==" ":
                assert instr[0][-2]!=" " , f"## {instr[0]} statement Token Error in line at line_no {ct_line_no} statement_no {statement_no} ## "
            else:
                ########################
                label_lst.append(instr[0][0:-1])
                vars[instr[0][:-1]]=bit_extend(code_size)  
                # vars[instr[0][:-1]]=bit_extend(code_size)
                # instr=instr[1:] 
                # code_size+=1
       
        if instr[0]=="var":
            # pass
            vars[instr[1]]=bit_extend(code_size)
            # code_size+=1

    ct_line_no=0
    statement_no=0
    # code_size=code_size-var_line

    for Instr in instr_list:
        ct_line_no+=1
        # print(f"{ct_line_no}")
        if Instr=="\n":
            continue
        instr=Instr.split()

        if instr==[]:
            continue
        statement_no+=1
        # print(f"{statement_no}")
        if instr=="":
            break
        if (instr[0] not in A.keys()) and (instr[0] not in B.keys()) and (instr[0] not in C.keys()) and (instr[0] not in D.keys()) and (instr[0] not in E.keys()) and instr[0]!="var" and instr[0]!="hlt" and instr[0][-1]!=":":
            print(f"## {instr[0]} statement Token Error in line at line_no {ct_line_no} statement_no {statement_no} ## ")
            raise AssertionError
        ################
        if instr[0][-1]==":":
            if instr[0][0:-1] in label_lst and label_lst.count(instr[0][0:-1])!=1:
                print (f"label {instr[0][0:-1]} is already given above , Error in line at line_no {ct_line_no} statement_no {statement_no} ##")
                raise AssertionError
            elif len(instr)<=1:
                print (f"label {instr[0][0:-1]} Token Error in line at line_no {ct_line_no} statement_no {statement_no} ##")
                raise AssertionError
            else:
                pass
        
        ###############
        if instr[0][-1]==":":
            if instr[0][:-1] in A or instr[0][:-1] in B or instr[0][:-1] in C or instr[0][:-1] in D or instr[0][:-1] in E or instr[0][:-1] in F or instr[0][:-1] in Register:
                print(f"## {instr[0]} statement Token Error in line at line_no {ct_line_no} statement_no {statement_no} ## ")
                raise AssertionError
            if instr[0][-2]==" ":
                assert instr[0][-2]!=" " , f"## {instr[0]} statement Token Error in line at line_no {ct_line_no} statement_no {statement_no} ## "
            else:
                ########################
                label_lst.append(instr[0][0:-1])
                vars[instr[0][:-1]]=bit_extend(code_size)  
                # vars[instr[0][:-1]]=bit_extend(code_size)
                instr=instr[1:] 
                code_size+=1
       
        if instr[0]=="var":
            vars[instr[1]]=bit_extend(code_size)
            code_size+=1
            
        elif instr[0] in A:
            temp=instr[2]
            instr[2]=instr[3]
            (A[instr[0]] + "00" + Register[instr[1]] + Register[instr[2]] + Register[instr[3]])
            instr[2]=temp
            out+=(A[instr[0]] + "00" + Register[instr[1]] + Register[instr[2]] + Register[instr[3]])
            out+="\n"
        elif instr[0] in B and instr[2][0]=="$":
            if len(instr)!=3:
                print(f"## {instr[0]} statement Token Error in line at line_no {ct_line_no} statement_no {statement_no} ## ")
                raise AssertionError  
            if (instr[2][1:]).isdigit() and instr[0]!="movf":
                if (int(instr[2][1:])>=0 and int(instr[2][1:])<256 ):
                    if (instr[2][0]=="$"):
                        num=int(instr[2][1:])
                        out+=(B[instr[0]] + Register[instr[1]] + bit_extend(num))
                        out+="\n"
                    else:
                        print(f"## {instr[0]} statement Token Error in line at line_no {ct_line_no} statement_no {statement_no} ## ")
                        raise AssertionError
                else:
                    print(f"## {instr[0]} statement Token Error in line at line_no {ct_line_no} statement_no {statement_no} ## ")
                    raise AssertionError
            elif isfloat(instr[2][1:]) and instr[0]=="movf":
                if (float(instr[2][1:])>=0 and float(instr[2][1:])<256):
                    if (instr[2][0]=="$"):
                            out+=(B[instr[0]] + Register[instr[1]] )
                            flag=0
                            a=instr[2][1:]
                            start_zero=0
                            start_non_zero=0
                            for i in a:
                                if i!='0':
                                    start_non_zero+=1
                                else:
                                    start_zero+=1
                                    
                            # a1_len=len(a.split('.')[0])-1##-1 is so that first position is left

                            # print(a1_len)
                            b=''
                            b=b.join((a.split('.')))
                            # print(b)
                            k=len(bin(len((bin(int(a.split('.')[0]))).split('b')[1][1:])).split('b')[1])
                            while k<3:
                                # print(0,end='')
                                out+=("0")
                                k+=1
                            # print(bin(len((bin(int(a.split('.')[0]))).split('b')[1][1:])).split('b')[1],end='')
                            out+=(bin(len((bin(int(a.split('.')[0]))).split('b')[1][1:])).split('b')[1])
                            # print((bin(int(a.split('.')[0]))).split('b')[1][1:],end='')
                            out+=(bin(int(a.split('.')[0]))).split('b')[1][1:]
                            left=5-len((bin(int(a.split('.')[0]))).split('b')[1][1:])
                            # print(left)
                            try:
                                c=int(a.split('.')[1])
                            except:
                                c=0
                                pass
                            # print(c)
                            while c!=0 and left!=0:
                                # print(c)
                                c=c*2
                                # print(c)
                                if len(str(int(c/2)))<len(str(c)) or c==0:
                                    # print(1,end='')
                                    out+=('1')
                                    c=int((str(c))[1:])
                                else:
                                    # print(0,end='')
                                    out+=('0')
                                    c=int((str(c)))
                                left-=1
                                if left==0 and c!=0:
                                    print("resolution required can not be expressed in given bits")
                                    print(f"statement Token Error in line at line_no {ct_line_no} statement_no {statement_no} ## ")
                                    raise AssertionError
                                    break
                                
                            while left!=0:
                                out+="0"
                                # print(0,end='')
                                left-=1
                            out+="\n"
            else:
                print(f"## {instr[0]} statement Token Error in line at line_no {ct_line_no} statement_no {statement_no} ## ")
                raise AssertionError
            
        elif instr[0] in C:
            if len(instr)!=3:
                print(f"## {instr[0]} statement Token Error in line at line_no {ct_line_no} statement_no {statement_no} ## ")
                raise AssertionError
            if ((instr[2][0]=="R") and (int(instr[2][1:])<=6)) or instr[2][:]=="FLAGS":
                out+=(C[instr[0]] + "00000" + Register[instr[1]] + Register[instr[2]])
                out+="\n"
            else:
                print(f"## {instr[0]} statement Token Error in line at line_no {ct_line_no} statement_no {statement_no} ## ")
                raise AssertionError
                
        elif instr[0] in D:
            # print((bin(var_dict[instr[2]])).split('b')[1])
            a=incr_len((bin(var_dict[instr[2]])).split('b')[1])
            # print(a)
            b=""
            b=b.join((a))
            # print(b)
            out+=(D[instr[0]] + Register[instr[1]] + b)
            out+="\n"
        elif instr[0] in E:
            # instr.append(instr[1])
            # a=incr_len((bin(label_dict[instr[1]])).split('b')[1])
            a=incr_len((bin(label_dict[instr[1]])).split('b')[1])
            # print(a)
            b=""
            b=b.join((a))
            out+=(E[instr[0]] + "000" + b)
            out+="\n"
        elif Instr=="hlt\n" or Instr=="hlt" or instr==['hlt']:
            out+="0101000000000000"
        elif instr[0]=="hlt":
            out+="0101000000000000"
        else:
            print(f"statement Token Error in line at line_no {ct_line_no} statement_no {statement_no} ## ")
            raise AssertionError
    print(out)
except AssertionError as Error:
    # try:
        print(Error)
    # except:
    #     print(f"## Error at line_no {ct_line_no} and statement_no {statement_no} ##")
except KeyError as Error:
    try:
        print(f"{instr[2]} not initialized KeyError, ## Error at line_no {ct_line_no} and statement_no {statement_no} ## ")
    except:
        print(f"KeyError Error at line_no {ct_line_no} and statement_no {statement_no} ##")
except IndexError as Error:
    try:
        print(f"## {instr[0]} statement Token Error IndexError in line at line_no {ct_line_no} statement_no {statement_no} ## ")
    except:
        print(f"IndexError Error at line_no {ct_line_no} and statement_no {statement_no} ##")
except:
    # try:
        print(f"GENERAL SYNTAX statement Token Error in line at line_no {ct_line_no} statement_no {statement_no} ## ")
    # except:
    #     print(f"## Error at line_no {ct_line_no} and statement_no {statement_no} ##")





# # CO PROJECT

# # AVINASH BARALA 2021028
# # DAKSH PANDEY 2021036
# # HARSHIT RAJ 2021051

# import sys
# from sys import stdin

# # do we have to print code of label file?
# # stdin=open("input.txt",'r')
# # sys.stdout=open("Output.txt",'w')

# try:

#     A={"add":"10000", "sub":"10001", "mul":"10110", "xor":"11010", "or":"11011", "and":"11100"}
#     B={"mov":"10010", "rs":"11000", "ls":"11001"}
#     C={"mov":"10011", "div":"10111", "not":"11101", "cmp":"11110"}
#     D={"ld":"10100", "st":"10101"}
#     E={"jmp":"11111", "jlt":"01100", "jgt":"01101", "je":"01111"}
#     F={"hlt":"0101000000000000"}

#     Register={"R0":"000", "R1":"001", "R2":"010", "R3":"011", "R4":"100", "R5":"101", "R6":"110", "FLAGS":"111"}

#     def bit_extend(num):
#         binum=bin(num)
#         return "0"*(10-len(binum)) + binum[2:]

#     instr_list=stdin.readlines()
    
#     label_lst=[]
#     labls=[]
#     vars={}
#     var_lst=[]
#     ct_line_no=0 #
#     statement_no=0
#     ct_hlt=0
#     empt_line=0
#     var_line=0
#     hlt_flag=False
    
#     for i in instr_list:
#         statement_no+=1
#         ct_line_no+=1
            
#         # if (i!="\n" or i=="") and ct_hlt==1:
#         if (i.isascii())==False and ct_hlt==1:
#             assert ct_hlt!=1 , f"## More statement written after 1 hlt , hlt Error at line_no {ct_line_no} and statement_no {statement_no} ##"
            
#         # print(f"{i}")
#         temp=i.split()
#         # print(temp)
#         # print(len(temp))
#         if len(temp)==0:
#             statement_no-=1
#             ct_line_no+=1
#             continue
        
#         if i=="hlt\n" or i=="hlt" or temp==['hlt']:
#             hlt_flag=True
#             ct_hlt+=1
#             if (ct_hlt>1):
#                 print(f"More than 1 hlt , ## hlt Error at line_no {ct_line_no} and statement_no {statement_no} ##")
#                 raise AssertionError
            
#         if i.startswith("hlt"):
#             if temp!=['hlt']:
#                 assert temp==['hlt'] , f"## hlt statement Token Error in line at line_no {ct_line_no} statement_no {statement_no} ## "
#         if temp[0][-1]==":" and temp[1]=="hlt":
#             ct_hlt+=1
#             hlt_flag=True
#         # print(instr_list[statement_no-1])
#         if i=="\n" or instr_list[statement_no-1]==['\n']:
#             empt_line+=1
#             statement_no-=1
            
#         if i.startswith("var"):
#             var_line+=1
#             assert len(i.split())==2 , f" ## var Token Error in line_no {ct_line_no} and statement_no {statement_no} ##"
#             assert statement_no<=var_line , f"var not declared at top ## var Token Error in line_no {ct_line_no} and statement_no {statement_no} ##"
#             if i.split()[1] not in var_lst:
#                 var_lst.append(i.split()[1])
#             else:
#                 print(f"var {i.split()[1]} already declared above , ## Error at line_no {ct_line_no} and statement_no {statement_no} ##")
#                 raise AssertionError
             
#             if temp[1] in A or temp[1] in B or temp[1] in C or temp[1] in D or temp[1] in E or temp[1] in F or temp[1] in Register:
#                 print(f" ## var Token Error in line_no {ct_line_no} and statement_no {statement_no} ##")
#                 raise AssertionError
            
#     if hlt_flag==False:
#         print(f"## No hlt given at end of code , error after line_no {ct_line_no} and statement_no {statement_no} ##")
#         raise AssertionError
    
#     code_size=len(instr_list)-(empt_line) 
    
#     if code_size>256:
#         print("No of instructions exceed 256 statements ## var line is considered as instructions")
#         raise AssertionError
    
#     ct_line_no=0
#     code_size=code_size-var_line
#     statement_no=0
#     var_name=""
#     out=""
#     for Instr in instr_list:
#         ct_line_no+=1
#         if Instr=="\n":
#             continue
#         instr=Instr.split()
#         if instr==[]:
#             continue
#         statement_no+=1
#         if instr=="":
#             break
#         if (instr[0] not in A.keys()) and (instr[0] not in B.keys()) and (instr[0] not in C.keys()) and (instr[0] not in D.keys()) and (instr[0] not in E.keys()) and instr[0]!="var" and instr[0]!="hlt" and instr[0][-1]!=":":
#             print(f"## {instr[0]} statement Token Error in line at line_no {ct_line_no} statement_no {statement_no} ## ")
#             raise AssertionError
#         ################
#         if instr[0][-1]==":":
#             if instr[0][0:-1] in label_lst :
#                 print (f"label {instr[0][0:-1]} is already given above , Error in line at line_no {ct_line_no} statement_no {statement_no} ##")
#                 raise AssertionError
#             elif len(instr)<=1:
#                 print (f"label {instr[0][0:-1]} Token Error in line at line_no {ct_line_no} statement_no {statement_no} ##")
#                 raise AssertionError
#             else:
#                 pass
        
#         ################
#         if instr[0][-1]==":":
#             if instr[0][:-1] in A or instr[0][:-1] in B or instr[0][:-1] in C or instr[0][:-1] in D or instr[0][:-1] in E or instr[0][:-1] in F or instr[0][:-1] in Register:
#                 print(f"## {instr[0]} statement Token Error in line at line_no {ct_line_no} statement_no {statement_no} ## ")
#                 raise AssertionError
#             if instr[0][-2]==" ":
#                 assert instr[0][-2]!=" " , f"## {instr[0]} statement Token Error in line at line_no {ct_line_no} statement_no {statement_no} ## "
#             else:
#                 ########################
#                 label_lst.append(instr[0][0:-1])
#                 # vars[instr[0][:-1]]=bit_extend(code_size)  
#                 vars[instr[0][:-1]]=bit_extend(code_size)
#                 instr=instr[1:] 
#                 code_size+=1
       
#         if instr[0]=="var":
#             vars[instr[1]]=bit_extend(code_size)
#             code_size+=1
            
#         elif instr[0] in A:
#             temp=instr[2]
#             instr[2]=instr[3]
#             (A[instr[0]] + "00" + Register[instr[1]] + Register[instr[2]] + Register[instr[3]])
#             instr[2]=temp
#             out+=(A[instr[0]] + "00" + Register[instr[1]] + Register[instr[2]] + Register[instr[3]])
#             out+="\n"
#         elif instr[0] in B and instr[2][0]=="$":
#             if len(instr)!=3:
#                 print(f"## {instr[0]} statement Token Error in line at line_no {ct_line_no} statement_no {statement_no} ## ")
#                 raise AssertionError                
#             if (instr[2][1:]).isdigit():
#                 if (int(instr[2][1:])>=0 and int(instr[2][1:])<256):
#                     if (instr[2][0]=="$"):
#                         pass
#                     else:
#                         print(f"## {instr[0]} statement Token Error in line at line_no {ct_line_no} statement_no {statement_no} ## ")
#                         raise AssertionError
#                 else:
#                     print(f"## {instr[0]} statement Token Error in line at line_no {ct_line_no} statement_no {statement_no} ## ")
#                     raise AssertionError
#             else:
#                 print(f"## {instr[0]} statement Token Error in line at line_no {ct_line_no} statement_no {statement_no} ## ")
#                 raise AssertionError
#             num=int(instr[2][1:])
#             out+=(B[instr[0]] + Register[instr[1]] + bit_extend(num))
#             out+="\n"
            
#         elif instr[0] in C:
#             if len(instr)!=3:
#                 print(f"## {instr[0]} statement Token Error in line at line_no {ct_line_no} statement_no {statement_no} ## ")
#                 raise AssertionError
#             if ((instr[2][0]=="R") and (int(instr[2][1:])<=6)) or instr[2][:]=="FLAGS":
#                 out+=(C[instr[0]] + "00000" + Register[instr[1]] + Register[instr[2]])
#                 out+="\n"
#             else:
#                 print(f"## {instr[0]} statement Token Error in line at line_no {ct_line_no} statement_no {statement_no} ## ")
#                 raise AssertionError
                
#         elif instr[0] in D:
#             out+=(D[instr[0]] + Register[instr[1]] + vars[instr[2]])
#             out+="\n"
#         elif instr[0] in E:
#             instr.append(instr[1])
#             out+=(E[instr[0]] + "000" + vars[instr[1]])
#             out+="\n"
#         elif Instr=="hlt\n" or Instr=="hlt" or instr==['hlt']:
#             out+="0101000000000000"
#         elif instr[0]=="hlt":
#             out+="0101000000000000"
#         else:
#             print(f"statement Token Error in line at line_no {ct_line_no} statement_no {statement_no} ## ")
#             raise AssertionError
#     print(out)
# except AssertionError as Error:
#     # try:
#         print(Error)
#     # except:
#     #     print(f"## Error at line_no {ct_line_no} and statement_no {statement_no} ##")
# except KeyError as Error:
#     try:
#         print(f"{instr[2]} not initialized KeyError, ## Error at line_no {ct_line_no} and statement_no {statement_no} ## ")
#     except:
#         print(f"KeyError Error at line_no {ct_line_no} and statement_no {statement_no} ##")
# except IndexError as Error:
#     try:
#         print(f"## {instr[0]} statement Token Error IndexError in line at line_no {ct_line_no} statement_no {statement_no} ## ")
#     except:
#         print(f"IndexError Error at line_no {ct_line_no} and statement_no {statement_no} ##")
# except:
#     # try:
#         print(f"GENERAL SYNTAX statement Token Error in line at line_no {ct_line_no} statement_no {statement_no} ## ")
#     # except:
#     #     print(f"## Error at line_no {ct_line_no} and statement_no {statement_no} ##")























# # from sys import stdin

# # A={"add":"10000", "sub":"10001", "mul":"10110", "xor":"11010", "or":"11011", "and":"11100"}
# # B={"mov":"10010", "rs":"11000", "ls":"11001"}
# # C={"mov":"10011", "div":"10111", "not":"11101", "cmp":"11110"}
# # D={"ld":"10100", "st":"10101"}
# # E={"jmp":"11111", "jlt":"01100", "jgt":"01101", "je":"01111"}

# # Register={"R0":"000", "R1":"001", "R2":"010", "R3":"011", "R4":"100", "R5":"101", "R6":"110", "FLAGS":"111"}

# # def bit_extend(num):
# #     binum=bin(num)
# #     return "0"*(10-len(binum)) + binum[2:]

# # try:
# #     instr_list=stdin.readlines()
# #     var_address=-1
# #     for instr in instr_list:
# #         if not((instr=="\n" or instr=="") and instr.startswith("var")):
# #             var_address+=1

# #     assert var_address<=255

# #     labels=set()
# #     vars={}
# #     Errors=[]

# #     for i in range(len(instr_list)):
# #         Instr=instr_list[i]
# #         instr=Instr.split()
# #         start=instr[0]
# #         if Instr=="\n":
# #             continue
# #         elif start=="var":
# #             if i!=0:
# #                 bef_Instr=instr_list[i-1]
# #                 bef_instr=bef_Instr.split()
# #                 if bef_instr[0]!="var":
# #                     Errors.append(f"Error: At line {i+1}, variable not declared at the beginning of the program")
# #                 else:
# #                     vars[instr[1]]=bit_extend(var_address)
# #                     var_address+=1
# #             else:
# #                 vars[instr[1]]=bit_extend(var_address)
# #                 var_address+=1
# #         elif Instr=="hlt\n" and i!=len(instr_list)-1:
# #             Errors.append(f"Error: At line {i+1}, hlt instruction used in the middle of the program")
# #         elif i==len(instr_list)-1 and Instr!="hlt\n":
# #             Errors.append(f"Error: At line {i+1}, no hlt instruction at the end of the program")
# #         elif start[-1]==":":
# #             label=start[:-1]
# #             if label in A or label in B or label in C or label in D or label in E or label=="hlt" or label=="var":
# #                 Errors.append(f"Error: At line {i+1}, a label can't be an instruction")
# #             else:
# #                 labels.add(label)
# #         elif start in label:
# #             Errors.append(f"Error: At line {i+1}, improper use of label")
# #         elif "FLAGS" in Instr:
# #             illegal=False
# #             for i in range(7):
# #                 if Instr!=f"mov R{i} FLAGS":
# #                     illegal=True
# #             if illegal:
# #                 Errors.append(f"Error: At line {i+1}, illegal use of FLAGS")
# #         elif start in A and ((instr[1] not in Register) or (instr[2] not in Register) or (instr[3] not in Register)):
# #             Errors.append(f"Error: At line {i+1}, used undefined registers")
# #         elif start in B:
# #             if instr[1] not in Register:
# #                 Errors.append(f"Error: At line {i+1}, used undefined register")
# #             imm=int(instr[2][1:])
# #             if imm>255:
# #                 Errors.append(f"Error: At line {i+1}, immediate value exceeds 8 bits")
# #         elif start in C and ((instr[1] not in Register) or (instr[2] not in Register)):
# #             Errors.append(f"Error: At line {i+1}, used undefined registers")
# #         elif start in D:
# #             if instr[1] not in Register:
# #                 Errors.append(f"Error: At line {i+1}, used undefined registers")
# #             if instr[2] not in vars:
# #                 Errors.append(f"Error: At line {i+1}, tried to use an unallocated variable")
# #             if instr[2] in labels:
# #                 Errors.append(f"Error: At line {i+1}, tried to operate on a label")
# #         elif start in E:
# #             if instr[1] not in vars:
# #                 Errors.append(f"Error: At line {i+1}, tried to use an unallocated variable")
# #             if instr[1] in labels:
# #                 Errors.append(f"Error: At line {i+1}, tried to operate on a label")
# # except AssertionError:
# #     Errors.append("Not enough memory space")
# # except:
# #     Errors.append("General Syntax Error")

# # if not(Errors):
# #     print(Errors[0])
# # else:
# #     for Instr in instr_list:
# #         instr=Instr.split()
# #         if Instr=="\n" or instr[0]=="var":
# #             continue
# #         instr=Instr.split()
# #         if Instr=="":
# #             break
# #         elif instr[0] in A:
# #             print(A[instr[0]] + "00" + Register[instr[1]] + Register[instr[2]] + Register[instr[3]])
# #         elif instr[0] in B:
# #             num=int(instr[2][1:])
# #             print(B[instr[0]] + Register[instr[1]] + bit_extend(num))
# #         elif instr[0] in C:
# #             print(C[instr[0]] + "00000" + Register[instr[1]] + Register[instr[2]])
# #         elif instr[0] in D:
# #             print(D[instr[0]] + Register[instr[1]] + vars[instr[2]])
# #         elif instr[0] in E:
# #             print(E[instr[0]] + "000" + vars[instr[1]])
# #         elif Instr=="hlt\n":
# #             print("0101000000000000")
















# # import sys
# from sys import stdin

# # do we have to print code of label file?


# # stdin=open("CO Programme\input.txt","r")
# # sys.stdout=open("CO Programme\output.txt","w")
# try:

#     A={"add":"10000", "sub":"10001", "mul":"10110", "xor":"11010", "or":"11011", "and":"11100"}
#     B={"mov":"10010", "rs":"11000", "ls":"11001"}
#     C={"mov":"10011", "div":"10111", "not":"11101", "cmp":"11110"}
#     D={"ld":"10100", "st":"10101"}
#     E={"jmp":"11111", "jlt":"01100", "jgt":"01101", "je":"01111"}

#     Register={"R0":"000", "R1":"001", "R2":"010", "R3":"011", "R4":"100", "R5":"101", "R6":"110", "FLAGS":"111"}

#     def bit_extend(num):
#         binum=bin(num)
#         return "0"*(10-len(binum)) + binum[2:]

#     instr_list=stdin.readlines()
    
#     label_lst=[]
#     vars={}
#     var_lst=[]
#     ct_line_no=0 #
#     statement_no=0
#     ct_hlt=0
#     empt_line=0
#     var_line=0
#     hlt_flag=False
#     # var_top=True
#     # r=10
#     for i in instr_list:
#         statement_no+=1
#         ct_line_no+=1 #
#         # if r==0 and not i.startswith("var"):
            
#         if (i!="\n" or i=="") and ct_hlt==1:
#             # print(f"## More statement written after 1 hlt , hlt Error at line_no {ct_line_no} and statement_no {statement_no} ##")
#             assert ct_hlt!=1 , f"## More statement written after 1 hlt , hlt Error at line_no {ct_line_no} and statement_no {statement_no} ##"
#         temp=i.split()
#         if i=="hlt\n" or i=="hlt" or temp==['hlt']:
#             hlt_flag=True
#             ct_hlt+=1
#             # print(i,ct_line_no,ct_hlt,end="")
#             if (ct_hlt>1):
#                 print(f"More than 1 hlt , ## hlt Error at line_no {ct_line_no} and statement_no {statement_no} ##")
#                 raise AssertionError
#         if i.startswith("hlt"):
#             if temp!=['hlt']:
#                 assert temp==['hlt'] , f"## hlt statement Token Error in line at line_no {ct_line_no} statement_no {statement_no} ## "
            
#         if i=="\n":
#             empt_line+=1
#             statement_no-=1
#         if i.startswith("var"):
#             # assert i.startswith("var ") , f" ## var Token Error in line_no {ct_line_no} ##"
#             var_line+=1
#             assert len(i.split())==2 , f" ## var Token Error in line_no {ct_line_no} and statement_no {statement_no} ##"
#             # print(ct_line_no)
#             # print(var_line)
#             assert statement_no<=var_line , f"var not declared at top ## var Token Error in line_no {ct_line_no} and statement_no {statement_no} ##"
#             if i.split()[1] not in var_lst:
#                 var_lst.append(i.split()[1])
#             else:
#                 print(f"var {i.split()[1]} already declared above , ## Error at line_no {ct_line_no} and statement_no {statement_no} ##")
#                 raise AssertionError
#         # print(i,ct_line_no,ct_hlt,end="")
#         # if i.startswith("var"):
#         #     temp=i.strip()
#     if hlt_flag==False:
#         print(f"## No hlt given at end of code , error after line_no {ct_line_no} and statement_no {statement_no} ##")
#         raise AssertionError
#     # code_size=len(instr_list)-(var_line+empt_line)  
#     code_size=len(instr_list)-(empt_line) 
#     # print(code_size)
#     if code_size>256:
#         print("No of instructions exceed 256 statements ## var line is considered as instructions")
#         raise AssertionError
#     # if code_size>255 and var_line!=0:
#     #     print("No of instructions exceed 256 statements ## var line is considered as instructions")
#     #     raise AssertionError
#     ct_line_no=0
#     code_size=code_size-var_line
#     statement_no=0
#     var_name=""
#     out=""
#     for Instr in instr_list:
#         ct_line_no+=1
#         if Instr=="\n":
#             continue
#         statement_no+=1
#         instr=Instr.split()
#         # instr1=Instr.split()
#         # print(instr)
#         if instr=="":
#             break
#                 # if instr[0] not in A and instr[0] not in B and instr[0] not in C and instr[0] not in D and instr[0] not in E:
#         #     assert AssertionError
#         if (instr[0] not in A.keys()) and (instr[0] not in B.keys()) and (instr[0] not in C.keys()) and (instr[0] not in D.keys()) and (instr[0] not in E.keys()) and instr[0]!="var" and instr[0]!="hlt" and instr[0][-1]!=":":
#             # print(instr[0])
#             print(f"## {instr[0]} statement Token Error in line at line_no {ct_line_no} statement_no {statement_no} ## ")
#             raise AssertionError
#         ################
#         if instr[0][-1]==":":
#             if instr[0][0:-1] in label_lst :
#                 print (f"label {instr[0][0:-1]} is already given above , Error in line at line_no {ct_line_no} statement_no {statement_no} ##")
#                 raise AssertionError
#             elif len(instr)<=2:
#                 print (f"label {instr[0][0:-1]} Token Error in line at line_no {ct_line_no} statement_no {statement_no} ##")
#                 raise AssertionError
#             else:
#                 pass
#         #     code_size+=1
        
#         ################
#         if instr[0][-1]==":":
#             if instr[0][-2]==" ":
#                 assert instr[0][-2]!=" " , f"## {instr[0]} statement Token Error in line at line_no {ct_line_no} statement_no {statement_no} ## "
#             else:
#                 ########################
#                 label_lst.append(instr[0][0:-1])
#                 # label_lst[instr[0][:-1]]=bit_extend(code_size)
#                 # code_size-=1
#                 # print(code_size)
#                 vars[instr[0][:-1]]=bit_extend(code_size)  
#                 instr=instr[1:]
#                 # print(instr)              
#                 code_size+=1

                
#         if instr[0]=="var":
#             vars[instr[1]]=bit_extend(code_size)
#             code_size+=1
            
#         elif instr[0] in A:
#             temp=instr[2]
#             instr[2]=instr[3]
#             (A[instr[0]] + "00" + Register[instr[1]] + Register[instr[2]] + Register[instr[3]])
#             instr[2]=temp
#             out+=(A[instr[0]] + "00" + Register[instr[1]] + Register[instr[2]] + Register[instr[3]])
#             out+="\n"
#             # print(A[instr[0]] + "00" + Register[instr[1]] + Register[instr[2]] + Register[instr[3]])
#         elif instr[0] in B:
#             # print(instr[2][1:])
#             if (instr[2][1:]).isdigit():
#                 if (int(instr[2][1:])>=0 and int(instr[2][1:])<256):
#                     pass
#                 else:
#                     print(f"## {instr[0]} statement Token Error in line at line_no {ct_line_no} statement_no {statement_no} ## ")
#                     raise AssertionError
#             else:
#                 print(f"## {instr[0]} statement Token Error in line at line_no {ct_line_no} statement_no {statement_no} ## ")
#                 raise AssertionError
#             num=int(instr[2][1:])
#             # print(B[instr[0]] + Register[instr[1]] + bit_extend(num))
#             out+=(B[instr[0]] + Register[instr[1]] + bit_extend(num))
#             out+="\n"
#         elif instr[0] in C:
#             # print(C[instr[0]] + "00000" + Register[instr[1]] + Register[instr[2]])
#             out+=(C[instr[0]] + "00000" + Register[instr[1]] + Register[instr[2]])
#             out+="\n"
#         elif instr[0] in D:
#             # print(D[instr[0]] + Register[instr[1]] + vars[instr[2]])
#             # out+=(D[instr[0]] + Register[instr[1]] + vars[instr[2]])
#             out+=(D[instr[0]] + Register[instr[1]] + vars[instr[2]])
#             out+="\n"
#         elif instr[0] in E:
#             # print(E[instr[0]] + "000" + vars[instr[1]])
#             # out+=(E[instr[0]] + "000" + vars[instr[1]])
#             # print(instr[1])
#             # print(vars[instr[1]])
#             # print(E[instr[0]])
#             instr.append(instr[1])
#             out+=(E[instr[0]] + "000" + vars[instr[1]])
#             out+="\n"
#         elif Instr=="hlt\n" or Instr=="hlt" or instr==['hlt']:
#             # print("0101000000000000") 
#             out+="0101000000000000"
#             # out+="\n"
#     print(out)
# except AssertionError as Error:
#     print(Error)
# except KeyError as Error:
#     print(f"{instr[2]} not initialized, ## Error at line_no {ct_line_no} and statement_no {statement_no} ## ")
# except IndexError as Error:
#     print(f"## {instr[0]} statement Token Error in line at line_no {ct_line_no} statement_no {statement_no} ## ")