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
    j = 2
    while j <= n1:
        if p[j - 1] == p[l]:
            l = l + 1
            t[j - 1] = l
            j = j + 1
        elif l != 0:
            l = t[l - 1]
        else:
            t[j - 1] = 0
            j = j + 1
    return t


def search(M: list[str], P: list[str]):
    m1 = len(M)
    m2 = len(M[0])
    n1 = len(P)
    n2 = len(P[0])

    automaton = build_automaton(P)
    t = build_kmp_table(P)
    a = [1] * m2
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
                while state.key != P[k - 1] and k != 0:
                    k = t[k - 1]

                if k == n1:
                    k = t[k - 1]
                    S.append((j + 1, i + 1)) # output should assume indices start at 1
                a[j] = k + 1
                    
            else:
                a[j] = 1
    return S


def main():
    M = ['ababc', 'abcba', 'cbabc', 'abcba', 'ababc']
    P = ['abc', 'cba', 'abc']
    print(search(M, P))


if __name__ == '__main__':
    main()