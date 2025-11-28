import sys
import pathlib
import argparse

# do no use resolve()
runfiles_dir = pathlib.Path(__file__).parent
rust_dir = runfiles_dir.parent / "rust"

print("RUNFILES_DIR:", runfiles_dir)
print("RUST_DIR:", rust_dir)

sys.path.insert(0, str(rust_dir))

import rust_fib

def main() -> None:

    parser = argparse.ArgumentParser()
    parser.add_argument("n", type=int, 
                        default = 20,
                        help="Fibonacci number")
    
    args = parser.parse_args()

    result = rust_fib.fib(args.n)
    print(f"Rust fib({args.n}) = {result}")

if __name__ == "__main__":
    main()
    


#===============    
# END 
#===============    
