import os
from typing import List


class ModelsFilesManager:
    """
    Class to manage the model folder, including encoding/decoding the fields from the path
    """

    def __init__(self, root_folder: str, fields: List[str], ext: str = '.pt'):
        """
        Constructor

        Args:
            root_folder (str): all models are under this folder
            fields (List[str]): fields to encode/decode into the files names
        """
        self._root_folder = root_folder
        self._fields = fields
        self._ext = ext
        pass


    @staticmethod
    def path_escape(name: str) -> str:
        """
        Escape from path illegal chars (windows has a lot)

        Args:
            name (str): original name

        Returns:
            str: safe to use name
        """
        assert name is not None and len(name) > 0, 'Name cannot be None or empty'

        return name.replace('&', '&et;').replace('/', '&slash;').replace('\\', '&backslash;').replace('<', '&lt;').replace('>', '&gt;').replace('\"', '&quote;').replace('|', '&pipe;').replace('?', '&qest;').replace('*', '&ast;')

    @staticmethod
    def path_decode(path: str) -> str:
        """
        Decode from escaped path

        Args:
            path (str): escaped path name

        Returns:
            str: original name
        """
        assert path is not None and len(path) > 0, 'Path cannot be None'

        return path.replace('&pipe;', '|').replace('&qest;', '?').replace('&ast;', '*').replace('&quote;', '\"').replace('&gt;', '>').replace('&lt;', '<').replace('&backslash;', '\\').replace('&slash;', '/').replace('&et;', '&')

    def get_fields_values(self, path: str) -> dict:
        """
        Get the fields and values from the path.
        Ignore the folder.

        Args:
            path (str): model path

        Raises:
            Exception: on invalid path

        Returns:
            dict: fields and values (as strings)
        """
        assert path is not None and len(path) > 0, 'Path cannot be None or empty'
        assert path.endswith(self._ext), f'Path {path} does not end with {self._ext}'

        path_parts = path.split('/')
        filename = path_parts[-1][: -len(self._ext)-1]
        parts = filename.split('_')

        parts = [self.path_decode(p) for p in parts]

        if len(parts) < len(self._fields):
            raise Exception(f'Path {path} does not have all fields (expecting {self._fields})')

        return {self._fields[i]: parts[i] for i in range(len(self._fields))}

    def get_file_name(self, fields: dict) -> str:
        """
        Generate a file name from the fields

        Args:
            fields (dict): _description_

        Returns:
            str: file name
        """
        assert fields is not None, 'Fields cannot be None'
        assert len(fields) == len(self._fields), f'Missing fields. Expected {len(self._fields)}, found {len(fields)}.'

        return '_'.join([self.path_escape(fields[field]) for field in self._fields]) + '.' + self._ext

    def get_model_files(self, where = None) -> List[str]:
        """
        Get all model files from the output folder, optionally filtered by a callback

        Args:
            where (_type_, optional): Callback gets dict of fields, returns True/False. Defaults to None.

        Returns:
            List[str]: List of paths to models
        """
        res: List[str] = []
        for (root, dirs, files) in os.walk(self._root_folder, topdown=True):
            for dir in dirs:
                dirpath = os.path.join(root, dir)
                for (dirpath, dirnames, filenames) in os.walk(dirpath, topdown=True):
                    for filename in filenames:
                        if not filename.endswith('.' + self._ext):
                            continue
                        
                        if where is not None:
                            fields = self.get_fields_values(filename)
                            if not where(fields):
                                continue

                        fn = os.path.join(dirpath, filename)
                        res.append(fn)
        
        return res
