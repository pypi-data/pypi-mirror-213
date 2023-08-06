import multiprocessing
import os
import shutil
import subprocess

PYPI_URL = "https://pypi.org/simple"

class VenvManager:

    def __init__(self, venv_name, packages):
        self.venv_name = venv_name
        self._create_venv()
        self.packages = packages

    def _get_activation_script_path(self):
        if os.path.exists(os.path.join(self.venv_name, 'Scripts', 'activate_this.py')):
            return os.path.join(self.venv_name, 'Scripts', 'activate_this.py')
        else:
            return os.path.join(self.venv_name, 'bin', 'activate_this.py')

    def activate_venv(self):
        with open(self._get_activation_script_path(), 'r', encoding='utf-8') as activate_script:
            exec(activate_script.read(), {'__file__': self._get_activation_script_path()})

    def _create_venv(self):
        subprocess.run(["virtualenv", self.venv_name], check=True)

    def _prepare_environment(self):
        self.activate_venv()
        subprocess.call(["pip", "install", "--index-url", PYPI_URL, "keyring"])
        for package in self.packages:
            subprocess.call(["pip", "install", package])

    def prepare_environment(self):
        if self.packages:
            preparation_process = multiprocessing.Process(target=self._prepare_environment)
            preparation_process.start()
            preparation_process.join()
