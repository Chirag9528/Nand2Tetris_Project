from SymbolTable import SymbolTable
from VMWriter import VMWriter
class CompilationEngine:
    def __init__(self,file1,file2):
        self.f=open(file1,"r")
        self.f.readline()
        self.classtable=SymbolTable()
        self.routinetable=SymbolTable()
        self.towrite=VMWriter(file2)
        self.counter=0
        self.classname=""
        
    def compileClass(self):
        self.classtable.reset()
        keyword=self.f.readline()
        classname=self.f.readline()
        self.classname=classname.split(">")[1].split("<")[0].strip(" ")
        symbol=self.f.readline()
        run=True
        while run:
            a=self.f.tell()
            nexttoken=self.f.readline()
            if nexttoken.find("static")!=-1 or nexttoken.find("field")!=-1:
                self.f.seek(a)
                self.compileClassVarDec()
            elif nexttoken.find("function")!=-1 or nexttoken.find("method")!=-1 or nexttoken.find("constructor")!=-1:
                self.f.seek(a)
                self.compileSubroutine()
            else:
                self.f.seek(a)
                run=False
        symbol=self.f.readline()
        
    def compileClassVarDec(self):
        keyword=self.f.readline()
        keyword=keyword.split(">")[1].split("<")[0].strip(" ")
        typetoken=self.f.readline()
        typetoken=typetoken.split(">")[1].split("<")[0].strip(" ")
        identifier=self.f.readline()
        identifier=identifier.split(">")[1].split("<")[0].strip(" ")
        self.classtable.define(identifier,typetoken,keyword)
        run=True
        while run:
            a=self.f.tell()
            nexttoken=self.f.readline()
            self.f.seek(a)
            if nexttoken.find(";")!=-1:
                symbol=self.f.readline()
                run=False
            elif nexttoken.find(",")!=-1:
                symbol=self.f.readline()
                identifier=self.f.readline()
                identifier=identifier.split(">")[1].split("<")[0].strip(" ")
                self.classtable.define(identifier,typetoken,keyword)
            else:
                break

    def compileSubroutine(self):
        keyword=self.f.readline()
        keyword1=keyword.split(">")[1].split("<")[0].strip(" ")
        keyword=self.f.readline()
        keyword2=keyword.split(">")[1].split("<")[0].strip(" ")
        subroutineName=self.f.readline()
        subname1=subroutineName.split(">")[1].split("<")[0].strip(" ")
        symbol=self.f.readline()
        self.compileParameterList(keyword1)
        symbol=self.f.readline()
        self.compileSubroutineBody(keyword1,keyword2,subname1)

    def compileParameterList(self,funct):
        self.routinetable.reset()
        if funct=="method":
            self.routinetable.define("this",self.classname,"argument")
        a=self.f.tell()
        nexttoken=self.f.readline()
        self.f.seek(a)
        if nexttoken.find("<keyword>")!=-1 or nexttoken.find("<identifier>")!=-1:
            typetoken=self.f.readline()
            varName=self.f.readline()
            typetoken=typetoken.split(">")[1].split("<")[0].strip(" ")
            varName=varName.split(">")[1].split("<")[0].strip(" ")
            self.routinetable.define(varName,typetoken,"argument")
            run=True
            while run:
                a=self.f.tell()
                nexttoken=self.f.readline()
                self.f.seek(a)
                if nexttoken.find(";")!=-1:
                    symbol=self.f.readline()
                    run=False
                elif nexttoken.find(",")!=-1:
                    symbol=self.f.readline()
                    typetoken=self.f.readline()
                    typetoken=typetoken.split(">")[1].split("<")[0].strip(" ")
                    identifier=self.f.readline()
                    identifier=identifier.split(">")[1].split("<")[0].strip(" ")
                    self.routinetable.define(identifier,typetoken,"argument")
                else:
                    break

    def compileSubroutineBody(self,funct,type,name):
        symbol=self.f.readline()
        run=True
        while run:
            a=self.f.tell()
            nexttoken=self.f.readline()
            if nexttoken.find("var")!=-1:
                self.f.seek(a)
                self.compileVarDec()
            else:
                self.f.seek(a)
                run=False
        if funct=="constructor":
            fieldcount=self.classtable.varCount("field")
            localcount=self.routinetable.varCount("local")
            name=f'{type}.{name}'
            self.towrite.writeFunction(name,localcount)
            self.towrite.writePush("constant",fieldcount)
            self.towrite.writeCall("Memory.alloc",1)
            self.towrite.writePop("pointer",0)
        if funct=="method":
            localcount=self.routinetable.varCount("local")
            name=f'{self.classname}.{name}'
            self.towrite.writeFunction(name,localcount)
            self.towrite.writePush("argument",0)
            self.towrite.writePop("pointer",0)
        if funct=="function":
            localcount=self.routinetable.varCount("local")
            name=f'{self.classname}.{name}'
            self.towrite.writeFunction(name,localcount)
        self.compileStatements()
        symbol=self.f.readline()

    def compileVarDec(self):
        keyword=self.f.readline()
        keyword=keyword.split(">")[1].split("<")[0].strip(" ")
        typetoken=self.f.readline()
        typetoken=typetoken.split(">")[1].split("<")[0].strip(" ")
        varName=self.f.readline()
        varName=varName.split(">")[1].split("<")[0].strip(" ")
        self.routinetable.define(varName,typetoken,"local")
        run=True
        while run:
            a=self.f.tell()
            nexttoken=self.f.readline()
            self.f.seek(a)
            if nexttoken.find(";")!=-1:
                run=False
            else:
                symbol=self.f.readline()
                varName=self.f.readline()
                varName=varName.split(">")[1].split("<")[0].strip(" ")
                self.routinetable.define(varName,typetoken,"local")
        symbol=self.f.readline()

    def compileStatements(self):
        run=True
        while run:
            a=self.f.tell()
            nexttoken=self.f.readline()
            self.f.seek(a)            
            if nexttoken.find(" let ")!=-1:
                self.compileLet()
            elif nexttoken.find(" if ")!=-1:
                self.compileIf()
            elif nexttoken.find(" while ")!=-1:
                self.compileWhile()
            elif nexttoken.find(" do ")!=-1:
                self.compileDo()
            elif nexttoken.find(" return ")!=-1:
                self.compileReturn()
            else:
                run=False

    def compileLet(self):
        keyword=self.f.readline()
        varName=self.f.readline()
        nexttoken=self.f.readline()
        if nexttoken.find("[")!=-1:
            varName=varName.split(">")[1].split("<")[0].strip(" ")
            found=self.routinetable.member(varName)
            if found:
                kind=self.routinetable.kindOf(varName)
                idx=self.routinetable.indexOf(varName)
                self.towrite.writePush(kind,idx)
            else:
                found=self.classtable.member(varName)
                if found:
                    kind=self.classtable.kindOf(varName)
                    idx=self.classtable.indexOf(varName)
                    self.towrite.writePush(kind,idx)
                else:
                    print("Variable not found")
            self.compileExpression()
            self.towrite.writeArithmetic("+")
            symbol=self.f.readline()
            symbol=self.f.readline()
            self.compileExpression()
            self.towrite.writePop("temp",0)
            self.towrite.writePop("pointer",1)
            self.towrite.writePush("temp",0)
            self.towrite.writePop("that",0)
        else:
            self.compileExpression()
            varName=varName.split(">")[1].split("<")[0].strip(" ")
            found=self.routinetable.member(varName)
            if found:
                kind=self.routinetable.kindOf(varName)
                idx=self.routinetable.indexOf(varName)
                self.towrite.writePop(kind,idx)
            else:
                found=self.classtable.member(varName)
                if found:
                    kind=self.classtable.kindOf(varName)
                    idx=self.classtable.indexOf(varName)
                    self.towrite.writePop(kind,idx)
                else:
                    print("Variable not found")
        symbol=self.f.readline()

    def compileIf(self):
        keyword=self.f.readline()
        symbol=self.f.readline()
        self.compileExpression()
        self.towrite.writeArithmetic("~")
        label1=self.counter
        self.towrite.writeIf(label1)
        self.counter+=1
        symbol=self.f.readline()
        symbol=self.f.readline()
        self.compileStatements()
        label2=self.counter
        self.towrite.writeGoto(label2)
        self.towrite.writeLabel(label1)
        self.counter+=1
        symbol=self.f.readline()
        a=self.f.tell()
        nexttoken=self.f.readline()
        if nexttoken.find("else")!=-1:
            symbol=self.f.readline()
            self.compileStatements()
            symbol=self.f.readline()
        else:
            self.f.seek(a)
        self.towrite.writeLabel(label2)

    def compileWhile(self):
        label3=self.counter
        self.counter+=1
        self.towrite.writeLabel(label3)
        keyword=self.f.readline()
        symbol=self.f.readline()
        self.compileExpression()
        self.towrite.writeArithmetic("~")
        label4=self.counter
        self.counter+=1
        self.towrite.writeIf(label4)
        symbol=self.f.readline()
        symbol=self.f.readline()
        self.compileStatements()
        self.towrite.writeGoto(label3)
        self.towrite.writeLabel(label4)
        symbol=self.f.readline()   

    def compileDo(self):
        keyword=self.f.readline()
        self.compileSubroutineCall()
        symbol=self.f.readline()
        self.towrite.writePop("temp",0)

    def compileReturn(self):
        keyword=self.f.readline()
        a=self.f.tell()
        nexttoken=self.f.readline()
        if nexttoken.find(";")==-1:
            self.f.seek(a)
            self.compileExpression()
            symbol=self.f.readline()
            self.towrite.writeReturn()
        else:
            self.towrite.writePush("constant",0)
            self.towrite.writeReturn()

    def compileExpression(self):
        op_list=['+','-','*',' / ','&amp;','|','&lt;','&gt;','=']
        self.compileTerm()
        run=True
        while run:
            a=self.f.tell()
            nexttoken=self.f.readline()
            found=False
            for i in op_list:
                if nexttoken.find(i)!=-1:
                    found=True
                    break
            if found:
                self.compileTerm()
                operator=nexttoken.split(">")[1].split("<")[0].strip(" ")
                if operator=="*":
                    self.towrite.writeCall("Math.multiply",2)
                elif operator=="/":
                    self.towrite.writeCall("Math.divide",2)
                else:
                    self.towrite.writeArithmetic(operator)
            else:
                self.f.seek(a)
                run=False

    def compileTerm(self):
        a=self.f.tell()
        nexttoken=self.f.readline()
        nexttonext=self.f.readline()
        ntoken=nexttoken.split(">")[1].split("<")[0].strip(" ")
        ntonext=nexttonext.split(">")[1].split("<")[0].strip(" ")
        if nexttoken.find("<identifier>")!=-1 and ntonext=="[":
            found=self.routinetable.member(ntoken)
            if found:
                kind=self.routinetable.kindOf(ntoken)
                idx=self.routinetable.indexOf(ntoken)
                self.towrite.writePush(kind,idx)
            else:
                found=self.classtable.member(ntoken)
                if found:
                    kind=self.classtable.kindOf(ntoken)
                    idx=self.classtable.indexOf(ntoken)
                    self.towrite.writePush(kind,idx)
                else:
                    print("Variable not found")
            self.compileExpression()
            self.towrite.writeArithmetic("+")
            self.towrite.writePop("pointer",1)
            self.towrite.writePush("that",0)
            symbol=self.f.readline()
        elif ntoken=="(":
            self.f.seek(a)
            symbol=self.f.readline()
            self.compileExpression()
            symbol=self.f.readline()
        elif ntoken=="-" or ntoken=="~":
            self.f.seek(a)
            symbol=self.f.readline()
            self.compileTerm()
            if ntoken=="-":
                self.towrite.writeArithmetic("neg")
            if ntoken=="~":
                self.towrite.writeArithmetic(ntoken)
        elif ntoken.isdigit()==True:
            self.f.seek(a)
            symbol=self.f.readline()
            symbol=symbol.split(">")[1].split("<")[0].strip(" ")
            self.towrite.writePush("constant",symbol)
        elif ntoken in ['true','false','null','this']:
            self.f.seek(a)
            keyword=self.f.readline()
            keyword=keyword.split(">")[1].split("<")[0].strip(" ")
            if keyword=='true':
                self.towrite.vm.write(f'push constant 1\nneg\n')
            elif keyword=='false' or keyword=='null':
                self.towrite.vm.write(f'push constant 0\n')
            elif keyword=="this":
                self.towrite.vm.write(f'push pointer 0\n')
        elif nexttoken.find("stringConstant")!=-1:
            self.f.seek(a)
            string=self.f.readline()
            string=string.split(">")[1].split("<")[0].lstrip(" ")[:-1]
            length=len(string)
            self.towrite.writePush("constant",length)
            self.towrite.writeCall("String.new",1)
            for i in range(0,length):
                self.towrite.writePush("constant",ord(string[i]))
                self.towrite.writeCall("String.appendChar",2)
        elif ntonext!="(" and ntonext!="." and nexttoken.find("<identifier>")!=-1:
            self.f.seek(a)
            varName=self.f.readline()
            varName=varName.split(">")[1].split("<")[0].strip(" ")
            found=self.routinetable.member(varName)
            if found:
                kind=self.routinetable.kindOf(varName)
                idx=self.routinetable.indexOf(varName)
                self.towrite.writePush(kind,idx)
            else:
                found=self.classtable.member(varName)
                if found:
                    kind=self.classtable.kindOf(varName)
                    idx=self.classtable.indexOf(varName)
                    self.towrite.writePush(kind,idx)
                else:
                    print("Variable not found")
        else:
            self.f.seek(a)
            self.compileSubroutineCall()

    def compileSubroutineCall(self):
        nexttoken=self.f.readline()
        nexttonext=self.f.readline()
        ntoken=nexttoken.split(">")[1].split("<")[0].strip(" ")
        ntonext=nexttonext.split(">")[1].split("<")[0].strip(" ")
        name=ntoken
        check = False
        if ntonext=="(":  
            name=self.classname+"."+name
            self.towrite.writePush("pointer",0)
            check=True
            count=self.compileExpressionList()
            symbol=self.f.readline()
        else:
            check=self.routinetable.member(name)
            if check:
                idx=self.routinetable.indexOf(name)
                self.towrite.writePush("local",idx)
                type=self.routinetable.typeOf(name)
                name=type
            else:
                check=self.classtable.member(name)
                if check:
                    idx=self.classtable.indexOf(name)
                    self.towrite.writePush("this",idx)
                    type=self.classtable.typeOf(name)
                    name=type
            subroutinueName=self.f.readline()
            subroutinueName=subroutinueName.split(">")[1].split("<")[0].strip(" ")
            name=name+"."+subroutinueName
            symbol=self.f.readline()
            count=self.compileExpressionList()
            symbol=self.f.readline()
        if check:
            count+=1
        self.towrite.writeCall(name,count)

    def compileExpressionList(self):
        a=self.f.tell()
        nexttoken=self.f.readline()
        nexttonext=self.f.readline()
        ntoken=nexttoken.split(">")[1].split("<")[0].strip(" ")
        ntonext=nexttonext.split(">")[1].split("<")[0].strip(" ")
        count=0
        if nexttoken.find("<integerConstant>")!=-1 or nexttoken.find("<stringConstant>")!=-1 or nexttoken.find("<identifier>")!=-1:
            self.f.seek(a)
            count+=1
            self.compileExpression()
            run=True
            while run:
                b=self.f.tell()
                next=self.f.readline()
                if next.find(",")!=-1:
                    count+=1
                    self.compileExpression()
                else:
                    self.f.seek(b)
                    run=False
        elif ntoken=="(" or ntoken=="-" or ntoken=="~":
            self.f.seek(a)
            count+=1
            self.compileExpression()
            run=True
            while run:
                b=self.f.tell()
                next=self.f.readline()
                if next.find(",")!=-1:
                    count+=1
                    self.compileExpression()
                else:
                    self.f.seek(b)
                    run=False
        elif ntoken in ['true','false','null','this']:
            self.f.seek(a)
            count+=1
            self.compileExpression()
            run=True
            while run:
                b=self.f.tell()
                next=self.f.readline()
                if next.find(",")!=-1:
                    count+=1
                    self.compileExpression()
                else:
                    self.f.seek(b)
                    run=False
        else:
            self.f.seek(a)
        return count
