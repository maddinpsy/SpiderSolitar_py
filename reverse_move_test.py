import unittest
from SpiderSolitar import SpiderSolitaire
from spider_next_moves import apply_random_move
from spider_reverse import do_random_reverse_move
from spider_parser import tableau_from_string



class TestReverseMove(unittest.TestCase):

    def test_many_moves(self):
        s = SpiderSolitaire()
        # start with random moves
        for _ in range(100):
            apply_random_move(s)

        # just do a lot of random moves and check that each is a valid move
        before = [[card for card in pile ] for pile in s.tableau]
        # print(s.tableau_to_string())
        for _ in range(10000):
            move = do_random_reverse_move(s)
            # print(move)
            self.assertNotEqual(before, s.tableau)
            if move == 'deal':
                s.deal()
            else:
                source_pile, dest_pile, num_cards = move
                s.move_card(source_pile, dest_pile, num_cards)
            self.assertEqual(before, s.tableau)
    
    @unittest.skip("skip")
    def test_error_case(self):
        s = SpiderSolitaire()
        s.tableau = tableau_from_string("""
            9s Kd Js Kd 7h 3d 8d Ah Jc As 
            Ad 6d 6c 8c Qd Ks 4c Qc Ts 7d
            3s Jd 3s 4c 9d Ad 9d 2c Ts 4d
            9h 5c 8s Kh 7c Th Qs 6d 7s 5c
            9s 5d 7c 4h 2h Jd 2d 9c Qh 7h
            9h Jc    Qh Ac 5s Ah Qd 5s 6s
            8s Td    Kc 2s 4d Ac Js 4h 8h
            8h 4s    Qs Ks 3h Kc Tc 3c 7s
            6h 3h    4s Td As 8c    5h
            3d 2h    3c Jh 7d Kh
                     2s Tc 6h Qc
                     5h 9c 5d Jh
                        8d    Th
        """)
        before = [[card for card in pile ] for pile in s.tableau]
        # move = (9, 1, 2) #-> okay
        # move = (0, 2, 1) #-> okay
        move = (3, 5, 2) #-> fails
        dest_pile, source_idx, number_of_cards = move
        # apply the reverse move
        cards_to_move = s.tableau[source_idx][-number_of_cards:]
        s.tableau[dest_pile].extend(cards_to_move)
        s.tableau[source_idx] = s.tableau[source_idx][:-number_of_cards]
        # apply the move
        r = s.move_card(dest_pile,source_idx, number_of_cards)
        print(r)
        self.assertEqual(before,s.tableau)

if __name__ == '__main__':
    unittest.main(exit=False)