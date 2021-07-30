import cirq
import cirq_google

import cirq

# This examples uses named qubits to remain abstract.
# However, we can also use LineQubits or GridQubits to specify a geometry
a = cirq.NamedQubit('a')
b = cirq.NamedQubit('b')
c = cirq.NamedQubit('c')

# Example Operations, that correspond to the moments above
print(cirq.H(b))
print(cirq.CNOT(b, c))
print(cirq.CNOT(a, b))
print(cirq.H(a))
print(cirq.measure(a,b))
