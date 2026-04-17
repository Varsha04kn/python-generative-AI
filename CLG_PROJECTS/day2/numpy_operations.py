import numpy as np


def main():
    a = np.array([10, 20, 30])
    b = np.array([1, 2, 3])

    print("a:", a)
    print("b:", b)
    print("a + b:", a + b)
    print("a - b:", a - b)
    print("a * b:", a * b)
    print("a / b:", a / b)

    print("sum(a):", a.sum())
    print("mean(b):", b.mean())
    print("a squared:", a ** 2)


if __name__ == "__main__":
    main()
