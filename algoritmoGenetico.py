import random as rd

# Criação da classe Cromossomo, com os atributos A, B, C e o SSE (Aptidão)
class Cromossomo():
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c
        self.sse = None

    def getA(self):
        return self.a

    def getB(self):
        return self.b
    
    def getC(self):
        return self.c

    def setSse(self, sse):
        self.sse = sse

    def __str__(self):
        return "A: " + str(self.a) + ", B: " + str(self.b) + ", C: " + str(self.c) + ", SSE: " + str(self.sse)

def getSse(cromossomo): # Função para permitir a ordenação da população pelo SSE calculado
    return cromossomo.sse

def lerArquivo(name):
    array = []
    arquivo = open(name, 'r')
    for line in arquivo:
        array.append(float(line.strip('\n')))
    return array

def calcularAptidao(populacao, vX, vY):
    for i in range(len(populacao)):
        ind = populacao[i]
        vYO = [] # Valores de Y obtidos

        for j in range(len(vX)):
            y = ind.a + (ind.b * vX[j]) + (ind.c * (vX[j] ** 2))
            vYO.append(y)

        somatorio = 0
        for j in range(len(vY)):
            somatorio += (vYO[j] - vY[j]) ** 2

        populacao[i].sse = round((somatorio / len(vY)), 4)
    
    return populacao


# Variáveis do Algoritmo Genético
limInf = -5 # Valor mínimo para A, B e C
limSup = 5  # Valor máximo para A, B e C
tamP = 100  # Tamanho da População (PAR)
numG = 20   # Número de Gerações
proM = 0.1  # Probabilidade de Mutação
numI = 10   # Número máximo de iterações sem melhora
qtdeT = int(0.25 * tamP) # Porcentagem dos indivíduos da população selecionados para o torneio
if(qtdeT < 2):
    qtdeT = 2

# Leitura dos Arquivos
vX = lerArquivo('x-data.txt') # Valores de X dados
vY = lerArquivo('y-data.txt') # Valores de Y esperados

# GERAÇÃO DA POPULAÇÃO INICIAL DE FORMA ALEATÓRIA:  x = a + c * (b-a), sendo 'a' e 'b' os 
# limites inferiores e superiores dos valores e 'c' um número aleatório entre 0 e 1 
populacao = []
for i in range(tamP):
        numA = rd.random()
        a = round(limInf + numA * (limSup - limInf), 4)
        numA = rd.random()
        b = round(limInf + numA * (limSup - limInf), 4)
        numA = rd.random()
        c = round(limInf + numA * (limSup - limInf), 4)

        populacao.append(Cromossomo(a, b, c))


# Calcular Aptidão
populacao = calcularAptidao(populacao, vX, vY)
populacaoTorneio = populacao

# Ordenar população de acordo com a aptidão de cada indivíduo
populacao.sort(key=getSse)

print("População Inicial:")
for i in range(tamP):
    print(populacao[i])

melhor = populacao[0]
geracao = 0
solucao = False
semMelhora = 0

while(solucao != True and geracao < numG and semMelhora < numI):
    
    novaGeracao = []
    novosInds = 0

    # Elitismo - Passar os 2 melhores indivíduos da população para a próxima geração
    novaGeracao.append(populacao[0])
    novaGeracao.append(populacao[1])
    novosInds += 2


    while(novosInds < tamP):
        
        # # Roleta
        # sseTotal = 0
        # prob = [] # Probabilidade de cara individuo
        # probTotal = [] # Probabilidade Acumulada
        # for i in range(tamP):
        #     sseTotal += populacao[i].sse

        # for i in range(tamP):
        #    prob.append(populacao[i].sse / sseTotal)

        # prob.reverse()

        # for i in range(tamP):
        #     if(i == 0):
        #         probTotal.append(prob[i])
        #     else:
        #         probTotal.append(prob[i] + probTotal[i-1])


        # numA = rd.random()
        # i = 0
        # while(numA>probTotal[i]):
        #     i += 1
        # pai1 = i

        # numA = rd.random()
        # i = 0
        # while(numA>probTotal[i]):
        #     i += 1
        # pai2 = i

        # while(pai1 == pai2):
        #     numA = rd.random()
        #     i = 0
        #     while(numA>probTotal[i]):
        #         i += 1
        #     pai2 = i

        # pai1 = populacao[pai1]
        # pai2 = populacao[pai2]

        # Torneio - Não acha a solução ótima facilmente
        # Seleção aleatória dos indivíduos para o torneio
        individuosSelecionados = []
        indicesSelecionados = rd.sample(range(0, tamP), qtdeT) 
        for i in range(qtdeT):
            individuosSelecionados.append(populacaoTorneio[indicesSelecionados[i]])

        # Escolha dos 2 mais aptos
        individuosSelecionados.sort(key=getSse)
        pai1 = individuosSelecionados[0]
        pai2 = individuosSelecionados[1]

        # Reprodução
        # Filho 1
        numA = rd.random()
        a = round((numA*pai1.a + (1-numA)*pai2.a),4)
        numA = rd.random()
        b = round((numA*pai1.b + (1-numA)*pai2.b),4)
        numA = rd.random()
        c = round((numA*pai1.c + (1-numA)*pai2.c),4)

        filho1 = Cromossomo(a, b, c)

        # Filho 2
        numA = rd.random()
        a = round(((1-numA)*pai1.a + numA*pai2.a),4)
        numA = rd.random()
        b = round(((1-numA)*pai1.b + numA*pai2.b),4)
        numA = rd.random()
        c = round(((1-numA)*pai1.c + numA*pai2.c),4)

        filho2 = Cromossomo(a, b, c)

        # Mutação
        # Filho 1
        numA = rd.random()
        if(numA <= proM):
            numA = rd.random()
            c = rd.random()
            if(numA <= 0.33):
                filho1.a = round(limInf + c * (limSup - limInf), 4)
            elif(numA > 0.33 and numA<= 0.66):
                filho1.b = round(limInf + c * (limSup - limInf), 4)
            else:
                filho1.c = round(limInf + c * (limSup - limInf), 4)   

        # Filho 2
        numA = rd.random()
        if(numA <= proM):
            numA = rd.random()
            c = rd.random()
            if(numA <= 0.33):
                filho2.a = round(limInf + c * (limSup - limInf), 4)
            elif(numA > 0.33 and numA<= 0.66):
                filho2.b = round(limInf + c * (limSup - limInf), 4)
            else:
                filho2.c = round(limInf + c * (limSup - limInf), 4)        

        novaGeracao.append(filho1)
        novaGeracao.append(filho2)
        novosInds += 2

    calcularAptidao(novaGeracao, vX, vY)
    novaGeracao.sort(key=getSse)

    if(novaGeracao[0].sse < melhor.sse):
        melhor = novaGeracao[0]
        semMelhora = 0
    else:
        semMelhora += 1

    if(novaGeracao[0].sse == 0):
        solucao = True
    print("Melhor da", geracao + 1, "ª Geração:")
    print(novaGeracao[0])

    sseT = []
    for i in range(tamP):
        sseT.append(populacao[i])
    
    populacao = novaGeracao
    geracao += 1

print("Melhor solução encontrada:", melhor)
