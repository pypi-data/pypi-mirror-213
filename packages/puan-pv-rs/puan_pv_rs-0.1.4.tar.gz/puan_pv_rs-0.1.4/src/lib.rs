use pyo3::prelude::*;
use std::hash::{Hash, Hasher};
use std::collections::hash_map::DefaultHasher;

// A functional way
// #[pyfunction]
// fn and(operands: Vec<i64>) -> impl Fn(Vec<i64>) -> bool {
//     move |interpretation: Vec<i64>| {
//         operands.iter().all(|operand| interpretation.contains(operand))
//     }
// }

// #[pyfunction]
// fn or(operands: Vec<i64>) -> impl Fn(Vec<i64>) -> bool {
//     move |interpretation: Vec<i64>| {
//         operands.iter().any(|operand| interpretation.contains(operand))
//     }
// }

// #[pyfunction]
// fn not(operands: Vec<i64>) -> impl Fn(Vec<i64>) -> bool {
//     move |interpretation: Vec<i64>| {
//         !operands.iter().any(|operand| interpretation.contains(operand))
//     }
// }

// fn conjunction(fn1: impl Fn(Vec<i64>) -> bool, fn2: impl Fn(Vec<i64>) -> bool) -> impl Fn(Vec<i64>) -> bool {
//     move |interpretation: Vec<i64>| {
//         fn1(interpretation.clone()) && fn2(interpretation.clone())
//     }
// }

// fn disjunction(
//     fn1: impl Fn(Vec<i64>) -> bool, 
//     fn2: impl Fn(Vec<i64>) -> bool,
// ) -> impl Fn(Vec<i64>) -> bool {
//     move |interpretation: Vec<i64>| {
//         fn1(interpretation.clone()) || fn2(interpretation.clone())
//     }
// }

// fn composition_val<T>(
//     composition: impl Fn(Vec<i64>) -> bool,
//     value: T,
// ) -> impl Fn(Vec<i64>) -> Option<T> where T: Clone {
//     move |interpretation: Vec<i64>| {
//         match composition(interpretation) {
//             true => Some(value.clone()),
//             false => None,
//         }
//     }
// }

fn hashit<T>(obj: T) -> u64
where
    T: Hash,
{
    let mut hasher = DefaultHasher::new();
    obj.hash(&mut hasher);
    hasher.finish()
}

// A simple way
#[pyclass]
#[derive(Clone, Hash)]
pub struct Disjunction {
    variables: Vec<String>
}

#[pymethods]
impl Disjunction {

    #[new]
    pub fn new(variables: Vec<String>) -> Self {
        Self {
            variables
        }
    }

    #[getter]
    pub fn variables(&self) -> PyResult<Vec<String>> {
        Ok(self.variables.clone())
    }

    pub fn hash(&self) -> u64 {
        hashit(self)
    }

    pub fn evaluate(&self, interpretation: Vec<String>) -> bool {
        self.variables.iter().any(|variable| interpretation.contains(variable))
    }
}

#[pyclass]
#[derive(Clone, Hash)]
pub struct Conjunction {
    variables: Vec<String>
}

#[pymethods]
impl Conjunction {

    #[new]
    pub fn new(variables: Vec<String>) -> Self {
        Self {
            variables
        }
    }

    #[getter]
    pub fn variables(&self) -> PyResult<Vec<String>> {
        Ok(self.variables.clone())
    }

    pub fn ident(&self) -> PyResult<String> {
        Ok(self.variables.join(""))
    }

    pub fn hash(&self) -> u64 {
        hashit(self)
    }

    pub fn evaluate(&self, interpretation: Vec<String>) -> bool {
        self.variables.iter().all(|variable| interpretation.contains(variable))
    }
}

#[pyclass]
#[derive(Clone, Hash)]
pub struct ConjunctiveComposition {
    composite_operands: Vec<Disjunction>,
    single_operands: Vec<String>,
}

#[pymethods]
impl ConjunctiveComposition {

