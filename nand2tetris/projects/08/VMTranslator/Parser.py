class Parser:
    def __init__(self,file):
        f=open(file,"r")
        self.f=f
        self.current_command=None
    def hasMoreLines(self):
        a=self.f.tell()
        line=self.f.readline().rstrip('\n')
        line=line.lstrip(" ")
        if line.startswith("//")==True or len(line)==0:
            b=self.f.read().rstrip('\n')
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
            line=self.f.readline().rstrip('\n')
            line=line.lstrip(" ")
            if line.startswith("//") or len(line)==0:
                self.advance()
            else:
                b=line.find("//")
                if b!=-1:
                    lis=line.split("//")[0]
                    line=lis.rstrip(" ")
                else:
                    line=line.rstrip(" ")
                self.current_command=line
    def commandType(self):
        line=self.current_command
        if line in ["add","sub","neg","not","and","or","lt","gt","eq"]:
            return "C_ARITHMETIC"
        if line.find("push")!=-1:
            return "C_PUSH"
        if line.find("pop")!=-1:
            return "C_POP"
        if line.find("label")!=-1:
            return "C_LABEL"
        if line.find("if-goto")!=-1:
            return "C_IF"
        if line.find("goto")!=-1:
            return "C_GOTO"
        if line.find("function")!=-1:
            return "C_FUNCTION"
        if line.find("call")!=-1:
            return "C_CALL"
        if line.find("return")!=-1:
            return "C_RETURN"
    def arg1(self):
        line=self.current_command
        if self.commandType()=="C_ARITHMETIC":
            return line
        else:
            list1=line.split(" ")
            return list1[1]
    def arg2(self):
        line=self.current_command
        if self.commandType()=="C_PUSH" or self.commandType()=="C_POP" or self.commandType()=="C_FUNCTION" or self.commandType()=="C_CALL":
            list1=line.split(" ")
            return list1[2]
