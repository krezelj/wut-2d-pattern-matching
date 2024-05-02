from trie import Trie


def build_automaton(P: list[str]) -> Trie:
    T = Trie()
    for i in range(len(P)):
        T.insert_key(P[i])
    T.link_suffixes()
    return T


def build_kmp_table(P: list[str]) -> list[int]:
    n1 = len(P)

    p = []
    T = Trie()
    for row in P:
        p.append(T.insert_key(row))

    t = [0] * n1
    l = 0
    i = 1
    while i < n1:
        if p[i] == p[l]:
            l += 1
            t[i] = l
            i += 1
        else:
            if l != 0:
                l = t[l - 1]
            else:
                t[i] = 0
                i += 1
    return t


def search(M: list[str], P: list[str]):
    m1 = len(M)
    m2 = len(M[0])
    n1 = len(P)
    n2 = len(P[0])

    automaton = build_automaton(P)
    t = build_kmp_table(P)
    a = [0] * m2
    S = []

    for i in range(m1):
        state = automaton.root
        for j in range(m2):
            char = M[i][j]
            while automaton.go(state, char) is None and state is not automaton.root:
                state = automaton.fail(state)
            state = automaton.go(state, char)

            if state.terminal:
                k = a[j]
                if state.key == P[k]:
                    k += 1
                    if k == n1:
                        k = t[k - 1]
                        S.append((i + 2 - n1, j + 2 - n2))
                    a[j] = k
            else:
                a[j] = 0
    return S


def main():
    M = ['ababc', 'abcba', 'cbabc', 'abcba', 'ababc']
    P = ['abc', 'cba', 'abc']
    print(search(M, P))


if __name__ == '__main__':
    main()