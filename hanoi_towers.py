import random
from collections import deque
from dataclasses import dataclass


@dataclass
class Tower:
    name: str
    stack: deque

    def is_empty(self) -> bool:
        return len(self.stack) == 0

    def top_disk(self) -> int:
        return self.stack[0]


class Game:
    def __init__(self, disk_count: int):
        self.disk_count = disk_count
        self.towers = None
        self.reset_state()

    def reset_state(self):
        self.towers = (
            Tower("left", deque(range(1, self.disk_count + 1))),
            Tower("middle", deque([])),
            Tower("right", deque([])),
        )

    def is_done(self) -> bool:
        return len(self.towers[-1].stack) == self.disk_count

    def show_state(self):
        result = []
        for tower in self.towers:
            if tower.is_empty():
                result.append("-".ljust(self.disk_count))
            else:
                result.append("".join(str(x) for x in tower.stack).ljust(self.disk_count))

        print(" ".join(result))

    def play_randomly(self):
        move_counter = 0
        while not self.is_done():
            success = self.make_random_move()
            if not success:
                self.reset_state()
                print("-" * 30)
                continue

            self.show_state()
            move_counter += 1

        print(f"took {move_counter} moves!")

    def make_random_move(self) -> bool:
        source = self.get_random_source()
        if not source:
            print("all towers are empty, somehow")
            return False

        destination = self.get_random_destination(source)
        if not destination:
            print("no suitable destination")
            return False

        disk = source.stack.popleft()
        destination.stack.appendleft(disk)
        return True

    def get_non_empty_towers(self) -> list[Tower]:
        return [tower for tower in self.towers if not tower.is_empty()]

    def get_suitable_destinations(self, source: Tower) -> list[Tower]:
        return [tower for tower in self.towers if
                tower.name != source.name and (tower.is_empty() or tower.top_disk() > source.top_disk())]

    def get_random_source(self) -> Tower | None:
        non_empty_towers = self.get_non_empty_towers()
        if not non_empty_towers:
            return

        return random.choice(non_empty_towers)

    def get_random_destination(self, source: Tower) -> Tower | None:
        suitable_destinations = self.get_suitable_destinations(source)
        if not suitable_destinations:
            return

        return random.choice(suitable_destinations)


if __name__ == "__main__":
    game = Game(3)
    game.play_randomly()
