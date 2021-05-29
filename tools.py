import classes as c

def obtenerDatos(infile, nlines, n, mode, item_list):
    line = infile.readline()
    if nlines == c.lines.DOUBLELINE.value : 
        line = infile.readline()
        line = infile.readline()
    for i in range(n):
        if mode == c.modes.INT_FLOAT.value:
            condition = c.condition()
            line = infile.readline()
            words = []
            for word in line.split():
                words.append(word)
            condition.setValues(c.indicators.NOTHING.value, c.indicators.NOTHING.value, c.indicators.NOTHING.value, int(words[0]), c.indicators.NOTHING.value, c.indicators.NOTHING.value, float(words[1]))
            item_list.append(condition) 

        if mode == c.modes.INT_FLOAT_FLOAT.value:
            node = c.node()
            line = infile.readline()
            words = []
            for word in line.split():
                words.append(word)
            node.setValues(int(words[0]),float(words[1]), float(words[2]), c.indicators.NOTHING.value, c.indicators.NOTHING.value, c.indicators.NOTHING.value, c.indicators.NOTHING.value)
            item_list.append(node)

        if mode == c.modes.INT_INT_INT_INT.value:
            element = c.element()
            line = infile.readline()
            words=[]
            for word in line.split():
                words.append(word)
            element.setValues(int(words[0]), c.indicators.NOTHING.value, c.indicators.NOTHING.value, int(words[1]), int(words[2]), int(words[3]), c.indicators.NOTHING.value)
            item_list.append(element)

def correctConditions(n, list, indices):
    for i in range(n):
        indices.insert(i, list[i].getNode1())
    
    for i in range(n-1):
        pivot = list[i].getNode1()
        for j in range(n):
            if list[j].getNode1() > pivot :
                list[j].setNode1(list[j].getNode1() - 1)

def addExtension(newfilename, filename, extension):
    for i in filename:
        newfilename += i
    for i in extension:
        newfilename += i
    return newfilename

def leerMallayCondiciones(m, filename):
    inputfilename = ''
    inputfilename = addExtension(inputfilename, filename, '.dat')
    infile = open(inputfilename, 'r')

    wordsline = []
    line1 = infile.readline()
    line2 = infile.readline()
    
    for word in line1.split():
        wordsline.append(word)
    
    k = float(wordsline[0])
    Q = float(wordsline[1])

    wordsline = []
    for word in line2.split():
        wordsline.append(word)

    nnodes = int(wordsline[0])
    neltos = int(wordsline[1])
    ndirich = int(wordsline[2])
    nneu = int(wordsline[3])

    m.setParameters(k, Q)
    m.setSizes(nnodes, neltos, ndirich, nneu)
    m.createData()

    infile.readline()
    obtenerDatos(infile, c.lines.SINGLELINE.value, nnodes, c.modes.INT_FLOAT_FLOAT.value, m.getNodes())
    obtenerDatos(infile,c.lines.DOUBLELINE.value, neltos, c.modes.INT_INT_INT_INT.value, m.getElements())
    obtenerDatos(infile, c.lines.DOUBLELINE.value, ndirich, c.modes.INT_FLOAT.value, m.getDirichlet())
    obtenerDatos(infile, c.lines.DOUBLELINE.value, nneu, c.modes.INT_FLOAT.value, m.getNeumann())

    infile.close()
    #Se corrigen los índices en base a las filas que serán eliminadas
    #luego de aplicar las condiciones de Dirichlet
    correctConditions(ndirich, m.getDirichlet(), m.getDirichletIndices())

def findIndex(v , s, arr):
    for i in range(s):
        if arr[i] == v : return True
    return False

def writeResults(m, T, filename):
    outputfilename = ''
    dirich_indices = m.getDirichletIndices()
    dirich = m.getDirichlet()

    outputfilename = addExtension(outputfilename, filename, '.post.res')
    infile = open(outputfilename,"w+")

    infile.write("GiD Post Results File 1.0\n")
    infile.write("Result \"Temperature\" \"Load Case 1\" 1 Scalar OnNodes\nComponentNames \"T\"\nValues\n")

    Dpos = 0
    Tpos = 0
    nd = m.getSize(c.sizes.DIRICHLET.value)
    n = m.getSize(c.sizes.NODES.value)
   

    for i in range(n):
        if findIndex( i+1, nd, dirich_indices):
            infile.write(str(i+1) + " " + str(dirich[Dpos].getValue()) + "\n")
            Dpos += 1
        else:
            infile.write(str(i+1) + " " + str(T[Tpos]) + "\n")
            Tpos += 1
    
    infile.write("End values\n")

    infile.close()