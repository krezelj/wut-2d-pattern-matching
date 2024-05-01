import time

import pandas as pd
import numpy as np
from tqdm import tqdm
from tqdm.contrib.itertools import product

from generator import generate_example
from search import search


def dump_data(M, P, result, p):
    with open('./dump/M.txt', 'w') as f:
        f.writelines('\n'.join(M) + '\n')
    with open('./dump/P.txt', 'w') as f:
        f.writelines('\n'.join(P) + '\n')
    with open('./dump/result.txt', 'w') as f:
        f.write(f"{len(result)} {len(p)}\n")
        f.write(str(result))
        f.write('\n')
        f.write(str(p))
    

def validate_result(result, p):
    if len(result) != len(p):
        raise Exception("length of result is not the same as length of p")
    for a, b in zip(result, p):
        if a != b:
            raise Exception("result and p do not match")


def run_benchmark():
    m1_space = np.arange(200, 199, -100)
    m2_space = np.arange(200, 199, -100)
    n1_space = np.arange(30, 4, -5)
    n2_space = np.arange(30, 4, -5)
    n_runs = [11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
    df = pd.DataFrame(columns=["m1", "m2", "n1", "n2", "m1m2", "n1n2", "conf_id", "t"])
    np.random.seed(0)
 

    for id, (m1, m2, n1, n2) in tqdm(enumerate(product(m1_space, m2_space, n1_space, n2_space))):
        lam = 1 + (m1 * m2) // (n1 * n2 * 10)
        n = n_runs[int(np.sqrt(m1 * m2)) // 100]
        for _ in tqdm(range(n), leave=False):
            k = 1 + np.random.poisson(lam)
            M, P, p, k = generate_example(m1, m2, n1, n2, k)

            # print(f"running configuration {m1}x{m2}/{n1}x{n2} run {i}... ", end="")
            start = time.process_time_ns()
            result = search(M, P)
            duration = time.process_time_ns() - start
            # print(f"done! ({duration/1e9})")
            try:
                validate_result(result, p)
            except Exception as e:
                print(e)
                dump_data(M, P, result, p)
                raise e

            new_row = {
                "m1": m1,
                "m2": m2,
                "n1": n1,
                "n2": n2,
                "m1m2": m1*m2,
                "n1n2": n1*n2,
                "conf_id": id,
                "t": duration,
            }
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_csv("benchmark_2.csv")


if __name__ == '__main__':
    run_benchmark()