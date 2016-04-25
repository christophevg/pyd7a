from d7a.support.schema import Validatable, Types

class Control(Validatable):

  SCHEMA = [{
    "is_dialog_start": Types.BOOLEAN(),
    "is_dialog_end": Types.BOOLEAN(),
    "is_ack_return_template_requested": Types.BOOLEAN(),
    "should_respond_only_if_ack_return_template_not_empty": Types.BOOLEAN(),
    "is_ack_recorded": Types.BOOLEAN(),
    "has_ack_template": Types.BOOLEAN()
  }]

  def __init__(self, is_dialog_start, is_dialog_end, is_ack_return_template_requested,
                 should_respond_only_if_ack_return_template_not_empty, is_ack_recorded, has_ack_template):
    self.is_dialog_start = is_dialog_start
    self.is_dialog_end = is_dialog_end
    self.is_ack_return_template_requested = is_ack_return_template_requested
    self.should_respond_only_if_ack_return_template_not_empty = should_respond_only_if_ack_return_template_not_empty
    self.is_ack_recorded = is_ack_recorded
    self.has_ack_template = has_ack_template
    super(Control, self).__init__()

  def __iter__(self):
    byte = 0
    if self.is_dialog_start: byte |= 1 << 7
    if self.is_dialog_end:  byte |= 1 << 6
    if self.is_ack_return_template_requested:  byte |= 1 << 3
    if self.should_respond_only_if_ack_return_template_not_empty:  byte |= 1 << 2
    if self.is_ack_recorded: byte |= 1 << 1
    if self.has_ack_template: byte |= 1
    yield byte