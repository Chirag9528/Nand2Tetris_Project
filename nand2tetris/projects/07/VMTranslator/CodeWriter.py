class CodeWriter:
    def __init__(self,file):
        self.file1=file
        g=open(file,"w")
        self.g=g
        self.variable=0
    def writeArithmetic(self,command):
        if command=="add":
            string=f'@SP\nM=M-1\nA=M\nD=M\n@SP\nM=M-1\nA=M\nD=D+M\nM=D\n@SP\nM=M+1\n'
            self.g.write(string)
        if command=="sub":
            string=f'@SP\nM=M-1\nA=M\nD=M\n@SP\nM=M-1\nA=M\nD=M-D\nM=D\n@SP\nM=M+1\n'
            self.g.write(string)
        if command=="neg":
            string=f'@SP\nM=M-1\nA=M\nM=-M\n@SP\nM=M+1\n'
            self.g.write(string)
        if command=="and":
            string=f'@SP\nM=M-1\nA=M\nD=M\n@SP\nM=M-1\nA=M\nD=D&M\nM=D\n@SP\nM=M+1\n'
            self.g.write(string)
        if command=="or":
            string=f'@SP\nM=M-1\nA=M\nD=M\n@SP\nM=M-1\nA=M\nD=D|M\nM=D\n@SP\nM=M+1\n'
            self.g.write(string)
        if command=="not":
            string=f'@SP\nM=M-1\nA=M\nM=!M\n@SP\nM=M+1\n'
            self.g.write(string)
        if command=="eq":
            string=f'@SP\nM=M-1\nA=M\nD=M\n@SP\nM=M-1\nA=M\nD=D-M\n@TRUE{self.variable}\nD;JEQ\n@SP\nA=M\nM=0\n@SP\nM=M+1\n@END{self.variable}\n0;JMP\n(TRUE{self.variable})\n@SP\nA=M\nM=-1\n@SP\nM=M+1\n(END{self.variable})\n'
            self.g.write(string)    
            self.variable+=1    
        if command=="lt":
            string=f'@SP\nM=M-1\nA=M\nD=M\n@SP\nM=M-1\nA=M\nD=D-M\n@TRUE{self.variable}\nD;JGT\n@SP\nA=M\nM=0\n@SP\nM=M+1\n@END{self.variable}\n0;JMP\n(TRUE{self.variable})\n@SP\nA=M\nM=-1\n@SP\nM=M+1\n(END{self.variable})\n'
            self.g.write(string)
            self.variable+=1       
        if command=="gt":
            string=f'@SP\nM=M-1\nA=M\nD=M\n@SP\nM=M-1\nA=M\nD=D-M\n@TRUE{self.variable}\nD;JLT\n@SP\nA=M\nM=0\n@SP\nM=M+1\n@END{self.variable}\n0;JMP\n(TRUE{self.variable})\n@SP\nA=M\nM=-1\n@SP\nM=M+1\n(END{self.variable})\n'
            self.g.write(string)
            self.variable+=1        
    def writePushPop(self,command,segment,index):
        if command=="C_PUSH":
            if segment=="constant":
                string=f'@{index}\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n'
                self.g.write(string)
            if segment=="local":
                string=f'@LCL\nD=M\n@{index}\nD=D+A\nA=D\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n'
                self.g.write(string)
            if segment=="argument":
                string=f'@ARG\nD=M\n@{index}\nD=D+A\nA=D\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n'
                self.g.write(string)
            if segment=="this":
                string=f'@THIS\nD=M\n@{index}\nD=D+A\nA=D\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n'
                self.g.write(string)
            if segment=="that":
                string=f'@THAT\nD=M\n@{index}\nD=D+A\nA=D\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n'
                self.g.write(string)
            if segment=="temp":
                string=f'@5\nD=A\n@{index}\nD=D+A\nA=D\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n'
                self.g.write(string)
            if segment=="pointer":
                if index=="0":
                    string=f'@THIS\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n'
                if index=="1":
                    string=f'@THAT\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n'
                self.g.write(string)
            if segment=="static":
                file=self.file1[:-4]
                b=0
                for i in range(len(file)-1,0,-1):
                    if file[i]=="\\" or file[i]=="/":
                        b=i
                        break
                file=file[b+1:]
                filename=f'{file}.{index}'
                string=f'@{filename}\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n'
                self.g.write(string)
        elif command=="C_POP":
            if segment=="local":
                string=f'@LCL\nD=M\n@{index}\nD=D+A\n@R13\nM=D\n@SP\nM=M-1\nA=M\nD=M\n@R13\nA=M\nM=D\n'
                self.g.write(string) 
            if segment=="argument":
                string=f'@ARG\nD=M\n@{index}\nD=D+A\n@R13\nM=D\n@SP\nM=M-1\nA=M\nD=M\n@R13\nA=M\nM=D\n'
                self.g.write(string) 
            if segment=="this":
                string=f'@THIS\nD=M\n@{index}\nD=D+A\n@R13\nM=D\n@SP\nM=M-1\nA=M\nD=M\n@R13\nA=M\nM=D\n'
                self.g.write(string) 
            if segment=="that":
                string=f'@THAT\nD=M\n@{index}\nD=D+A\n@R13\nM=D\n@SP\nM=M-1\nA=M\nD=M\n@R13\nA=M\nM=D\n'
                self.g.write(string)     
            if segment=="temp":
                string=f'@5\nD=A\n@{index}\nD=D+A\n@R13\nM=D\n@SP\nM=M-1\nA=M\nD=M\n@R13\nA=M\nM=D\n'
                self.g.write(string)
            if segment=="pointer":
                if index=="0":
                    string=f'@SP\nM=M-1\nA=M\nD=M\n@THIS\nM=D\n'
                if index=="1":
                    string=f'@SP\nM=M-1\nA=M\nD=M\n@THAT\nM=D\n'
                self.g.write(string)
            if segment=="static":
                file=self.file1[:-4]
                b=0
                for i in range(len(file)-1,0,-1):
                    if file[i]=="\\" or file[i]=="/":
                        b=i
                        break
                file=file[b+1:]
                filename=f'{file}.{index}'
                string=f'@SP\nM=M-1\nA=M\nD=M\n@{filename}\nM=D\n'
                self.g.write(string)
    def close(self):
        string=f'(END)\n@END\n0;JMP\n'
        self.g.write(string)