from search import search
from generator import generate_example
import time


def read_from_file():
    path = input("path: ")

    M = []
    P = []
    with open(path, 'r') as f:
        m1 = int(f.readline().strip())
        m2 = int(f.readline().strip())
        n1 = int(f.readline().strip())
        n2 = int(f.readline().strip())
        for _ in range(m1):
            M.append(f.readline().strip())
        for _ in range(n1):
            P.append(f.readline().strip())
    return M, P


def get_new():
    m1 = int(input("m1: "))
    m2 = int(input("m2: "))
    n1 = int(input("n1: "))
    n2 = int(input("n2: "))
    target_k = int(input("target k: "))
    M, P, _, k = generate_example(m1, m2, n1, n2, target_k)
    if k != target_k:
        print(f"the generator stopped before reaching target k, {k} patterns inserted instead")
    return M, P


# def save_result(result):
#     path


def main():
    choice = input("Read file (r) or generate example (g)? (r/g): ")
    if choice == 'r':
        M, P = read_from_file()
    if choice == 'g':
        M, P = get_new()
    
    print("searching for patterns... ", end='')
    start = time.time_ns()
    result = search(M, P)
    duration = time.time_ns() - start
    print(f"done! {duration/1e9}s")


if __name__ =="__main__":
    main()