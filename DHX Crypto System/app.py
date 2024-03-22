from flask import Flask, render_template, request
import random
import sympy

app = Flask(__name__)

# Primitive root modulo p (you can choose a specific value)
g = 2

def perform_diffie_hellman(p):
    # Generate private keys for Alice and Bob
    a = random.randint(2, p - 2)
    b = random.randint(2, p - 2)
    
    # Calculate public keys for Alice and Bob
    A = pow(g, a, p)
    B = pow(g, b, p)
    
    # Calculate shared secret key
    shared_key_A = pow(B, a, p)
    shared_key_B = pow(A, b, p)
    
    # Check if the shared keys match
    assert shared_key_A == shared_key_B
    
    return shared_key_A

def xor_encrypt(plaintext_ascii, shared_key_binary):
    ciphertext_binary = ''.join(chr(ord(plaintext_ascii[i]) ^ int(shared_key_binary[i % len(shared_key_binary)])) for i in range(len(plaintext_ascii)))
    return ciphertext_binary

def xor_decrypt(ciphertext_binary, shared_key_binary):
    plaintext_ascii = ''.join(chr(ord(ciphertext_binary[i]) ^ int(shared_key_binary[i % len(shared_key_binary)])) for i in range(len(ciphertext_binary)))
    return plaintext_ascii


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    prime = int(request.form['prime'])
    # Check if the number provided by the user is prime
    if not sympy.isprime(prime):
        return "The number you provided is not prime."
    
    # Perform Diffie-Hellman
    shared_key_decimal = perform_diffie_hellman(prime)
    shared_key_binary = bin(shared_key_decimal)[2:].zfill(8)  # Convert to binary string
    return render_template('encrypt_decrypt.html', shared_key_binary=shared_key_binary, shared_key=shared_key_decimal)


@app.route('/encrypt', methods=['POST'])
def encrypt():
    plaintext_ascii = request.form['plaintext']
    shared_key_binary = request.form['shared_key_binary']
    ciphertext_binary = xor_encrypt(plaintext_ascii, shared_key_binary)
    return render_template('encrypt.html', ciphertext_binary=ciphertext_binary)

@app.route('/decrypt', methods=['POST'])
def decrypt():
    ciphertext_binary = request.form['ciphertext']
    shared_key_binary = request.form['shared_key_binary']
    plaintext_ascii = xor_decrypt(ciphertext_binary, shared_key_binary)
    return render_template('decrypt.html', plaintext_ascii=plaintext_ascii)

if __name__ == '__main__':
    app.run(debug=True)
