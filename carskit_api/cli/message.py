from cliff.command import Command
import logging


class Message(Command):
    """A basic command"""

    def get_parser(self, prog_name):
        """Message argument parsing."""
        parser = super(Message, self).get_parser(prog_name)
        group = parser.add_mutually_exclusive_group()

        group.add_argument(
            "--lowercase",
            help="print result in lower case",
            action="store_true",
        )

        group.add_argument(
            "--uppercase",
            help="print result in upper case",
            action="store_true",
        )

        return parser

    def take_action(self, parsed_args):
        """Command action"""
        result = "Hello World!"

        if parsed_args.lowercase:
            return result.lower()

        if parsed_args.uppercase:
            return result.upper()

        return result
