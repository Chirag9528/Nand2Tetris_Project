class SymbolTable:
    def __init__(self):
        self.table = []
        self.localindex=0
        self.staticindex=0
        self.arguementindex=0
        self.fieldindex=0
    def reset(self):
        self.table=[]
        self.localindex=0
        self.staticindex=0
        self.arguementindex=0
        self.fieldindex=0
    def define(self,name,type,kind):
        if kind == "static":
            self.table.append([name,type,kind,self.staticindex])
            self.staticindex+=1
        if kind == "field":
            self.table.append([name,type,kind,self.fieldindex])
            self.fieldindex+=1
        if kind == "argument":
            self.table.append([name,type,kind,self.arguementindex])
            self.arguementindex+=1
        if kind == "local":
            self.table.append([name,type,kind,self.localindex])
            self.localindex+=1
    def varCount(self,kind):
        count=0
        for i in self.table:
            if i[2]==kind:
                count+=1
        return count
    def kindOf(self,name):
        for i in self.table:
            if i[0]==name:
                return i[2]
    def typeOf(self,name):
        for i in self.table:
            if i[0]==name:
                return i[1]
    def indexOf(self,name):
        for i in self.table:
            if i[0]==name:
                return i[3]
    def member(self,name):
        for i in self.table:
            if i[0]==name:
                return True
        return False
            