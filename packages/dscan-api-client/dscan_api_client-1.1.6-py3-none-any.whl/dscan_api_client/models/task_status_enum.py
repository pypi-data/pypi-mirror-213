from enum import IntEnum


class TaskStatusEnum(IntEnum):
    VALUE_0 = 0
    VALUE_1 = 1
    VALUE_2 = 2
    VALUE_3 = 3
    VALUE_9 = 9
    VALUE_10 = 10

    def __str__(self) -> str:
        return str(self.value)
