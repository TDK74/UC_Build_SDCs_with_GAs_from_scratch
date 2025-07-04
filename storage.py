import json


class Storage:
    def __init__(self, filename):
        self.filename = filename


    def save(self, chromosomes):
        with open(self.filename, "w") as file:
            json.dump({"chromosomes": chromosomes}, file)


    def load(self):
        try:
            with open(self.filename, "r") as file:
                data = json.load(file)

                return data["chromosomes"]

        except Exception:
            # something went worng and return an empty list of chromosomes
            return []
