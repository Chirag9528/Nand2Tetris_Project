import sys
import os
from JackTokenizer import JackTokenizer
from CompilationEngine import CompilationEngine

class JackCompiler:
    def __init__(self,file):
        if file.find(".jack")!=-1:
            self.file=file
            write=file[:-5]+"T.xml"
            rewrite=file[:-5]+".xml"
            self.rewrite=rewrite
            self.write=write
            g=open(write,"w")
            self.g=g
            self.g.write("<tokens>\n")
            self.tokenize()
            self.parsing()
        else:
            for (root,dir,files) in os.walk(file):
                for f in files:
                    if f.find(".jack")!=-1:
                        self.file=file+f
                        f=file+f
                        write=f[:-5]+"T.xml"
                        rewrite=f[:-5]+".xml"
                        self.rewrite=rewrite
                        self.write=write
                        g=open(write,"w")
                        self.g=g
                        self.g.write("<tokens>\n")
                        self.tokenize()
                        self.parsing()
    def tokenize(self):
        b=JackTokenizer(self.file)
        while (b.hasMoreLines()):
            b.filter()
        b.makingTokens()
        while (b.hasMoreTokens()):
            b.advance()
            string1=b.current_token
            if b.tokenType()=="KEYWORD":
                self.g.write(f'<keyword> {string1} </keyword>\n')
            elif b.tokenType()=="SYMBOL":
                self.g.write(f'<symbol> {b.symbol()} </symbol>\n')
            elif b.tokenType()=="IDENTIFIER":
                self.g.write(f'<identifier> {string1} </identifier>\n')
            elif b.tokenType()=="STRING_CONST":
                self.g.write(f'<stringConstant> {b.stringVal()} </stringConstant>\n')
            else:
                self.g.write(f'<integerConstant> {b.intVal()} </integerConstant>\n')
        self.g.write("</tokens>\n")
        self.g.close()
    def parsing(self):
        z=CompilationEngine(self.write,self.rewrite)
        z.compileClass()


if __name__=="__main__":
    filename=sys.argv[1]
    a=JackCompiler(filename)
