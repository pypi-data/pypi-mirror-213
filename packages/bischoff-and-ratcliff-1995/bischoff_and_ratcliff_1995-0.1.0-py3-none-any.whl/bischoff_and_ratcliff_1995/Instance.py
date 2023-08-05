import math

from .Random import Random


class Instance:
    NUMBER_OF_INITIAL_RANDOM_NUMBERS_TO_DISCARD = 10

    def __init__(self, C, n, a, b, L, s):
        # save parameters
        self.C = C
        T_c = math.prod(C.values())
        self.T_c = T_c
        self.n = n
        self.a = a
        self.b = b
        self.L = L
        self.s = s

        # initialize values
        d = [[] for i in range(n)]  # box dimensions
        o = [[] for i in range(n)]  # feasible vertical orientations
        m = [0 for i in range(n)]  # box quantity
        v = [0 for i in range(n)]  # box volume

        # initialize random number generator
        # and discard the first 10 random numbers
        random = Random(s)
        for _ in range(Instance.NUMBER_OF_INITIAL_RANDOM_NUMBERS_TO_DISCARD):
            random.real()

        # set box type i to 1
        i = 1

        for i in range(n):
            # generate three random numbers
            # r_j, \forall j \in \{1, 2, 3\}
            r = [random.real() for _ in range(3)]

            # determine the box dimensions using
            # d_{i,j} = a_j + floor(r_j * (b_j - a_j + 1))
            # \forall j \in \{1, 2, 3\}
            d[i] = [a[j] + math.floor(r[j] * (b[j] - a[j] + 1)) for j in range(3)]
            d[i].sort(reverse=True)

            # for each j \in \{1, 2, 3\} set d_{i,j}
            # to be a feasible vertical orientation
            # if and only if
            # [ d_{i,j} / min_{j \in \{1, 2, 3\}}(d_{i,j}) ] < L
            o[i] = [(d[i][j] / min(d[i])) < L for j in range(3)]

            # initialize box quantity m_i
            # for box type i: m_i = 1
            m[i] = 1

            # let the box volume v_i = prod_{j \in \{1, 2, 3\}}(d_{i,j})
            v[i] = math.prod(d[i])

        while True:
            # calculate the cargo volume
            # C = sum_{i \in \{1, ..., n\}}(m_i * v_i)
            C = sum([m[i] * v[i] for i in range(n)])

            # generate the next random number r
            # and set box type indicator
            # k = 1 + floor(r * n)
            r = random.real()
            k = math.floor(r * n)

            # compare cargo volume with
            # the target value:
            # T_c > C + v_k?
            if T_c < (C + v[k]):
                break

            # set m_k = m_k + 1
            m[k] = m[k] + 1

        # save values
        self.d = d
        self.o = o
        self.m = m

        return

    def to_dict(self):
        return {
            "type": "input",
            "version": "0.3.0",
            "large_object": {
                "measurement": {
                    "x": self.C["length"],
                    "y": self.C["width"],
                    "z": self.C["height"],
                }
            },
            "small_items": [
                {
                    "measurement": {
                        "x": self.d[i][0],
                        "y": self.d[i][1],
                        "z": self.d[i][2],
                    },
                    "quantity": self.m[i],
                    "constraint": {
                        "orientation": {
                            "xyz": self.o[i][2],
                            "yxz": self.o[i][2],
                            "zyx": self.o[i][0],
                            "xzy": self.o[i][1],
                            "zxy": self.o[i][1],
                            "yzx": self.o[i][0],
                        },
                    },
                }
                for i in range(self.n)
            ],
        }
