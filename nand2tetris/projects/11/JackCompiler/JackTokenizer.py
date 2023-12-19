class JackTokenizer:
    def __init__(self,file):
        self.file=file
        f=open(file,"r")
        self.f=f
        self.list=self.f.readlines()
        self.current_index=0
        self.length=len(self.list)
        self.current_token=""
        self.filteredlist=""
        self.tokenlist=[]
        self.current_position=0
        self.tokenlistlength=0

    def hasMoreLines(self):
        if self.current_index<=(self.length-1):
            return True
        else:
            return False
    def filter(self):
        if self.hasMoreLines()==True:
            line=self.list[self.current_index].lstrip(" ").rstrip("\n").lstrip("\t")
            if len(line)==0:
                self.current_index+=1
                self.filter()
            else:
                comment=line[0:2]
                if comment=="//":
                    self.current_index+=1
                    self.filter()
                elif comment=="/**" or comment=="/*":
                    idx=self.current_index
                    for i in range(idx,len(self.list)):
                        last=line.find("*/")
                        if last==-1:
                            self.current_index+=1
                            line=self.list[self.current_index].lstrip(" ").rstrip("\n").lstrip("\t")
                            continue
                        else:
                            self.current_index+=1
                            break
                    self.filter()
                
                else:
                    a=line.find("//")
                    if a!=-1:
                        line=line.split("//")[0].rstrip(" ")
                    self.filteredlist+=line
                    self.current_index+=1
    def makingTokens(self):
        token=""
        stringidx=0
        delimiters = [' ','{','}','(',')','[',']','.',',',';','+','-','*','/','&','|','<','>','=','~']
        for j in range(len(self.filteredlist)):
            if self.filteredlist[j]=="\"":
                stringidx+=1
                if len(token)!=0:
                    token+="\""
                    self.tokenlist.append(token)
                    token=""
            if (stringidx%2)==0:
                if self.filteredlist[j]!="\"":
                    if self.filteredlist[j] not in delimiters:
                        token+=self.filteredlist[j]
                    else:
                        # changes
                        if len(token)!=0:
                            token=token.lstrip('\t')
                            if len(token)!=0:
                                self.tokenlist.append(token)
                        if self.filteredlist[j]!=" ":
                            if len(self.filteredlist[j].lstrip('\t'))!=0:
                                self.tokenlist.append(self.filteredlist[j].lstrip('\t'))
                        token=""
                        # /changes
            else:
                token+=self.filteredlist[j]
        self.tokenlistlength=len(self.tokenlist)
    def hasMoreTokens(self):
        if self.current_position<=(self.tokenlistlength-1):
            return True
        else:
            return False
    def advance(self):
        if self.hasMoreTokens()==True:
            self.current_token=self.tokenlist[self.current_position]
            self.current_position+=1
    def tokenType(self):
        keyword_list=['class','constructor','function','method','field','static','var','int','char','boolean','void','true','false','null','this','let','do','if','else','while','return']
        symbol_list=['{','}','(',')','[',']','.',',',';','+','-','*','/','&','|','<','>','=','~']
        token=self.current_token
        if token in keyword_list:
            return "KEYWORD"
        elif token in symbol_list:
            return "SYMBOL"
        elif token.find("\"")!=-1:
            return "STRING_CONST"
        elif token.isdigit()==True:
            return "INT_CONST"
        else:
            return "IDENTIFIER"
        
    def keyWord(self):
        key=self.current_token
        if self.tokenType()=="KEYWORD":
            if key=="class":
                return "CLASS"
            elif key=="method":
                return "METHOD"
            elif key=="function":
                return "FUNCTION"
            elif key=="constructor":
                return "CONSTRUCTOR"
            elif key=="int":
                return "INT"
            elif key=="boolean":
                return "BOOLEAN"
            elif key=="char":
                return "CHAR"
            elif key=="void":
                return "VOID"
            elif key=="var":
                return "VAR"
            elif key=="static":
                return "STATIC"
            elif key=="field":
                return "FIELD"
            elif key=="let":
                return "LET"
            elif key=="do":
                return "DO"
            elif key=="if":
                return "IF"
            elif key=="else":
                return "ELSE"
            elif key=="while":
                return "WHILE"
            elif key=="return":
                return "RETURN"
            elif key=="true":
                return "TRUE"
            elif key=="false":
                return "FALSE"
            elif key=="null":
                return "NULL"
            else:
                return "THIS"
    def symbol(self):
        if self.tokenType()=="SYMBOL":
            if self.current_token=='<':
                return "&lt;"
            elif self.current_token=='>':
                return "&gt;"
            elif self.current_token=="&":
                return "&amp;"
            else:
                return self.current_token
    def identifier(self):
        if self.tokenType()=="IDENTIFIER":
            return self.current_token
    def intVal(self):
        if self.tokenType()=="INT_CONST":
            digit=int(self.current_token)
            return digit
    def stringVal(self):
        if self.tokenType()=="STRING_CONST":
            string=self.current_token[1:]
            string=string[:-1]
            return string