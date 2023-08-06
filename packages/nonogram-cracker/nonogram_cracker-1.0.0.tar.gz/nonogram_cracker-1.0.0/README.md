
# Nonogram Cracker

## Takes in a nonogram puzzle and returns its solution

---

## Usage

```python
import json
from nonogram_cracker import solve

solution = solve({
  "name": "turtle",
  "rows": [
    [1, 1, 1],
    [5],
    [3],
    [5],
    [1, 1]
  ],
  "cols": [
    [2, 2],
    [3],
    [4],
    [3],
    [2, 2]
  ]
})

print(json.dumps(solution, indent=2, ensure_ascii=False))
# [
#   "█ █ █",
#   "█████",
#   " ███ ",
#   "█████",
#   "█   █"
# ]
```

---

### Input Schema
#### TODO

### Output Schema
#### TODO
