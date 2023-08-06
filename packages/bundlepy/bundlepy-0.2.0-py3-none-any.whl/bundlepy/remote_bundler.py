import base64
import json
import os
import shutil
import tempfile
import zipfile

from datetime import datetime

import requests

class RemoteBundler:

    def __init__(self, project_dir, packages, transitive_imports, entry_point, cluster_conf_file=None):
        self.cluster_conf_file = cluster_conf_file
        self.project_dir = project_dir
        self.packages = packages
        self.transitive_imports = transitive_imports
        self.entry_point = entry_point
        self.win_servers = None
        self.linux_servers = None
        self.osx_servers = None
        self._parse_servers()

    def _parse_servers(self):
        if not self.cluster_conf_file:
            self.cluster_conf_file = os.path.join(os.path.dirname(__file__), "config", "cluster_conf.json")
        if os.path.exists(self.cluster_conf_file):
            with open(self.cluster_conf_file, "r") as cluster_conf:
                servers = json.load(cluster_conf)
            self.win_servers = servers.get("windows_servers", None)
            self.linux_servers = servers.get("linux_servers", None)
            self.osx_servers = servers.get("osx_servers", None)

    def _compress_project_path(self):
        tmp_dir = tempfile.mkdtemp()
        shutil.copytree(self.project_dir, os.path.join(tmp_dir, os.path.basename(self.project_dir)))
        directory_path = os.path.join(tmp_dir, os.path.basename(self.project_dir))
        self.zip_path = os.path.join(os.getcwd(), f"{os.path.basename(self.project_dir)}.zip")
        with zipfile.ZipFile(self.zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(directory_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    zipf.write(file_path, os.path.relpath(file_path, directory_path))
        shutil.rmtree(tmp_dir)

    def _get_host_request(self, host_type):
        if host_type == "windows" and self.win_servers:
                return f"{self.win_servers[0].get('protocol')}://{self.win_servers[0].get('ip')}:{self.win_servers[0].get('port')}"
        elif host_type == "osx" and self.osx_servers:
            return f"{self.osx_servers[0].get('protocol')}://{self.osx_servers[0].get('ip')}:{self.osx_servers[0].get('port')}"
        elif host_type == "linux" and self.linux_servers:
            return f"{self.linux_servers[0].get('protocol')}://{self.linux_servers[0].get('ip')}:{self.linux_servers[0].get('port')}"
        print(f"No {host_type} servers are found in config. Use --cluster-conf-file flag to use custom configuration")
        sys.exit(1)

    def _create_dist_dir(self, exe_name, exe_data, os_type):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        directory_name = f"{timestamp}-{os_type}"
        os.mkdir(directory_name)
        with open(os.path.join(directory_name, exe_name), "wb") as exe:
            content = base64.b64decode(exe_data)
            exe.write(content)

    def bundle_app(self, os_type):
        self._compress_project_path()
        with open(self.zip_path, "rb") as example:
            project_file = base64.b64encode(example.read()).decode("utf-8")
        headers = {"Content-Type": "application/json"}
        data = {"packages": self.packages, "transitive_imports": self.transitive_imports, "entry_point": self.entry_point,
                "project_file": project_file, "project_name": os.path.basename(self.zip_path)}

        host_url = self._get_host_request(os_type)
        res = requests.post(f"{host_url}/bundle", headers=headers, json=data)
        self._create_dist_dir(os.path.splitext(self.entry_point)[0], json.loads(res._content)["file"], os_type)
        os.unlink(self.zip_path)
