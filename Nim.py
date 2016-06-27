from abc import ABCMeta, abstractmethod
import os
from copy import deepcopy
import random



class AI:
    """
    Abstract Base class AI.

        The methods defined here:
        getname()
            The implementation of this virtual function is left to the subclasses.
        nextmove(board)
        The implementation of this virtual function is left to the subclasses.
        """
    @abstractmethod
    def getname(self):
        """ Gets the name of the respective player """
        pass

    @abstractmethod
    def nextmove(self, board):
        """ Returns the next move of the player """
        pass
        
        

class MisereAI(AI):
    """ 
        Class MisereAi inherites from abstract base class AI.
        Methods defined here include:

    getname()
        Returns the AI's name.

    nextmove(board)
        Returns the optimal move of the computer if nimsum is not zero, returns a random move if the nimsum is already zero.

    nimsum(heap)
        Calculates the nimsum of the heap.

    optimalmove(heap)
        Calculates the optimal move, by checking the row number and the number of sticks to be removed, in order to make the nimsum zero.	    
        """
    
    def getname(self):
        """ Returns the name of the AI. """
        return "Computer"

    def nextmove(self, board):
        """ Returns the nextmove of the AI. If the nimsum is already 0, then a random move is selected. Calculates the optimal move otherwise."""
        print self.getname(),"'s move"
        heapcopy = board.getboardcopy()
        if self.nimsum(heapcopy) == 0:
            idx = heapcopy.index(max(heapcopy))
            heapcopy[idx] -= random.randint(1, max(heapcopy))
            #print idx, heapcopy[idx]
            return idx, heapcopy[idx]
        else:
            y = self.optimalmove(heapcopy)
            heapcopy[y] ^= self.nimsum(heapcopy)
            #print y, heapcopy[y]
            return y, heapcopy[y]

    def nimsum(self, heap):
        """ Calculates the nimsum. """
        return reduce(lambda x, y: x ^ y, heap)

    def optimalmove(self, heap):
        """ Calculates the optimal move, by checking the row number and the number of sticks to be removed, in order to make the nimsum zero."""
        return [x ^ self.nimsum(heap) < x for x in heap].index(True)

        
        


class player(AI):
    """
    This class defines the attributes of a player. It inherits from AI class.

        Methods defined here are:
        getname()
            Returns the name of the player.

        nextmove(board)
            Takes in raw_input from the players, manipulates the gameboard, and prints the board after the respective player's move. Raises an exception for invalid move.
    """
    def __init__(self):
        """ Initializes the name of the player. AI is named Computer """
        self.name = raw_input("Enter the name of the player")

    def getname(self):
        """ Returns the name of the respective player."""
        return self.name

    def nextmove(self, board):
        """ Responsible for manipulating the board according to the player input. Raises exception for invalid input.""" 
        print self.getname(),"'s move"
        heapcopy = board.getboardcopy()
        str = raw_input("Enter the row and number of sticks to be removed, ex: (2 1): ")
        try:
            if not str:
                raise
            row, num = str.split()
            row = int(row) - 1
            num = int(num)
            if row < 0:
                raise
            if num < 1 or num > heapcopy[row]:
                raise

        except:
            print "Enter valid numbers only\n"
            return self.nextmove(board)

        num = heapcopy[row] - num
        #print row, num
        return row, num

        


