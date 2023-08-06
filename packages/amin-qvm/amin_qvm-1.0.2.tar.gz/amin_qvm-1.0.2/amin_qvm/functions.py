from qiskit import QuantumCircuit, Aer, execute
import pennylane as qml
from pennylane import numpy as np
from sklearn.preprocessing import StandardScaler


def quantum_model(params, x):
    qml.Rot(*params[0], wires=0)
    qml.Rot(*params[1], wires=1)
    qml.CNOT(wires=[0, 1])
    qml.Rot(*params[2], wires=0)
    qml.Rot(*params[3], wires=1)
    return qml.expval(qml.PauliZ(0))


def cost(params, X, Y):
    predictions = [quantum_model(params, x) for x in X]
    return np.mean((predictions - Y) ** 2)


def train(X_train, Y_train, num_qubits, num_layers, num_steps):
    dev = qml.device("default.qubit", wires=num_qubits)

    @qml.qnode(dev)
    def circuit(params, x=None):
        qml.templates.AngleEmbedding(x, wires=range(num_qubits))
        for l in range(num_layers):
            qml.templates.StronglyEntanglingLayers(params[l], wires=range(num_qubits))
        return [qml.expval(qml.PauliZ(w)) for w in range(num_qubits)]

    params = np.random.uniform(high=2 * np.pi, size=(num_layers, num_qubits, 3))

    opt = qml.GradientDescentOptimizer(stepsize=0.1)

    for i in range(num_steps):
        params = opt.step(lambda v: cost(v, X_train, Y_train), params)

    return params


def test(X_test, Y_test, params, num_qubits):
    predictions = [np.sign(quantum_model(params, x)) for x in X_test]
    accuracy = np.mean(predictions == Y_test)
    return accuracy


def custom_quantum_machine_learning(X_train, Y_train, X_test, Y_test, num_qubits, num_layers, num_steps):
    # Standardize the features
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    # Train the quantum model
    params = train(X_train, Y_train, num_qubits, num_layers, num_steps)

    # Test the quantum model
    accuracy = test(X_test, Y_test, params, num_qubits)
    return accuracy

def grover_search(secret_bitstring):
    # Determine the number of qubits needed to represent the secret bitstring
    num_qubits = len(secret_bitstring)

    # Create a quantum circuit with the required number of qubits
    circuit = QuantumCircuit(num_qubits, num_qubits)

    # Apply Hadamard gates to all qubits
    for i in range(num_qubits):
        circuit.h(i)

    print("Step 1: Apply Hadamard gates to all qubits")

    # Apply Grover's algorithm iterations
    num_iterations = int((3.14/4) * (2 ** (num_qubits / 2)))
    for iteration in range(num_iterations):
        print(f"\nIteration {iteration + 1}:")

        # Oracle to mark the desired state (secret bitstring)
        for i in range(num_qubits):
            if secret_bitstring[i] == '1':
                circuit.z(i)
        circuit.cz(0, num_qubits - 1)

        print("   Applied Oracle")

        # Apply Hadamard gates again
        for i in range(num_qubits):
            circuit.h(i)

        print("   Apply Hadamard gates")

        # Apply phase flip about the mean
        for i in range(num_qubits):
            circuit.x(i)
        circuit.h(num_qubits - 1)
        circuit.mct(list(range(num_qubits - 1)), num_qubits - 1)  # Multi-Control Toffoli gate
        circuit.h(num_qubits - 1)
        for i in range(num_qubits):
            circuit.x(i)

        print("   Apply phase flip about the mean")

    # Measure the qubits
    circuit.measure(range(num_qubits), range(num_qubits))

    print("\nStep 2: Measurement")

    # Simulate the circuit using a classical simulator
    simulator = Aer.get_backend('qasm_simulator')
    job = execute(circuit, simulator, shots=1000)
    result = job.result()

    # Get the counts of the different measurement outcomes
    counts = result.get_counts(circuit)

    return counts
