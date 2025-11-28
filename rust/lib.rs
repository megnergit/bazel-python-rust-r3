use pyo3::prelude::*;

#[pyfunction]
fn fib(n: u64) -> u64 {
    fn inner(x: u64) -> u64 {
        match x {
            0 => 0,
            1 => 1,
            _ => inner(x - 1) + inner(x - 2),
        }
    }
    inner(n)
}

#[pymodule]
fn rust_fib(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(fib, m)?)?;
    Ok(())
}

