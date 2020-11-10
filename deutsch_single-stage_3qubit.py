# -*- coding: utf-8 -*-
"""
Created on Mon Apr 15 21:30:11 2019
    Deutsch - Single Stage - 3 qubit

@author: User
"""

import math

from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
from qiskit import execute

pair1 = QuantumRegister(2, "pair1")
pair2 = QuantumRegister(2, "pair2")
pair3 = QuantumRegister(2, "pair3")

check1 = ClassicalRegister(2, "check1")
check2 = ClassicalRegister(2, "check2")

result = ClassicalRegister(2, "result")


sys = QuantumCircuit(pair1, pair2, pair3,
                     check1, check2,
                     result)


#introducing infidelity
sys.ry(4*math.pi/11, pair1[0])
sys.ry(4*math.pi/11, pair2[0])
sys.ry(4*math.pi/11, pair3[0])


#creating bell-pairs
sys.h(pair1[0])
sys.cx(pair1[0], pair1[1])

sys.h(pair2[0])
sys.cx(pair2[0], pair2[1])

sys.h(pair3[0])
sys.cx(pair3[0], pair3[1])

sys.barrier()

#stage-1

#rotation-1
#rotation-Alice
sys.rx(math.pi/2, pair1[0])
sys.rx(math.pi/2, pair2[0])
sys.rx(math.pi/2, pair3[0])

sys.barrier()

#rotation-Bob
sys.rx(-math.pi/2, pair1[1])
sys.rx(-math.pi/2, pair2[1])
sys.rx(-math.pi/2, pair3[1])

sys.barrier()



#entanglement pumping(1)
sys.cx(pair1[0], pair2[0])
sys.cx(pair1[0], pair3[0])
sys.barrier()


sys.cx(pair1[1], pair2[1])
sys.cx(pair1[1], pair3[1])
sys.barrier()


#distillation(1)
sys.measure(pair2, check1)
sys.measure(pair3, check2)


sys.barrier()


#checking fidelity through bell-measurement
sys.cx(pair1[0], pair1[1])
sys.h(pair1[0])
sys.barrier(pair1)
sys.measure(pair1, result)


print(sys.draw())

style = {'fold':24}
sys.draw(output='mpl', style=style, plot_barriers=True)

from qiskit import BasicAer
backend = BasicAer.get_backend('qasm_simulator')
job = execute(sys, backend=backend, shots=10000)

result = job.result()
from qiskit.tools.visualization import plot_histogram
counts = result.get_counts(sys)
plot_histogram(counts)


