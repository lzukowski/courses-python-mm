from returns.result import safe

from dev_droga_courses.shared.service import Command, CommandHandler, Result


class CommandHandlerService(CommandHandler):
    @safe
    def __call__(self, command: Command) -> Result:
        raise NotImplementedError
