# Models Files Manager

The Models Files Manager is a simple tool that helps you keep track of saved models (PyTorch/Keras/Onnx/etc.) saved on the hard drive. You can set up a number of fields, that will get encoded into the file names, and query the files saved.

The Models Files Manager helps you avoid illegal chars in the paths, and easily retrive saved files for loading.

## Installation

You can install the Models Files Manager from [PyPI](https://pypi.org/project/models-files-manager/):

    python -m pip install models-files-manager

The manager is supported and tested on Python 3.8 and above.

## How to use

To use the Models Files Manager, in your own Python code, by importing from the `models_files_manager` package:

    >>> from models_files_manager import ModelsFilesManager
    >>> manager = ModelsFilesManager(root, ['field1', 'field2'], 'ext')
    >>> models_file_names = manager.get_model_files(lambda d: d['field1'] == 'value1')

Or to create a new file name:

    >>> from models_files_manager import ModelsFilesManager
    >>> manager = ModelsFilesManager(root, ['field1', 'field2'], 'ext')
    >>> file_name = manager.get_file_name({'field1': 'value1', 'field2': 'value2'})

Or get the field values of a specific model, from the path:

    >>> from models_files_manager import ModelsFilesManager
    >>> manager = ModelsFilesManager(root, ['field1', 'field2'], 'ext')
    >>> fields = manager.get_fields_values('model file name')
    >>> print(fields['field1'])

To directly encode/decode into strings to a path-safe format:
    
    >>> from models_files_manager import ModelsFilesManager
    >>> safe_string = ModelsFilesManager.path_escape(string)
    >>> orig_string = ModelsFilesManager.path_decode(safe_string)

Free to use in any way, open source or commercial - see attached license.

Happy training!
Ram Nathaniel, 2023
