#!/usr/bin/python

# showdeal.py
#       April 8, 2005           bar
#       October 20, 2014        bar     no CRLF
#       October 22, 2014        bar     comment
#       October 26, 2014        bar     PySol code fixed
#
#
#       Print out a Spider deal.
#
#       PySol
#           self.moves.history is list of lists of dictionaries
#               dictionaries have "from_stack_id" : 0isdeck 9isfirstcol 1..8areUp          "to_stack_id" : N        "ncards" : N
#               deals move 1 card at a time - 10 cards moved from column 0 to the play columns - one card moved per dictionary
#               moving Up moves ncards:13 to column 1..8
#
#           Code to go in to game.py, called by self.save_in_plspider_move_format(filename) at the end of _saveGame():
#               And the number of cards moved must be changed to which card is the bottom card moved. (len(cards[stack_num]) - ncards_moved)
#
#   def save_in_plspider_move_format(me, fn) :
#       if  me.getTitleName() == 'Spider' :
#           import  os, re
#           fn  = os.path.splitext(fn)[0] + ".pysol_moves"
#           fo  = open(fn, "wt")
#           scs = int(max(0, me.stats.elapsed_time))
#           hs  = []
#           for i in xrange(len(me.moves.history)) :
#               # fo.write(repr(m) + '\n')
#               m   = me.moves.history[i]
#               ma  = []
#               for i in xrange(len(m)) :
#                   mm  = m[i]
#                   if  hasattr(mm, 'from_stack_id') and hasattr(mm, 'to_stack_id') and hasattr(mm, 'ncards') :
#                       ma.append(mm)
#                   pass
#               if  len(ma) in [ 1, 10 ] :
#                   hs.append(ma)
#               pass
#           fo.write("%s %5u %3u:%02u %5u seconds 9999 keys %4u moves %2u empties V9.99 %s " % (
#                                                                                                   ((me.finished and 'Won ') or 'Lost'),
#                                                                                                   me.random.initial_seed,
#                                                                                                   scs / 60,
#                                                                                                   scs % 60,
#                                                                                                   scs,
#                                                                                                   len(hs),
#                                                                                                   (me.finished and 10) or 0,
#                                                                                                   time.strftime("%a, %d %b %Y %H:%M:%S GMT",
#                                                                                                   time.gmtime()),
#                                                                                              )
#                   )
#           for ma in hs :
#               if  len(ma) == 10 :
#                   fo.write("D ")
#               elif len(ma) == 1 :
#                   mv  = ma[0]
#                   if (mv.ncards == 13) and (1 <= mv.to_stack_id <= 8) :
#                       fo.write("%uC " % (mv.from_stack_id - 8))
#                   else :
#                       fo.write("%u#%u>%u " % ( mv.from_stack_id - 8, mv.ncards, mv.to_stack_id - 8, ))
#                   pass
#               pass
#           fo.write("\n")
#           fo.close()
#       pass
#
#
#
#
#

import  sys

CLUBS           = 0x00
SPADES          = 0x10
HEARTS          = 0x20
DIAMONDS        = 0x30

ACE             =  1
KING            = 13


DECK_STK        =   0

PLAY_STKS       =   1
PLAY_STK_CNT    =   10

UP_STKS         =   PLAY_STKS + PLAY_STK_CNT
UP_STK_CNT      =   8

TOT_STKS        =   UP_STKS   + UP_STK_CNT


game = 31410

def card_name(n, s) :
    if  n  == ACE       :
        n  = "A"
    elif n == KING      :
        n  = "K"
    elif n == KING - 1  :
        n  = "Q"
    elif n == KING - 2  :
        n  = "J"
    else                :
        n  = str(n)

    if  s  == CLUBS     :
        s  = "C"
    elif s == SPADES    :
        s  = "S"
    elif s == HEARTS    :
        s  = "H"
    elif s == DIAMONDS  :
        s  = "D"

    return("%2s%s" % ( n, s ))



def get_card(cards, stknum, pos) :
    c = abs(cards[stknum][pos])
    return( ( c & 0xf, c & 0xf0 ) )

def move_cards(cards, f_stknum, f_pos, t_stknum) :

    committed        = False
    if  (f_pos > 0) and (get_card(cards, f_stknum, f_pos)[0] + 1 != get_card(cards, f_stknum, f_pos - 1)[0]) :
        committed    = True

    cards[t_stknum] += cards[f_stknum][f_pos:]
    del(cards[f_stknum][f_pos:])

    hite = len(cards[f_stknum])
    if  hite  > 0 :
        hite -= 1
        cards[f_stknum][hite] = abs(cards[f_stknum][hite])          # flip any top hidden card
        return(True)

    return(committed)

def flip_top_card(cards, stknum) :
    hite = len(cards[stknum])
    if  hite > 0 :
        hite -= 1
        cards[stknum][hite] = -cards[stknum][hite]                  # flip the top card
    pass

def deal_a_round(cards, mask, face_down) :
    for si in range(PLAY_STKS, PLAY_STKS + PLAY_STK_CNT) :
        if  mask & (1 << si) :
            pos = len(cards[DECK_STK]) - 1
            move_cards(cards, DECK_STK, pos, si)
            if  face_down :
                flip_top_card(cards, si)
            pass
        pass
    pass



def deal(deck) :
    cards = []
    cards.append(deck)
    for stknum in range(DECK_STK + 1, TOT_STKS) :
        stk = []
        cards.append(stk)

    for i in range(0, 4) :
        deal_a_round(cards, 0x7fe, True)

    deal_a_round(    cards, 0x492, True)

    deal_a_round(    cards, 0x7fe, False)

    return(cards)



def shuffle(game) :

    def get_random_index(seed, i) :
        seed = (seed * 214013 + 2531011 ) & 0x7FFFffff
        return( ( seed, int(seed >> 16) % (i + 1) ) )

    deck = []
    for dn in range(0, 2) :
        for suit in range(CLUBS, DIAMONDS + SPADES, SPADES) :
            for   crd in range(ACE, KING + 1) :
                deck.append(suit + crd)
            pass
        pass

    seed = game

    for i in range(len(deck) - 1, -1, -1) :
        (seed, si)  = get_random_index(seed, i)
        ( deck[si], deck[i] ) = ( deck[i], deck[si] )

    return(deck)


print("Game number", game)
print()

cards   = deal(shuffle(game))

i       = 0
while   True :
    done = True
    for si in range(PLAY_STKS, PLAY_STKS + PLAY_STK_CNT) :
        if  len(cards[si]) > i :
            done = False
            break
        pass
    if  done : break

    spc   = ""
    for si in range(PLAY_STKS, PLAY_STKS + PLAY_STK_CNT) :
        if  len(cards[si]) > i :
            shown = True
            ( n, s )  = get_card(cards, si, i)

            cnam    = card_name(n, s)

            print   ("%s%3s" % ( spc, cnam ), end="")
            spc     = " "
        else :
            print   ("%s%3s" % ( spc, ""   ), end="")
        pass

    print()

    i   += 1

print()

i   = len(cards[DECK_STK])
for di in range(0, 5) :
    spc           = ""
    for si in range(PLAY_STKS, PLAY_STKS + PLAY_STK_CNT) :
        i        -= 1
        ( n, s )  = get_card(cards, DECK_STK, i)

        cnam      = card_name(n, s)

        print  ( "%s%3s" % ( spc, cnam ), end="")
        spc     = " "

    print()

    pass

print()





#
#
#
# eof
