import unittest
from SpiderSolitar import SpiderSolitaire
from spider_reverse import max_cards_placed
from spider_parser import card_from_string


class TestAllowedCardMove(unittest.TestCase):
    def test_empty_pile(self):
        pile = []
        cards = max_cards_placed(pile)
        self.assertEqual(cards,0)

    def test_single_card(self):
        pile = [card_from_string("Ks")]
        cards = max_cards_placed(pile)
        self.assertEqual(cards,1)
        
    def test_two_different_cards(self):
        pile_str = "Ks 7h"
        pile = [card_from_string(str) for str in pile_str.split()]
        cards = max_cards_placed(pile)
        self.assertEqual(cards,0)
    
    def test_two_card_sequence_different_suite(self):
        pile_str = "Ks Qh"
        pile = [card_from_string(str) for str in pile_str.split()]
        cards = max_cards_placed(pile)
        self.assertEqual(cards,1)
        
    def test_two_card_sequence_same_suite(self):
        pile_str = "Kh Qh"
        pile = [card_from_string(str) for str in pile_str.split()]
        cards = max_cards_placed(pile)
        self.assertEqual(cards,2)
        
    def test_five_card_sequence_different_suite(self):
        pile_str = "Kh Qh Js Ts 9s"
        pile = [card_from_string(str) for str in pile_str.split()]
        cards = max_cards_placed(pile)
        self.assertEqual(cards,3)
        
    def test_five_card_sequence_same_suite(self):
        pile_str = "7h Ah Js Ts 9s 8s 7s"
        pile = [card_from_string(str) for str in pile_str.split()]
        cards = max_cards_placed(pile)
        self.assertEqual(cards,4)
        
    def test_different_suite_at_end_of_sequence(self):
        pile_str = "7h Ah Js Ts 9s 8s 7s 6c"
        pile = [card_from_string(str) for str in pile_str.split()]
        cards = max_cards_placed(pile)
        self.assertEqual(cards,1)


class TestConnectedCards(unittest.TestCase):
    def test_empty_pile(self):
        pile = []
        cards = SpiderSolitaire.num_connected_cards(pile)
        self.assertEqual(cards,0)

    def test_single_card(self):
        pile = [card_from_string("Ks")]
        cards = SpiderSolitaire.num_connected_cards(pile)
        self.assertEqual(cards,1)
        
    def test_two_different_cards(self):
        pile_str = "Ks 7h"
        pile = [card_from_string(str) for str in pile_str.split()]
        cards = SpiderSolitaire.num_connected_cards(pile)
        self.assertEqual(cards,1)
    
    def test_two_card_sequence_different_suite(self):
        pile_str = "Ks Qh"
        pile = [card_from_string(str) for str in pile_str.split()]
        cards = SpiderSolitaire.num_connected_cards(pile)
        self.assertEqual(cards,1)
        
    def test_two_card_sequence_same_suite(self):
        pile_str = "Kh Qh"
        pile = [card_from_string(str) for str in pile_str.split()]
        cards = SpiderSolitaire.num_connected_cards(pile)
        self.assertEqual(cards,2)
        
    def test_five_card_sequence_different_suite(self):
        pile_str = "Kh Qh Js Ts 9s"
        pile = [card_from_string(str) for str in pile_str.split()]
        cards = SpiderSolitaire.num_connected_cards(pile)
        self.assertEqual(cards,3)
        
    def test_five_card_sequence_same_suite(self):
        pile_str = "7h Ah Js Ts 9s 8s 7s"
        pile = [card_from_string(str) for str in pile_str.split()]
        cards = SpiderSolitaire.num_connected_cards(pile)
        self.assertEqual(cards,5)
        
    def test_different_suite_at_end_of_sequence(self):
        pile_str = "7h Ah Js Ts 9s 8s 7s 6c"
        pile = [card_from_string(str) for str in pile_str.split()]
        cards = SpiderSolitaire.num_connected_cards(pile)
        self.assertEqual(cards,1)