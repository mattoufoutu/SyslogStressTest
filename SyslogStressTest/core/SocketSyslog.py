__author__ = 'pyt'

import socket

LOG_EMERG		= 0		#  system is unusable
LOG_ALERT		= 1		#  action must be taken immediately
LOG_CRIT		= 2		#  critical conditions
LOG_ERR			= 3		#  error conditions
LOG_WARNING		= 4		#  warning conditions
LOG_NOTICE		= 5		#  normal but significant condition
LOG_INFO		= 6		#  informational
LOG_DEBUG		= 7		#  debug-level messages

#  facility codes
LOG_KERN		= 0		#  kernel messages
LOG_USER		= 1		#  random user-level messages
LOG_MAIL		= 2		#  mail system
LOG_DAEMON		= 3		#  system daemons
LOG_AUTH		= 4		#  security/authorization messages
LOG_SYSLOG		= 5		#  messages generated internally by syslogd
LOG_LPR			= 6		#  line printer subsystem
LOG_NEWS		= 7		#  network news subsystem
LOG_UUCP		= 8		#  UUCP subsystem
LOG_CRON		= 9		#  clock daemon
LOG_AUTHPRIV	= 10	#  security/authorization messages (private)

#  other codes through 15 reserved for system use
LOG_LOCAL0		= 16		#  reserved for local use
LOG_LOCAL1		= 17		#  reserved for local use
LOG_LOCAL2		= 18		#  reserved for local use
LOG_LOCAL3		= 19		#  reserved for local use
LOG_LOCAL4		= 20		#  reserved for local use
LOG_LOCAL5		= 21		#  reserved for local use
LOG_LOCAL6		= 22		#  reserved for local use
LOG_LOCAL7		= 23		#  reserved for local use

priority_names = {
"alert":	LOG_ALERT,
"crit":		LOG_CRIT,
"debug":	LOG_DEBUG,
"emerg":	LOG_EMERG,
"err":		LOG_ERR,
"error":	LOG_ERR,		#  DEPRECATED
"info":		LOG_INFO,
"notice":	LOG_NOTICE,
"panic": 	LOG_EMERG,		#  DEPRECATED
"warn":		LOG_WARNING,		#  DEPRECATED
"warning":	LOG_WARNING,
}

facility_names = {
"auth":		LOG_AUTH,
"authpriv":	LOG_AUTHPRIV,
"cron": 	LOG_CRON,
"daemon":	LOG_DAEMON,
"kern":		LOG_KERN,
"lpr":		LOG_LPR,
"mail":		LOG_MAIL,
"news":		LOG_NEWS,
"security":	LOG_AUTH,		#  DEPRECATED
"syslog":	LOG_SYSLOG,
"user":		LOG_USER,
"uucp":		LOG_UUCP,
"local0":	LOG_LOCAL0,
"local1":	LOG_LOCAL1,
"local2":	LOG_LOCAL2,
"local3":	LOG_LOCAL3,
"local4":	LOG_LOCAL4,
"local5":	LOG_LOCAL5,
"local6":	LOG_LOCAL6,
"local7":	LOG_LOCAL7,
}

class SocketSyslog():
    def __init__(self, address='/dev/log'):
        self.address = address
        self.log_format_string = '<%d>%s\000'
        if type(address) == type(''):
            self.socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            self.socket.connect(address)
            self.unix = 1
        else:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.unix = 0

    def log(self, message, facility=LOG_USER, priority=LOG_INFO):
        message = self.log_format_string % (
            self.encode_priority(facility, priority),
            message
        )
        if self.unix:
            self.socket.send(message)
        else:
            self.socket.sendto(message, self.address)

    def encode_priority(self, facility, priority):
        if type(facility) == type(''):
            facility = facility_names[facility]
        if type(priority) == type(''):
            priority = priority_names[priority]
        return (facility<<3) | priority

    def close(self):
        if self.unix:
            self.socket.close()