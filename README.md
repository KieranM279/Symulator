# Symulator

## Usage

### Parameters
The function FindParameters() reads in the parameters listed in the test file, 'parameters.txt'.

```
GRID_SIZE 128
POPULATION 100
GENERATIONS 50
SAVED_GENERATIONS [0,1,5,10,25,50]
TICKS 150
GENES 24
INTERNAL_NEURONS 4
MUTATION_RATE 0.001
```

| Parameter | Description | Format |
| --- | --- | -- |
| GRID_SIZE | Sets the size of the field that the creatures can exist in. A value of 128 creates a grid of 128x128. | Number |
| POPULATION | Sets the initial number of creatures to randomly generate and also the number of creatures to generate in the inheritance stage of the simulation. | Number |
| GENERATIONS | Sets the total number of generations to simulate. | Number |
| SAVED_GENERATIONS | A list of generations that you want to turn into gifs. Basic statistics on every generation are still saved however the coordinates for each creature on every tick of the generation are not saved unless they appear in this list.| Numeric list (e.g. [0,1,5,10,25,50]) |
| TICKS | Sets how long each generation must be simulated for. As the creature can only move a maximum of one space per tick, this value should be equal to or larger than the GRID_SIZE. This enables creature to traverse the entire grid if necassary. This is not a fixed requirement though. | Number |
| GENES | Sets the total number of connections that will form the creatures brain. | Number |
| INTERNAL_NEURONS | Sets the total number of nodes that separate the sensory neurons and the action neurons | Number |
| MUTATION_RATE | Sets the likelihood that the current base in the geome with flip to an alternate state, when you traverse the genome base by base, (0 -> 1, 1 -> 0) | Number |