from d7a.support.schema import Validatable, Types

class Control(Validatable):

  SCHEMA = [{
    "is_dialog_start": Types.BOOLEAN(),
    "is_dialog_end": Types.BOOLEAN(),
    "is_ack_return_template_requested": Types.BOOLEAN(),
    "is_ack_not_void": Types.BOOLEAN(),
    "is_ack_recorded": Types.BOOLEAN(),
    "has_ack_template": Types.BOOLEAN()
  }]

  def __init__(self, is_dialog_start, is_dialog_end, is_ack_return_template_requested,
                 is_ack_not_void, is_ack_recorded):
    self.is_dialog_start = is_dialog_start
    self.is_dialog_end = is_dialog_end
    self.is_ack_return_template_requested = is_ack_return_template_requested
    self.is_ack_not_void = is_ack_not_void
    self.is_ack_recorded = is_ack_recorded
    super(Control, self).__init__()

  def __iter__(self):
    byte = 0
    if self.is_dialog_start: byte |= 1 << 7
    if self.is_dialog_end:  byte |= 1 << 6
    if self.is_ack_return_template_requested:  byte |= 1 << 3
    if self.is_ack_not_void:  byte |= 1 << 2
    if self.is_ack_recorded: byte |= 1 << 1
    yield byte