    #[new]
    pub fn new(composite_operands: Vec<Disjunction>, single_operands: Vec<String>) -> Self {
        Self {
            composite_operands,
            single_operands,
        }
    }

    pub fn _variables(&self) -> Vec<String> {
        let mut variables = self.single_operands.clone();
        for operand in self.composite_operands.clone() {
            variables.extend(operand.variables);
        }
        variables
    }

    #[getter]
    pub fn composite_operands(&self) -> PyResult<Vec<Disjunction>> {
        Ok(self.composite_operands.clone())
    }

    #[getter]
    pub fn single_operands(&self) -> PyResult<Vec<String>> {
        Ok(self.single_operands.clone())
    }

    #[getter]
    pub fn variables(&self) -> PyResult<Vec<String>> {
        return Ok(self._variables())
    }

    pub fn hash(&self) -> u64 {
        hashit(self)
    }

    pub fn evaluate(&self, interpretation: Vec<String>) -> bool {
        self.single_operands.iter().all(|operand| interpretation.contains(operand)) &&
        self.composite_operands.iter().all(|operand| operand.evaluate(interpretation.clone()))
    }
}

#[pyclass]
#[derive(Clone, Hash)]
pub struct DisjunctiveComposition {
    composite_operands: Vec<Conjunction>,
    single_operands: Vec<String>,
}

#[pymethods]
impl DisjunctiveComposition {

    #[new]
    pub fn new(composite_operands: Vec<Conjunction>, single_operands: Vec<String>) -> Self {
        Self {
            composite_operands,
            single_operands,
        }
    }

    pub fn _variables(&self) -> Vec<String> {
        let mut variables = self.single_operands.clone();
        for operand in self.composite_operands.clone() {
            variables.extend(operand.variables);
        }
        variables
    }

    #[getter]
    pub fn variables(&self) -> PyResult<Vec<String>> {
        return Ok(self._variables())
    }

    #[getter]
    pub fn composite_operands(&self) -> PyResult<Vec<Conjunction>> {
        Ok(self.composite_operands.clone())
    }

    #[getter]
    pub fn single_operands(&self) -> PyResult<Vec<String>> {
        Ok(self.single_operands.clone())
    }

    pub fn hash(&self) -> u64 {
        hashit(self)
    }

    pub fn evaluate(&self, interpretation: Vec<String>) -> bool {
        self.single_operands.iter().any(|operand| interpretation.contains(operand)) ||
        self.composite_operands.iter().any(|operand| operand.evaluate(interpretation.clone()))
    }
}

#[pyclass]
#[derive(Clone, Hash)]
pub struct ConjunctiveCompositionKeys {
    conjuctive_compositions: ConjunctiveComposition,
    keys: Vec<String>,
}

#[pymethods]
impl ConjunctiveCompositionKeys {

    #[new]
    pub fn new(conjuctive_compositions: ConjunctiveComposition, keys: Vec<String>) -> Self {
        Self {
            conjuctive_compositions,
            keys,
        }
    }

    #[getter]
    pub fn variables(&self) -> PyResult<Vec<String>> {
        Ok(self.conjuctive_compositions._variables())
    }

    #[getter]
    pub fn conjunctive_compositions(&self) -> PyResult<ConjunctiveComposition> {
        Ok(self.conjuctive_compositions.clone())
    }

    #[getter]
    pub fn keys(&self) -> PyResult<Vec<String>> {
        Ok(self.keys.clone())
    }

    pub fn hash(&self) -> u64 {
        hashit(self)
    }

    pub fn evaluate(&self, interpretation: Vec<String>) -> Option<Vec<String>> {
        match self.conjuctive_compositions.evaluate(interpretation) {
            true => Some(self.keys.clone()),
            false => None,
        }
    }
}

#[pyclass]
#[derive(Clone, Hash)]
pub struct DisjunctiveCompositionKeys {
    disjunctive_compositions: DisjunctiveComposition,
    keys: Vec<String>,
}

