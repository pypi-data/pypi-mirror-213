# basedrelativity

Python package for solving relativity problems. Make no mistake, this package is not simply an alternative to Einstein's math. basedrelativity contains genuine corrections to both SR and GR and should always be used in place of the Lorentz transforms without exception.

Visit basedphysics.com for an overview of the logic and math.

## Installation

```pip install basedrelativity```

## Usage

Use the ForwardSolver to compute the data that would be collected by an observer from the local motions of distant observees. *All observer property inputs should be from the observee's local system.*

```
from basedrelativity import ForwardSolver

my_observer = Observer()
observee = Observer(5,5)
observee.local_v = 400000

solver = ForwardSolver()
solver.add_observer(my_observer)
solver.add_observer(observee)
observee_local_distance = solver.solve('x', my_observer, observee)
```

Use the InverseSolver to compute the local motions of observed objects from an observer's data. *All observer property inputs should be from the perspective of the primary observer.*

```
from basedrelativity import InverseSolver

my_observer = Observer()
observee = Observer(5,5)
observee.local_v = 400000

solver = ForwardSolver()
solver.add_observer(my_observer)
solver.add_observer(observee)
observee_local_distance = solver.solve('x', my_observer, observee)
```

## Contributing

If you find a bug 🐛, please open a bug report. If you have an idea for an improvement or new feature 🚀, please open a feature request.
