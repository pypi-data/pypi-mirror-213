# ------- start -------
from confattr import ConfigFileCommand
from confattr.configfile import Include
ConfigFileCommand.delete_command_type(Include)
# ------- end -------

from confattr import Message
_original_Message_str = Message.__str__
Message.__str__ = Message.format_msg_line  # type: ignore [method-assign]

from utils import run
run('example.py', nextto=__file__)

Message.__str__ = _original_Message_str  # type: ignore [method-assign]
