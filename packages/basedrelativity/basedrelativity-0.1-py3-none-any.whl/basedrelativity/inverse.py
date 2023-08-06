from .constants import *
from .observer import Observer

class InverseSolver:

  def __init__(self, primary_observer: Observer, gravity=False, general=False, c=SPEED_OF_LIGHT):
    self.primary_observer = primary_observer
    self.gravity = gravity
    self.general = general
    self.c = c
    self.observers = {}
    self.spheres = []
  
  def add_observer(self, observer: Observer):
    if self.observers.get(observer.id):
      raise ValueError(f'Observer with id {observer.id} already exists.')
    self.observers[observer.id] = observer

  def solve(self, find_variable, observer, observed, respect_to=None):
    if observer.id not in self.observers:
      raise ValueError(f'Observer with id {observer.id} does not exist.')
    if observed.id not in self.observers:
      raise ValueError(f'Observed with id {observed.id} does not exist.')
    if respect_to and respect_to.id not in self.observers:
      raise ValueError(f'Respect_to with id {respect_to.id} does not exist.')
    if not self.gravity and not self.general:
      match find_variable:
        case 'x':
          find_variable = 'x_prime'
        case 't':
          pass
        case 'v':
          pass
        case _:
          raise ValueError(f'Invalid find_variable: {find_variable}')
