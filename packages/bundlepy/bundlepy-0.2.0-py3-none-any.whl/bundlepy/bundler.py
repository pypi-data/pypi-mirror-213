import glob
import os
import shutil
import subprocess
import tempfile

BUNDLER_APP = "pyinstaller"

from bundlepy.venv_manager import VenvManager

class Bundler():

    def __init__(self, app_name, packages, transitive_imports=[], additional_args=[]):
        self.app_name = app_name
        self.packages = packages
        self.curr_dir = os.getcwd()
        self.temp_dir = tempfile.mkdtemp()
        os.chdir(self.temp_dir)
        self.venv = VenvManager("exe_env", packages)
        os.chdir(self.curr_dir)
        self.transitive_imports = transitive_imports or []
        self.additional_args = additional_args or []

    def __del__(self):
        os.chdir(self.curr_dir)
        shutil.rmtree(self.temp_dir)

    def bundle_app(self):
        os.chdir(self.temp_dir)
        self.venv.prepare_environment()
        self.venv.activate_venv()
        bundle_command = [BUNDLER_APP, "--onefile", "--noconfirm"]
        bundle_command += self._get_needed_packages_addition_arguments()
        bundle_command += self._get_transitive_imports()
        bundle_command += [self.app_name]
        subprocess.run(bundle_command)
        if os.path.exists(os.path.join(self.curr_dir, "dist")):
            shutil.rmtree(os.path.join(self.curr_dir, "dist"))
        shutil.move("dist", self.curr_dir)

    def _get_needed_packages_addition_arguments(self):
        additional_packages = []
        site_packages = glob.glob("**/site-packages", recursive=True)[0]
        for packages in self.packages:
            if packages.endswith(".py"):
                package_with_seperator = f"{packages}{os.pathsep}."
            else:
                package_with_seperator = f"{packages}{os.pathsep}{packages}"
            lib_path = os.path.join(site_packages, package_with_seperator)
            if os.path.exists(lib_path):
                additional_packages += ["--add-data", os.path.join(site_packages, package_with_seperator)]
        return additional_packages

    def _get_transitive_imports(self):
        transitive_imports = ["--hidden-import", "__future__"]
        for transitive_import in self.transitive_imports:
            transitive_imports += ["--hidden-import", transitive_import]
        return transitive_imports