<p align="center">
  <img width="50%" src="./.source/_static/deepchain.png">
</p>

![PyPI](https://img.shields.io/pypi/v/deepchain-apps)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python 3.7](https://img.shields.io/badge/python-3.7-blue.svg)](https://www.python.org/downloads/release/python-360/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
![Dependencies](https://img.shields.io/badge/dependencies-up%20to%20date-brightgreen.svg)

# `deepchain-apps` package documentation

This Package provide a **cli** for creating a personnal app to deploy on the DeepChain platform.
To leverage the apps capability, take a look at the [bio-transformers](https://pypi.org/project/bio-transformers/) and [bio-datasets](https://pypi.org/project/bio-datasets) package, which provide functionnality to download biological dataset and easily use pre-trained transformers.

# 1. Technical overview

## Package modules

  1. **cli**
  2. **components**
  3. **models**
  4. **utils**
  5. **app template**


## Modules details

  1. **cli**:

      - `deepchain_cli` is the entry point to register a new command.
      - each commands correpond to a sub-module.
      - 5 commands currently register:
      - `login` : used to registered the PAT generated on deepchain settings.
      - `apps` : give informations about apps created locally.
          - located in `apps.py` sub-module
      - `create` : create a new app in specified directory.
          - located in `scaffold.py` sub-module
      - `deploy` : upload files of the created personnal app.
          - located in `deploy.py`
          - deepchain URL deployement located in `config.ini`
          - deploying at : https://api.prod.deepchain.bio
      - `download` : download an app stored in deepchain hub.
          - located in `download.py`

  2. **components**

      - sub-module used for abstract class imported in deepchain template.
      - deepchain-apps template located at: https://github.com/DeepChainBio/deep-chain-apps

```python
class DeepChainApp(ABC):
    """
    A scorer instance is used to compute the criteria value for a genotype. This class
    is a template for DeepChain App Users.
    """

    def __init__(self):
        self._checkpoint_filename = None

    @staticmethod
    @abstractmethod
    def score_names() -> List[str]:
        """score names."""

    @abstractmethod
    def compute_scores(self, sequences: List[str]) -> List[Dict[str, float]]:
        """Score a list of genotype and for each of them return descriptors and score names."""

    def get_checkpoint_path(self, root_path: str) -> str:
        """Return solve checkpoint model path
        Args:
            root_path : path of the app file launch
        Raise:
            FileExistsError if no file are found inside the checkpoint folder
        """
        checkpoint_dir = (Path(root_path).parent / "../checkpoint").resolve()
        path_filename = checkpoint_dir / self._checkpoint_filename
        if not path_filename.is_file():
            raise FileExistsError(
                f"File {self._checkpoint_filename} not found in checkpoint folder."
                f" Set 'self._checkpoint_filename = None' if file not exists"
            )
        return path_filename
```
  3. **models**

      - Provide high level interface to build Multi-layer perceptron model
      - support keras and pytorch
      - utils functions used to evaluate models

  4. **utils**

      - Stores validation functions of apps before deployement
      - Stores custom exceptions

  5. **app template**

      - deepchain-apps template located at: https://github.com/DeepChainBio/deep-chain-apps
      - create new folder when using `deepchain create myapp`
      - app structure:

      ```bash
      .
      ├── README.md # explain how to create an app
      ├── __init__.py # __init__ file to create python module
      ├── checkpoint
      │   ├── __init__.py
      │   └── Optionnal : model.pt # optional: model to be used in app must be placed there
      ├── examples
      │   ├── app_with_checkpoint.py # example: app example with checkpoint
      │   └── torch_classifier.py # example: show how to train a neural network with pre-trained embeddings
      └── src
          ├── DESC.md # Desciption file of the application
          ├── __init__.py
          ├── app.py # main application script. Main class must be names App.
          └── tags.json # file to register the tags on the hub.
      ```
# 2. CLI commands

The CLI provides 4 main commands:

- **login** : you need to supply the token provide on the plateform (PAT: personnal access token).

  ```
  deepchain login
  ```

- **create** : create a folder with a template app file

  ```
  deepchain create my_application
  ```

- **deploy** : the code and checkpoint are deployed on the plateform, you can select your app in the interface on the plateform.
  - with checkpoint upload

    ```
    deepchain deploy my_application --checkpoint
    ```

  - Only the code

    ```
    deepchain deploy my_application
    ```

- **apps** :
  - Get info on all local/upload apps

    ```
    deepchain apps --infos
    ```

  - Remove all local apps (files & config):

    ```
    deepchain apps --reset
    ```

  - Remove a specific application (files & config):

    ```
    deepchain apps --delete my_application
    ```

  - List all public apps:

    ```
    deepchain apps --public
    ```

- **download** :
  - Download locally an app deployed on deepchain hub

  ```
  deepchain download user.name@mail.com/AppName AppName
  ```


# 3. Logging

When running deepchain-apps, printed messages are entirely controles by deepchain-apps code.
The log level controls which types of log messages would be printed.

bio-transformers uses the Python module ``logging` <https://docs.python.org/3/library/logging.html>`_ to log the messages. The log level is controlled by the environment variable DEEPCHAIN_LOG_LEVEL. The levels are given in the table below. The default level is “2”.

To adjust the logging level, you can export the environment variable:

  ```bash
  export DEEPCHAIN_LOG_LEVEL=1
  ```

  | DEEPREG_LOG_LEVEL | Behavior                                                                                   |
| ----------------- | ------------------------------------------------------------------------------------------ |
| "0"               | Log all messages, equivalent to `logging.DEBUG`. Same as log level "1".                    |
| "1"               | Log all messages, equivalent to `logging.DEBUG`.                                           |
| "2"               | Log all messages except DEBUG, equivalent to `logging.INFO`. (default)                     |
| "3"               | Log all messages except DEBUG and INFO, equivalent to `logging.WARNING`.                   |
| "4"               | Log all messages except DEBUG, INFO, and WARNING, equivalent to `logging.ERROR`.           |
| "5"               | Log all messages except DEBUG, INFO, WARNING, and ERROR, equivalent to `logging.CRITICAL`. |



# License

This source code is licensed under the **Apache 2** license found in the `LICENSE` file in the root directory.
