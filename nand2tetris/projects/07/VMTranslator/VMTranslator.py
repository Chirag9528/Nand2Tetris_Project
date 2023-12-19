import sys
from CodeWriter import CodeWriter
from Parser import Parser
class VMTranslator:
    def __init__(self,file):
        self.parser=Parser(file)
        file=file[:-3]+".asm"
        self.code=CodeWriter(file)
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
        self.code.close()
if __name__=="__main__":
    filename=sys.argv[1]
    a=VMTranslator(filename)
    a.translate()
