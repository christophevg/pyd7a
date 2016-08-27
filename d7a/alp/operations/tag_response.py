from d7a.alp.operands.tag_id import TagId
from d7a.alp.operations.operation import Operation


class TagResponse(Operation):
  def __init__(self, *args, **kwargs):
    self.op     = 35
    self.operand_class = TagId
    super(TagResponse, self).__init__(*args, **kwargs)