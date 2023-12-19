class VMWriter:
    def __init__(self,outfile):
        outfile=outfile[:-4]+".vm"
        self.vm=open(outfile,"w")
    def writePush(self,segment,index):
        if segment=="field":
            write=f'push this {index}\n'
            self.vm.write(write)
        else:
            write=f'push {segment} {index}\n'
            self.vm.write(write)
    def writePop(self,segment,index):
        if segment=="field":
            write=f'pop this {index}\n'
            self.vm.write(write)
        else:
            write=f'pop {segment} {index}\n'
            self.vm.write(write)
    def writeArithmetic(self,command):
        if command=="+":
            self.vm.write(f'add\n')
        elif command=="-":
            self.vm.write(f'sub\n')
        elif command=="neg":
            self.vm.write(f'neg\n')
        elif command=="=":
            self.vm.write(f'eq\n')
        elif command=="&gt;":
            self.vm.write(f'gt\n')
        elif command=="&lt;":
            self.vm.write(f'lt\n')
        elif command=="&amp;":
            self.vm.write(f'and\n')
        elif command=="|":
            self.vm.write(f'or\n')
        elif command=="~":
            self.vm.write(f'not\n')
    def writeLabel(self,label):
        self.vm.write(f'label {label}\n')
    def writeGoto(self,label):
        write=f'goto {label}\n'
        self.vm.write(write)
    def writeIf(self,label):
        write=f'if-goto {label}\n'
        self.vm.write(write)
    def writeCall(self,name,nArgs):
        write=f'call {name} {nArgs}\n'
        self.vm.write(write)
    def writeFunction(self,name,nVars):
        write=f'function {name} {nVars}\n'
        self.vm.write(write)
    def writeReturn(self):
        self.vm.write(f'return\n')
    def close(self):
        self.vm.close()
