


def det2(m):
    return m[0][0] * m[1][1] - m[0][1] * m[1][0]


def det3(m):
    d = m[0][0] * m[1][1] * m[2][2] + \
        m[0][1] * m[1][2] * m[2][0] + \
        m[0][2] * m[2][1] * m[1][0] - \
        m[2][0] * m[1][1] * m[0][2] - \
        m[1][0] * m[0][1] * m[2][2] - \
        m[0][0] * m[1][2] * m[2][1]
    return d


def det4(m):
    m0 = [
        [m[1][1], m[1][2], m[1][3]],
        [m[2][1], m[2][2], m[2][3]],
        [m[3][1], m[3][2], m[3][3]]
    ]
    m1 = [
        [m[1][0], m[1][2], m[1][3]],
        [m[2][0], m[2][2], m[2][3]],
        [m[3][0], m[3][2], m[3][3]]
    ]
    m2 = [
        [m[1][0], m[1][1], m[1][3]],
        [m[2][0], m[2][1], m[2][3]],
        [m[3][0], m[3][1], m[3][3]]
    ]
    m3 = [
        [m[1][0], m[1][1], m[1][2]],
        [m[2][0], m[2][1], m[2][2]],
        [m[3][0], m[3][1], m[3][2]]
    ]
    return m[0][0] * det3(m0) - m[0][1] * det3(m1) + m[0][2] * det3(m2) - m[0][3] * det3(m3)


def set_identity(m, n):
    for i in range(0, n):
        for j in range(0, n):
            if i == j:
                m[i][j + n] = 1
            else:
                m[i][j + n] = 0


def gaus_jordan(m, size):
    for i in range(0, size):
        if m[i][i] == 0: raise Exception("MATHMATILCAL ERROR")
        for j in range(0, size):
            if i != j:
                ratio = m[j][i]/m[i][i]
                for k in range(2*size):
                    m[j][k] = m[j][k] - ratio * m[i][k]


def row_operations_principal_diagonal(m, size):
    for i in range(0, size):
        for j in range(size, 2*size):
            m[i][j] = m[i][j]/m[i][i]


def flatten(obj):
    return [ x for x in obj]


