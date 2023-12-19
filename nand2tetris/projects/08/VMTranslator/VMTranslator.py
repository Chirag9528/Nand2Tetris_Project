import sys
from CodeWriter import CodeWriter
from Parser import Parser
import os
class VMTranslator:
    def __init__(self,file):
        samp=file
        if samp.find(".vm")!=-1:
            file=file[:-3]+".asm"
            self.code=CodeWriter(file,samp)
            self.parser=Parser(samp)
            self.translate()
        else:
            if samp[-1]=="\\":
                fileabc=samp.split("\\")[-2]
            elif samp[-1]=="/":
                fileabc=samp.split("/")[-2]
            else:
                fileabc=samp.split("\\")[-1].split("/")[-1]
            listabc=[]
            for (root,dirs,files) in os.walk(samp):
                for f in files:
                    if f.find(".vm")!=-1:
                        listabc.append(f)
            if len(listabc)!=1:
                if samp.find("\\")!=-1:
                    self.code=CodeWriter(samp+"\\"+fileabc+".asm",samp)
                else:
                    self.code=CodeWriter(samp+"/"+fileabc+".asm",samp)
                string=f'@256\nD=A\n@SP\nM=D\n'
                self.code.g.write(string)
                self.code.writeCall("Sys.init",0)
            for (root,dirs,files) in os.walk(samp):
                for f in files:
                    if f.find(".vm")!=-1:
                        if samp.find("\\")!=-1:
                            self.code=CodeWriter(samp+"\\"+fileabc+".asm",samp+"\\"+f)
                            self.parser=Parser(samp+"\\"+f)
                        else:
                            self.code=CodeWriter(samp+"/"+fileabc+".asm",samp+"/"+f)
                            self.parser=Parser(samp+"/"+f)
                        self.translate()
            
    def translate(self):
        while self.parser.hasMoreLines()==True:
            self.parser.advance()
            line=self.parser.current_command
            if self.parser.commandType()=="C_ARITHMETIC":
                self.code.writeArithmetic(line)
            if self.parser.commandType()=="C_PUSH":
                segment=self.parser.arg1()
                index=self.parser.arg2()
                self.code.writePushPop("C_PUSH",segment,index)
            if self.parser.commandType()=="C_POP":
                segment=self.parser.arg1()
                index=self.parser.arg2()
                self.code.writePushPop("C_POP",segment,index)
            if self.parser.commandType()=="C_LABEL":
                label=self.parser.arg1()
                self.code.writeLabel(label)
            if self.parser.commandType()=="C_IF":
                label=self.parser.arg1()
                self.code.writeIf(label)
            if self.parser.commandType()=="C_GOTO":
                label=self.parser.arg1()
                self.code.writeGoto(label)
            if self.parser.commandType()=="C_FUNCTION":
                functionname=self.parser.arg1()
                nVars=self.parser.arg2()
                self.code.writeFunction(functionname,nVars)
            if self.parser.commandType()=="C_CALL":
                functionname=self.parser.arg1()
                nVars=self.parser.arg2()
                self.code.writeCall(functionname,nVars)
            if self.parser.commandType()=="C_RETURN":
                self.code.writeReturn()
        self.code.close()
if __name__=="__main__":
    filename=sys.argv[1]
    a=VMTranslator(filename)
