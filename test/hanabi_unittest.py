import unittest
import hanabi



class ColorTest(unittest.TestCase):
    def test_1(self):
        pass


class CardTest(unittest.TestCase):
    def test_1(self):
        pass


class HandTest(unittest.TestCase):
    # test __special__ functions
    def setUp(self):
        self.deck1=hanabi.deck.Deck()
        self.hand1=hanabi.deck.Hand(self.deck1)
        self.deck2=self.deck1.shuffle()
        self.hand2=hanabi.deck.Hand(self.deck2)
    def test_len(self):
        self.assertEqual(5, len(self.hand1))
    
    def test_shuffle(self):
        


    # test normal functions
    pass

class DeckTest(unittest.TestCase):
    # test __special__ functions
    

    # test normal functions
    pass



class GameTest(unittest.TestCase):

    def setUp(self):
        self.unshuffled_game = hanabi.Game()
        self.random_game = hanabi.Game()
        # ... group G here! 
        self.predefined_game = hanabi.Game()
        # ...


    # lines 193, 227
    def test_A1(self):
        pass

    # lines 227, 261
    def test_B1(self):
        pass


    # lines 261, 295


    # lines 295, 329


    # lines 329, 363


    # lines 363, 397


    # lines 397, 431


    pass



if __name__ == '__main__':
    unittest.main()
