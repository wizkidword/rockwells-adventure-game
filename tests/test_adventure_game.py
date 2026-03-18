from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from adventure_game import AdventureGame


def make_game():
    outputs = []
    game = AdventureGame(input_func=lambda _='': 'quit', output_func=outputs.append)
    return game, outputs


def test_initial_location_and_look():
    game, outputs = make_game()
    game.look()
    joined = "\n".join(outputs)
    assert "cave entrance" in joined.lower()
    assert game.current_location == "start"


def test_move_path_to_boss_chamber():
    game, _ = make_game()
    game.move("north")
    assert game.current_location == "cave_start"
    game.move("north")
    assert game.current_location == "cave_deep"
    game.move("north")
    assert game.current_location == "chamber_boss"


def test_take_item_requires_actual_item_name_and_removes_it():
    game, outputs = make_game()
    game.move("north")
    game.move("north")  # now cave_deep with gem

    game.take_item("banana")
    assert "don't see" in "\n".join(outputs).lower()
    assert "banana" not in game.inventory

    game.take_item("gem")
    assert "gem" in game.inventory
    assert "gem" not in game.rooms["cave_deep"].items


def test_fight_without_gem_causes_damage():
    game, _ = make_game()
    game.move("north")
    game.move("north")
    game.move("north")

    health_before = game.player_health
    game.fight_boss()
    assert game.player_health == health_before - 30


def test_fight_with_gem_rewards_gold_and_resets_location():
    game, _ = make_game()
    game.move("north")
    game.move("north")
    game.take_item("gem")
    game.move("north")

    game.fight_boss()
    assert game.player_gold == 100
    assert game.current_location == "cave_deep"
