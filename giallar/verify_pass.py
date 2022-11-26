import subprocess
import os
import time
import sys


if __name__ == '__main__':

    if len(sys.argv) < 2:
        print('Please specify the pass to verify.')
        exit(-1)
    pass_name = sys.argv[1]

    if pass_name == "all":
        files = []
        file_root = '../verified_passes/'
        for root, directories, filenames in os.walk(file_root):
            for filename in filenames:
                files.append(os.path.join(root, filename))
        
        for pass_path in files:
            cur_pass_name = pass_path.split("/")[-1].split(".")[0]
            if cur_pass_name == "__init__":
                continue
            print("======= Proving {} =======".format(cur_pass_name))
            preprocessor_ret = subprocess.run(['python', 'preprocessor.py', '--file', '../{}'.format(pass_path)], cwd='preprocessor/')
            if preprocessor_ret.returncode != 0:
                print('preprocessor failed')
                continue

            proof_goal_path = 'preprocessor/output_files'
            with open('{}/{}_count.txt'.format(proof_goal_path, cur_pass_name), 'rt') as proof_goal_count_file:
                num_proof_goal = int(proof_goal_count_file.readlines()[0])

            pre_time = time.time()
            for proof_goal_idx in range(num_proof_goal):
                proof_ret = subprocess.run(['python', '{}_{}.py'.format(proof_goal_idx, cur_pass_name)], cwd=proof_goal_path, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
                print('Proving {}th subgoal'.format(proof_goal_idx))
            print("Time: {}s".format(time.time() - pre_time))

    else:
        pass_path = '../verified_passes/{}.py'.format(pass_name)
        if not os.path.exists(pass_path):
            print('Cannot find pass {} in verified_passes'.format(pass_name))
            exit(-1)

        preprocessor_ret = subprocess.run(['python', 'preprocessor.py', '--file', '../{}'.format(pass_path)], cwd='preprocessor/')
        if preprocessor_ret.returncode != 0:
            print('preprocessor failed')
            exit(-1)

        proof_goal_path = 'preprocessor/output_files'
        with open('{}/{}_count.txt'.format(proof_goal_path, pass_name), 'rt') as proof_goal_count_file:
            num_proof_goal = int(proof_goal_count_file.readlines()[0])

        pre_time = time.time()
        for proof_goal_idx in range(num_proof_goal):
            print('Proving {}th subgoal'.format(proof_goal_idx))
            proof_ret = subprocess.run(['python', '{}_{}.py'.format(proof_goal_idx, pass_name)], cwd=proof_goal_path)
        print("Time: {}s".format(time.time() - pre_time))