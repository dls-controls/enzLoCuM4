from iocbuilder import Substitution
from iocbuilder.arginfo import *
from iocbuilder.modules.streamDevice import AutoProtocol

class enzLoCuM4(Substitution, AutoProtocol):
    '''A brief description for this class goes here'''

    # The __init__ method specifies arguments and defaults
    def __init__(self, device, adr, port, name = '', desc = '', gda = True):
        # If gda then define gda_name and gda_desc
        if gda:
            gda_name, gda_desc = name, desc
        else:
            gda_name, gda_desc = '', ''
        # Filter the list of local variables by the argument list,
        # then initialise the super class
        self.__super.__init__(**filter_dict(locals(), self.Arguments))

    # __init__ arguments
    ArgInfo = makeArgInfo(__init__,
        device = Simple('Description for device', str),
        adr    = Simple('Description for adr', str),
        port   = Simple('Description for port', str),
        name   = Simple('Object name, also used for gda_name if gda', str),
        desc   = Simple('Object description, also used for gda_desc if gda', str),
        gda    = Simple('Set to True to make available to gda', bool))

    # Substitution attributes
    TemplateFile = 'enzLoCuM4.template'
    Arguments = ArgInfo.Names()

    # AutoProtocol attributes
    ProtocolFiles = ['enzLoCuM4.protocol']


class simulation_enzLoCuM4(Substitution, AutoProtocol):
    '''A brief description for this class goes here'''

    # The __init__ method specifies arguments and defaults
    def __init__(self, device, adr, port):
        # Filter the list of local variables by the argument list,
        # then initialise the super class
        self.__super.__init__(**filter_dict(locals(), self.Arguments))

    # __init__ arguments
    ArgInfo = makeArgInfo(__init__,
        device = Simple('Description for device', str),
        adr    = Simple('Description for adr', str),
        port   = Simple('Description for port', str))

    # Substitution attributes
    TemplateFile = 'simulation_enzLoCuM4.template'
    Arguments = ArgInfo.Names()

    # AutoProtocol attributes
    ProtocolFiles = ['enzLoCuM4.protocol']


class enzLoCuM4Readback(Substitution):
    '''A brief description for this class goes here'''

    # The __init__ method specifies arguments and defaults
    def __init__(self, device, gda_curr_name, desc_prefix, blade_a_card, blade_a_chan, blade_b_card, blade_b_chan, blade_c_card, blade_c_chan, blade_d_card, blade_d_chan, egu, name = '', desc = '', gda = True):
        # If gda then define gda_name and gda_desc
        if gda:
            gda_name, gda_desc = name, desc
        else:
            gda_name, gda_desc = '', ''
        # Filter the list of local variables by the argument list,
        # then initialise the super class
        self.__super.__init__(**filter_dict(locals(), self.Arguments))

    # __init__ arguments
    ArgInfo = makeArgInfo(__init__,
        device        = Simple('Description for device', str),
        gda_curr_name = Simple('Description for gda_curr_name', str),
        desc_prefix   = Simple('Description for desc_prefix', str),
        blade_a_card  = Simple('Description for blade_a_card', str),
        blade_a_chan  = Simple('Description for blade_a_chan', str),
        blade_b_card  = Simple('Description for blade_b_card', str),
        blade_b_chan  = Simple('Description for blade_b_chan', str),
        blade_c_card  = Simple('Description for blade_c_card', str),
        blade_c_chan  = Simple('Description for blade_c_chan', str),
        blade_d_card  = Simple('Description for blade_d_card', str),
        blade_d_chan  = Simple('Description for blade_d_chan', str),
        egu           = Simple('Description for egu', str),
        name          = Simple('Object name, also used for gda_name if gda', str),
        desc          = Simple('Object description, also used for gda_desc if gda', str),
        gda           = Simple('Set to True to make available to gda', bool))

    # Substitution attributes
    TemplateFile = 'enzLoCuM4Readback.template'
    Arguments = ArgInfo.Names()


