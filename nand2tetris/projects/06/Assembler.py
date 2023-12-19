import sys
class Parser:
    def __init__(self,file):
        f=open(file,"r")
        self.f=f
        self.current_instruction=None
    def hasMoreLines(self):
        a=self.f.tell()
        line=self.f.readline()
        line=line.rstrip('\n')
        if len(line)==0:
            b=self.f.read()
            if b=="":
                return False
            else:
                self.f.seek(a)
                return True
        else:
            self.f.seek(a)
            return True
    def advance(self):
        if self.hasMoreLines()==True:
            line=self.f.readline().rstrip("\n")
            if line.startswith("//")==True or len(line)==0:
                self.advance()
            else:
                line=line.lstrip(" ")
                c=line.find("//")
                if c!=-1:
                    d=line.find(" ")
                    line=line[:d]
                line=line.rstrip(" ")
                self.current_instruction=line
    def instructionType(self):
        if self.current_instruction.startswith("@")==True:
            return "A_INSTRUCTION"
        elif self.current_instruction.startswith("(")==True:
            return "L_INSTRUCTION"
        else:
            return "C_INSTRUCTION"
    def dest(self):
        line=self.current_instruction
        e=line.find("=")
        if e!=-1:
            return line[:e]
        else:
            return "null"
    def comp(self):
        line=self.current_instruction
        f=line.find("=")
        g=line.find(";")            
        if f!=-1:
            return line[f+1:]
        else:
            return line[:g]
    def jump(self):
        line=self.current_instruction
        h=line.find(";")
        if h!=-1:
            return line[h+1:]
        else:
            return "null"

class CodeModule:
    def __init__(self):
        pass
    def dest(self,string):
        if string=="M":
            return '001'
        elif string=="D":
            return "010"
        elif string=="A":
            return "100"
        elif string=="DM" or string=="MD":
            return "011"
        elif string=="AM" or string=="MA":
            return "101"
        elif string=="AD" or string=="DA":
            return "110"
        elif string in ["AMD","ADM","DAM","DMA","MAD","MDA"]:
            return "111"
        else:
            return "000"
    def jump(self,string):
        if string=="null":
            return "000"
        elif string=="JGT":
            return "001"
        elif string=="JEQ":
            return "010"
        elif string=="JGE":
            return "011"
        elif string=="JLT":
            return "100"
        elif string=="JNE":
            return "101"
        elif string=="JLE":
            return "110"
        else:
            return "111"
    def comp(self,string):
        if string=="D|A":
            return "0010101"
        elif string=="D&A":
            return "0000000"
        elif string=="A-D":
            return "0000111"
        elif string=="D-A":
            return "0010011"
        elif string=="D+A":
            return "0000010"
        elif string=="A-1":
            return "0110010"
        elif string=="D-1":
            return "0001110"
        elif string=="A+1":
            return "0110111"
        elif string=="D+1":
            return "0011111"
        elif string=="-A":
            return "0110011"
        elif string=="-D":
            return "0001111"
        elif string=="!A":
            return "0110001"
        elif string=="!D":
            return "0001101"
        elif string=="A":
            return "0110000"
        elif string=="D":
            return "0001100"
        elif string=="-1":
            return "0111010"
        elif string=="1":
            return "0111111"
        elif string=="0":
            return "0101010"
        elif string=="M":
            return "1110000"
        elif string=="!M":
            return "1110001"
        elif string=="-M":
            return "1110011"
        elif string=="M+1":
            return "1110111"
        elif string=="M-1":
            return "1110010"
        elif string=="D+M":
            return "1000010"
        elif string=="D-M":
            return "1010011"
        elif string=="M-D":
            return "1000111"
        elif string=="D&M":
            return "1000000"
        else:
            return "1010101"

class SymbolTable:
    def __init__(self):
        self.table={"R0":0,"R1":1,"R2":2,"R3":3,"R4":4,"R5":5,"R6":6,"R7":7,"R8":8,"R9":9,"R10":10,"R11":11,"R12":12,"R13":13,"R14":14,"R15":15,"SCREEN":16384,"KBD":24576,"SP":0,"LCL":1,"ARG":2,"THIS":3,"THAT":4}
    def addEntry(self,symbol,address):
        self.table.update({symbol:address})
    def contains(self,symbol):
        if symbol in self.table.keys():
            return True
        else:
            return False
    def getAddress(self,symbol):
        return self.table[symbol]

class HackAssembler:
    def __init__(self,file):
        self.file=file
        j=SymbolTable()
        self.j=j
        file1=file[:-4]+".hack"
        g=open(file1,"w")
        self.g=g
    def dectobin(self,string):
        convert=bin(int(string))[2:]
        while len(convert)!=15:
            convert="0"+convert
        return convert
    def assemble(self):
        parser=Parser(self.file)
        code=CodeModule()
        counter=0
        while parser.hasMoreLines()==True:
            parser.advance()
            line=parser.current_instruction
            if parser.instructionType()=="L_INSTRUCTION":
                symbol=parser.current_instruction[1:len(line)-1]
                self.j.addEntry(symbol,counter)
            else:
                counter+=1
        parser.f.seek(0)
        blank=16
        while parser.hasMoreLines()==True:
            parser.advance()
            line=parser.current_instruction
            if parser.instructionType()=="A_INSTRUCTION":
                k=line[1:]
                if k.isdigit()==True:
                    write="0"+self.dectobin(k)+"\n"
                    self.g.write(write)
                else:
                    if self.j.contains(k):
                        address=self.j.getAddress(k)
                        write="0"+self.dectobin(address)+"\n"
                        self.g.write(write)
                    else:
                        self.j.addEntry(k,blank)
                        write="0"+self.dectobin(blank)+"\n"
                        self.g.write(write)
                        blank+=1
            if parser.instructionType()=="C_INSTRUCTION":
                dest=parser.dest()
                comp=parser.comp()
                jump=parser.jump()
                dest=code.dest(dest)
                comp=code.comp(comp)
                jump=code.jump(jump)
                write="111"+comp+dest+jump+"\n"
                self.g.write(write)

if __name__=="__main__":
    filename=sys.argv[1]
    a=HackAssembler(filename)
    a.assemble()
    
