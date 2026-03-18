"""Simple text adventure game.

This module is designed to run interactively and to be easy to test.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable


@dataclass
class Room:
    description: str
    exits: dict[str, str] = field(default_factory=dict)
    items: list[str] = field(default_factory=list)


class AdventureGame:
    def __init__(
        self,
        input_func: Callable[[str], str] = input,
        output_func: Callable[[str], None] = print,
    ) -> None:
        self.input_func = input_func
        self.output = output_func

        self.player_health = 100
        self.player_gold = 0
        self.inventory: list[str] = []
        self.is_running = True
        self.current_location = "start"

        self.rooms: dict[str, Room] = {
            "start": Room(
                description=(
                    "You are at the cave entrance. A narrow passage leads NORTH into darkness."
                ),
                exits={"north": "cave_start"},
            ),
            "cave_start": Room(
                description="You stand in a damp cavern. You can go SOUTH or deeper NORTH.",
                exits={"south": "start", "north": "cave_deep"},
            ),
            "cave_deep": Room(
                description=(
                    "A faintly glowing GEM lies on the ground. The air feels dangerous here."
                ),
                exits={"south": "cave_start", "north": "chamber_boss"},
                items=["gem"],
            ),
            "chamber_boss": Room(
                description=(
                    "A dragon blocks the treasure chamber! You can FIGHT or FLEE south."
                ),
                exits={"south": "cave_deep"},
            ),
        }

    def start_game(self) -> None:
        self.output("\n" + "=" * 34)
        self.output(" Welcome to Rockwell's Adventure ")
        self.output("=" * 34)
        self.output("Type: look, go <direction>, take <item>, use <item>, fight, status, help, quit")
        self.look()

    def get_input(self) -> str:
        try:
            return self.input_func("> ").strip().lower()
        except EOFError:
            return "quit"

    def process_command(self, command: str) -> None:
        if not command:
            self.output("Enter a command. Type 'help' for options.")
            return

        parts = command.split()
        verb = parts[0]

        if verb in {"go", "move", "walk"}:
            if len(parts) < 2:
                self.output("Go where? Example: go north")
                return
            self.move(parts[1])
        elif verb == "look":
            self.look()
        elif verb == "take":
            if len(parts) < 2:
                self.output("Take what?")
                return
            self.take_item(parts[1])
        elif verb == "use":
            if len(parts) < 2:
                self.output("Use what?")
                return
            self.use_item(parts[1])
        elif verb in {"status", "stats"}:
            self.show_status()
        elif verb == "fight":
            self.fight_boss()
        elif verb in {"help", "?"}:
            self.show_help()
        elif verb in {"quit", "exit"}:
            self.output("\nThanks for playing! Goodbye.")
            self.is_running = False
        else:
            self.output("Unknown command. Type 'help' for options.")

    def move(self, direction: str) -> None:
        room = self.rooms[self.current_location]
        target = room.exits.get(direction)
        if not target:
            self.output(f"You cannot go {direction} from here.")
            return

        self.current_location = target
        self.look()

        if self.current_location == "chamber_boss":
            self.output("The dragon roars! You may FIGHT or go SOUTH to flee.")

    def look(self) -> None:
        room = self.rooms[self.current_location]
        self.output(room.description)
        if room.items:
            self.output("You see: " + ", ".join(room.items))
        if room.exits:
            self.output("Exits: " + ", ".join(sorted(room.exits.keys())))

    def take_item(self, item_name: str) -> None:
        room = self.rooms[self.current_location]
        if item_name not in room.items:
            self.output("You don't see that item here.")
            return

        room.items.remove(item_name)
        self.inventory.append(item_name)
        self.output(f"You took the {item_name}.")

    def use_item(self, item_name: str) -> None:
        if item_name not in self.inventory:
            self.output(f"You don't have a {item_name}.")
            return

        if item_name == "gem":
            self.output("The gem pulses warmly, illuminating hidden cracks in the cave walls.")
        else:
            self.output(f"You use the {item_name}, but nothing obvious happens.")

    def fight_boss(self) -> None:
        if self.current_location != "chamber_boss":
            self.output("There's nothing to fight here.")
            return

        if "gem" in self.inventory:
            self.output("The dragon is blinded by the gem's light and flees!")
            self.player_gold += 100
            self.output("You claim 100 gold from the treasure hoard.")
            self.current_location = "cave_deep"
            return

        self.player_health -= 30
        self.output("The dragon breathes fire! You take 30 damage.")
        if self.player_health <= 0:
            self.output("\n💀 You have fallen in combat... Game Over.")
            self.is_running = False
        else:
            self.output(f"Health remaining: {self.player_health}")

    def show_status(self) -> None:
        self.output("\n--- Status ---")
        self.output(f"Location: {self.current_location}")
        self.output(f"Health: {self.player_health}")
        self.output(f"Gold: {self.player_gold}")
        self.output(f"Inventory: {', '.join(self.inventory) if self.inventory else 'Empty'}")

    def show_help(self) -> None:
        self.output(
            "Commands: look | go <north/south> | take <item> | use <item> | fight | status | quit"
        )

    def run(self) -> None:
        self.start_game()
        while self.is_running:
            command = self.get_input()
            self.process_command(command)


if __name__ == "__main__":
    AdventureGame().run()
