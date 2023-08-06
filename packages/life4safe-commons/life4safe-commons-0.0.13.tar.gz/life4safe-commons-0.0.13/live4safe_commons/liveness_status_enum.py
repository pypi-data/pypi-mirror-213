from enum import Enum


class LivenessStatusEnum(Enum):
    unknown = 0
    not_requested = 1
    queued = 10
    pending = 11
    processing = 20
    processed = 21
    error = 40
    execption = 50
