# Giallar
Artifact for the Paper Giallar: Push-button Verification for the Qiskit Quantum Compiler

## Building the software

### Requirements

Giallar requires python>=3.8 Qiskit=0.31.0 (https://qiskit.org/documentation/), Z3>=4.8.12 networkx>=2.7.1 and astroid>=2.4.1, which can be installed by 

    pip install -Iv z3-solver==4.8.12 qiskit==0.31.0 astroid scipy numpy networkx

## Installation

To install Giallar, run

    pip install .


## Code structure

```
├── giallar                   # main Giallar code
│   ├── coq_proof             # coq proof of soundness and rewriting rules
│   ├── core                  # Giallar library code
│   │   ├── impl              # Giallar library implementation
│   │   └── spec              # Giallar library specification
│   ├── preprocessor          # Giallar preprocessor
│   ├── qiskit_wrapper        # Giallar-to-qiskit translator 
│   └── utility_library       # Giallar utility library
├── verified_passes           # verified passes
├── tests                     # QASM benchmarks  
└── setup.py                  # setup Giallar 
```

## Running the verification (Table 2)

Enter the directory

    cd giallar

To verify all passes, run

    python verify_pass.py all

Notes

- The running time depends on hardware and the randomness of Z3 solver, but will typically be in 10 minutes.
- The number of subgoals/running time may be different from the data in the paper, but the does not affect the conclusion.
- To verify a specific pass, run `python verify_pass.py <passname>`

## Running the benchmark (Figure 11)

Enter the directory

    cd tests

To run benchmarks, run

    python batch_run.py --category=[small|medium|large]

the benchmarks is splitted into 3 categories small, medium and large.

After running, find statistics at [small|medium|large]_summary.csv. The running time depends on hardware, but will typically be in 10 minutes.