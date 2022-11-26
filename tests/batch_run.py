import os
import time
import sys
import getopt


if __name__ == '__main__':

    valid_options = ["category=", "circuit="]
    args = sys.argv
    opts, args = getopt.getopt(args[1:], '', valid_options)
    category, circuit = None, None
    for opt, arg in opts:
        if opt == '--category':
            if arg not in ['small', 'medium', 'large']:
                print('Invalid category. Choose from "small", "medium", and "large".')
                exit(-1)
            category = arg
        if opt == '--circuit':
            circuit = arg
    if category == None:
        print('Please specify a category (small, medium, or large)')
        exit(-1)
    qasm_files = []
    benchmark_root = 'qasm/QASMBench'
    if circuit is None:
        for root, directories, filenames in os.walk('{}/{}'.format(benchmark_root, category)):
            for filename in filenames:
                if filename.endswith('.qasm'):
                    # circuit file
                    qasm_files.append(os.path.join(root, filename))
        print('Running all {} circuits.'.format(category))
    else:
        target_qasm_file = '{}/{}/{}/{}.qasm'.format(benchmark_root, category, circuit, circuit)
        if not os.path.exists(target_qasm_file):
            print('{} does not exists.'.format(target_qasm_file))
            exit(-1)
        qasm_files.append(target_qasm_file)

    result_table = []
    for qasm_file in qasm_files:

        qiskit_start_time = time.time()
        ret = os.system("python run_qiskit.py {} 2> /dev/null".format(qasm_file))
        qiskit_runtime = time.time() - qiskit_start_time
        if ret != 0:
            continue
        print("qiskit {} = {:.1f}s, {}".format(qasm_file, qiskit_runtime, ret))

        giallar_start_time = time.time()
        ret = os.system("python compiler.py {} > /dev/null 2> /dev/null".format(qasm_file))
        giallar_runtime = time.time() - giallar_start_time
        print("giallar {} = {:.1f}s, {}".format(qasm_file, giallar_runtime, ret))

        result_table.append((qasm_file.split('/')[-1].split('\\')[-1], qiskit_runtime, giallar_runtime))

    if circuit is None:
        summary_file_name = '{}_summary.csv'.format(category)
        with open(summary_file_name, 'wt') as summary_file:
            summary_file.write('circuit,Qiskit_runtime,Giallar_runtime\n')
            for (filename, qiskit_runtime, giallar_runtime) in result_table:
                summary_file.write('{},{},{}\n'.format(filename, qiskit_runtime, giallar_runtime))
        print('Summary written to {}'.format(summary_file_name))
