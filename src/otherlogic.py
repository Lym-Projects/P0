alphabet = "abcdefghijklmnñopqrstuvwxyz"
alphanumeric = alphabet + "0123456789"
def instruction_verify(instruction:str,proceduresnames=[])->bool:
    #hay tres posibilidades
    flag=False
    recursividad=False
    iscomando=False
    isprocedure=False
    #supongamos que es comando
    comandos=["assignto:","goto:","move:","turn:","face:","put:","pick:","movetothe:","moveindir:","jumptothe:","jumpindir:","nop:" ]
    for comando in comandos:
        if instruction.startswith(comando):
            #print('before',instruction)
            instruction=instruction.replace(comando,'')
            #print('after',instruction)
            iscomando=True
            flag=True
            print("es comando")
            return flag
    #falta revisar los parametros de los comandos
    #Revisar si es un procedure call
    for proname in proceduresnames:
        if proname in instruction:
            if instruction.startswith(proname+':'):
                #falta revisar que pone de parametros y si son parametros validos, pendiente
                flag=True
                isprocedure=True
                print("es procedure")
                return flag
    #


def reviewvariable(stringgg):
    flag=True
    if stringgg[0] not in alphabet:
        flag=False
        for caracter in stringgg:
            if caracter not in alphanumeric:
                flag = False
    return flag
def namecheck(methods: dict)->bool:
    flag=True
    for metodo in methods:
        if metodo != "instructionsblock0":
            name=metodo
            if name[0] not in alphabet:
                 flag=False
            for caracter in name:
                if caracter not in alphanumeric:
                     flag = False
    return flag
def bodycheck(methods: dict)->bool:
    flag=True
    parameters={}
    proceduresnames=[]
    for metodo in methods:
        i=0
        if metodo is not "instructionsblock0":
            proceduresnames.append(metodo)
            body=methods[metodo]["body"]
            if body.startswith("[|") and body[len(body)-1]=="]":
                body=body[2:len(body)-1]
                for tokk in body:
                    if tokk=="|":
                        parameters[metodo]=body[:i] 
                        body=body[i+1:len(body)]
                        methods[metodo]=body # modifico el methods
                    i+=1
            else:
                flag=False
    #verificar que los parametros sean correctos
    if flag:
        for metodo in parameters:
            if len(parameters[metodo])>0:
                params=(parameters[metodo]).split(",")
                for par in params:
                    flag=reviewvariable(par)
    #Revisa si tiene mas de una instruccion
    instructions={}
    for llave in methods:
        if llave is not "instructionsblock0":
            instructions=(methods[llave]).split(";")
        for inst in instructions:
            flag=instruction_verify(inst,proceduresnames)
    return flag