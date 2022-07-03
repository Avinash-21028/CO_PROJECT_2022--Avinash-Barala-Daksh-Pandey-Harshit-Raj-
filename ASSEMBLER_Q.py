# import sys
from sys import stdin

# do we have to print code of label file?


# stdin=open("CO Programme\input.txt","r")
# sys.stdout=open("CO Programme\output.txt","w")
try:

    A={"add":"10000", "sub":"10001", "mul":"10110", "xor":"11010", "or":"11011", "and":"11100"}
    B={"mov":"10010", "rs":"11000", "ls":"11001"}
    C={"mov":"10011", "div":"10111", "not":"11101", "cmp":"11110"}
    D={"ld":"10100", "st":"10101"}
    E={"jmp":"11111", "jlt":"01100", "jgt":"01101", "je":"01111"}

    Register={"R0":"000", "R1":"001", "R2":"010", "R3":"011", "R4":"100", "R5":"101", "R6":"110", "FLAGS":"111"}

    def bit_extend(num):
        binum=bin(num)
        return "0"*(10-len(binum)) + binum[2:]

    instr_list=stdin.readlines()
    
    label_lst=[]
    vars={}
    var_lst=[]
    ct_line_no=0 #
    statement_no=0
    ct_hlt=0
    empt_line=0
    var_line=0
    hlt_flag=False
    # var_top=True
    # r=10
    for i in instr_list:
        statement_no+=1
        ct_line_no+=1 #
        # if r==0 and not i.startswith("var"):
            
        if (i!="\n" or i=="") and ct_hlt==1:
            # print(f"## More statement written after 1 hlt , hlt Error at line_no {ct_line_no} and statement_no {statement_no} ##")
            assert ct_hlt!=1 , f"## More statement written after 1 hlt , hlt Error at line_no {ct_line_no} and statement_no {statement_no} ##"
        temp=i.split()
        if i=="hlt\n" or i=="hlt" or temp==['hlt']:
            hlt_flag=True
            ct_hlt+=1
            # print(i,ct_line_no,ct_hlt,end="")
            if (ct_hlt>1):
                print(f"More than 1 hlt , ## hlt Error at line_no {ct_line_no} and statement_no {statement_no} ##")
                raise AssertionError
        if i.startswith("hlt"):
            if temp!=['hlt']:
                assert temp==['hlt'] , f"## hlt statement Token Error in line at line_no {ct_line_no} statement_no {statement_no} ## "
            
        if i=="\n":
            empt_line+=1
            statement_no-=1
        if i.startswith("var"):
            # assert i.startswith("var ") , f" ## var Token Error in line_no {ct_line_no} ##"
            var_line+=1
            assert len(i.split())==2 , f" ## var Token Error in line_no {ct_line_no} and statement_no {statement_no} ##"
            # print(ct_line_no)
            # print(var_line)
            assert statement_no<=var_line , f"var not declared at top ## var Token Error in line_no {ct_line_no} and statement_no {statement_no} ##"
            if i.split()[1] not in var_lst:
                var_lst.append(i.split()[1])
            else:
                print(f"var {i.split()[1]} already declared above , ## Error at line_no {ct_line_no} and statement_no {statement_no} ##")
                raise AssertionError
        # print(i,ct_line_no,ct_hlt,end="")
        # if i.startswith("var"):
        #     temp=i.strip()
    if hlt_flag==False:
        print(f"## No hlt given at end of code , error after line_no {ct_line_no} and statement_no {statement_no} ##")
        raise AssertionError
    # code_size=len(instr_list)-(var_line+empt_line)  
    code_size=len(instr_list)-(empt_line) 
    # print(code_size)
    if code_size>256:
        print("No of instructions exceed 256 statements ## var line is considered as instructions")
        raise AssertionError
    # if code_size>255 and var_line!=0:
    #     print("No of instructions exceed 256 statements ## var line is considered as instructions")
    #     raise AssertionError
    ct_line_no=0
    code_size=code_size-var_line
    statement_no=0
    var_name=""
    out=""
    for Instr in instr_list:
        ct_line_no+=1
        if Instr=="\n":
            continue
        statement_no+=1
        instr=Instr.split()
        # instr1=Instr.split()
        # print(instr)
        if instr=="":
            break
                # if instr[0] not in A and instr[0] not in B and instr[0] not in C and instr[0] not in D and instr[0] not in E:
        #     assert AssertionError
        if (instr[0] not in A.keys()) and (instr[0] not in B.keys()) and (instr[0] not in C.keys()) and (instr[0] not in D.keys()) and (instr[0] not in E.keys()) and instr[0]!="var" and instr[0]!="hlt" and instr[0][-1]!=":":
            # print(instr[0])
            print(f"## {instr[0]} statement Token Error in line at line_no {ct_line_no} statement_no {statement_no} ## ")
            raise AssertionError
        ################
        if instr[0][-1]==":":
            if instr[0][0:-1] in label_lst :
                print (f"label {instr[0][0:-1]} is already given above , Error in line at line_no {ct_line_no} statement_no {statement_no} ##")
                raise AssertionError
            elif len(instr)<=2:
                print (f"label {instr[0][0:-1]} Token Error in line at line_no {ct_line_no} statement_no {statement_no} ##")
                raise AssertionError
            else:
                pass
        #     code_size+=1
        
        ################
        if instr[0][-1]==":":
            if instr[0][-2]==" ":
                assert instr[0][-2]!=" " , f"## {instr[0]} statement Token Error in line at line_no {ct_line_no} statement_no {statement_no} ## "
            else:
                ########################
                label_lst.append(instr[0][0:-1])
                # label_lst[instr[0][:-1]]=bit_extend(code_size)
                # code_size-=1
                # print(code_size)
                vars[instr[0][:-1]]=bit_extend(code_size)  
                instr=instr[1:]
                # print(instr)              
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
            # print(A[instr[0]] + "00" + Register[instr[1]] + Register[instr[2]] + Register[instr[3]])
        elif instr[0] in B:
            # print(instr[2][1:])
            if (instr[2][1:]).isdigit():
                if (int(instr[2][1:])>=0 and int(instr[2][1:])<256):
                    pass
                else:
                    print(f"## {instr[0]} statement Token Error in line at line_no {ct_line_no} statement_no {statement_no} ## ")
                    raise AssertionError
            else:
                print(f"## {instr[0]} statement Token Error in line at line_no {ct_line_no} statement_no {statement_no} ## ")
                raise AssertionError
            num=int(instr[2][1:])
            # print(B[instr[0]] + Register[instr[1]] + bit_extend(num))
            out+=(B[instr[0]] + Register[instr[1]] + bit_extend(num))
            out+="\n"
        elif instr[0] in C:
            # print(C[instr[0]] + "00000" + Register[instr[1]] + Register[instr[2]])
            out+=(C[instr[0]] + "00000" + Register[instr[1]] + Register[instr[2]])
            out+="\n"
        elif instr[0] in D:
            # print(D[instr[0]] + Register[instr[1]] + vars[instr[2]])
            # out+=(D[instr[0]] + Register[instr[1]] + vars[instr[2]])
            out+=(D[instr[0]] + Register[instr[1]] + vars[instr[2]])
            out+="\n"
        elif instr[0] in E:
            # print(E[instr[0]] + "000" + vars[instr[1]])
            # out+=(E[instr[0]] + "000" + vars[instr[1]])
            # print(instr[1])
            # print(vars[instr[1]])
            # print(E[instr[0]])
            instr.append(instr[1])
            out+=(E[instr[0]] + "000" + vars[instr[1]])
            out+="\n"
        elif Instr=="hlt\n" or Instr=="hlt" or instr==['hlt']:
            # print("0101000000000000") 
            out+="0101000000000000"
            # out+="\n"
    print(out)
except AssertionError as Error:
    print(Error)
except KeyError as Error:
    print(f"{instr[2]} not initialized, ## Error at line_no {ct_line_no} and statement_no {statement_no} ## ")
except IndexError as Error:
    print(f"## {instr[0]} statement Token Error in line at line_no {ct_line_no} statement_no {statement_no} ## ")