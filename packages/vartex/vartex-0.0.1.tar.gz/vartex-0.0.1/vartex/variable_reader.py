import json
from csv import DictReader


class KeyValueReader:
    """
    A class for reading key-value pairs from a file.
    """

    def __init__(self, file_path: str, mode: str = "json"):
        """
        Initialize the KeyValueReader class.

        Args:
            file_path: The path to the file.
            mode: The file format. Defaults to "json".
        """
        self.__file_path = file_path
        self.__mode = mode

    def read(self) -> dict:
        """
        Read the variables from the file.

        Returns:
            A dictionary of variables.
        """
        if self.__mode == "json":
            return self._read_json(self.__file_path)
        elif self.__mode == "csv":
            return self._read_csv(self.__file_path)

    def _read_json(self, file_path: str) -> dict:
        """
        Read variables from a JSON file.

        Args:
            file_path: The path to the JSON file.

        Returns:
            A dictionary of variables.
        """
        with open(file_path, "r") as f:
            _object = json.load(f)

        # Ensure all lists are the same length
        n = None
        for val in _object.values():
            if type(val) != list:
                continue
            if n is None:
                n = len(val)
            elif len(val) != n:
                raise ValueError("All list values must be the same length.")

        variables = [dict() for _ in range(n)]

        for key, value in _object.items():
            # If single element, extract
            if type(value) == list and len(value) == 1:
                value = value[0]

            # If list, assign each unique value to each variable
            if type(value) == list:
                for i, val in enumerate(value):
                    variables[i][key] = val
            # If single element, assign to all
            else:
                for i in range(n):
                    variables[i][key] = value

        return variables

    def _read_csv(self, file_path: str) -> dict:
        """
        Read variables from a CSV file.

        Args:
            file_path: The path to the CSV file.

        Returns:
            A dictionary of variables.
        """
        with open(file_path, "r") as f:
            reader = DictReader(f)
            return list(reader)
