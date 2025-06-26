import os
from canvas import Canvas
from network import Network
from racetrack import Track
from storage import Storage


# Network configuration
network_dimensions = 5, 4, 2    # input neurons, hidden layer neurons, output neurons

cars_image_path = [os.path.join("images", f"car{idx}.png") for idx in range(5)]
print("\n>>> TEST DRIVE ON UNSEEN TRACK 4 <<<\n")
canvas = Canvas(Track(4), cars_image_path)
storage = Storage("brain.json")
networks = [Network(network_dimensions) for _ in range(4)]
best_chromosomes = storage.load()
print(f"Loaded {len(best_chromosomes)} chromosomes from brain.json.")
simulation_round = 1

for c, n in zip(best_chromosomes, networks):
    n.deseriliaze(c)

while simulation_round <= 5 and canvas.is_simulating:
    canvas.simulate_generation(networks, simulation_round)
    simulation_round += 1
