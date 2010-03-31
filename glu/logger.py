"""
Logger functions.

We don't use native Python or Java logging, since we want
to use this here as an abstraction around whatever logging
infrastructure we will have in our finished system.

"""
import sys
import datetime


# Log levels
LOG_DEBUG       = "DEBUG"
LOG_INFO        = "INFO"
LOG_WARNING     = "WARNING"
LOG_ERROR       = "ERROR"
LOG_CRITICAL    = "CRITICAL"

# Log facilities
LOGF_GLU_CORE   = "GLU_CORE"
LOGF_ACCESS_LOG = "ACCESS_LOG"
LOGF_RESOURCES  = "RESOURCES"
LOGF_BEANS      = "BEANS"

__KNOWN_LEVELS     = [ LOG_DEBUG, LOG_INFO, LOG_WARNING, LOG_ERROR, LOG_CRITICAL ]
__KNOWN_FACILITIES = [ LOGF_GLU_CORE, LOGF_ACCESS_LOG, LOGF_RESOURCES, LOGF_BEANS ]



def log(msg, level=LOG_INFO, facility=LOGF_GLU_CORE, start_time=None):
    """
    Log a message with specified log level and facility.
    
    @param msg:        The log message.
    @type  msg:        string
    
    @param level:      The log level.
    @type  level:      string
    
    @param facility:   The system facility from which the message was produced.
    @type  facility:   string
    
    @param start_time: The time at which processing of this request started.
    @type  start_time: datetime
    
    """
    if level not in __KNOWN_LEVELS  or  facility not in __KNOWN_FACILITIES:
        msg = "### Invalid level (%s) or facility (%s). Original message: %s" % (level, facility, msg)
        level    = LOG_INFO
        facility = LOGF_GLU_CORE
    if not start_time:
        start_time = datetime.datetime.now()
    timestring = start_time.isoformat()
    if facility == LOGF_ACCESS_LOG:
        facility_level = LOGF_ACCESS_LOG
    else:
        facility_level = "%s:%s" % (facility, level)
    sys.stderr.write("### %s - %s - %s\n" % (timestring, facility_level, msg))

