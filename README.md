# Symulator
In progress readme (Sorry)


## Example generated gifs
### Generation 0
![Generation 0](gifs/gen0_animated.gif)
This shows the first generation that was simulated. Their genomes have been randomly generated and as a result they have random and non-productive behaviour. At the end of this, and every generation simulated, all creatures in the left half of the grid by the final tick were killed. The genomes of the following generation are built on the random coupling, of the survivors, and recombination of their two sets of genes.
### Generation 50
![Generation 50](gifs/gen50_animated.gif)
After 50 generations the creatures all now migrate to the right of the grid. These creatures don't "know" that they need to do this, but their genomes are built from the generations that came before them (i.e. those that survived by travelling right and then passing on their genes to the following generation)


## Usage

Three scripts to run the simulation:

1. Simulation.py
2. basicplotter.R
3. makeGIFS.sh



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






## Outputs
The script Simulation.py generates two folders 'Outputs/' and 'frames/'. The 'frames folder is the location where the R script BasicPlotter.R puts the individual frames of the GIFs. This is left untouched by the main python script. The 'Outputs/' folder is were the all the creature coordinate data and  genome information is kept.

1. Outputs/
   - Generation0/
        - field.csv
        - population.csv
        - pheromone.csv
   - Generation1/
   - Generation5/
   - GenerationX/ (etc.)
2. frames/
3. stat_summary.csv



## Genomes

Example genome, comprised of 6 genes, for a randomly generated creature in the simulation
```
['6AE1F13F', 'C9872A8C', 'F7C6201F', '51C24B12', '897C608D', 'CC134376']
```


The genome is a list of genes up to the size specficied in 'parameters.txt'. Each gene is encoded as a 8 digit hexadecimal. This can be converted to a 32 bit binary integer. Within each genes is the information required to determine a single connection between two nodes in a creatures brain. Below is a table to show hoe that informations is stored, using the first gene, '6AE1F13F', in the genome above as an example.

```
6AE1F13F = 01101010111000011111000100111111 = 32 bits
```

| Bit range | Example | Identity | Explanation |
| -- | -- | -- | -- |
| Gene[0] | 0 | Input neuron type | 0 = Sensory neuron, 1 = Internal neuron |
| Gene[1:8] | 1101010 | Input neuron identity |  |
| Gene[8] | 1 | Output neuron identity |  |
| Gene[9:16] | 1100001 | Output neuron identity |  |
| Gene[16:32] | 1111000100111111 | Connection weight |  |

