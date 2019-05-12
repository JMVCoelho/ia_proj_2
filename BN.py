# Grupo:72  86448 João Coelho, 87658 Francisco Santos

from toposort import toposort_flatten

# -*- coding: utf-8 -*-


#Uma rede pode ser definida como um grafo da seguinte forma:
#gra = [[],[],[0,1],[2],[2]]
#Com uma lista em que cada elemento representa os pais de cada uma das variáveis.

class Node:
    def __init__(self, prob, parents =[]):
        self.parents=parents
        self.prob=prob #probabilidade de evento ser verdade
        '''positions: 0=false, 1=true
        se tiver varios pais prob_node =prob[FirstPai]...[LastPai]
        em que {FirstPai, ..., LastPai} sao as dependencias, cada elemento tem valor
        1 ou 0 dependendo se se verifica ou nao cada pai'''

    def computeProb(self, evid):  
        context_prob=self.prob

        if not self.parents: # se nao tiver pais:
            return [1-context_prob[0],context_prob[0]]
        
        for parent in self.parents:# se tiver pais avaliar:
            context_prob=context_prob[evid[parent]]
        
        return [1-context_prob,context_prob];
    
class BN:
    def __init__(self, gra, prob):
        self.gra=gra
        self.nodes=prob
        
    def computeJointProb(self,evid):# O(2^n)
        context_prob=1

        for i in range(0,len(self.nodes)):
            node=self.nodes[i]
            context_prob*= node.computeProb(evid)[evid[i]]
        return context_prob
        
        
    def computePostProb(self, Givenevid):#O(2^n)
        ''' calcula P(x|evidConhecidos)[=P(x,evidConhecidos)/P(evid)]
        estrategia: calcular P(x,evidConhecidos)= sum y(P(x,evidConhecidos,Y))  
        Y-evidDesconhecidos, y-valores possiveis para Y'''
        def computePostProbAux(self, evid,node_order):
            product=1
            count=0

            if not node_order:
                return 1

            for node in node_order:
                if evid[node]==[]:
                    prob=self.nodes[node].computeProb(evid)
                    #como esta ordenado garanto que os pais va têm evid definido
                    
                    evid[node]=0

                    result0=computePostProbAux(self, evid,node_order[count+1:])
                    result0*=prob[0]

                    evid[node]=1

                    result1=computePostProbAux(self, evid,node_order[count+1:])
                    result1*=prob[1]

                    evid[node]=[]
                    product*=(result1+result0)
                    return product

                product*=self.nodes[node].computeProb(evid)[evid[node]]
                count+=1

            return product

        def orderNodes(self):#O(v+e)->O(n^2)
            graph={}
            for i in range(0,len(self.gra)):
                graph[i]=set(self.gra[i])
            return toposort_flatten(graph)

        evid=list(Givenevid)
        node_order=orderNodes(self)
        x=0
        for x in range(0,len(evid)):#encontrar node x
            if evid[x]==-1:
                break
        evid[x]=1
        probx=computePostProbAux(self, evid,node_order)#probabilidade de x verdadeiro e evidencias
        evid[x]=0
        probnx=computePostProbAux(self, evid,node_order)#probabilidade de x falso e evidendias
        #alpha= 1/P(evid)
        #alphaP(x,e)+alphaP(¬x,e)=1->alpha=1/(p(x,e)+p(¬x,e))
        alpha=1/(probx+probnx)
        return alpha*probx
