from .constants import *
from .observer import Observer

class ForwardSolver:

  def __init__(self, gravity=False, general=False, c=SPEED_OF_LIGHT):
    self.gravity = gravity
    self.general = general
    self.c = c
    self.observers = {}
    self.spheres = []
  
  def add_observer(self, observer: Observer):
    if self.observers.get(observer.id):
      raise ValueError(f'Observer with id {observer.id} already exists.')
    self.observers[observer.id] = observer

  def solve(self, find_variable, observer_id: str, observee_id: str, t, respect_to_id=None):
    if observer_id not in self.observers:
      raise ValueError(f'Observer with id {observer_id} does not exist.')
    if observee_id not in self.observers:
      raise ValueError(f'Observed with id {observee_id} does not exist.')
    if respect_to_id and respect_to_id not in self.observers:
      raise ValueError(f'Respect_to with id {respect_to_id} does not exist.')

    # align all motions relative to the observer
    aligned_observers = [observer_to_align.align_relative(observer) for observer_to_align in self.observers]
    aligned_spheres = [sphere.align_relative(observer) for sphere in self.spheres]

    observer = aligned_observers.get(observer_id)
    observee = aligned_observers.get(observee_id)

    if self.gravity or self.general:
      raise NotImplementedError('Gravity and general relativity are not yet implemented.')
    
    if not self.gravity and not self.general:
      match find_variable:
        case 'x':
          observee_distance = observer.x
        case 't':
          observee_distance = observee.x
          return t + (observee_distance/self.c)
        case 'v':
          return observee.x/[self.local_time*(1 + observee.local_v/self.c)]
        case _:
          raise ValueError(f'Invalid find_variable: {find_variable}')
