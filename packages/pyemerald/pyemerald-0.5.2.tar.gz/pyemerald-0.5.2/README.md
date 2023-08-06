# pyemerald

Pyemerald is a python package which lets you modify save files from Pokemon Emerald (Sapphire, Ruby, Leaf Green and Fire Red to come). It lets you modify Pokemon in your team and on the PC, and lets you modify items on the PC. It can also be used to inspect a Pokemons attributes like EV's (IV's to come).

Other and more advanced projects exist e.g. [pkHex](https://projectpokemon.org/home/files/file/1-pkhex/) which inspired this project. However, it annoyed me that I was unable to run pkHex on Linux, and thus pyemerald was created.

Please make sure to never overwrite your original save file, as this software could accidentially make an invalid save file. You are responsible for using the software correctly.
## Installation

Pyemerald can be installed from pypi with the following command:

```
pip install pyemerald
```

It has no dependencies so it should be a simple install.

## Usage

Several examples are available in the `examples` folder. But basically it works by loading an `.sav` file using a `Save` object, which can then emit a `Game` object that is modifiable. Once modification is done, the `Game` object is passed back to the `Save` object and saved to a new file (Please always save to a new file, so you don't accidentially delete your current save file!).

```python
from pyemerald.save import Save
from pyemerald.pokemon import PCPokemon
from pyemerald.moves import Move

save = Save.from_file("data/marie_treecko_pokedex_pc.sav")

game = save.to_game()

# Simple create pokemon
flygon = PCPokemon.from_name(
    name="Flygon",
    level=48,
    move_1=Move.from_name("Thunder"),
    move_2=Move.from_name("Thunder Punch"),
    move_3=Move.from_name("Ice Beam"),
    move_4=Move.from_name("Fly"),
)

# Add Pokemon to user PC
game.add_pc_pokemon(flygon)

# Put modification back to the Save Object
save.update_from_game(game)

# Write new Save file
save.to_file("data/emerald.sav")

```
