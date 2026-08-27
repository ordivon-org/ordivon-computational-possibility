#!/usr/bin/env python3
"""Concrete provider traces used by Runtime dogfood."""

import json


class PointwiseOnlyProvider:
    def call(self):
        return 0


class StatefulCounterProvider:
    def __init__(self):
        self.state = 0

    def call(self):
        output = self.state
        self.state += 1
        return output


def trace(provider):
    return [provider.call(), provider.call()]


def pointwise_valid(values):
    return all(value in (0, 1) for value in values)


def history_valid(values):
    return values[0] == 0 and values[1] == values[0] + 1


bad = trace(PointwiseOnlyProvider())
good = trace(StatefulCounterProvider())

assert bad == [0, 0]
assert good == [0, 1]
assert pointwise_valid(bad) and pointwise_valid(good)
assert not history_valid(bad) and history_valid(good)

print(
    json.dumps(
        {
            "actualPointwiseOnlyTrace": bad,
            "actualStatefulCounterTrace": good,
            "pointwiseOnlySatisfiesPointwise": pointwise_valid(bad),
            "pointwiseOnlySatisfiesHistory": history_valid(bad),
            "statefulSatisfiesPointwise": pointwise_valid(good),
            "statefulSatisfiesHistory": history_valid(good),
        },
        sort_keys=True,
    )
)
