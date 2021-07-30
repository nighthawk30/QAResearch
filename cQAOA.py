#!/usr/bin/env python
# coding: utf-8

# In[1]:


#Quantum Approximate Optimization Algorithm - This is it
import cirq
import numpy as np
import random


# In[2]:


#Functions
def chooseHp():
    H = np.array([[0]*4]*12) #qubit indices ijk (1-6) and coefficient (+-1)
    check = np.array([0]*6) #keeps track of all indices that have been chosen

    #12 triplets
    for x in range(12):
        free = [0,1,2,3,4,5] #remaining qubit options(each can be chosen once)
        #3 qubits
        for y in range(3):
            qindex = free[random.randint(0,len(free)-1)]
            free.remove(qindex)
            H[x,y] = qindex
            check[qindex] = 1
        #Coefficient
        H[x, 3] = (-1) ** random.randint(0, 1)

    #If an index hasn't been chosen, redo
    for x in range(6):
        if check[x] == 0:
            return chooseHp()
        else:
            return H

def findGround(H_p):
    ground_energy = 13
    
    #build the state vector
    stateList = []
    for a in range(2):
        for b in range(2):
            for c in range(2):
                for d in range(2):
                    for e in range(2):
                        for f in range(2):
                            estate = [a,b,c,d,e,f,0]
                            stateList.append(estate)

    #Calculate the energy of each state
    for state in stateList:
        #For each triplet of h_p if the qubits are 1 in the state, multiply by 1 else -1
        for triplet in H_p:
            weight = 1
            for i in range(3):
                if state[triplet[i]]:
                    weight *= 1
                else:
                    weight *= -1
            weight *= triplet[3]#then scale by the weight
            state[6] += weight#energy is the sum of the 12 weights
        #update the ground state energy
        if state[6] < ground_energy:
            ground_energy = state[6]
    
    #Find ground states
    ground_state = []
    for state in stateList:
        if state[6] == ground_energy:
            ground_state.append(state)
    
    return(ground_state)

#Cant mix lists and generators in python
def rotation3X(q0, q1, q2, anc, angle):
    oplist = []
    oplist.append(cirq.H(q0))
    oplist.append(cirq.H(q1)) 
    oplist.append(cirq.H(q2))
    oplist.append(cirq.CNOT(q0, anc))
    oplist.append(cirq.CNOT(q1, anc))
    oplist.append(cirq.CNOT(q2, anc))
    oplist.append(cirq.rz(2 * angle)(anc))
    oplist.append(cirq.CNOT(q2, anc))
    oplist.append(cirq.CNOT(q1, anc))
    oplist.append(cirq.CNOT(q0, anc))
    oplist.append(cirq.H(q0))
    oplist.append(cirq.H(q1)) 
    oplist.append(cirq.H(q2))
    return oplist

def make_QAOA(qbit, ancilla, H_p ,alpha, beta):
    #|ψ) → e^iβH_D*e^iαH_P|ψ) : 
    oplist = []
    #Add Hadamards
    for q in qbit:
        oplist.append(cirq.H(q))
    #Add H_p: 3 qubit rotations
    for x in range(len(H_p)):
        oplist.append(rotation3X(qbit[H_p[x][0]], qbit[H_p[x][1]], qbit[H_p[x][2]], ancilla, alpha))
    #Add X rotations
    for q in qbit:
        oplist.append(cirq.rx(-2 * beta)(q))
        
    return oplist

#Finds the expectation value of a measurement in the z basis
def expectation3Z(oplist, mqbits):
    sim = cirq.Simulator()
    circuit = cirq.Circuit(oplist)
    circuit.append(cirq.measure(*mqbits, key='z'))
    
    counts = 1000
    samples = sim.run(circuit, repetitions=counts)
    data = samples.histogram(key='z')
    
    binaryformat = "{0:0" + str(6) + "b}"
    z3obj = 0
    
    for key, value in data.items():
        bitstring = binaryformat.format(int(key))
        z3obj += int(value) * (-1)**(int(bitstring[0])+int(bitstring[1])+int(bitstring[2]))
        
    z3obj /= counts
    return z3obj

def expectHp(oplist, qubits):
    #For expectation value of the H_p operator is the sum of the weighted products of the
    #expectation values of each qubit in each triplet ie(sum(<Z_i*Z_j*Z_k>*W_ijk))
    
    energy = 0
    for triplet in H_p:
        qmeasure = [qubits[triplet[0]],qubits[triplet[1]],qubits[triplet[2]]]
        product = expectation3Z(oplist, qmeasure) * triplet[3]
        energy += product
    return energy


# In[3]:


#Initialize
H_p = chooseHp()
ground = findGround(H_p)
print("Ground Energy: ", ground[0][6])


# In[4]:


#Test Cell
'''
alpha = -np.pi/2
beta = 0
qbits = cirq.LineQubit.range(6)
anc = cirq.NamedQubit("A")
ops = make_QAOA(qbits, anc, H_p, alpha, beta)
energy = expectHp(ops, qbits)
print(energy)
print(cirq.Circuit(ops))
'''


# In[5]:


qbits = cirq.LineQubit.range(6)
anc = cirq.NamedQubit("A")
angles = np.pi/2 * np.arange(-1,1,.2)
for a in angles:
    for b in angles:
        ops = make_QAOA(qbits, anc, H_p, a, b)
        energy = expectHp(ops, qbits)
        print(energy, a*180/np.pi, b*180/np.pi)


# In[ ]:




