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

Define one boolean option, someopt, which defaults to false; users can
specify -s at the command line, or put someopt = true in the config
file.

.. code-block:: python

  import optini
  optini.spec.someopt.help = 'Set a flag'
  # implies -s and --someopt command line options
  desc = 'This code does a thing'
  optini.Config(appname='myapp', file=True, desc=desc)
  if optini.opt.someopt:
      print("someopt flag is set")

Config file defaults to ~/.<appname>.ini

Enable logging config:

.. code-block:: python

  import logging
  import optini
  optini.Config(appname='something', logging=True)
  # the verbose (-v) option enables info messages
  logging.info('this is an info message')
  # the debug (-d) option enables debug messages
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

__author__ = """Brendan Strejcek"""
__email__ = 'brendan@datagazing.com'
__version__ = '0.4.4'

from .optini import Config, opt, spec, section # noqa F401
