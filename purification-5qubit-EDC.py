# -*- coding: utf-8 -*-
"""
Created on Sat Mar 23 20:28:55 2019
    Entanglement Purification - Repetition Code
    5-qubit Error Detection Code

@author: User
"""

import math

from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
from qiskit import execute

pair1 = QuantumRegister(2, "pair1")
pair2 = QuantumRegister(2, "pair2")
pair3 = QuantumRegister(2, "pair3")
pair4 = QuantumRegister(2, "pair4")
pair5 = QuantumRegister(2, "pair5")

check1 = ClassicalRegister(2, "check1")
check2 = ClassicalRegister(2, "check2")
check3 = ClassicalRegister(2, "check3")
check4 = ClassicalRegister(2, "check4")

result = ClassicalRegister(2, "result")

sys = QuantumCircuit(pair1, pair2, pair3, pair4, pair5,
                     check1, check2, check3, check4,
                     result)


#introducing infidelity
sys.ry(4*math.pi/13, pair1[0])
sys.ry(4*math.pi/13, pair2[0])
sys.ry(4*math.pi/13, pair3[0])
sys.ry(4*math.pi/13, pair4[0])
sys.ry(4*math.pi/13, pair5[0])


#creating bell-pairs
sys.h(pair1[0])
sys.cx(pair1[0], pair1[1])

sys.h(pair2[0])
sys.cx(pair2[0], pair2[1])

sys.h(pair3[0])
sys.cx(pair3[0], pair3[1])

sys.h(pair4[0])
sys.cx(pair4[0], pair4[1])

sys.h(pair5[0])
sys.cx(pair5[0], pair5[1])

sys.barrier()


#entanglement pumping
sys.cx(pair1[0], pair2[0])
sys.cx(pair1[0], pair3[0])
sys.cx(pair1[0], pair4[0])
sys.cx(pair1[0], pair5[0])
sys.barrier()

sys.cx(pair1[1], pair2[1])
sys.cx(pair1[1], pair3[1])
sys.cx(pair1[1], pair4[1])
sys.cx(pair1[1], pair5[1])
sys.barrier()

#distillation
sys.cx(pair2[0], pair2[1])
sys.h(pair2[0])
sys.barrier(pair2)
sys.measure(pair2, check1)

sys.cx(pair3[0], pair3[1])
sys.h(pair3[0])
sys.barrier(pair3)
sys.measure(pair3, check2)

sys.cx(pair4[0], pair4[1])
sys.h(pair4[0])
sys.barrier(pair4)
sys.measure(pair4, check3)

sys.cx(pair5[0], pair5[1])
sys.h(pair5[0])
sys.barrier(pair5)
sys.measure(pair5, check4)

sys.barrier()


#checking fidelity through bell-measurement
sys.cx(pair1[0], pair1[1])
sys.h(pair1[0])
sys.barrier(pair1)
sys.measure(pair1, result)




print(sys.draw())

#style = {'fold':20}
#sys.draw(output='mpl', style=style)
#
#
#from qiskit import BasicAer
#backend = BasicAer.get_backend('qasm_simulator')
#job = execute(sys, backend=backend, shots=100000)
#
#result = job.result()
#from qiskit.tools.visualization import plot_histogram
#counts = result.get_counts(sys)
#plot_histogram(counts)







