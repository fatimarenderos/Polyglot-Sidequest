from math import sqrt
import classes as c
import math_tools as mt

#Funcion mostrar matriz
def showMatrix(K):
    for i in range(len(K[0])):
        print("[\t")
        for j in range(len(K)):
            print(str(K[i][j]) + "\t")
        print("]\n")
#Funcion mostrar KS
def showKs(Ks):
    for i in range(len(Ks)):
        print("K del elemento " + str(i + 1) + ":\n")
        showMatrix(Ks[i])
        print("*************************************\n")
#Funcion mostrar Vector
def showVector(b):
    print("[\t")
    for i in range(len(b)):
        print(str(b[i]) + "\t")
    print("]\t")
#Funcion mostrar BS
def showbs(bs):
    for i in range(len(bs)):
        print("b del elemento " + str(i+1) + ":\n")
        showVector(bs[i])
        print("*************************************\n")
# Funcion Calcular local 1D
def calculateLocalD(i, m):
    e = m.getElement(i)
    n1 = m.getNode(e.getNode1()-1)
    n2 = m.getNode(e.getNode2()-1)
    n3 = m.getNode(e.getNode3()-1)
    a = n2.getX()-n1.getX()
    b = n2.getY()-n1.getY()
    c = n3.getX()-n1.getX()
    d = n3.getY()-n1.getY()

    D = d*a - c*b

    return D
#Funcion mostar matriz
def calculateMagnitude(v1, v2):
    A = pow(v1,2)
    B = pow(v2,2)
    resultado = A+B
    return sqrt(resultado)

# Funcion Calcular area local
def calculateLocalArea(i, m):
    e = m.getElement(i)
    n1 = m.getNode(e.getNode1()-1)
    n2 = m.getNode(e.getNode2()-1)
    n3 = m.getNode(e.getNode3()-1)
    
    a = calculateMagnitude(n2.getX()-n1.getX(), n2.getY()-n1.getY())
    b = calculateMagnitude(n3.getX()-n2.getX(), n3.getY()-n2.getY())
    c = calculateMagnitude(n3.getX()-n1.getX(), n3.getY()-n1.getY())
    s = (a+b+c)/2

    A = sqrt(s*(s-a)*(s-b)*(s-c))
    return A
# Funcion Calcular area local LA

def calculateLocalA(i, A, m):
    e = m.getElement(i)
    n1 = m.getNode(e.getNode1()-1)
    n2 = m.getNode(e.getNode2()-1)
    n3 = m.getNode(e.getNode3()-1)

    A[0][0] = n3.getY()-n1.getY()
    A[0][1] = n1.getY()-n2.getY()
    A[1][0] = n1.getX()-n3.getX()
    A[1][1] = n2.getX()-n1.getX()

# Funcion Calcular B

def calculateB(B):
    B[0][0] = -1 
    B[0][1] = 1
    B[0][2] = 0
    B[1][0] = -1
    B[1][1] = 0
    B[1][2] = 1

# Funcion Calcular area local LK

def createLocalK(element, m):
    k = m.getParameter(c.parameters.THERMAL_CONDUCTIVITY.value)
    A = []
    B = []
    K = []
    Bt = []
    At = []

    Dv = calculateLocalD(element, m)
    Ae = calculateLocalArea(element, m)

    mt.zeroes1(A,2)
    mt.zeroes2(B,2,3)
    calculateLocalA(element, A, m)
    calculateB(B)
    mt.transpose(A, At)
    mt.transpose(B, Bt)

    mt.productRealMatrix(k*Ae/(Dv*Dv),mt.productMatrixMatrix(Bt,mt.productMatrixMatrix(At,mt.productMatrixMatrix(A,B,2,2,3),2,2,3),3,2,3),K)

    return K
# Funcion Calcular area local LJ

def calculateLocalJ(i, m):
    e = m.getElement(i)
    n1 = m.getNode(e.getNode1()-1)
    n2 = m.getNode(e.getNode2()-1)
    n3 = m.getNode(e.getNode3()-1)

    a = n2.getX()-n1.getX()
    b = n3.getX()-n1.getX()
    c = n2.getY()-n1.getY()
    d = n3.getY()-n1.getY()

    J = a*d -b*c

    return J
# Funcion Calcular area local LB

def createLocalb(element, m):
    b = []

    Q = m.getParameter(c.parameters.HEAT_SOURCE.value)
    J = calculateLocalJ(element, m)

    b_i = ( Q * J ) / 6

    b.append(b_i)
    b.append(b_i)
    b.append(b_i)

    return b
# Funcion Crear sistemas locales

def crearSistemasLocales(m, localKs, localbs):
    for i in range(m.getSize(c.sizes.ELEMENTS.value)):
        localKs.append(createLocalK(i, m))
        localbs.append(createLocalb(i, m))
# Funcion ensamblaje l y k

def assemblyK(e, localK, K):
    index1 = e.getNode1()-1
    index2 = e.getNode2()-1
    index3 = e.getNode3()-1

    K[index1][index1] += localK[0][0]
    K[index1][index2] += localK[0][1]
    K[index1][index3] += localK[0][2]
    K[index2][index1] += localK[1][0]
    K[index2][index2] += localK[1][1]
    K[index2][index3] += localK[1][2]
    K[index3][index1] += localK[2][0]
    K[index3][index2] += localK[2][1]
    K[index3][index3] += localK[2][1]
# Funcion ensamblaje l y b

def assemblyb(e, localb, b):
    index1 = e.getNode1()-1
    index2 = e.getNode2()-1
    index3 = e.getNode3()-1

    b[index1] += localb[0]
    b[index2] += localb[1]
    b[index3] += localb[2]
# Funcion ensamblaje 

def ensamblaje(m, localKs, localbs, K, b):
    for i in range(m.getSize(c.sizes.ELEMENTS.value)):
        e = m.getElement(i)
        assemblyK(e, localKs[i], K)
        assemblyb(e, localbs[i], b)
# Funcion aplicando Neumann

def applyNeumann(m, b):
    for i in range(m.getSize(c.sizes.NEUMANN.value)):
        ce = m.getCondition(i, c.sizes.NEUMANN.value)
        b[ce.getNode1() - 1] += ce.getValue()
# Funcion aplicando Dirichlet

def applyDirichlet(m, K, b):
    for i in range(m.getSize(c.sizes.DIRICHLET.value)):
        ce = m.getCondition(i, c.sizes.DIRICHLET.value)
        index = ce.getNode1() - 1

        del K[index]
        del b[index]

        for row in range(len(K)):
            cell = K[row][index]
            del K[row][index]
            b[row] += -1*ce.getValue()*cell 
# Funcion calcular 

def calculate(K, b, T):
    print("Iniciando calculo de respuesta...\n")
    Kinv = []
    print("Calculo de inversa\n")
    mt.inversaMatrix(K, Kinv)
    print("Calculo de respuesta\n")
    mt.productMatrixVector(Kinv, b, T)