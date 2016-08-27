from d7a.support.schema import Validatable, Types


class TagId(Validatable):

  SCHEMA = [{
    "tag_id" : Types.BYTE(),
  }]

  def __init__(self, tag_id):
    self.tag_id = tag_id
    super(TagId, self).__init__()

  def __iter__(self):
    yield self.tag_id

  def __str__(self):
    return "tag_id={}".format(self.tag_id)
