import os
from canvas import Canvas
from racetrack import Track
from network import Network
from evolution import Evolution
from storage import Storage


cars_image_path = [os.path.join("images", f"car{idx}.png") for idx in range(5)]
network_dimensions = 5, 4, 2    # input neurons, hidden layer neurons,
population_count = 34
max_generation_iterations = 5
keep_count = 4
storage = Storage("brain.json")

for track_index in range(4):
    print(f"\n>>> STARTING TRAINING on TRACK {track_index} <<<")
    canvas = Canvas(Track(track_index), cars_image_path)
    networks = [Network(network_dimensions) for _ in range(population_count)]
    evolution = Evolution(population_count, keep_count)
    best_chomosomes = storage.load()

    for c, n in zip(best_chomosomes, networks):
        n.deseriliaze(c)

    simulation_round = 1

    while simulation_round <= max_generation_iterations and canvas.is_simulating:
        print(f"=== Round: {simulation_round} (Track {track_index}) ===")
        canvas.simulate_generation(networks, simulation_round)
        simulation_round += 1

        if canvas.is_simulating:
            print(f"-- Average checkpoint:\
                  {sum(n.highest_checkpoint for n in networks) / len(networks): .2f}")
            print(f"-- Avg edge distance:\
                  {sum(n.smallest_edge_distance for n in networks[ : keep_count]) / keep_count: .2f}")
            print(f"-- Reached goal:\
                  {sum(n.has_reached_goal for n in networks)} / {population_count}")

            serialized = [n.serialize() for n in networks]
            offspring = evolution.execute(serialized)
            storage.save(offspring[ : keep_count])  # Keep only best

            networks = []

            for chromosome in offspring:
                n = Network(network_dimensions)
                n.deseriliaze(chromosome)
                networks.append(n)

    canvas.close()
