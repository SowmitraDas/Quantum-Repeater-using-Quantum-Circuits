# -*- coding: utf-8 -*-
"""
Created on Mon Feb 18 22:41:25 2019

@author: User
"""

#channel length
n = 1

import math

from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
from qiskit import execute


from qiskit.tools.qi import qi

ebit = QuantumRegister(2, "ebits")
channel = QuantumRegister(n, "channel")
receiver = QuantumRegister(1, "receiver")

data = ClassicalRegister(2, "data")

sys = QuantumCircuit(ebit)
rcv = QuantumCircuit(receiver, data)
ch = QuantumCircuit(channel)

#creating bell pair
sys.h(ebit[0])
sys.cx(ebit[0], ebit[1])

circ = list(range(n))

for j in range(n):
    circ[j] = sys + ch + rcv
    
    #introducing one ebit into channel
    circ[j].swap(ebit[1], channel[0])
    
    circ[j].barrier(channel)
    
    #transmitting through channel
    for i in range(j):
        circ[j].swap(channel[i], channel[i+1])
        
    circ[j].barrier(channel)
    
    #receiving at receiver
    circ[j].swap(channel[j], receiver[0])
    
    #bell-basis measurement on the ebits
    circ[j].cx(ebit[0], receiver[0])
    circ[j].h(ebit[0])
    circ[j].barrier()
    
    circ[j].measure(ebit[0], data[0])
    circ[j].measure(receiver[0], data[1])


print(circ[n-1].draw())

#from qiskit import IBMQ
#
#IBMQ.load_accounts()
#backend = IBMQ.get_backend('ibmq_16_melbourne')
#
#shots = 5000           # Number of shots to run the program (experiment); maximum is 8192 shots.
#max_credits = 10        # Maximum number of credits to spend on executions.
#
#job = execute(circ[n-1], backend=backend, shots=shots, max_credits=max_credits)
#from qiskit.tools.monitor import job_monitor
#job_monitor(job)
#
#result = job.result()
#from qiskit.tools.visualization import plot_histogram
#counts = result.get_counts(circ[n-1])
#plot_histogram(counts)







