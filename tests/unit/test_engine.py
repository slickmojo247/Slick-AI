import unittest
from engine.SlickLogicEngine import SlickLogicEngine
from memory.MemoryBank import MemoryBank

class TestEngine(unittest.TestCase):
    def setUp(self):
        self.memory = MemoryBank(":memory:")
        self.engine = SlickLogicEngine(self.memory)

    def test_mode_switching(self):
        self.assertTrue(self.engine.set_mode("technical"))
        self.assertEqual(self.engine.mode, "technical")
        with self.assertRaises(ValueError):
            self.engine.set_mode("invalid_mode")

    def test_processing(self):
        result = self.engine.process("test query")
        self.assertEqual(result["status"], "success")
        self.assertIn("test query", result["response"])

if __name__ == "__main__":
    unittest.main()
