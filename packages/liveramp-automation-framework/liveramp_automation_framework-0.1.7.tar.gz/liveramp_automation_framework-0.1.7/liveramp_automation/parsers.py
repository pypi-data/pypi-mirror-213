from pytest_bdd.parsers import StepParser
import parse as base_parse

EXTRA_TYPES = {}


class parse(StepParser):
    """parse step parser."""

    def __init__(self, name, *args):
        """Compile parse expression."""
        super(parse, self).__init__(name)
        self.parser = base_parse.compile(self.name, *args, extra_types=EXTRA_TYPES)

    def parse_arguments(self, name):
        """Get step arguments.
        :return: `dict` of step arguments
        """
        return self.parser.parse(name).named

    def is_matching(self, name):
        """Match given name with the step name."""
        try:
            return bool(self.parser.parse(name))
        except ValueError:
            return False