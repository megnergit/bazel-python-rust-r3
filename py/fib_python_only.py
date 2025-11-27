# fib_python.py
# 
import argparse


def fib(n: int) -> int:
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)


def main() -> None:

    parser = argparse.ArgumentParser()
    parser.add_argument("n", type=int, 
                        default = 20,
                        help="Fibonacci number")
    
    args = parser.parse_args()

    print(f"n = {args.n}")
        
#    n = 35  # compute-intensive task
    print(f"Python fib({args.n}) = {fib(args.n)}")

if __name__ == "__main__":
    main()
