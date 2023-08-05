# THIS FILE IS AUTO-GENERATED. DO NOT EDIT
from verta._swagger.base_type import BaseType

class JobStatusEnumJobStatus(BaseType):
  _valid_values = [
    "NOT_STARTED",
    "IN_PROGRESS",
    "COMPLETED",
  ]

  def __init__(self, val):
    if val not in JobStatusEnumJobStatus._valid_values:
      raise ValueError('{} is not a valid value for JobStatusEnumJobStatus'.format(val))
    self.value = val

  def to_json(self):
    return self.value

  def from_json(v):
    if isinstance(v, str):
      return JobStatusEnumJobStatus(v)
    else:
      return JobStatusEnumJobStatus(JobStatusEnumJobStatus._valid_values[v])

