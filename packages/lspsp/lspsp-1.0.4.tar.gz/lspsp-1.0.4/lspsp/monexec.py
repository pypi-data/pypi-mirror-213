import argparse
from lspsp.executable import Executable
from lspsp.lspmon import Lspmon


class MonitorExecutable(Executable):
    def parse(self):
        parser = argparse.ArgumentParser(
            description='LSPSP Monitor Executable.')
        cmd_parser = parser.add_subparsers(dest='cmd', help="Command Options")
        cmd_parser.add_parser(
            'run', help='Run Monitor Service.')
        cmd_parser.add_parser(
            'test', help='Run Notification Test.')
        self._parser = parser
        self._args = parser.parse_args()

    def run(self):
        lspmon = Lspmon(1)
        lspmon.launch()

    def test(self):
        lspmon = Lspmon(0)
        lspmon.launch()

    def execute(self):
        if self._args.cmd == 'run':
            self.run()
        elif self._args.cmd == 'test':
            self.test()
        else:
            self._parser.print_help()
