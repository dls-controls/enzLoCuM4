from iocbuilder import AutoSubstitution
from iocbuilder.arginfo import *
from iocbuilder.modules.streamDevice import AutoProtocol

class enzLoCuM4(AutoSubstitution, AutoProtocol):
    TemplateFile = 'enzLoCuM4.template'
    ProtocolFiles = ['enzLoCuM4.protocol']
