# Grupo:72  86448 João Coelho, 87658 Francisco Santos

# -*- coding: utf-8 -*-
"""
BASE CODE:
Created on Mon Oct 16 20:31:54 2017

@author: mlopes
"""
import numpy as np
import random

from tempfile import TemporaryFile
outfile = TemporaryFile()
	
class finiteMDP:

    def __init__(self, nS, nA, gamma, P=[], R=[], absorv=[]):
        self.nS = nS
        self.nA = nA
        self.gamma = gamma
        self.Q = np.zeros((self.nS,self.nA))
        self.P = P
        self.R = R
        self.absorv = absorv
        # completar se necessario
        
            
    def runPolicy(self, n, x0,  poltype = 'greedy', polpar=[]):
        #nao alterar
        traj = np.zeros((n,4))
        x = x0
        J = 0
        for ii in range(0,n):
            a = self.policy(x,poltype,polpar)
            r = self.R[x,a]
            y = np.nonzero(np.random.multinomial( 1, self.P[x,a,:]))[0][0]
            traj[ii,:] = np.array([x, a, y, r])
            J = J + r * self.gamma**ii
            if self.absorv[x]:
                y = x0
            x = y
        
        return J,traj


    def VI(self):
        #nao alterar
        nQ = np.zeros((self.nS,self.nA))
        while True:
            self.V = np.max(self.Q,axis=1) 
            for a in range(0,self.nA):
                nQ[:,a] = self.R[:,a] + self.gamma * np.dot(self.P[:,a,:],self.V)
            err = np.linalg.norm(self.Q-nQ)
            self.Q = np.copy(nQ)
            if err<1e-7:
                break
            
        #update policy
        self.V = np.max(self.Q,axis=1) 
        #correct for 2 equal actions
        self.Pol = np.argmax(self.Q, axis=1)
                    
        return self.Q,  self.Q2pol(self.Q)

            
    def traces2Q(self, trace):
        Q_new = np.zeros((self.nS,self.nA))
        while True:
            for jump in trace:
                Q_new[int(jump[0]),int(jump[1])] = Q_new[int(jump[0]),int(jump[1])] + 0.05 * (jump[3] + self.gamma * max(Q_new[int(jump[2])]) - Q_new[int(jump[0]),int(jump[1])])
            deviation = np.sqrt(sum(sum((self.Q-Q_new)**2))) #FROBENIUS NORM
            self.Q = np.copy(Q_new)
            if deviation<1e-2:
                #Frobenius norm is used for matrix convergency. If the frobenius norm of self.Q - nQ is aprox 0, there's no evolution, therefore we can stop.
                break
        return self.Q
    
    def policy(self, x, poltype = 'exploration', par = []):
        if poltype == 'exploitation':
            a = 0
            m_value = max(self.Q[x])
            for i in range(0, self.nA):
                if m_value == self.Q[x,i]:
                    a = i
                    #if there are more than one max values, we chose the FIRST one.
                    break
                
        elif poltype == 'exploration':
            a = random.randint(0,self.nA-1)
        return a
    
    def Q2pol(self, Q, eta=5):
        return np.exp(eta*Q)/np.dot(np.exp(eta*Q),np.array([[1,1],[1,1]]))


            