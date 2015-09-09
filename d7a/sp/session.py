# Session States
# author: Christophe VG <contact@christophe.vg>

# class implementation of (FIFO) configuration

class States(object):
  IDLE    = 0  # Inactive Session
  DORMANT = 1  # The group of Requests needs to be executed within a timeout 
               # period, which has not expired. After completion of the 
               # period, the Dormant Session is transformed into Pending 
               # Session.
  PENDING = 2  # The group of Requests needs to be executed as soon as 
               # possible.
  ACTIVE  = 3  # The Session is being currently executed using the D7A 
               # Session Protocol.
  DONE    = 4  # Terminated Session

  ALL     = [ IDLE, DORMANT, PENDING, ACTIVE, DONE ]

  SCHEMA  = { "type": "integer", "allowed" : ALL }
