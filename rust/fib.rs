use pyo3::prelude::*;

#[pyfunction]
fn fib(n: u64) -> u64 {
    match n {

        0 => 0, 
        1 => 1, 
        _ => fib(n - 1) + fib(n - 2), 

    }
}

#[pymodule]
fn rusty (_py: Python, m: &PyModule) -> PyResult<()> {

    m.add_function(wrap_pyfunction!(fib, m)?)?;
    Ok(())
}

