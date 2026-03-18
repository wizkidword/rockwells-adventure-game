# Adventure Game (Audited)

A lightweight text adventure game with a small cave/dragon storyline.

## Run

```bash
python3 adventure_game.py
```

## Commands

- `look`
- `go <direction>`
- `take <item>`
- `use <item>`
- `fight`
- `status`
- `help`
- `quit`

## Notes

- The boss fight happens in `chamber_boss`.
- Carrying the `gem` gives you a winning path in the fight.
- Code was refactored for testability using injectable input/output functions.

## Test

```bash
pytest -q
```
