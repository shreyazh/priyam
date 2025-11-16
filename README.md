# Priyam: A Comprehensive Python Package for Mathematics, Science, and Utilities

Priyam is an advanced open-source Python package designed to streamline and supercharge mathematical, scientific, algorithmic, and utility tasks. With comprehensive modules for mathematics, physics, chemistry, computer science, LaTeX generation, and daily utilities, Priyam is ideal for students, educators, researchers, and developers.

---

## Table of Contents
- [Features](#features)
- [Modules & Capabilities](#modules--capabilities)
- [Installation](#installation)
- [Quick Usage Examples](#quick-usage-examples)
- [Applications (GUI Tools)](#applications-gui-tools)
- [LaTeX/Pretty Printing](#latexpretty-printing)
- [Documentation](#documentation)
- [Contributing](#contributing)
- [License & Credits](#license--credits)
- [Support](#support)

---

## Features
- Algebra (linear, quadratic, cubic equations, symbolic math, calculus)
- Probability, statistics, number theory, and matrices
- Physics (kinematics, dynamics, thermodynamics, electromagnetism, optics)
- Chemistry helpers (molar mass, stoichiometry, pH, gas laws, equilibrium)
- Computer science (classic algorithms, sorting, graph theory, DP)
- String utilities (title case, slugs, reverse words)
- LaTeX utilities (matrices, equations, fractions)
- Built-in Desktop Utilities:
  - Broken Link Checker (with JS rendering)
  - Notepad clone (dark-mode, multi-tab)
  - Slide extractor from YouTube videos (OCR, PDF export)
- Date/time, timezone converters, working days calculator

---

## Modules & Capabilities

### 1. `pmath`: Advanced Mathematics
- Equation solvers (linear, quadratic, cubic, symbolic)
- Calculus (differentiation, integration, Taylor/series expansion, limits)
- Probability and statistics (mean, median, mode, variance, regression, binomial)
- Number theory (primes, prime factorization, perfect numbers, GCD, LCM)
- Linear algebra (matrices, determinants, eigenvalues/solutions)
- ODEs and systems solver
- Utility tools (Newton-Raphson, time zones, working days, countdown timer)

### 2. `physics`: Physics Formulas and Simulators
- Kinematics, dynamics, projectiles, forces, energy, momentum
- Wave/optics: Snell's law, wave speed, refraction
- Electromagnetism: Coulomb’s law, electric/magnetic fields, Lorentz force
- Thermodynamics: ideal gas, internal energy, work, heat, first law

### 3. `chemistry`: Chemistry Problem Solvers
- Compute molar mass, convert grams-to-moles, moles-to-grams
- Ideal gas volume calculations
- Acid-base pH, buffer calculations (Henderson-Hasselbalch)
- Equilibrium for reactions: extent-of-reaction, numeric solver

### 4. `cs`: Computer Science Algorithms
- Classic graph algorithms (BFS, DFS, Dijkstra, topo-sort)
- Searching and sorting: binary search, quicksort, mergesort
- DP patterns: knapsack, longest subsequence, edit distance, LIS
- Greedy patterns: activity selection, interval scheduling
- Complexity helpers: Big-O lookups

### 5. `string_utils`: String Utilities
- Smart title-casing (with custom exceptions)
- Reverse word order
- Slugify (convert strings for URLs)

### 6. `latex_support`: LaTeX Helpers
- Pretty-print matrices, equations, fractions for papers and reports

### 7. Applications (Desktop GUI in `apps` and `external`):
- **linkchecker**: Graphical broken link checker (JS/CSS support, bulk export)
- **notepad**: Multi-tab, dark-mode modern notepad/editor
- **slide_extract**: Extracts slides from YouTube (OCR, similarity), batch PDF export

---

## Installation

```bash
pip install priyam
# or install dependencies for full functionality including GUI apps and slide extraction:
pip install -r requirements.txt
```

---

## Quick Usage Examples

```python
from priyam import pmath, physics, chemistry, cs, string_utils

# Math: Solve quadratic
roots = pmath.MathSolver.solve_quadratic(1, -3, 2)   # (2.0, 1.0)

# Physics: projectile range
r = physics.ProjectileMotion.range(10, 0.5)

# Chemistry: Molar mass
mm = chemistry.ChemistrySolver.molar_mass('H2SO4')

# CS: Dijkstra's shortest path
graph = {'A': [('B', 1), ('C', 5)], 'B': [('C', 2)], 'C': []}
dist = cs.GraphAlgorithms.dijkstra(graph, 'A')

# String utils: Slugify
slug = string_utils.slugify('Hello World!')
```

---

## Applications (GUI Tools)

- **Broken Link Checker**
  - GUI: `python -m priyam.linkchecker`
  - JS/React support, export/bulk, dark mode
- **Advanced Notepad**
  - GUI: `python -m priyam.notepad`
  - Features: Tabs, dark mode, autosave, find/replace, formatting
- **Slide Extractor**
  - GUI: `python -m priyam.slide_extract`
  - Extract slides from YouTube lectures, convert to PDF (requires dependencies)

---

## LaTeX/Pretty Printing

Generate LaTeX for fractions, matrices, and equations for reports:

```python
from priyam import latex_support as ls
print(ls.latex_fraction(1, 2))  # \frac{1}{2}
```

---

## Documentation

Full API documentation, usage tutorials, and examples:
[https://github.com/shreyazh/priyam/docs](https://github.com/shreyazh/priyam/docs)

---

## Contributing

We welcome contributions! Fork, submit pull requests, and file issues at:
[https://github.com/shreyazh/priyam](https://github.com/shreyazh/priyam)

---

## License & Credits

Priyam is MIT licensed.
Developed by The Priyam Team. Major contributions by @justshreyash.
Initial author: Shreyash Srivastva

---

## Support

Issues, questions, and community:
[https://github.com/shreyazh/priyam/issues](https://github.com/shreyazh/priyam/issues)
