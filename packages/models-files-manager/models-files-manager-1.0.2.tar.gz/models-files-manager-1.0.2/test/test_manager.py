import os
import tempfile
from models_files_manager.models_files_manager import ModelsFilesManager


def test_constructor():
    manager = ModelsFilesManager('root_folder', ['field1', 'field2'], 'ext')

    assert manager is not None
    assert manager._root_folder == 'root_folder'
    assert manager._fields == ['field1', 'field2']
    assert manager._ext == 'ext'

def test_get_fields_values():
    manager = ModelsFilesManager('root_folder', ['field1', 'field2'], 'ext')

    fields = manager.get_fields_values('root_folder/value1_value2.ext')

    assert fields is not None
    assert len(fields) == 2
    assert fields['field1'] == 'value1'
    assert fields['field2'] == 'value2'

    # test with more fields in name than manager - take first 2
    fields = manager.get_fields_values('root_folder/value1_value2_value3.ext')

    assert fields is not None
    assert len(fields) == 2
    assert fields['field1'] == 'value1'
    assert fields['field2'] == 'value2'

def test_get_file_name():
    manager = ModelsFilesManager('root_folder', ['field1', 'field2'], 'ext')
    file_name = manager.get_file_name({'field1': 'value1', 'field2': 'value2'})

    assert file_name is not None
    assert file_name == 'value1_value2.ext'

    manager = ModelsFilesManager('root_folder', ['field1', 'field2', 'field3'], 'ext')
    filename = manager.get_file_name({'field1': 'value1', 'field2': 'value2', 'field3': 'value3'})

    assert filename is not None
    assert filename == 'value1_value2_value3.ext'

    manager = ModelsFilesManager('root_folder', ['field1', 'field2', 'field3', 'field4', 'field5'], 'ext')
    filename = manager.get_file_name({'field1': '/', 'field2': '\\', 'field3': '.', 'field4': ' ', 'field5': '\t'})

    assert filename is not None
    fields = manager.get_fields_values(f'root_folder/{filename}')

    assert fields['field1'] == '/'
    assert fields['field2'] == '\\'
    assert fields['field3'] == '.'
    assert fields['field4'] == ' '
    assert fields['field5'] == '\t'

def test_where():    
    # create folder in temp folder
    with tempfile.TemporaryDirectory() as root:
        manager = ModelsFilesManager(root, ['field1', 'field2'], 'ext')
        fn1 = manager.get_file_name({'field1': 'value1', 'field2': 'value2'})
        fn2 = manager.get_file_name({'field1': 'value3', 'field2': 'value4'})

        # create folder
        os.makedirs(os.path.join(root, 'folder1'))
        os.makedirs(os.path.join(root, 'folder2'))
        
        with open(os.path.join(root, 'folder1', fn1), 'w') as f:
            f.write('data')

        with open(os.path.join(root, 'folder2', fn2), 'w') as f:
            f.write('data')

        files = manager.get_model_files()

        assert files is not None
        assert len(files) == 2
        assert os.path.join(root, 'folder1', fn1) in files
        assert os.path.join(root, 'folder2', fn2) in files

        files = manager.get_model_files(lambda d: d['field1'] == 'value1')

        assert files is not None
        assert len(files) == 1
        assert os.path.join(root, 'folder1', fn1) in files
        assert os.path.join(root, 'folder2', fn2) not in files

        files = manager.get_model_files(lambda d: d['field1'] == 'value3')

        assert files is not None
        assert len(files) == 1
        assert os.path.join(root, 'folder1', fn1) not in files
        assert os.path.join(root, 'folder2', fn2) in files

        files = manager.get_model_files(lambda d: d['field1'] == 'xxx')

        assert files is not None
        assert len(files) == 0
        

def test_escape_decode():
    name = 'a.b./\c&d.e_f'
    assert ModelsFilesManager.path_decode(ModelsFilesManager.path_escape(name)) == name, 'name'
    assert '/' not in ModelsFilesManager.path_escape(name), '/'
    assert '\\' not in ModelsFilesManager.path_escape(name), '\\'
