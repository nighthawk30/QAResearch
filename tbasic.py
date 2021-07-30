import cirq

q = cirq.GridQubit(0,0)

c = cirq.Circuit(cirq.X(q) ** .5, cirq.measure(q, key='m'))

print(c)

sim = cirq.Simulator()
result = sim.run(c, repetitions=20)

print("Result: " + str(result))
