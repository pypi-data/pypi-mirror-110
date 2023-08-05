"""
Class to get options from command line and config file

Features
--------

- Aggressively conventional defaults
- Collect configuration from command line, config file, and defaults
    - Configuration hierarchy: command line > config file > defaults
- Interface is a module-level variable: optini.opt
    - Module-level interface allows libraries to access config
- Access config options through module-level dotmap interface
    - Example: optini.opt.verbose
- Derives command line options from option names
    - Example: "verbose" => -v and --verbose
- Single flag to support (mostly) conventional logging options
    - (-v, -d, -q, -L, -F LOGFILE)
- Single flag to support I/O options (-i input and -o output)
- Supports top-level ini section without a header
- Uses standard libraries under the hood (logging, argparse, configparser)

Limitations
-----------

- Only top-level code (such as UI script) should initialize Config

Examples
--------

Defines one boolean option, someopt, which defaults to false; users can
specify -s at the command line, or put someopt = true in the config
file. Config file defaults to ~/.<appname>.ini

.. code-block:: python

  import optini
  optini.spec.someopt.help = 'Set a flag'
  # implies -s and --someopt command line options
  desc = 'This code does a thing'
  optini.Config(appname='myapp', file=True, desc=desc)
  if optini.opt.someopt:
      print("someopt flag is set")

Enable logging config:

.. code-block:: python

  import logging
  import optini
  confobj = optini.Config(appname='something', logging=True)
  # the verbose (-v) option enables info messages
  logging.info('this is an info message')
  # the debug (-d) option enables info messages
  logging.debug('this is a debug message')
  # the Log (-L) option writes logs to file (default: <appname>.log)

Option Specification Format
---------------------------

- Nested data structure (either dict or dotmap is valid)
- The top level key is the option name
- To configure each option, specify second level keys:
    - help : str, default=None
        - for argparse usage message, default config file comments
    - type : type, default=bool
        - type hint for parsers
        - Supported: bool, str, int, float
    - default, default=None
        - the default value for the option
    - required, default=False
        - Declare the option mandatory at the command line
    - short : str
        - Short form command line option (example: -v)
    - long : str
        - Long form command line option (example: --verbose)
    - configfile : bool
        - Specify False for command line only options
- Second level keys, apart from configfile, are passed to argparse
"""

import argparse
import configparser
import copy
import logging
import os
import pathlib
import sys

import attr
import dotmap

myself = pathlib.Path(__file__).stem

# configure library-specific logger
logger = logging.getLogger(myself)
logging.getLogger(myself).addHandler(logging.NullHandler())

########################################################################

# public module-level variables: spec, unparsed, opt, section
# section is currently not implemented

spec = dotmap.DotMap()
"""Empty dotmap object for ease of initialization"""

opt = dotmap.DotMap(_unparsed=None)
"""
opt : dotmap.DotMap
Global data structure storing top-level config options

Example ini config file::

  top_level_option = topthing

  [some_section]
  secondary_option = something

Results in opt being defined as::

  DotMap(top_level_option='topthing')

To access::

  print(optini.opt.top_level_option)
"""

section = dotmap.DotMap()
"""
Note: not supported yet

section : dotmap.DotMap
Global data structure storing secondary config options (ini section)

Example ini config file::

  top_level_option = something

  [some_section]
  secondary_option = something

Results in secion being defined as::

  DotMap(some_section=DotMap(secondary_option='something'))

To access::

  print(optini.section.some_section.secondary_option)
"""

# private module-level variables

_lock = None
"""Only main user interface code should initialize config"""

_LOGGINGSPEC = {
    # verbose corresponds to INFO log level
    'verbose': {
        'help': 'report performed actions',
    },
    'debug': {
        'help': 'report planned actions and diagnostics',
    },
    'quiet': {
        'help': 'avoid all non-error console output',
    },
    'Log': {
        'help': 'log output to logfile (see File4log option)',
    },
    'File4log': {
        'type': str,
        'help': 'log file',
        'default': 'optini.log',
    },
}

_IOSPEC = dotmap.DotMap()
_IOSPEC.input.type = argparse.FileType('r')
_IOSPEC.input.default = sys.stdin
_IOSPEC.input.help = 'input file'
_IOSPEC.output.type = argparse.FileType('w')
_IOSPEC.output.help = 'output file'
_IOSPEC.output.default = sys.stdout

########################################################################

# helper functions


