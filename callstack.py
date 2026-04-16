from dataclasses import dataclass
from enum import Enum

class EventType(Enum):
    START = 'start'
    END = 'end'

@dataclass
class Sample:
    ts: int
    stack: list[str]

@dataclass
class Event:
    ts: int
    type: EventType
    fn: str

def main(samples: list[Sample]):
    events = []
    padded = [Sample(0, [])] + samples

    for (previous, current) in zip(padded, padded[1:]):
        j = 0

        while j < len(previous.stack) and j < len(current.stack) and previous.stack[j] == current.stack[j]:
            j += 1

        for k in reversed(range(j, len(previous.stack))):
            events.append(Event(current.ts, EventType.END, previous.stack[k]))

        for k in range(j, len(current.stack)):
            events.append(Event(current.ts, EventType.START, current.stack[k]))

    return events

events = main([
    Sample(7, ['main']),
    Sample(8, ['main', 'my_fn']),
    Sample(9, ['main', 'my_fn', 'my_fn2', 'my_fn3']),
    Sample(10, ['main', 'my_fn', 'my_fn4']),
    Sample(11, ['main']),
])

for event in events:
    print(event)
