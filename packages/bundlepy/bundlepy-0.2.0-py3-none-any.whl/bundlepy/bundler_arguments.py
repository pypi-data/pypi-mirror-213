import argparse
import sys

class BundlerArguments():

    def __init__(self):
        self.parser = argparse.ArgumentParser(description="Example Argument Parser")
        self.parsed_args = None
        self._add_options()

    def _add_options(self):
        self.parser.add_argument("--app", type=str, help="Python app's entry point", required=True)
        self.parser.add_argument("--packages", nargs="+", type=str, help="List of packages", required=False)
        self.parser.add_argument("--packages-file", type=str, help="Text file which lists all needed packages", required=False)
        self.parser.add_argument("--transitive-imports-file", type=str, help="List of imports which can't be found automatically", required=False)

        self.parser.add_argument("--project-dir", type=str, help="It's only needed when bundle in cluster")
        self.parser.add_argument("--cluster-conf-file", type=str, help="Cluster configuration file", required=False)
        self.parser.add_argument("--linux", action="store_true", required=False)
        self.parser.add_argument("--osx", action="store_true", required=False)
        self.parser.add_argument("--windows", action="store_true", required=False)
        self.parser.add_argument("--all-targets", action="store_true", help="", required=False)

    def parse_arguments(self):
        self.parsed_args = self.parser.parse_args()
        if not self.parsed_args.app:
            self.parser.print_help()
            sys.exit(1)
