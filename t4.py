import cirq
import cirq_google

q=cirq.GridQubit(1, 1)
optimizer=cirq.MergeSingleQubitGates()
c=cirq.Circuit(cirq.X(q) ** 0.25, cirq.Y(q) ** 0.25, cirq.Z(q) ** 0.25)
print(c)
optimizer.optimize_circuit(c)
print(c)
