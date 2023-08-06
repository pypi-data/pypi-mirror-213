from __future__ import annotations

class Observer:

  def __init__(self, id, x=0, y=0, z=0, local_v=0, local_v_dir=0, v_x=0, v_y=0, v_z=0):
    self.id = 0
    self.x = x
    self.y = y
    self.z = z
    self.local_v = local_v
    self.local_v_dir = local_v_dir
    self.v_x = v_x
    self.v_y = v_y
    self.v_z = v_z

  def align_relative(self, observer: Observer):
    self.x -= observer.x
    self.y -= observer.y
    self.z -= observer.z
  