def log_spec(spec):
    """Procedure to log contents of spec, one message per item"""
    for optname, optconfig in spec.items():
        logger.debug(f"option: {optname}")
        [logger.debug(f"  {k} = {v}") for k, v in optconfig.items()]


########################################################################


@attr.s(auto_attribs=True)
class Config:
    """
    Class to get options from command line and config file

    - Configuration hierarchy: command line > config file > defaults
    - Interface is a module-level variable: optini.opt
    - Access specific config options using DotMap attributes
        - Example: optini.opt.verbose
    - Config derives command line options from option names
        - Example: "verbose" => -v and --verbose

    Examples
    --------

    .. code-block:: python

      import optini
      import dotmap
      spec = dotmap.DotMap()
      spec.someopt.help = 'Set a flag'
      # implies -s and --someopt command line options
      confobj = optini.Config(spec=spec, file=True)
      if optini.opt.someopt:
          print("someopt flag is set")

    This defines one boolean option, someopt, which defaults to false;
    users can specify -s at the command line, or put someopt = true in
    the config file.

    Attributes
    ----------

    appname : str
        Application identifier (required)
    description : str
        If not None, optini will use this in argparse usage message
    desc : str
        Alias for description
    file : bool (default: False)
        Enable config file
    filename : str (default: <appname>.ini)
        If provided, optini will use this file as config file
    logging : bool (default: False)
        Incorporate logging config, with (mostly) conventional options
            (-v, -d, -q, -L, -F LOGFILE)
    io : bool (default: False)
        Incorporate file input/output with conventional options
            (-i inputfile, -o outputfile; defaults: stdin/stdout)
    skeleton : bool (default: True)
        Create default config file if using config files
    spec : dotmap.DotMap or dict
        Mapping of option names to option configuration

    Option Specification Format
    ---------------------------

    - Specify options by passing a dict of dicts (the spec attribute)
    - The top level key is the option name
    - optini recognizes the following second-level keys:
        - help : str
            - for argparse usage message, default config file comments
        - type : type
            - type hint for parsers (default is bool)
        - default
            - the default value for the option
        - configfile : bool
            - Specify False for command line only options
        - short : str
            - Short form command line option (example: -v)
        - long : str
            - Long form command line option (example: --verbose)

    Logging
    -------

    Config has special support for configuring the standard logging
    module using several (mostly) conventional options controlling
    logs and verbosity (-v, -d, -q, -L and -F). Note: 'verbose' (-v)
    corresponds to the INFO log level. The default log file name is
    <appname>.log

    .. code-block:: python

      import optini
      confobj = optini.Config(appname='something', logging=True)

    """
    appname: str
    description: str = None
    # use desc as the canonical value
    desc: str = None
    file: bool = False
    filename: str = None
    io: bool = False
    logging: bool = False
    skeleton: bool = True
    spec: bool = None

    def __attrs_post_init__(self):
        global _lock
        if _lock is not None:
            logger.warning('configuration already initialized')
            logger.warning('only top-level module should initialize config')
            logger.warning(f"lock held by {_lock}")
            logger.warning('cowardly refusing to proceed')
            return
        _lock = self.appname
        self.desc = self.description if self.description else self.desc
        self._set_spec()
        # prepare option specification
        self._update_loggingspec()
        self._set_optspec()
        # set configuration from defaults, then config file, then arguments
        self._set_config_defaults()
        self._parse_config_file()
        self._parse_args()
        self._merge()
        self._configure_logging()

    def _set_spec(self):
        """Default to module-level spec variable for input"""

        # this streamlines user config (no need to import dotmap module)
        # for example:
        # import optini
        # optini.spec.path.type = str
        # optini.spec.path.help = 'File search path'
        # confobj = optini.Config(file=True)
        if self.spec is None:
            logger.debug('no spec provided, using module-level spec')
            self.spec = spec
            log_spec(self.spec)

    def _configure_logging(self):
        if not self.logging:
            return

        # numeric log levels, according to logging module:
        # CRITICAL 50, ERROR 40, WARNING 30, INFO 20, DEBUG 10, NOTSET 0

        # by default, only show warning and higher messages
        loglevel = logging.WARNING
        if opt.verbose:
            loglevel = min(loglevel, logging.INFO)
        if opt.debug:
            loglevel = min(loglevel, logging.DEBUG)

        handlers = []
        if not opt.quiet:
            handlers.append(logging.StreamHandler())
        if opt.Log:
            handlers.append(logging.FileHandler(opt.File4log))

        # yyy use a different format for optini logs
        format = f"{self.appname}: %(levelname)s: %(message)s"

        logging.basicConfig(
            level=loglevel,
            handlers=handlers,
            format=format,
        )

        if opt.Log:
            logger.info(f"logging to {opt.File4log}")

    def skeleton_configfile(self):
        'Generate sample config file showing default values'

        contents = []
        contents.append(f"# {self.appname} configuration file\n")
        for option in self._optspec:
            # ignore options marked as not for config file
            if 'configfile' in self._optspec[option]:
                if not self._optspec[option].configfile:
                    continue
            lhs = option
            if 'default' in self._optspec[option]:
                if type(self._optspec[option].default) is bool:
                    rhs = str(self._optspec[option].default).lower()
                else:
                    rhs = self._optspec[option].default
            else:
                if self._optspec[option].type is bool:
                    rhs = 'false'
                else:
                    rhs = "''"
            if 'help' in self._optspec[option]:
                contents.append(f"# {self._optspec[option].help}")
            contents.append(f"#{lhs} = {rhs}\n")
        return('\n'.join(contents))

    def merge_spec(self, spec):
        """
        Procedure to add option specifications

        - On option name clash, new options override old options
        - This procedure also adds various defaults

        Parameters
        ----------

        spec : dotmap.DotMap or dict
            Option specification
        """

        if not type(spec) in {dict, dotmap.DotMap}:
            logger.warning('expecting dict or dotmap.DotMap')
            logger.warning(f"ignoring option specification: {spec}")
            return

        # convert spec to a DotMap object if necessary
        spec = dotmap.DotMap(spec)
        # process this spec then merge it in at the end of procedure

        for optname, optconfig in dotmap.DotMap(spec).items():
            # create a new object to iterate over
            # this allows updating the original
            logger.debug(f"merge_spec: processing option spec {optname}")

            # set default type
            if 'type' not in optconfig:
                # default type is bool (for option flags)
                spec[optname].type = bool

            # set default action and default value
            # make sure to reference the potentially updated spec
            # (rather than the optconfig set in the current iteration)
            if spec[optname].type is bool:
                if 'action' not in optconfig:
                    spec[optname].action = 'store_true'
                    # 'count' would be another reasonable possibility
                if 'default' not in optconfig:
                    spec[optname].default = False
            else:
                if 'default' not in optconfig:
                    spec[optname].default = None

            logger.debug('processed option specification, prior to merge:')
            log_spec(spec)
        self._optspec.update(spec)

    def _update_loggingspec(self):
        'Procedure to update logging defaults with runtime info'

        # updating _LOGGINGSPEC depends on appname
        # appname is only known at runtime
        logfile = f"{self.appname}.log"
        _LOGGINGSPEC['File4log'] = {
            'type': str,
            'help': f"Log file (default: {logfile})",
            'default': f"{logfile}",
        }

    def _set_optspec(self):
        'determine and augment option specification'
        # option specification, DotMap form
        # we will iterate over self.spec to create this
        self._optspec = dotmap.DotMap()

        self.merge_spec(self.spec)
        if self.logging:
            self.merge_spec(_LOGGINGSPEC)
        if self.io:
            self.merge_spec(_IOSPEC)

    def _set_config_defaults(self):
        'Procedure to set default option values based on spec'

        logger.debug('setting option value defaults')
        for optname, optconfig in self._optspec.items():
            # after _set_optspec(), all items should have a default
            opt[optname] = optconfig.default
        logger.debug('final default option values:')
        [logger.debug(f"  {k} = {v}") for k, v in opt.items()]

    def _parse_config_file(self):
        """Procedure to parse config file, if config files are enabled"""

        # initialize config file parser even if config file is not enabled
        # this is so iteration works without issue in the merge code
        self._configparser = configparser.ConfigParser(allow_no_value=True)

        if not self.file:
            logger.debug('config files not enabled')
            return

        if self.filename is None:
            # default config file = $HOME/.<appname>.ini
            home = os.environ['HOME']
            self.filename = f"{home}/.{self.appname}.ini"
            logger.debug(f"config file = {self.filename}")
        if self.skeleton:
            if not os.path.exists(self.filename):
                # create a skeleton config file
                logger.debug(f"no such file: {self.filename}")
                logger.debug('creating skeleton config file')
                open(self.filename, 'w').write(self.skeleton_configfile())
        with open(self.filename) as f:
            # support options without an ini section header
            # to do this, prepend an implicit default [optini] section
            config_file_content = f"[optini]\n{f.read()}"
        self._configparser.read_string(config_file_content)

        # also save variables defined in all config file subsections
        # subsection variables are not added to default global opt variable
        # instead, subsection variables can be accessed through section
        # subsections are useful for libraries etc.
        # all values are collected (not limited to optspec)
        global section
        for sectname in self._configparser.sections():
            for optname in self._configparser.options(sectname):
                logger.debug(f"self.filename: [{sectname}] {optname}")
                # yyy might need to do something to get typed options
                section[sectname][optname] = section.get(optname)

    def _parse_args(self):
        """Procedure to populate self._args from command line arguments"""

        parser = argparse.ArgumentParser(description=self.desc)

        # derive add_argument kwargs from option specification
        for optname, optconfig in self._optspec.items():
            kwargs = copy.deepcopy(optconfig)
            # ignore invalid argparse keys
            # (these keys are added optini functionality)
            kwargs.pop('configfile')
            kwargs.pop('type')

            # short and long need to be here, because:
            # - they are not argpase keys like 'action' or 'help'
            # - instead, they are passed as separate initial arguments

            # short option form defaults to first character of option name
            if 'short' in kwargs:
                short = kwargs.pop('short')
            else:
                short = f"-{optname[0:1]}"

            # long option form defaults to --option name
            if 'long' in kwargs:
                long = kwargs.pop('long')
            else:
                long = f"--{optname}"

            # at this point kwargs is optconfig minus custom keys
            parser.add_argument(long, short, **kwargs.toDict())

        # argparse returns (Namespace, list)
        parsed_args, unparsed_args = parser.parse_known_args()
        # save any remaining, unparsed command line arguments
        opt._unparsed = unparsed_args

        self._args = dotmap.DotMap(vars(parsed_args))

    def _merge(self):
        """Merge command line, config file, and default options"""

        # for each option in the specification, check config file then args
        for optname, optconfig in self._optspec.items():
            logger.debug('merging in options from config file')
            # override defaults with values from config file
            if self.file:
                # 'optini' is the default implicit section name
                section = self._configparser['optini']
                if optname in section:
                    # ignore options marked as not for config file
                    if 'configfile' in optconfig:
                        if not optconfig.configfile:
                            continue

                    if optconfig.type is str:
                        opt[optname] = section.get(optname)
                    elif optconfig.type is int:
                        opt[optname] = section.getint(optname)
                    elif optconfig.type is float:
                        opt[optname] = section.getfloat(optname)
                    elif optconfig.type is bool:
                        opt[optname] = section.getboolean(optname)
                    else:
                        logger.warning('unable to process config file opt')
                        logger.warning(f"specific issue: {optname}")

            logger.debug('merging in options from command line')
            # override defaults, config file values with command line args
            if optname in self._args and self._args[optname] is not None:
                if self._optspec[optname].type is int:
                    # attempt to convert value to int
                    try:
                        opt[optname] = int(self._args[optname])
                    except ValueError:
                        logger.warning('command line option type issue')
                        logger.warning(f"option type mismatch: {optname}")
                        logger.warning('ignoring type hint: int')
                        logger.warning(f"treating {optname} as str")
                        logger.debug(f"option spec: {self._optspec[optname]}")
                        opt[optname] = self._args[optname]
                if self._optspec[optname].type is float:
                    # attempt to convert value to float
                    try:
                        opt[optname] = float(self._args[optname])
                    except ValueError:
                        logger.warning('command line option type issue')
                        logger.warning(f"option type mismatch: {optname}")
                        logger.warning('ignoring type hint: float')
                        logger.warning(f"treating {optname} as str")
                        logger.debug(f"option spec: {self._optspec[optname]}")
                        opt[optname] = self._args[optname]
                else:
                    # argparse can handle string and boolean
                    opt[optname] = self._args[optname]

    def __str__(self):
        ret = [f"options from config file ({self.filename}):"]
        for sectname in self.configparser.sections():
            ret.append(f"config file section: {sectname}")
            for option in self.configparser.options(sectname):
                optval = self.configparser.get(sectname, option)
                ret.append(f"  {option} = {optval}")
        ret.append("\noptions from command line:")
        ret.append(str(self._args))
        ret.append("\nconfigured options:")
        ret.append(str(self.opt))
        return("\n".join(ret))
