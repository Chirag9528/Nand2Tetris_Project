class CompilationEngine:
    def __init__(self,file1,file2):
        self.f=open(file1,"r")
        self.f.readline()
        self.h=open(file2,"w")
        self.tab=1
        
    def compileClass(self):
        self.h.write("<class>\n")
        tabshift=self.tab * "  "
        keyword=self.f.readline()
        self.h.write(f'{tabshift}{keyword}')
        classname=self.f.readline()
        self.h.write(f'{tabshift}{classname}')
        symbol=self.f.readline()
        self.h.write(f'{tabshift}{symbol}')
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
        tabshift=self.tab * "  "
        self.h.write(f'{tabshift}{symbol}')
        self.h.write("</class>\n")
        
    def compileClassVarDec(self):
        tabshift=self.tab * "  "
        self.h.write(f'{tabshift}<classVarDec>\n')
        self.tab+=1
        tabshift=self.tab * "  "
        keyword=self.f.readline()
        self.h.write(f'{tabshift}{keyword}')
        typetoken=self.f.readline()
        self.h.write(f'{tabshift}{typetoken}')
        identifier=self.f.readline()
        self.h.write(f'{tabshift}{identifier}')
        run=True
        while run:
            a=self.f.tell()
            nexttoken=self.f.readline()
            self.f.seek(a)
            if nexttoken.find(";")!=-1:
                symbol=self.f.readline()
                self.h.write(f'{tabshift}{symbol}')
                run=False
            elif nexttoken.find(",")!=-1:
                symbol=self.f.readline()
                self.h.write(f'{tabshift}{symbol}')
                identifier=self.f.readline()
                self.h.write(f'{tabshift}{identifier}')
            else:
                break
        self.tab-=1
        tabshift=self.tab * "  "
        self.h.write(f'{tabshift}</classVarDec>\n')

    def compileSubroutine(self):
        tabshift=self.tab * "  "
        self.h.write(f'{tabshift}<subroutineDec>\n')
        self.tab+=1
        tabshift=self.tab * "  "
        keyword=self.f.readline()
        self.h.write(f'{tabshift}{keyword}')
        keyword=self.f.readline()
        self.h.write(f'{tabshift}{keyword}')
        subroutineName=self.f.readline()
        self.h.write(f'{tabshift}{subroutineName}')
        symbol=self.f.readline()
        self.h.write(f'{tabshift}{symbol}')
        self.compileParameterList()
        symbol=self.f.readline()
        self.h.write(f'{tabshift}{symbol}')
        self.compileSubroutineBody()
        self.tab-=1
        tabshift=self.tab * "  "
        self.h.write(f'{tabshift}</subroutineDec>\n')

    def compileParameterList(self):
        tabshift=self.tab * "  "
        self.h.write(f'{tabshift}<parameterList>\n')
        self.tab+=1
        tabshift=self.tab * "  "
        a=self.f.tell()
        nexttoken=self.f.readline()
        self.f.seek(a)
        if nexttoken.find("<keyword>")!=-1 or nexttoken.find("<identifier>")!=-1:
            typetoken=self.f.readline()
            varName=self.f.readline()
            self.h.write(f'{tabshift}{typetoken}')
            self.h.write(f'{tabshift}{varName}')
            run=True
            while run:
                a=self.f.tell()
                nexttoken=self.f.readline()
                self.f.seek(a)
                if nexttoken.find(";")!=-1:
                    symbol=self.f.readline()
                    self.h.write(f'{tabshift}{symbol}')
                    run=False
                elif nexttoken.find(",")!=-1:
                    symbol=self.f.readline()
                    self.h.write(f'{tabshift}{symbol}')
                    typetoken=self.f.readline()
                    self.h.write(f'{tabshift}{typetoken}')
                    identifier=self.f.readline()
                    self.h.write(f'{tabshift}{identifier}')
                else:
                    break
        self.tab-=1
        tabshift=self.tab * "  "
        self.h.write(f'{tabshift}</parameterList>\n')

    def compileSubroutineBody(self):
        tabshift=self.tab * "  "
        self.h.write(f'{tabshift}<subroutineBody>\n')
        self.tab+=1
        tabshift=self.tab * "  "
        symbol=self.f.readline()
        self.h.write(f'{tabshift}{symbol}')
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
        self.compileStatements()
        symbol=self.f.readline()
        self.h.write(f'{tabshift}{symbol}')
        self.tab-=1
        tabshift=self.tab * "  "
        self.h.write(f'{tabshift}</subroutineBody>\n')

    def compileVarDec(self):
        tabshift=self.tab * "  "
        self.h.write(f'{tabshift}<varDec>\n')
        self.tab+=1
        tabshift=self.tab * "  "
        keyword=self.f.readline()
        self.h.write(f'{tabshift}{keyword}')
        typetoken=self.f.readline()
        self.h.write(f'{tabshift}{typetoken}')
        varName=self.f.readline()
        self.h.write(f'{tabshift}{varName}')
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
                self.h.write(f'{tabshift}{symbol}')
                self.h.write(f'{tabshift}{varName}')
        symbol=self.f.readline()
        self.h.write(f'{tabshift}{symbol}')
        self.tab-=1
        tabshift=self.tab * "  "
        self.h.write(f'{tabshift}</varDec>\n')

    def compileStatements(self):
        tabshift=self.tab * "  "
        self.h.write(f'{tabshift}<statements>\n')
        self.tab+=1
        tabshift=self.tab * "  "
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
        self.tab-=1
        tabshift=self.tab * "  "
        self.h.write(f'{tabshift}</statements>\n')

    def compileLet(self):
        tabshift=self.tab * "  "
        self.h.write(f'{tabshift}<letStatement>\n')
        self.tab+=1
        tabshift=self.tab * "  "
        keyword=self.f.readline()
        self.h.write(f'{tabshift}{keyword}')
        varName=self.f.readline()
        self.h.write(f'{tabshift}{varName}')
        nexttoken=self.f.readline()
        if nexttoken.find("[")!=-1:
            self.h.write(f'{tabshift}{nexttoken}')
            self.compileExpression()
            symbol=self.f.readline()
            self.h.write(f'{tabshift}{symbol}')
            symbol=self.f.readline()
            self.h.write(f'{tabshift}{symbol}')
        else:
            self.h.write(f'{tabshift}{nexttoken}')
        self.compileExpression()
        symbol=self.f.readline()
        self.h.write(f'{tabshift}{symbol}')
        self.tab-=1
        tabshift=self.tab * "  "
        self.h.write(f'{tabshift}</letStatement>\n')

    def compileIf(self):
        tabshift=self.tab * "  "
        self.h.write(f'{tabshift}<ifStatement>\n')
        keyword=self.f.readline()
        self.h.write(f'{tabshift}{keyword}')
        symbol=self.f.readline()
        self.h.write(f'{tabshift}{symbol}')
        self.compileExpression()
        symbol=self.f.readline()
        self.h.write(f'{tabshift}{symbol}')
        symbol=self.f.readline()
        self.h.write(f'{tabshift}{symbol}')
        self.compileStatements()
        symbol=self.f.readline()
        self.h.write(f'{tabshift}{symbol}')
        a=self.f.tell()
        nexttoken=self.f.readline()
        if nexttoken.find("else")!=-1:
            self.h.write(f'{tabshift}{nexttoken}')
            symbol=self.f.readline()
            self.h.write(f'{tabshift}{symbol}')
            self.compileStatements()
            symbol=self.f.readline()
            self.h.write(f'{tabshift}{symbol}')
        else:
            self.f.seek(a)
        self.tab-=1
        tabshift=self.tab * "  "
        self.h.write(f'{tabshift}</ifStatement>\n')

    def compileWhile(self):
        tabshift=self.tab * "  "
        self.h.write(f'{tabshift}<whileStatement>\n')
        self.tab+=1
        tabshift=self.tab * "  "
        keyword=self.f.readline()
        self.h.write(f'{tabshift}{keyword}')
        symbol=self.f.readline()
        self.h.write(f'{tabshift}{symbol}')
        self.compileExpression()
        symbol=self.f.readline()
        self.h.write(f'{tabshift}{symbol}')
        symbol=self.f.readline()
        self.h.write(f'{tabshift}{symbol}')
        self.compileStatements()
        symbol=self.f.readline()
        self.h.write(f'{tabshift}{symbol}')
        self.tab-=1
        tabshift=self.tab * "  "
        self.h.write(f'{tabshift}</whileStatement>\n')

    def compileDo(self):
        tabshift=self.tab * "  "
        self.h.write(f'{tabshift}<doStatement>\n')
        self.tab+=1
        tabshift=self.tab * "  "
        keyword=self.f.readline()
        self.h.write(f'{tabshift}{keyword}')
        self.compileSubroutineCall()
        symbol=self.f.readline()
        self.h.write(f'{tabshift}{symbol}')
        self.tab-=1
        tabshift=self.tab * "  "
        self.h.write(f'{tabshift}</doStatement>\n')

    def compileReturn(self):
        tabshift=self.tab * "  "
        self.h.write(f'{tabshift}<returnStatement>\n')
        keyword=self.f.readline()
        self.h.write(f'{tabshift}{keyword}')
        a=self.f.tell()
        nexttoken=self.f.readline()
        if nexttoken.find(";")==-1:
            self.f.seek(a)
            self.compileExpression()
            symbol=self.f.readline()
            self.h.write(f'{tabshift}{symbol}')
        else:
            self.h.write(f'{tabshift}{nexttoken}')
        self.tab-=1
        tabshift=self.tab * "  "
        self.h.write(f'{tabshift}</returnStatement>\n')

    def compileExpression(self):
        tabshift=self.tab * "  "
        op_list=['+','-','*',' / ','&amp;','|','&lt;','&gt;','=']
        self.h.write(f'{tabshift}<expression>\n')
        self.tab+=1
        tabshift=self.tab * "  "
        self.compileTerm()
        run=True
        while run:
            a=self.f.tell()
            nexttoken=self.f.readline()
            found=False
            for i in op_list:
                if nexttoken.find(i)!=-1:
                    self.h.write(f'{tabshift}{nexttoken}')
                    found=True
                    break
            if found:
                self.compileTerm()
            else:
                self.f.seek(a)
                run=False
        self.tab-=1
        tabshift=self.tab * "  "
        self.h.write(f'{tabshift}</expression>\n')

    def compileTerm(self):
        tabshift=self.tab * "  "
        self.h.write(f'{tabshift}<term>\n')
        self.tab+=1
        tabshift=self.tab * "  "
        a=self.f.tell()
        nexttoken=self.f.readline()
        nexttonext=self.f.readline()
        ntoken=nexttoken.split(">")[1].split("<")[0].strip(" ")
        ntonext=nexttonext.split(">")[1].split("<")[0].strip(" ")
        if nexttoken.find("<identifier>")!=-1 and ntonext=="[":
            self.h.write(f'{tabshift}{nexttoken}')
            self.h.write(f'{tabshift}{nexttonext}')
            self.compileExpression()
            symbol=self.f.readline()
            self.h.write(f'{tabshift}{symbol}')
        elif ntoken=="(":
            self.f.seek(a)
            symbol=self.f.readline()
            self.h.write(f'{tabshift}{symbol}')
            self.compileExpression()
            symbol=self.f.readline()
            self.h.write(f'{tabshift}{symbol}')
        elif ntoken=="-" or ntoken=="~":
            self.f.seek(a)
            symbol=self.f.readline()
            self.h.write(f'{tabshift}{symbol}')
            self.compileTerm()
        elif ntoken.isdigit()==True:
            self.f.seek(a)
            symbol=self.f.readline()
            self.h.write(f'{tabshift}{symbol}')
        elif ntoken in ['true','false','null','this']:
            self.f.seek(a)
            keyword=self.f.readline()
            self.h.write(f'{tabshift}{keyword}')
        elif nexttoken.find("stringConstant")!=-1:
            self.f.seek(a)
            string=self.f.readline()
            self.h.write(f'{tabshift}{string}')
        elif ntonext!="(" and ntonext!="." and nexttoken.find("<identifier>")!=-1:
            self.f.seek(a)
            varName=self.f.readline()
            self.h.write(f'{tabshift}{varName}')
        else:
            self.f.seek(a)
            self.compileSubroutineCall()
        self.tab-=1
        tabshift=self.tab * "  "
        self.h.write(f'{tabshift}</term>\n')

    def compileSubroutineCall(self):
        nexttoken=self.f.readline()
        nexttonext=self.f.readline()
        ntonext=nexttonext.split(">")[1].split("<")[0].strip(" ")
        self.tab+=1
        tabshift=self.tab * "  "
        if ntonext=="(":
            self.h.write(f'{tabshift}{nexttoken}')
            self.h.write(f'{tabshift}{nexttonext}')
            self.compileExpressionList()
            symbol=self.f.readline()
            self.h.write(f'{tabshift}{symbol}')
        else:
            self.h.write(f'{tabshift}{nexttoken}')
            self.h.write(f'{tabshift}{nexttonext}')
            subroutinueName=self.f.readline()
            self.h.write(f'{tabshift}{subroutinueName}')
            symbol=self.f.readline()
            self.h.write(f'{tabshift}{symbol}')
            self.compileExpressionList()
            symbol=self.f.readline()
            self.h.write(f'{tabshift}{symbol}')

    def compileExpressionList(self):
        tabshift=self.tab * "  "
        self.h.write(f'{tabshift}<expressionList>\n')
        a=self.f.tell()
        nexttoken=self.f.readline()
        nexttonext=self.f.readline()
        ntoken=nexttoken.split(">")[1].split("<")[0].strip(" ")
        ntonext=nexttonext.split(">")[1].split("<")[0].strip(" ")
        self.tab+=1
        tabshift=self.tab * "  "
        if nexttoken.find("<integerConstant>")!=-1 or nexttoken.find("<stringConstant>")!=-1 or nexttoken.find("<identifier>")!=-1:
            self.f.seek(a)
            self.compileExpression()
            run=True
            while run:
                b=self.f.tell()
                next=self.f.readline()
                if next.find(",")!=-1:
                    self.h.write(f'{tabshift}{next}')
                    self.compileExpression()
                else:
                    self.f.seek(b)
                    run=False
        elif ntoken=="(" or ntoken=="-" or ntoken=="~":
            self.f.seek(a)
            self.compileExpression()
            run=True
            while run:
                b=self.f.tell()
                next=self.f.readline()
                if next.find(",")!=-1:
                    self.h.write(f'{tabshift}{next}')
                    self.compileExpression()
                else:
                    self.f.seek(b)
                    run=False
        elif ntoken in ['true','false','null','this']:
            self.f.seek(a)
            self.compileExpression()
            run=True
            while run:
                b=self.f.tell()
                next=self.f.readline()
                if next.find(",")!=-1:
                    self.h.write(f'{tabshift}{next}')
                    self.compileExpression()
                else:
                    self.f.seek(b)
                    run=False
        else:
            self.f.seek(a)
        self.tab-=1
        tabshift=self.tab * "  "
        self.h.write(f'{tabshift}</expressionList>\n')