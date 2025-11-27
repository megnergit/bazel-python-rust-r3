import sys
import pathlib
import argparse

# do no use resolve()
runfiles_dir = pathlib.Path(__file__).parent
cpp_dir = runfiles_dir.parent / "cpp"

print("RUNFILES_DIR:", runfiles_dir)
print("CPP_DIR:", cpp_dir)

sys.path.insert(0, str(cpp_dir))

import fib_module

def main() -> None:

    parser = argparse.ArgumentParser()
    parser.add_argument("n", type=int, 
                        default = 20,
                        help="Fibonacci number")
    
    args = parser.parse_args()

    result = fib_module.fib(args.n)
    print(f"C++ fib({args.n}) = {result}")

if __name__ == "__main__":
    main()
    


#===============    
# END 
#===============    
