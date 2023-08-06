use ndarray;
use numpy::{IntoPyArray, PyArray1, PyArray2, PyArrayDyn, PyReadonlyArrayDyn, PyReadonlyArray1};
use pyo3::prelude::*;

/// Formats the sum of two numbers as string.

#[pyfunction]
fn generate_data() -> (Vec<f64>, Vec<f64>) {
    let x_values = vec![0.01, 0.02, 0.05, 0.10, 0.20, 0.50, 1.00, 2.00, 5.00];
    let y_values = vec![129867.0, 284533.0, 655220.0, 1469586.0, 3359871.0, 5820969.0, 13009337.0, 22875222.0, 43101398.0];

    let x_values_f64: Vec<f64> = x_values.into_iter().map(|x| x as f64).collect();
    let y_values_f64: Vec<f64> = y_values.into_iter().map(|y| y as f64).collect();

    (x_values_f64, y_values_f64)
}

#[pyfunction]
fn calculate_mean(
   
    values: PyReadonlyArrayDyn<f64>) -> f64 {
    let values = values.as_array();
    let n = values.len() as f64;    
    let values = values.iter().sum::<f64>() / n;
    values
}

#[pyfunction]
fn calculate_slope(x_vals: PyReadonlyArrayDyn<f64>, y_vals: PyReadonlyArrayDyn<f64>) -> f64 {

 

    let x_vals =  x_vals.as_array();
    let y_vals = y_vals.as_array();

    let x_vals_n = x_vals.len() as f64;
    let x_vals_mean = x_vals.iter().sum::<f64>() / x_vals_n;        

    let y_vals_n = y_vals.len() as f64;
    let y_vals_mean = y_vals.iter().sum::<f64>() / y_vals_n; 



    let numerator = x_vals
        .iter()
        .zip(y_vals.iter())
        .map(|(&xi, &yi)| (xi - x_vals_mean) * (yi - y_vals_mean))
        .sum::<f64>();

    let denominator = x_vals
        .iter()
        .map(|&xi| (xi - x_vals_mean).powi(2))
        .sum::<f64>();

    numerator / denominator
}

#[pyfunction]
fn calculate_intercept(x_vals: PyReadonlyArrayDyn<f64>, y_vals: PyReadonlyArrayDyn<f64>) -> f64 {

    let x_vals =  x_vals.as_array();
    let y_vals = y_vals.as_array();

    let x_vals_n = x_vals.len() as f64;
    let x_vals_mean = x_vals.iter().sum::<f64>() / x_vals_n;        

    let y_vals_n = y_vals.len() as f64;
    let y_vals_mean = y_vals.iter().sum::<f64>() / y_vals_n; 

    let numerator = x_vals
        .iter()
        .zip(y_vals.iter())
        .map(|(&xi, &yi)| (xi - x_vals_mean) * (yi - y_vals_mean))
        .sum::<f64>();

    let denominator = x_vals
        .iter()
        .map(|&xi| (xi - x_vals_mean).powi(2))
        .sum::<f64>();

    
    let slope = numerator / denominator;


    let intercept = y_vals_mean - slope * x_vals_mean;
    return intercept;
}

// fn get_params(x_vals: &[f64], y_vals: PyReadonlyArrayDyn<f64>) -> (f64, f64) {
//     let slope = calculate_slope(x_vals, y_vals);
//     let intercept = calculate_intercept(x_vals, y_vals);

//     (slope, intercept)
// }
#[pyfunction]
fn calculate_r_squared(x_vals: PyReadonlyArrayDyn<f64>, y_vals: PyReadonlyArrayDyn<f64>) -> f64 {
    // let y_mean = calculate_mean(y_vals);

    let x_vals =  x_vals.as_array();
    let y_vals = y_vals.as_array();

    let x_vals_n = x_vals.len() as f64;
    let x_vals_mean = x_vals.iter().sum::<f64>() / x_vals_n;        

    let y_vals_n = y_vals.len() as f64;
    let y_vals_mean = y_vals.iter().sum::<f64>() / y_vals_n; 

    let numerator = x_vals
        .iter()
        .zip(y_vals.iter())
        .map(|(&xi, &yi)| (xi - x_vals_mean) * (yi - y_vals_mean))
        .sum::<f64>();

    let denominator = x_vals
        .iter()
        .map(|&xi| (xi - x_vals_mean).powi(2))
        .sum::<f64>();

    
    let slope = numerator / denominator;


    let intercept = y_vals_mean - slope * x_vals_mean;

    let total_sum_squares = y_vals
        .iter()
        .map(|&y| (y - y_vals_mean).powi(2))
        .sum::<f64>();

    let residuals_sum_squares = y_vals
        .iter()
        .zip(x_vals.iter())
        .map(|(&y, &x)| {
            let predicted = slope * x + intercept;
            (y - predicted).powi(2)
        })
        .sum::<f64>();

    1.0 - (residuals_sum_squares / total_sum_squares)
}

/// A Python module implemented in Rust.
#[pymodule]
fn rustregression(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(generate_data, m)?)?;
    m.add_function(wrap_pyfunction!(calculate_mean, m)?)?;
    m.add_function(wrap_pyfunction!(calculate_slope, m)?)?;
    m.add_function(wrap_pyfunction!(calculate_intercept, m)?)?;
    // m.add_function(wrap_pyfunction!(get_params, m)?)?;
    m.add_function(wrap_pyfunction!(calculate_r_squared, m)?)?;

    Ok(())
}