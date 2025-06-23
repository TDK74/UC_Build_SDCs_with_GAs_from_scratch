import os
from canvas import Canvas
from racetrack import Track
from network import Network # FirstNetwork
from evolution import Evolution
from storage import Storage


# track_image_path = os.path.join("images", "parkinglot.png")
cars_image_path = [os.path.join("images", f"car{idx}.png") for idx in range(5)]
# canvas = Canvas(track_image_path, cars_image_path)
canvas = Canvas(Track(3), cars_image_path)

# Network and genetic algorithm configuration
network_dimensions = 5, 4, 2    # input neurons, hidden layer neurons, output neurons
population_count = 10
max_generation_iterations = 5
keep_count = 4

# networks = [FirstNetwork() for _ in range(population_count)]
networks = [Network(network_dimensions) for _ in range(population_count)]
evolution = Evolution(population_count, keep_count)
storage = Storage("brain.json")

best_chomosomes = storage.load()

for c, n in zip(best_chomosomes, networks):
    n.deseriliaze(c)

simulation_round = 1

while simulation_round <= max_generation_iterations and canvas.is_simulating:
    print(f"=== Round: {simulation_round} ===")
    canvas.simulate_generation(networks, simulation_round)
    simulation_round += 1

    if canvas.is_simulating:
        print(f"-- Average checkpoint reached:\
              {sum(n.highest_checkpoint for n in networks) / len(networks): .2f}")
        print(f"-- Average edge distance:\
              {sum(n.smallest_edge_distance for n in networks[ : keep_count]) / keep_count: .2f}")
        print(f"-- Cars reached goal:\
              {sum(n.has_reached_goal for n in networks)} of population {population_count}.")

        serialized = [network.serialize() for network in networks]
        offspring = evolution.execute(serialized)
        storage.save(offspring[ : keep_count])  # save the nest chromosomes

        # create network from offspring
        networks = []

        for chromosome in offspring:
            network = Network(network_dimensions)
            network.deseriliaze(chromosome)
            networks.append(network)
