from d7a.alp.operands.tag_id import TagId
from d7a.alp.operations.operation import Operation


class TagRequest(Operation):
  def __init__(self, *args, **kwargs):
    self.op     = 52
    self.operand_class = TagId
    super(TagRequest, self).__init__(*args, **kwargs)