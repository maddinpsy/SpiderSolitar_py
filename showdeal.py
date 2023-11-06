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

from    webresults  import  *

try :
    game = int(sys.argv[1])
except :
    print "Tell me a deal number to print the cards for."
    sys.exit(254)



print "Game number", game
print

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

            print   "%s%3s" % ( spc, cnam ),
            spc     = " "
        else :
            print   "%s%3s" % ( spc, ""   ),
        pass

    print

    i   += 1

print

i   = len(cards[DECK_STK])
for di in range(0, 5) :
    spc           = ""
    for si in range(PLAY_STKS, PLAY_STKS + PLAY_STK_CNT) :
        i        -= 1
        ( n, s )  = get_card(cards, DECK_STK, i)

        cnam      = card_name(n, s)

        print   "%s%3s" % ( spc, cnam ),
        spc     = " "

    print

    pass

print





#
#
#
# eof
