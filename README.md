# Bazel, Python, Rust, C++

## Table of Contents

- [Motivation](#motivation) 
- [Goal](#goal) 
- [Build Rust Code by Bazel](#build-rust-by-bazel)
  - [Performance Test 1](#performance-test-1)

- [Run Python Code by Basel](#run-python-by-bazel)
  - [Performance Test 2](#performance-test-2)

- [Build Python and C++ Code by Bazel]


---
## Motivation

I would like to understand how bazel works. 

Bazel is a build tool that can build almost all contemporary programing language. 

- fast, because 
  + use caches
  + build intelligently (build only the codes that needs to be build again)

- sandbox environment, 
  + means bazel does not use user's own local directory to compile codes, but 
    set up a separate 'workspace' (= directory?) to compile codes (all 
    tools and dependencies are deployed there). There is no dependies on 
    users's own individual environment. It is a bit like 'runner' when we 
    do CI/CD on gitlab. 


This makes Bazel particularly useful when the codes are stored in a single 
giangic repository (= mono-repo), as opposed to the codes stored separatley 
according to the projects. Bazel is originally developped by Google, who is
known to store all its code-base in a company-wide mono-repo. 


However, basel is not easy to learn. 

- There are detailed official documentations by Gooogle, 
  + but with little (not enough) working examples. 

- On the internet, neither.  

- In particular when WORKSPACE migrated to bzlmod in 2023.
  + very little working examples for MODULE.bazel


## Goal 

The goal is to create a small project that combines 

- Python
- Rust 

and build the artifact using Bazel. 

... it turns out the road is quite long, and had to start small. 

We will do the following. 


1. Build Python and Rust code **separately** by bazel. 
2. Build Python and C++ code **together** by basel.  
3. Build Python and Rust code **together** by basel.  
4. Combine Python, Rust, and C++ by basel. 


Every time we complete these sub-projects, we will measure the advantage of 
bazel, such as 

- acceleration of build by bazel 
- offloading compute-intensive function to Rust/C++


---

# Build Rust by Bazel

The goal of this sub-project is to learn the basics of bazel. 

1. directory structure
2. prepare MODULE.bazel
3. prepare BUILD.bazel

The directory structure is as follows. 

```sh

$ tree .
.
├── MODULE.bazel
├── README.md
├── py
│   ├── BUILD.bazel
│   └── hello.py
└── rust
    ├── BUILD.bazel
    └── main.rs

```
'$' here means, do it on the terminal at a shell prompt. 

The main.rs of rust is as follows.  

```rust
fn main(){
    println!("Hello from Rust via Bazel.");
}
```

The points of bazel setup are two fold: 

1. We need ```MODULE.bazel ``` at the project root. 
2. We need ```BUILD.bazel ``` at each package (here this is synonym to the language, like python and rust)


```MODULE.bazel``` takes care of the dependencies on external resources common to 
all the packages. 

```BUILD.bazel``` takes care of instantiation of rules. 

The minimum setup is as follwso. 

```sh MODULE.bazel

bazel_dep(name = "rules_rust", version = "0.67.0")

```

The code tells bazel that we will need the repo 'rules_rust' as we will build rust codes.  

The latest version of rules_rust is found 
at [Bazel Central Registry](https://registry.bazel.build/modules/rules_rust).

We will have BUILD.bazel in ./rust directory.

```sh BUILD.bazel
load("@rules_rust//rust:defs.bzl", "rust_binary")

rust_binary(
    name = "hello",
    srcs = ["main.rs"],
)
```

The ```load...``` line is like 'import' a class in python. In this case, 'rust_binary' is the name of the 
class. ```rust_binary()``` line 'instantiate' the class by the name 'hello_rust'. 

# Performance Test 1!

Let us run the code, rustc and bazel.  We will do the following.

1. time rustc rust/hello.rs
2. bazel build //rust:hello (first time)
3. bazel build //rust:hello (second time)

First time.

```sh rustc 
$ time rustc rust/main.rs
rustc rust/main.rs  0.23s user 0.12s system 63% cpu 0.548 total
```

Second time.

```sh rustc
$ time rustc rust/main.rs
rustc rust/main.rs  0.24s user 0.16s system 50% cpu 0.784 total
```

First clean up the previous artefacts.

```sh bazel

$ bazel clean --expunge
```

The command deletes ./bazel-* directories and artefacts. 

```sh bazel
$ bazel build //rust:hello
```

```//rust``` part of the argument represents that we have 
./rust directory (= package) under the project root. 

```:hello``` part corresponds to 
```sh
rust_binary(
  name = "hello",         <- HERE
  ...
)
``` 
in ./rust/BUILD.bazel file. This is the name of the `target`. 

First time.

```sh bazel
$ bazel build //rust:hello

WARNING: Ignoring JAVA_HOME, because it must point to a JDK, not a JRE.
Starting local Bazel server (8.4.2) and connecting to it...
INFO: Analyzed target //rust:hello (89 packages loaded, 1327 targets configured).
INFO: Found 1 target...
Target //rust:hello up-to-date:
  bazel-bin/rust/hello
INFO: Elapsed time: 45.621s, Critical Path: 9.39s
INFO: 106 processes: 103 internal, 3 darwin-sandbox.
INFO: Build completed successfully, 106 total actions
```


Second time (we have now cache).

```sh baze$ bazel build //rust:hello
WARNING: Ignoring JAVA_HOME, because it must point to a JDK, not a JRE.
INFO: Analyzed target //rust:hello (32 packages loaded, 316 targets configured).
INFO: Found 1 target...
Target //rust:hello up-to-date:
  bazel-bin/rust/hello
INFO: Elapsed time: 0.478s, Critical Path: 0.00s
INFO: 1 process: 3 action cache hit, 1 internal.
INFO: Build completed successfully, 1 total action

```

**Summary**
builder|  trial     | elapsed time|
------|-------------|---------|
rustc | first time  | 0.548 s | 
rustc | second time | 0.784 s | 
bazel | first time  |  45 s   | 
bazel | second time  | 0.478 s | 


All right. 







---
# Run Python by Bazel

Python is interpreter, therefore there is little 
to do in 'build' other than preparing the runtime 
(= python interpreter) in the sandbox. 

We will then run a python code by local python interpreter
and bazel, and compare the performance. 

Current directory structure, 

```sh
$ tree .
.
├── LICENSE
├── MODULE.bazel
├── MODULE.bazel.lock
├── README.md
├── py
│   ├── BUILD.bazel
│   └── hello.py
└── rust
    ├── BUILD.bazel
    ├── main
    └── main.rs
```


```sh MODULE.bazel
bazel_dep(name = "rules_python", version = "1.7.0")
```

```sh py/BUILD.bazel

load("@rules_python//python:defs.bzl", "py_binary")

py_binary(
    name = "hello",
    srcs = ["hello.py"],
)    
```


```py hello.py
def hello() -> None:
  print("Hi from bazel.")

if __name__ == "__main__":
  hello()
```

## Performance Test 2!

First time.
```sh
$ time python py/hello.py
Hi from bazel.
python py/hello.py  0.09s user 0.06s system 88% cpu 0.176 total
```

Second time. 
```sh
$ time python py/hello.py
Hi from bazel.
python py/hello.py  0.10s user 0.07s system 88% cpu 0.185 total
```

Clean.
```sh
$ bazel clean --expunge
```

First time.
```sh
$ bazel run //py:hello
WARNING: Ignoring JAVA_HOME, because it must point to a JDK, not a JRE.
Starting local Bazel server (8.4.2) and connecting to it...
INFO: Analyzed target //py:hello (81 packages loaded, 3487 targets configured).
INFO: Found 1 target...
Target //py:hello up-to-date:
  bazel-bin/py/hello
INFO: Elapsed time: 10.172s, Critical Path: 0.41s
INFO: 8 processes: 8 internal.
INFO: Build completed successfully, 8 total actions
INFO: Running command line: bazel-bin/py/hello
Hi from bazel.
```

Second time.
```sh
$ bazel run //py:hello
WARNING: Ignoring JAVA_HOME, because it must point to a JDK, not a JRE.
INFO: Analyzed target //py:hello (32 packages loaded, 316 targets configured).
INFO: Found 1 target...
Target //py:hello up-to-date:
  bazel-bin/py/hello
INFO: Elapsed time: 0.402s, Critical Path: 0.01s
INFO: 1 process: 1 action cache hit, 1 internal.
INFO: Build completed successfully, 1 total action
INFO: Running command line: bazel-bin/py/hello
Hi from bazel.
```


**Summary**
run by    |   trial     | elapsed time|
----------|-------------|---------|
python    | first time  | 0.176 s | 
python    | second time | 0.185 s | 
bazel run | first time  | 10.2 s  | 
bazel run | second time | 0.402 s | 

Satisfied. 

---

# Build Python and C++ code by Bazel

If you do not build codes of multiple language at once, 
you are only taking the tiny part of the advantage of bazel. 

The idea is to offload compute intensive part to C++, 
while writing other soft part in Python. 

We will use Fibonacci to test and compare the performance. 

Tree. 

```sh

$ tree .
.
├── LICENSE
├── MODULE.bazel
├── README.md
├── cpp
│   ├── BUILD.bazel
│   └── fib_mod.cc
└── py
    ├── BUILD.bazel
    ├── fib.py
    └── hello.py

```

A few notes that I do not understand. 

```sh  MODULE.bazel
...
bazel_dep(name = "pybind11_bazel", version = "2.13.6") # 3.0.0
bazel_dep(name = "platforms", version = "0.0.11")
...
```

The first line is to build a python module (= *.so file) out of C++ source code. pybind11 will create a module that a python code can 
directly import by ```import [module name]```.

The second line is not clear to me, but necessary to build 
(bazel complaints, and requests to add this line) 


```py fib_cpp_offload.py
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

...
```

This is something that I do not understand. 
Somehow in order to import newly created python module (from C++ source code), I had to add runfile directory to sys.path. 
It seems that such stuff would be well taken care of builder (=bazel), but apparently not. 


## Performance Test 3!

We will compare the speed of Fibonacci series in 

1. python only
2. C++ offloaded. built and run by Bazel. 


```sh
$ time python py/fib_python_only.py 32
n = 32
Python fib(32) = 2178309
python py/fib_python_only.py 32  0.53s user 0.07s system 96% cpu 0.627 total
$ time python py/fib_python_only.py 33
n = 33
Python fib(33) = 3524578
python py/fib_python_only.py 33  0.77s user 0.07s system 97% cpu 0.853 total
$ time python py/fib_python_only.py 34
n = 34
Python fib(34) = 5702887
python py/fib_python_only.py 34  1.15s user 0.07s system 98% cpu 1.234 total
$ time python py/fib_python_only.py 35
n = 35
Python fib(35) = 9227465
python py/fib_python_only.py 35  1.78s user 0.07s system 98% cpu 1.866 total
$ time python py/fib_python_only.py 36
n = 36
Python fib(36) = 14930352
python py/fib_python_only.py 36  2.79s user 0.07s system 99% cpu 2.873 total
$ 
```

Then offloaded-to-C++ version. Firts clean the artefact. 

```sh bazel
$ bazel clean --expunge
```

Then, 
```sh bazel
$ bazel  run //py:fib_cpp_offload -- 32
WARNING: Ignoring JAVA_HOME, because it must point to a JDK, not a JRE.
Starting local Bazel server (8.4.2) and connecting to it...
INFO: Analyzed target //py:fib_cpp_offload (84 packages loaded, 3545 targets configured).
INFO: Found 1 target...
Target //py:fib_cpp_offload up-to-date:
  bazel-bin/py/fib_cpp_offload
INFO: Elapsed time: 12.507s, Critical Path: 2.62s
INFO: 13 processes: 11 internal, 2 darwin-sandbox.
INFO: Build completed successfully, 13 total actions
INFO: Running command line: bazel-bin/py/fib_cpp_offload <args omitted>
RUNFILES_DIR: /private/var/tmp/_bazel_meg/577fcf44d4e22393c110bef87b8577b8/execroot/_main/bazel-out/darwin_x86_64-fastbuild/bin/py/fib_cpp_offload.runfiles/_main/py
CPP_DIR: /private/var/tmp/_bazel_meg/577fcf44d4e22393c110bef87b8577b8/execroot/_main/bazel-out/darwin_x86_64-fastbuild/bin/py/fib_cpp_offload.runfiles/_main/cpp
C++ fib(32) = 2178309


must point to a JDK, not a JRE.
INFO: Analyzed target //py:fib_cpp_offload (32 packages loaded, 316 targets configured).
INFO: Found 1 target...
Target //py:fib_cpp_offload up-to-date:
  bazel-bin/py/fib_cpp_offload
INFO: Elapsed time: 0.501s, Critical Path: 0.01s
INFO: 1 process: 1 action cache hit, 1 internal.
INFO: Build completed successfully, 1 total action
INFO: Running command line: bazel-bin/py/fib_cpp_offload <args omitted>
RUNFILES_DIR: /private/var/tmp/_bazel_meg/577fcf44d4e22393c110bef87b8577b8/execroot/_main/bazel-out/darwin_x86_64-fastbuild/bin/py/fib_cpp_offload.runfiles/_main/py
CPP_DIR: /private/var/tmp/_bazel_meg/577fcf44d4e22393c110bef87b8577b8/execroot/_main/bazel-out/darwin_x86_64-fastbuild/bin/py/fib_cpp_offload.runfiles/_main/cpp
C++ fib(33) = 3524578
[meg@elias ~/rust/bazel-python-rust-r3]$ 

....

```

**Summary**


Fibonacci # |  Python | C++ offload
------------|---------|------------- 
32	        | 0.627 s |  12.5 s (First time)
33 	        | 0.853 s |  0.501 s
34	        | 1.234 s |  0.167 s
35 	        | 1.866 s |  0.177 s
36	        | 2.873 s |  0.201 s

Satisfied. 



-------------------------------------

# Appendix 

## Install rust


[Read](https://rust-lang.org/tools/install/)

```sh install rust
$ curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

```
Do not use 'brew'. It would take forever.

Add $HOME/.cargo/bin to your ```PATH``` environmental variable in .zshrc.

```sh ~/.zshrc
...
#===================================================
# for Rust
#===================================================
export PATH="$HOME/.cargo/bin:$PATH"
#---------------------------------------------------
```

Then, 
```sh
$ source ~/.zshrc
$ rehash
```


Check 
```sh
$ rustc --version
rustc 1.91.1 (ed61e7d7e 2025-11-07)
$ cargo --version
cargo 1.91.1 (ea2d97820 2025-10-10)
```

All right. 



-----
## Install Python
Use pyenv. 

```sh install pyenv
$ brew install pyenv
```

Then 

```sh
pyenv install 3.11.14

```

for example.

## Install C++

```sh install c++

$ bres install cpp 

```

## Install bazel 

Use [bazelisk](https://formulae.brew.sh/formula/bazelisk)

```sh install bazelisk

$ brew install bazelisk

```

---
# END
---