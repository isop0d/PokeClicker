import unittest

state = {"points": 0, "pokemon": []}

def on_click():
    state["points"] += 1

def catch_pokemon(name):
    if state["points"] < 50:
        return "not enough points"
    if name in state["pokemon"]:
        return "duplicate"
    state["points"] -= 50
    state["pokemon"].append(name)
    return "caught"

class TestClick(unittest.TestCase):
    def setUp(self):
        state["points"] = 0
        state["pokemon"] = []

    def test_adds_point(self):
        on_click()
        self.assertEqual(state["points"], 1)

class TestCatch(unittest.TestCase):
    def setUp(self):
        state["points"] = 50
        state["pokemon"] = []

    def test_deducts_points(self):
        catch_pokemon("pikachu")
        self.assertEqual(state["points"], 0)

    def test_not_enough_points(self):
        state["points"] = 10
        self.assertEqual(catch_pokemon("pikachu"), "not enough points")

class TestDuplicates(unittest.TestCase):
    def setUp(self):
        state["points"] = 100
        state["pokemon"] = ["pikachu"]

    def test_no_duplicates(self):
        self.assertEqual(catch_pokemon("pikachu"), "duplicate")

if __name__ == "__main__":
    unittest.main()