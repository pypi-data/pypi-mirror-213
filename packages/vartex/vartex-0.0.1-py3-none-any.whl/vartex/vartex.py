import copy
import os
import re
import uuid
import glob
import logging
from typing import Optional

from vartex.variable_reader import KeyValueReader as kvreader


class VarTex:
    def __init__(
        self,
        tex_file: str,
        variables_file: str,
        build_directory: Optional[str] = None,
        variable_format: str = "json",
    ):
        self.__build_directory = build_directory or "vartex_build"
        self.__variables = kvreader(variables_file, variable_format).read()
        self._read_tex_file(tex_file)

    @property
    def variables(self) -> list:
        """
        Get the variables.
        """
        return self.__variables

    def run(self):
        """
        Run the VarTex program.
        """
        self._make_build_dir()
        logging.info("Generating tex files...")
        self._create_pdfs()
        logging.info("Done.")
        logging.info("Cleaning up...")
        self._cleanup()
        logging.info("Done.")

    def _create_pdfs(self) -> None:
        """
        Create a tex file for each set of variables and compile them.
        """
        # Generate tex files
        for i in range(len(self.__variables)):
            # Generate tex file
            filename = self._generate_tex_file(self.__variables[i])
            logging.info(f"Generated tex file `{filename}.tex`.")
            # Compile tex file
            logging.info(f"Compiling tex file `{filename}.tex`...")
            self._compile(f"{self.__build_directory}/{filename}.tex")

    def _cleanup(self) -> None:
        """
        Clean up the build directory.
        """
        extensions = ["aux", "log", "out"]

        # Find files to delete
        files = []
        for ext in extensions:
            files.extend(glob.glob(f"{self.__build_directory}/*.{ext}"))

        # Delete files
        for file in files:
            try:
                os.remove(file)
            except OSError:
                logging.warning(f"Failed to delete file `{file}`.")
                pass

    def _generate_tex_file(self, variables: dict) -> str:
        """
        Generate a tex file with the variables replaced.

        Args:
            variables: The variables to replace.

        Returns:
            The name of the tex file that was generated.
        """
        replaced_contents = self._replace_variables(variables)

        # Generate unique filename
        filename = None
        while filename is None or os.path.exists(
            f"{self.__build_directory}/{filename}"
        ):
            filename = "vartex_" + uuid.uuid4().hex

        with open(f"{self.__build_directory}/{filename}.tex", "w") as f:
            f.write(replaced_contents)

        return filename

    def _make_build_dir(self) -> None:
        """
        Create a build directory for the project
        """

        # If the build directory already exists, generate a new one
        dir_name = self.__build_directory
        if os.path.exists(dir_name):
            logging.warning(
                f"Directory `{dir_name}` already exists, generating a new directory..."
            )

            # Generate a new directory name
            while os.path.exists(dir_name):
                dir_name = "build_" + uuid.uuid4().hex

        # Create the build directory
        os.makedirs(dir_name)
        self.__build_directory = dir_name

        logging.info(f"Created build directory `{dir_name}`.")

    def _read_tex_file(self, tex_file: str) -> None:
        """
        Read the tex file.

        Args:
            tex_file: The tex file to read.
        """
        with open(tex_file, "r") as f:
            self.__contents = f.read()

    def _replace_variables(self, variables) -> str:
        """
        Replace the variables in the tex file.

        Returns:
            The tex file as a string with the variables replaced.
        """
        return_str = copy.deepcopy(self.__contents)
        for key, value in variables.items():
            pattern = r"\\newcommand{\\" + key + r"}{(.+)}"
            return_str = re.sub(
                pattern, r"\\newcommand{\\" + key + r"}{" + value + r"}", return_str
            )
        return return_str

    def _compile(self, tex_file: str) -> None:
        """
        Compile the tex file.

        Args:
            tex_file: The filepath of the tex file to compile.
        """
        os.system(f"pdflatex -output-directory={self.__build_directory} {tex_file}")
