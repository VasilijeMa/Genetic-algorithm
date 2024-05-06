from ann_criterion import optimality_criterion
import numpy as np


def genAlg(lowerLimit, upperLimit, popSize, mutatProb, maxParentCount, iterations):

    # 1. Kodiranje
    
    popul = []
    for i in range(popSize):
        w = list(np.random.uniform(lowerLimit, upperLimit, 60))
        popul.append([w, optimality_criterion(w)])

    for iter in range(iterations):

    # 2. Selekcija

        ranked = []

        for i in range(len(popul)-1):
            for j in range(i, len(popul)):
                if popul[i][1]<popul[j][1]:
                    popul[i], popul[j] = popul[j], popul[i]
            ranked.append([i+1, popul[i][0], popul[i][1]])
        ranked.append([popSize, popul[popSize-1][0], popul[popSize-1][1]])

        # 3. Ukrštanje

        pairs = []
        for it in range(int(np.floor(popSize/2))):
            r0 = np.random.random() * ranked[0][0]
            r1 = np.random.random() * ranked[1][0]
            max0 = 0
            max1 = 1
            if r0<r1:
                r0, r1 = r1, r0
                max1 = 0
                max0 = 1
            for i in range(2,popSize):
                rnew = np.random.random() * ranked[i][0]
                if rnew>r0:
                    r1 = r0
                    r0 = rnew
                    max1=max0
                    max0=i
                elif rnew>max1:
                    r1 = rnew
                    max1=i
            pairs.append([ranked[max0][1], ranked[max1][1]])


        children = []
        for p in pairs:
            r = np.random.random()
            p1 = []
            p2 = []
            for j in range(60):
                p1.append(r*p[0][j] + (1-r)*p[1][j])
                p2.append(r*p[1][j] + (1-r)*p[0][j])
            children.append([p1, optimality_criterion(p1)])
            children.append([p2, optimality_criterion(p2)])

        # 4. Mutacija

        newpop = []

        for c in children:
            for i in range(len(c[0])):
                if np.random.random() < mutatProb:
                    r=np.random.random()  
                    c[0][i] = c[0][i] + 2 * (r - 0.5)
            newpop.append([c, "c"])

        for p in popul:
            newpop.append([p, "p"])

        for i in range(len(newpop)-1):
            for j in range(i, len(newpop)):
                if newpop[i][0][1]>newpop[j][0][1]:
                    newpop[i], newpop[j] = newpop[j], newpop[i]

        # 5. Selekcija nove populacije

        popul = []
        counter = 0
        newCounter = 0
        parentCounter = 0
        while newCounter < popSize:
            if newpop[counter][1]=="c":
                popul.append(newpop[counter][0])
                newCounter+=1
            elif parentCounter<maxParentCount:
                popul.append(newpop[counter][0])
                newCounter+=1
                parentCounter+=1
            counter+=1
    return popul[0]

if __name__ == "__main__":
    print("Minimum of function f is approximately equal to: " + str(round(genAlg(-5, 5, 200, 0.3, 10, 20)[1], 6)))





