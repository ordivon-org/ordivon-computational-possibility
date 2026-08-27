#!/usr/bin/env python3
"""External-carrier query used by CP capability-substitution dogfood.

Requires the external `z3-solver` Python package. It is intentionally not a CP
repository dependency.
"""

import json
import z3


o1, o2 = z3.Ints("o1 o2")
solver = z3.Solver()
solver.add(o1 == 0)
solver.add(o1 >= 0, o1 <= 1, o2 >= 0, o2 <= 1)
solver.add(z3.Not(o2 == o1 + 1))

status = solver.check()
assert status == z3.sat
model = solver.model()
trace = [model[o1].as_long(), model[o2].as_long()]
assert trace == [0, 0]

print(
    json.dumps(
        {
            "carrier": "z3-solver",
            "carrierVersion": z3.get_version_string(),
            "status": str(status),
            "counterexampleTrace": trace,
            "control": "PointwiseValidity != HistoryValidity",
        },
        sort_keys=True,
    )
)
