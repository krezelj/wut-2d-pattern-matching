import numpy as np

MAX_ATTEMPTS = 100


def convert_to_chars(A):
    result = []
    for i in range(A.shape[0]):
        result.append("")
        for j in range(A.shape[1]):
            result[-1] += chr(97 + A[i, j])
    return result


def generate_example(m1, m2, n1, n2, target_k):
    M = np.random.randint(0, 25, size=(m1, m2))
    P = np.random.randint(0, 25, size=(n1, n2))
    P[np.random.randint(n1), np.random.randint(n2)] = 25
    available = np.full(shape=(m1, m2), fill_value=True)
    if n1 > 1:
        available[1 - n1:,:] = False
    if n2 > 1:
        available[:,1 - n2:] = False

    positions = []
    attempts = 0
    for k in range(target_k):
        attempts = 0
        while True:
            attempts += 1
            if attempts == MAX_ATTEMPTS:
                break
            i = np.random.randint(m1)
            j = np.random.randint(m2)
            if available[i, j]:
                break
        if attempts == MAX_ATTEMPTS:
            target_k = k
            break
        
        positions.append((i + 1, j + 1))
        M[i:i+n1, j:j+n2] = P
        available[max(0, i-n1):i+n1, max(0, j-n2):j+n2]=False

    M = convert_to_chars(M)
    P = convert_to_chars(P)
    positions.sort(key = lambda p : (p[0], p[1]))
    return M, P, positions, target_k

