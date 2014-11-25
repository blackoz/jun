###############################################################################
#
# Copyright (c) 2011 Rainmaker Entertainment
# All Rights Reserved.
#
# This file contains unpublished confidential and proprietary
# information of Rainmaker Entertainment.  The contents of this file
# may not be copied or duplicated, in whole or in part, by any
# means, electronic or hardcopy, without the express prior
# written permission of Rainmaker Entertainment.
#
#    $HeadURL: /corp/projects/eng/jkim/workspace/rnkRig/rigWorkshop/ws_functions/logger.py
#    $Revision: 001 $
#    $Author: Jung Hun Kim $
#    $Date: 2014-10-07 
#
###
"""
======
Logger
======

Overview
========

Use this logger for all message logging within the cfxpipeline package. This
is for developer use and should not be needed from outside the package.

Features
--------

 * Logging levels allow the logging level to be set so only a certain level of
   messages are logged. For example, debug-level messages can be turned on for
   development but off by default.

 * Formatting is based on a pattern that displays important information, such as
   the module and line number where the logger was used.

 * Silences several PyQt loggers that spam the log when a .ui file is read.

 * Prevents logging from bubbling up to Maya which causes double messages


Usage
-----
Instead of using print(), use one of the logger "level" methods. The results
shown here are just examples of possible output. 

from logger import logger 

as INFO is default logger setting, DEBUG message which is lower level than 
INFO won't be output. 

def foo():
    logger.debug("this is debug message")
    logger.info("this is info message")
foo()
# rigging:INFO:<maya console> foo (5) | this is info message

to change DEBUG level, type as follow

logger.setLevel(logging.DEBUG)

and the result will show like below.

foo()
# rigging:DEBUG:<maya console> foo (4) | this is debug message
# rigging:INFO:<maya console> foo (5) | this is info message

For more advanced information see 
https://docs.python.org/2/howto/logging.html

There are other levels and options, such as *critical*, but these are rarely
used. In fact, error is rarely needed because in most cases an error should
just raise an exception, making warning the highest commonly used level.

Logging Level
`````````````
To set the level that is displayed, import the python logger module to access
the constant values::

Level     Numeric value
CRITICAL     50
ERROR        40
WARNING      30
INFO         20
DEBUG        10
NOTSET        0
"""

import logging
#import dd.QtCore   # Used at the bottom to check if this is run in Maya

LOGGER_NAME = "Rigging"  # Keep this the same as the package name

DEFAULT_LEVEL = logging.INFO

# Create a format handler for the logger
FORMAT = logging.Formatter(
"Rigging:%(levelname)s:%(module)s %(funcName)s (%(lineno)d) | %(message)s"
)


# Determine if we need to assign the handler. Only do it once to avoid
#    double messages.
add_handler = True
if LOGGER_NAME in logging.Logger.manager.loggerDict:
    add_handler = False
# end if


# Create the logger and add the handler
# Get the package name. This assumes the parent folder of this module is the
#    package root
logger = logging.getLogger(LOGGER_NAME)
if add_handler:
    stream = logging.StreamHandler()
    stream.setFormatter(FORMAT)
    logger.addHandler(stream)

# end if

# prevent logging from bubbling up to maya's logger
logger.propagate=0

# Default
logger.setLevel(DEFAULT_LEVEL)