#[pymethods]
impl DisjunctiveCompositionKeys {

    #[new]
    pub fn new(disjunctive_compositions: DisjunctiveComposition, keys: Vec<String>) -> Self {
        Self {
            disjunctive_compositions,
            keys,
        }
    }

    #[getter]
    pub fn variables(&self) -> PyResult<Vec<String>> {
        Ok(self.disjunctive_compositions._variables())
    }

    #[getter]
    pub fn disjunctive_compositions(&self) -> PyResult<DisjunctiveComposition> {
        Ok(self.disjunctive_compositions.clone())
    }

    #[getter]
    pub fn keys(&self) -> PyResult<Vec<String>> {
        Ok(self.keys.clone())
    }

    pub fn hash(&self) -> u64 {
        hashit(self)
    }

    pub fn evaluate(&self, interpretation: Vec<String>) -> Option<Vec<String>> {
        match self.disjunctive_compositions.evaluate(interpretation) {
            true => Some(self.keys.clone()),
            false => None,
        }
    }
}

#[pyclass]
#[derive(Clone, Hash)]
pub struct CCKeysIterable {
    conjunctive_composition_string_values: Vec<ConjunctiveCompositionKeys>,
}

#[pymethods]
impl CCKeysIterable {

    #[new]
    pub fn new(conjunctive_composition_string_values: Vec<ConjunctiveCompositionKeys>) -> Self {
        Self {
            conjunctive_composition_string_values,
        }
    }

    #[getter]
    pub fn conjunctive_composition_string_values(&self) -> PyResult<Vec<ConjunctiveCompositionKeys>> {
        Ok(self.conjunctive_composition_string_values.clone())
    }

    pub fn hash(&self) -> u64 {
        hashit(self)
    }

    pub fn evaluate(&self, interpretation: Vec<String>) -> Vec<ConjunctiveCompositionKeys> {
        self.conjunctive_composition_string_values
            .iter()
            .filter_map(|conjunctive_composition_string_value| {
                match conjunctive_composition_string_value.evaluate(interpretation.clone()) {
                    Some(_) => Some(conjunctive_composition_string_value.clone()),
                    None => None,
                }
            })
            .collect()
    }
}

#[pyclass]
#[derive(Clone, Hash)]
pub struct DCKeysIterable {
    disjunctive_composition_string_values: Vec<DisjunctiveCompositionKeys>,
}

#[pymethods]
impl DCKeysIterable {

    #[new]
    pub fn new(disjunctive_composition_string_values: Vec<DisjunctiveCompositionKeys>) -> Self {
        Self {
            disjunctive_composition_string_values,
        }
    }

    #[getter]
    pub fn disjunctive_composition_string_values(&self) -> PyResult<Vec<DisjunctiveCompositionKeys>> {
        Ok(self.disjunctive_composition_string_values.clone())
    }

    pub fn hash(&self) -> u64 {
        hashit(self)
    }

    pub fn evaluate(&self, interpretation: Vec<String>) -> Vec<DisjunctiveCompositionKeys> {
        self.disjunctive_composition_string_values
            .iter()
            .filter_map(|disjunctive_composition_string_value| {
                match disjunctive_composition_string_value.evaluate(interpretation.clone()) {
                    Some(_) => Some(disjunctive_composition_string_value.clone()),
                    None => None,
                }
            })
            .collect()
    }
}

/// A Python module implemented in Rust.
#[pymodule]
fn puan_pv_rs(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<Disjunction>()?;
    m.add_class::<ConjunctiveComposition>()?;
    m.add_class::<ConjunctiveCompositionKeys>()?;
    m.add_class::<CCKeysIterable>()?;
    m.add_class::<Conjunction>()?;
    m.add_class::<DisjunctiveComposition>()?;
    m.add_class::<DisjunctiveCompositionKeys>()?;
    m.add_class::<DCKeysIterable>()?;
    Ok(())
}


#[cfg(test)]
mod tests {

    use super::*;

    #[test]
    fn test() {
        
    }
}