class nimboard(object):
    """
    Responsible for creating the board and populating the heap with items.

    Methods defined here include:

    create_nimboard()
        Creates the main game board, and populates the heap, according to the user.

    print_nimboard()
        Prints the board.

    getboardcopy()
        Returns the copy of the playing board.

    moveonboard(board) 
        Manipulates the playing board based on the player's move.
    """
    
    def __init__(self):
        """ Constructor of nimboard, initializes the heap."""

        #os.system('clear')
        self.heap = []
        self.heapsize = None

    def create_nimboard(self):
        """ Creates the playing board."""
        try:
            self.heapsize = int(input("Enter number of heaps in the game: "))
            if(self.heapsize == 0):
                raise
        except:
            print 'Enter numbers only \n'
            return self.create_nimboard()
        for x in range(1,int(self.heapsize)+1):
            try:
                num = int(raw_input("Enter number of matches on heap %d: " % x))
                if(num ==0):
                    raise
                self.heap.append(int(num))
                print
            except:
                print 'Enter numbers only \n'
                return self.create_nimboard()


    def print_nimboard(self):
        """ Prints the board. """

        #os.system('clear')
        num = 0
        for num,row in enumerate(self.heap):
            print num+1,': ',
            for matches in range(1,row+1):
                print '*',
            print

    def getboardcopy(self):
        """ Returns the copy of the playing board. """
        return deepcopy(self.heap)

    def moveonboard(self, row, num):
        """ Manipulates the playing board, based on the player's move. """
        if row <= -1:
            raise
        if row > self.heapsize:
            return False
        if num > -1 and num <= self.heap[row]:
            self.heap[row] = num
            self.print_nimboard()
            return True
        return False

        
def nimgame(p1, p2, board):

    """
    This method manages the game. When the game is over, it prints the name of the winning player.
    """
    #os.system('clear')
    board.print_nimboard()
    interrupt = True
    while interrupt:
        row, num = p1.nextmove(board)
        board.moveonboard(row, num)
        if gameover(board):
            print p1.getname(), "won"
            interrupt = False
            break
        row, num = p2.nextmove(board)
        board.moveonboard(row, num)
        if gameover(board):
            interrupt = False
            print p2.getname(), "won"


def continue_game():
    """ Asks user whether to continue the game or not """
    restart = raw_input("Do you want to try again (Y or N) ?")
    if (restart.lower().startswith('y')):
        return True

def gameover (board):
    """Returns true if there are no items to remove in the heap. Returns false otherwise."""
    heap = board.getboardcopy()
    return all(z == 0 for z in heap)

def main():
    """This is a driver method."""

    raw_input("Press Enter to continue...")
    interrupt = True
    while interrupt:
        board = nimboard()
        board.create_nimboard()
        try:
            #os.system('clear')
            print 'Enter 1 for playing against computer: '
            print 'Enter 2 for playing against 2nd player: '
            option = int(raw_input("Enter your choice"))
            if option == 1:
                nimgame(player(), MisereAI(), board)
                interrupt = continue_game()
            elif option == 2:
                nimgame(player(), player(), board)
                interrupt = continue_game()
        except:
            print "invalid input"

if __name__ == "__main__":
    main()


# In[ ]:

import unittest, sys
import exceptions
#from gameboard import nimboard
#from nimgame import gameover

class TestGameboard(unittest.TestCase):
    """ 
        This is a test suite for checking the Nimgame.
        Methods defined here are 

        test_illegalmove()
            tests if the move made by the player is illegal

        test_winning_condition()
            tests if the game terminates after the winning condition

        test_initialize()
            tests if the board is initialized properly
    """
    def test_illegalmove(self):
        """ tests if the move made by the player is illegal. This is done by checking for removing sticks on the invalid row 
            Enter the heap size lesser than 5 to successfully run this case.
        """
        print "Test for illegal moves. The test cases are hardcoded to check for illegal moves. Enter the heap size lesser than 5 to successfully run this case."
        board = nimboard()
        board.create_nimboard()
        self.assertEqual(board.moveonboard(5,5),False)

    def test_winning_condition(self):
        """ tests if the game terminates after the winning condition has occurred
            Please enter heap size 1 for successfully running this case.
        """
        print "Test for winning condition. The test cases are hardcoded to check for the winning condition. Please enter heap size 1 for successfully running this case."
        board = nimboard()
        board.create_nimboard()
        board.moveonboard(0,0)
        self.assertEqual(gameover(board), True)

    def test_initialize(self):
        """ tests if the board is initialized properly by creating the board and check for gameover immediately 
        """
        print "Test for initialization"
        board=nimboard()
        board.create_nimboard()
        self.assertEqual(gameover(board), False)


suite1 = unittest.TestLoader().loadTestsFromTestCase(TestGameboard)
unittest.TextTestRunner().run(suite1)
