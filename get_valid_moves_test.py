import unittest
from SpiderSolitar import SpiderSolitaire
from spider_parser import SpiderSolitaireParser
from spider_next_moves import SpiderSolitaireNextMoves


class TestGetValidMoves(unittest.TestCase):

    def test_basic_moves(self):
        s = SpiderSolitaire()
        s.tableau = SpiderSolitaireParser.tableau_from_string(
        """
        Jh Ts 5d 4d Ad Ks 7c 9d Kc Kd
        """
        )
        moves = SpiderSolitaireNextMoves.get_valid_moves(s)
        self.assertEqual(moves, [(1, 0, 1), (3, 2, 1), (7, 1, 1), "deal"])
    
    def test_sequence_moves(self):
        s = SpiderSolitaire()
        s.deck = []
        s.tableau = SpiderSolitaireParser.tableau_from_string(
        """
        Jh Ts 5d 4d Ad Ks 3c 9d Kc Kd
        As 3h 3d 9h 4d 8s    2h 
        7d 4s 3c 8h Td 5s    8c 
        Jh Th 5d 7h Ad Ks     
        """
        )
        moves = SpiderSolitaireNextMoves.get_valid_moves(s)
        self.assertEqual(moves, [(1, 0, 1), (3, 1, 3)])
        
    def test_single_empty_pile(self):
        s = SpiderSolitaire()
        s.tableau = SpiderSolitaireParser.tableau_from_string(
        """
        Jh Ts    4d Ad Ks 3c 9d 7c Kd
        Kh Js    4d Ad Ks 7c 9d 
        """
        )
        moves = SpiderSolitaireNextMoves.get_valid_moves(s)
        self.assertEqual(moves, [(0, 2, 1), (1, 2, 1), (3, 2, 1), (4, 2, 1), (5, 2, 1), (6, 2, 1), (7, 2, 1)])
    
    def test_multiple_empty_piles(self):
        s = SpiderSolitaire()
        s.tableau = SpiderSolitaireParser.tableau_from_string(
        """
        Jh Ts    4d    Ks 3c 9d 
        Kh Js    4d    Ks 7c 9d 
        """
        )
        moves = SpiderSolitaireNextMoves.get_valid_moves(s)
        self.assertEqual(moves, [(0, 2, 1), (1, 2, 1), (3, 2, 1), (5, 2, 1), (6, 2, 1), (7, 2, 1)])
    
    def test_dont_move_between_emptie_piles(self):
        s = SpiderSolitaire()
        s.tableau = SpiderSolitaireParser.tableau_from_string(
        """
        Jh Ts    4d    Ks 3c 8d 
        """
        )
        moves = SpiderSolitaireNextMoves.get_valid_moves(s)
        self.assertEqual(moves, [(1,0,1), (6,3,1)])
        
    def test_final_move(self):
        s = SpiderSolitaire()
        s.tableau = SpiderSolitaireParser.tableau_from_string(
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
        moves = SpiderSolitaireNextMoves.get_valid_moves(s)
        self.assertEqual(moves, [(0,1,1),(0,1,2),(0,1,3),(0,1,4),(0,1,5),(0,1,6), 
                                 (3,0,6),
                                 (3,1,1),(3,1,2),(3,1,3),(3,1,4),(3,1,5)
                                 ])
    
    @unittest.skip("enhancement not neccessary/too complex")
    def test_dont_move_to_same_twice(self):
        s = SpiderSolitaire()
        s.deck = []
        s.tableau = SpiderSolitaireParser.tableau_from_string(
        """
        Kh Ts 5d 4d 5d 5d 5d 5h 
        """
        )
        moves = SpiderSolitaireNextMoves.get_valid_moves(s)
        self.assertEqual(moves, [(3,2,1)])
        
    @unittest.skip("enhancement not neccessary/too complex")
    def test_dont_move_to_same_twice_complex(self):
        s = SpiderSolitaire()
        s.deck = []
        s.tableau = SpiderSolitaireParser.tableau_from_string(
        """
        5h 6s Kd 4d 4c 3d 3s 3h Kc Kd
           5s 5d       2d 2s
                          As
        """
        )
        moves = SpiderSolitaireNextMoves.get_valid_moves(s)
        self.assertEqual(moves, [(3,0,1),(4,0,1),(5,3,2),(6,3,3),(7,3,1)])
    
    def test_dont_move_between_same(self):
        s = SpiderSolitaire()
        s.deck = []
        s.tableau = SpiderSolitaireParser.tableau_from_string(
        """
        Kc Kc Kc Kc Kc Kc Kc Kc Kc Kc
        Kh Ts 5d    5d 5d 5d 5h 
              4d 
        """
        )
        moves = SpiderSolitaireNextMoves.get_valid_moves(s)
        self.assertEqual(moves, [])
    
    @unittest.skip("enhancement not neccessary/too complex")
    def test_dont_move_n_to_n(self):
        s = SpiderSolitaire()
        s.deck = []
        s.tableau = SpiderSolitaireParser.tableau_from_string(
        """
        Kc Kc Kc Kc Kc Kc Kc Kc Kc Kc
        Kh 4s 5d 4d 5c 5s 5d 5h 
        """
        )
        moves = SpiderSolitaireNextMoves.get_valid_moves(s)
        self.assertEqual(moves, [(1,2,1),(3,2,1)])
    
    
    @unittest.skip("enhancement not neccessary/too complex")
    def test_add_combinations_on_no_return(self):
        s = SpiderSolitaire()
        s.deck = []
        s.tableau = SpiderSolitaireParser.tableau_from_string(
        """
        Kc Kc Kc Kc Kc Kc Kc Kc Kc Kc
        Kh    5d 4d 5c 5s 5d 5h 
              4s
        """
        )
        moves = SpiderSolitaireNextMoves.get_valid_moves(s)
        self.assertEqual(moves, ["???"])
        
    @unittest.skip("enhancement not neccessary/too complex")
    def test_add_combinations_on_deal(self):
        s = SpiderSolitaire()
        s.deck = [(13,3),(13,3),(13,3),(13,3),(13,3),(13,3),(13,3),(13,3)]
        s.tableau = SpiderSolitaireParser.tableau_from_string(
        """
        Kc Kc Kc Kc Kc Kc Kc Kc Kc Kc
        Kc    5d Kc 5c Kc Kc Kc 
              4s
        """
        )
        moves = SpiderSolitaireNextMoves.get_valid_moves(s)
        self.assertEqual(moves, [(2,4,1),"deal"])
    