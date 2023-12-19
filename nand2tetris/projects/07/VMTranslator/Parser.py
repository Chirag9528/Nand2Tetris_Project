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
                    c=line.find(" ")
                    line=line[:c]
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
    def arg1(self):
        line=self.current_command
        if self.commandType()=="C_ARITHMETIC":
            return line
        if self.commandType()=="C_PUSH" or self.commandType()=="C_POP":
            list1=line.split(" ")
            return list1[1]
    def arg2(self):
        line=self.current_command
        if self.commandType()=="C_PUSH" or self.commandType()=="C_POP":
            list1=line.split(" ")
            return list1[2]
