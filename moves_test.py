import unittest
from SpiderSolitar import SpiderSolitaire


class TestMoves(unittest.TestCase):

    def test_single_card_same_suit(self):
        s = SpiderSolitaire()
        s.initialize_tableau_from_string(
        """
        Jh Ts 5d 4d Ad Ks 7c 9d 
        """
        )
        s.move_card(3,2,1)
        self.assertEqual(s.tableau, SpiderSolitaire.tableau_from_string("""
        Jh Ts 5d    Ad Ks 7c 9d
              4d
        """))
    
    def test_multiple_cards_same_suit(self):
        s = SpiderSolitaire()
        s.initialize_tableau_from_string(
        """
        As 3h 3d Th 4d 8s 9h 2h 
        7d 4s 3c 5h Td 5s 8h 8c 
        Jh Th 5d 4d Ad Ks 7h 9d 
        """
        )
        s.move_card(6,1,3)
        self.assertEqual(s.tableau, SpiderSolitaire.tableau_from_string(
        """
        As 3h 3d Th 4d 8s    2h 
        7d 4s 3c 5h Td 5s    8c 
        Jh Th 5d 4d Ad Ks    9d
           9h
           8h
           7h
        """))
    
    def test_single_card_other_suit(self):
        s = SpiderSolitaire()
        s.initialize_tableau_from_string(
        """
        Ah 2h 3h 4h 5c 6s 7c 8c 
        """
        )
        s.move_card(5,6,1)
        self.assertEqual(s.tableau, SpiderSolitaire.tableau_from_string(
        """
        Ah 2h 3h 4h 5c    7c 8c 
                          6s
        """))
    
    def test_multiple_cards_other_suit(self):
        s = SpiderSolitaire()
        s.initialize_tableau_from_string(
        """
        7d 4s 3c 5h Td 5s 8h 8c 
        Jh 9c 5d 4d Ad Ks 7h 9d 
        """
        )
        s.move_card(6,1,2)
        self.assertEqual(s.tableau, SpiderSolitaire.tableau_from_string(
        """
        7d 4s 3c 5h Td 5s    8c 
        Jh 9c 5d 4d Ad Ks    9d 
           8h
           7h
        """))
    
    def test_single_card_wrong_rank(self):
        s = SpiderSolitaire()
        s.initialize_tableau_from_string(
        """
        Ah 2h 3h 4h 5c 6s 7c 8c 
        """
        )
        with self.assertRaises(ValueError) as cm:
            s.move_card(1,3,1)
        self.assertEqual(cm.exception.args[0], "Invalid move")
    
    def test_multiple_cards_no_sequence(self):
        s = SpiderSolitaire()
        s.initialize_tableau_from_string(
        """
        Ah 2h 3h 4h 5c 6s 7c 8c 
        Ah 2h 3h 4h 5c 6s 7c 8c 
        """
        )
        with self.assertRaises(ValueError) as cm:
            s.move_card(1,2,2)
        self.assertEqual(cm.exception.args[0], "Invalid move")
        
    def test_single_card_to_free_space(self):
        s = SpiderSolitaire()
        s.initialize_tableau_from_string(
        """
        Kc Kc Kc Kc    Kc Kc Kc 
        Ah 2h 3h 4h    6s 7c 8c
        """
        )
        s.move_card(0,4,1)
        self.assertEqual(s.tableau, SpiderSolitaire.tableau_from_string(
        """
        Kc Kc Kc Kc Ah Kc Kc Kc 
           2h 3h 4h    6s 7c 8c 
        """))
        
        
    def test_multiple_cards_to_free_space(self):
        s = SpiderSolitaire()
        s.initialize_tableau_from_string(
        """
        As 3h 3d    4d 8s 9h 2h 
        7d 4s 3c    Td 5s 8h 8c 
        Jh Th 5d    Ad Ks 7h 9d 
        """
        )
        s.move_card(6,3,3)
        self.assertEqual(s.tableau, SpiderSolitaire.tableau_from_string(
        """
        As 3h 3d 9h 4d 8s    2h 
        7d 4s 3c 8h Td 5s    8c 
        Jh Th 5d 7h Ad Ks    9d 
        """))
        
    def test_final_move(self):
        s = SpiderSolitaire()
        s.initialize_tableau_from_string(
        """
        Kh       6h
        Qh       5h
        Jh       4h
        Th       3h
        9h       2h
        8h       Ah
        7h
        """
        )
        s.move_card(3,0,6)
        self.assertEqual(s.tableau, [[] for _ in range(SpiderSolitaire.NUM_PILES)])
        
