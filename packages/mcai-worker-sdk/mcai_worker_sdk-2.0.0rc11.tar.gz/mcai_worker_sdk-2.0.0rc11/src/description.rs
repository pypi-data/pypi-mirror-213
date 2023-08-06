use mcai_worker_sdk::prelude::*;
use pyo3::{pyclass, pymethods, PyAny, PyResult};
use pyproject_toml::PyProjectToml;

/// Description of the worker. The fields are automatically bound to the information contained in the pyproject.toml file when instantiating the class.
///
/// Arguments:
///   package_name (str): The name of the package.
///
/// Examples:
///   >>> desc = mcai.WorkerDescription(__package__)
#[pyclass(subclass)]
#[pyo3(text_signature = "(package_name)")]
#[derive(Clone, Debug, Default)]
pub struct WorkerDescription {
  /// Name of the worker.
  ///
  /// Bound to the field `name <https://peps.python.org/pep-0621/#name>`_ of the pyproject.toml.
  #[pyo3(get, set)]
  name: String,
  /// Version of the worker.
  ///
  /// Bound to the field `version <https://peps.python.org/pep-0621/#version>`_ of the pyproject.toml.
  #[pyo3(get, set)]
  version: String,
  /// Description of the worker.
  ///
  /// Bound to the field `description <https://peps.python.org/pep-0621/#description>`_ of the pyproject.toml.
  #[pyo3(get, set)]
  description: String,
  /// License of the worker.
  ///
  /// Bound to the field `license <https://peps.python.org/pep-0621/#license>`_ of the pyproject.toml.
  #[pyo3(get, set)]
  license: String,
}

#[pymethods]
impl WorkerDescription {
  #[new]
  fn new(package: &PyAny) -> PyResult<WorkerDescription> {
    if package.is_none() {
      // This means the worker hasn't been packaged and we need to get info through pyproject.toml

      let content = std::fs::read_to_string("./pyproject.toml")
        .map_err(|error| {
          format!(
            "Python Worker must be described by a 'pyproject.toml' file: {}",
            error
          )
        })
        .unwrap();

      let pyproject = PyProjectToml::new(&content)
        .map_err(|error| format!("Could not parse 'pyproject.toml' file: {}", error))
        .unwrap();

      let project = pyproject
        .project
        .expect("The 'pyproject.toml' must contain a 'project' section.");

      Ok(Self {
        name: project.name,
        version: project
          .version
          .expect("Version field must be present in pyproject.toml"),
        description: project.description.unwrap_or_default(),
        license: project
          .license
          .expect("License field must be present in pyproject.toml")
          .text
          .unwrap_or_default(),
      })
    } else {
      let py = package.py();

      let importlib_metadata = py.import("importlib.metadata")?;
      let package_info = importlib_metadata.getattr("metadata")?.call1((package,))?;

      Ok(Self {
        name: package_info.get_item("name")?.to_string(),
        version: package_info.get_item("version")?.to_string(),
        description: package_info.get_item("summary")?.to_string(),
        license: package_info.get_item("license")?.to_string(),
      })
    }
  }
}

impl McaiWorkerDescription for WorkerDescription {
  fn get_name(&self) -> String {
    self.name.clone()
  }

  fn get_description(&self) -> String {
    self.description.clone()
  }

  fn get_version(&self) -> Version {
    Version::parse(&self.version).expect(
      "unable to parse version (please use SemVer format) and specify it in your pyproject.toml",
    )
  }

  fn get_license(&self) -> McaiWorkerLicense {
    McaiWorkerLicense::new(&self.license)
  }
}

#[test]
fn test_worker_description() {
  use pyo3::marker::Python;

  pyo3::prepare_freethreaded_python();
  let worker_description =
    Python::with_gil(|py| WorkerDescription::new(Python::None(py).as_ref(py)).unwrap());

  assert_eq!(
    worker_description.get_description(),
    env!("CARGO_PKG_DESCRIPTION")
  );
  assert_eq!(
    worker_description.get_license(),
    McaiWorkerLicense::new(env!("CARGO_PKG_LICENSE"))
  );

  assert_eq!(
    worker_description.get_version(),
    Version::parse(env!("CARGO_PKG_VERSION")).unwrap()
  );

  #[cfg(feature = "media")]
  assert_eq!(
    format!("py_{}", worker_description.get_name()),
    format!("{}_media", env!("CARGO_PKG_NAME"))
  );

  #[cfg(not(feature = "media"))]
  assert_eq!(
    format!("py_{}", worker_description.get_name()),
    env!("CARGO_PKG_NAME")
  );
}
