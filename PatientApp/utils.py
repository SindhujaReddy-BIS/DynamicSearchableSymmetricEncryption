from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import base64
import hmac
import hashlib
from qiskit import QuantumCircuit, Aer, execute
from qiskit.visualization import plot_histogram
import random

# --- Helper Function for secure bit-to-byte conversion ---
def bits_to_bytes(bit_list):
    """Converts a list of 0s and 1s into a high-entropy bytes object."""
    byte_array = bytearray()
    
    # Pad the list with zeros to make its length a multiple of 8
    padding_needed = (8 - (len(bit_list) % 8)) % 8
    padded_bits = bit_list + [0] * padding_needed

    # Pack 8 bits into one byte
    for i in range(0, len(padded_bits), 8):
        byte = 0
        for j in range(8):
            # Shift the bit left to its correct position
            byte |= padded_bits[i + j] << (7 - j)
        byte_array.append(byte)
    
    return bytes(byte_array)

def bb84_protocol_qiskit():
    # Number of qubits to simulate - increased for a reasonable key length
    num_bits = 32 # Must be a multiple of 8 for clean byte conversion

    # Alice generates a random bit string (key)
    alice_bits = [random.randint(0, 1) for _ in range(num_bits)]
    print(f"Alice's bits (sent): {alice_bits}")

    # Alice prepares quantum states based on the bits
    alice_bases = [random.randint(0, 1) for _ in range(num_bits)]  # Randomly chosen bases (0: Z/standard, 1: X/diagonal)
    print(f"Alice's bases: {alice_bases}")

    # Create a quantum circuit to simulate the BB84 protocol
    qc = QuantumCircuit(num_bits, num_bits)

    # State Preparation (Alice)
    for i in range(num_bits):
        if alice_bits[i] == 1:
            qc.x(i)  # Apply X gate for bit state 1
        if alice_bases[i] == 1:
            qc.h(i)  # Apply Hadamard gate for diagonal basis

    # Simulate Bob's measurement with random bases
    bob_bases = [random.randint(0, 1) for _ in range(num_bits)]
    print(f"Bob's bases: {bob_bases}")

    # Apply the correct basis for Bob (H for diagonal, identity for standard)
    for i in range(num_bits):
        if bob_bases[i] == 1:
            qc.h(i)  # Apply Hadamard for Bob's measurement in diagonal basis

    # Measure the qubits
    qc.measure(range(num_bits), range(num_bits))

    # Simulate the circuit using Aer backend
    backend = Aer.get_backend('qasm_simulator')
    result = execute(qc, backend, shots=1).result()

    # Get the measurement results
    counts = result.get_counts()
    # The key is a string of measured bits. Qiskit gives the bits in reverse order (qn-1...q0).
    measured_bits_reversed = list(counts.keys())[0]
    
    # FIX: Reverse the bit string to align with the order Alice sent (q0...qn-1)
    measured_bits = measured_bits_reversed[::-1]
    print(f"Measured quantum bits: {measured_bits}")

    # Compare the bases to generate the final shared key (Sifting)
    quantum_key_bits = []
    for i in range(num_bits):
        if alice_bases[i] == bob_bases[i]:
            # Bases match, the measured bit is part of the raw key
            quantum_key_bits.append(int(measured_bits[i]))
        else:
            # Discard the bit
            pass

    print(f"Sifted Quantum Key (bits): {quantum_key_bits}")
    
    return quantum_key_bits

def generate_key_bytes(quantum_key_bits):
    # AES-128 requires a 16-byte key (128 bits)
    
    # 1. Ensure key length is exactly 128 bits (16 bytes)
    min_key_length = 128  # AES-128 uses 128-bit (16 bytes) keys
    if len(quantum_key_bits) < min_key_length:
        print(f"WARNING: Insufficient sifted key bits ({len(quantum_key_bits)}). Padding to {min_key_length} bits with 0s.")
        # Padding to ensure we have enough bits, but generally not ideal in real QKD
        quantum_key_bits += [0] * (min_key_length - len(quantum_key_bits))
    elif len(quantum_key_bits) > min_key_length:
        # Truncate the key to the required length (128 bits = 16 bytes)
        quantum_key_bits = quantum_key_bits[:min_key_length]

    # 2. Convert the list of bits into a secure bytes object
    quantum_key_bytes = bits_to_bytes(quantum_key_bits)
    
    # Ensure the key is 16 bytes (128 bits)
    if len(quantum_key_bytes) != 16:
        print(f"ERROR: The generated key length is incorrect: {len(quantum_key_bytes)} bytes")
        return None

    # Print the first 8 bytes of the quantum key for debugging
    print('Quantum byte key (first 8 bytes):', quantum_key_bytes[:8].hex(), '...')
    
    return quantum_key_bytes

# --- AES Encryption and Decryption Functions (Switched to AES-CBC) ---
def aes_encrypt(key, data):
    iv = get_random_bytes(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    
    # Check if data is already bytes, if not, encode it (assuming UTF-8)
    data_to_encrypt = data if isinstance(data, bytes) else data.encode()
    
    ciphertext = cipher.encrypt(pad(data_to_encrypt, AES.block_size))
    return iv + ciphertext

def aes_decrypt(key, ciphertext_with_iv):
    # Separate the IV (first AES.block_size bytes) from the actual ciphertext
    iv = ciphertext_with_iv[:AES.block_size]
    ciphertext = ciphertext_with_iv[AES.block_size:]
    
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted = unpad(cipher.decrypt(ciphertext), AES.block_size)
    return decrypted.decode()

# HMAC-SHA256 for Authentication (Remains the same)
def hmac_sha256(key, data) -> str:
    # Ensure data is in bytes format for hmac.new()
    if isinstance(data, str):
        data_bytes = data.encode()
    elif isinstance(data, bytes):
        data_bytes = data
    else:
        # Handle other types if necessary
        data_bytes = str(data).encode()
        
    digest = hmac.new(key, data_bytes, hashlib.sha256).digest()
    return base64.b64encode(digest).decode()