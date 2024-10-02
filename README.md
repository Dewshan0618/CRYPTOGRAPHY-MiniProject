1.	CRYPTOSYSTEM ARCHITECTURE

1.1 Block Cipher Design

The encryption mechanism operates on 8-bit units using a symmetric encryption approach, structured as a Substitution-Permutation Network (SPN). Key components include:
 	S-box: Substitutes 4-bit input values with corresponding 4-bit output values according to a predefined table, adding confusion and obscuring patterns in the data.
 	Permutation Table: Specifies how bits are shuffled within each unit to diffuse the input, ensuring that changes in one bit affect multiple output bits.
 	Feistel Function: Divides the data into halves, applies an XOR operation, and swaps the halves to add security through non-linear transformations.

1.2 ECB Mode

In ECB mode, each 8-bit unit is independently encrypted. However, this creates vulnerabilities, as identical input units produce identical ciphertexts, revealing patterns in the data.

1.3 CBC Mode

CBC mode improves security by XORing each plaintext unit with the previous ciphertext unit before encryption, preventing the production of identical ciphertexts for identical plaintext units. An initialization vector (IV) is used for the first block.



2. MATHEMATICAL FORMULAS
2.1 Substitution Formula

The S-box substitution is represented as:
S(x)=yS(x) = yS(x)=y
where xxx is the 4-bit input and yyy is the 4-bit output. This mapping adds confusion to the encryption process.


2.2 Permutation Formula

The permutation function reshuffles the bits of an 8-bit unit. If the unit is represented as P=[p1,p2,p3,p4,p5,p6,p7,p8]P = [p1, p2, p3, p4, p5, p6, p7, p8]P=[p1,p2,p3,p4,p5,p6,p7,p8], the permutation process rearranges the bits, contributing to diffusion.


2.3 Feistel Function

The Feistel process uses XOR operations on the right half of the unit and the result of applying a round function to the left half and the key:
Li+1=RiL_{i+1} = R_iLi+1=Ri Ri+1=Li⊕F(Ri,K)R_{i+1} = L_i \oplus F(R_i, K)Ri+1=Li⊕F(Ri,K)





3. DESIGN ANALYSIS
3.1 Complexity Analysis

The complexity of the encryption mechanism depends on the substitution, permutation, and Feistel operations. The Feistel structure adds non-linearity and increases security.

