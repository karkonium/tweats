"""Tester for the function common_words in tweets.
"""

import unittest
import tweets

class TestCommonWords(unittest.TestCase):
    """Tests for the function common_words in tweets.
    """

    def test_empty(self):
        """Test below the limit with an Empty dictionary with limit of 1 
        word-count pair. 
        """

        arg1 = {}
        arg2 = 1
        exp_arg1 = {}
        act_return = tweets.common_words(arg1, arg2)
        exp_return = None

        msg = "Expected {}, but returned {}".format(exp_return, act_return)
        self.assertEqual(act_return, exp_return, msg)

        msg = ("Expected dictionary to be\n {}, " +
               "but it was\n {}").format(exp_arg1, arg1)
        self.assertEqual(arg1, exp_arg1, msg)


    def test_one_word_limit_one(self):
        """Test at the limit with dictionary of lenght 1 and limit of 1 
        word-count pair.
        """

        arg1 = {'hello': 2}
        arg2 = 1
        exp_arg1 = {'hello': 2}
        act_return = tweets.common_words(arg1, arg2)
        exp_return = None

        msg = "Expected {}, but returned {}".format(exp_return, act_return)
        self.assertEqual(act_return, exp_return, msg)

        msg = ("Expected dictionary to be {}\n, " +
               "but it was\n {}").format(exp_arg1, arg1)
        self.assertEqual(arg1, exp_arg1, msg)


    def test_same_lenght_limit(self):
        """Test at the limit with Dictionary of lenght of 4 and limit of 4 
        word-count pairs. Where there are two occarnces of lowest count.
        """

        arg1 = {'hello': 5, 'hey': 3, 'wagwan': 4, 'yo': 3}
        arg2 = 4
        exp_arg1 = {'hello': 5, 'hey': 3, 'wagwan': 4, 'yo': 3}
        act_return = tweets.common_words(arg1, arg2)
        exp_return = None

        msg = "Expected {}, but returned {}".format(exp_return, act_return)
        self.assertEqual(act_return, exp_return, msg)

        msg = ("Expected dictionary to be {}\n, " +
               "but it was\n {}").format(exp_arg1, arg1)
        self.assertEqual(arg1, exp_arg1, msg)
        
        
    def test_larger_limit(self):
        """Test below the limit with Dictionary lenght of 5 and limit of 6 
        word-count pairs. Where all words have same counts.
        """

        arg1 = {'hel': 5, 'he': 5, 'wag1': 5, 'yo': 5, '23': 5}
        arg2 = 6
        exp_arg1 = {'hel': 5, 'he': 5, 'wag1': 5, 'yo': 5, '23': 5}
        act_return = tweets.common_words(arg1, arg2)
        exp_return = None

        msg = "Expected {}, but returned {}".format(exp_return, act_return)
        self.assertEqual(act_return, exp_return, msg)

        msg = ("Expected dictionary to be {}\n, " +
               "but it was\n {}").format(exp_arg1, arg1)
        self.assertEqual(arg1, exp_arg1, msg)
            
               
    def test_no_tie_excat_limit(self):
        """Test the dictionary with no repeating values and the limit is excatly
        equal to the lenght of dictionary.
        """

        arg1 = {'hel': 5, 'he': 4, 'wag1': 3, 'yo': 2, '23': 1}
        arg2 = 5
        exp_arg1 = {'hel': 5, 'he': 4, 'wag1': 3, 'yo': 2, '23': 1}
        act_return = tweets.common_words(arg1, arg2)
        exp_return = None

        msg = "Expected {}, but returned {}".format(exp_return, act_return)
        self.assertEqual(act_return, exp_return, msg)

        msg = ("Expected dictionary to be {}\n, " +
               "but it was\n {}").format(exp_arg1, arg1)
        self.assertEqual(arg1, exp_arg1, msg)        


    def test_smaller_limit(self):
        """Test below the limit with Dictionary lenght of 4 and limit of 3 
        word-count pairs. Where all word counts are different.
        """

        arg1 = {'1lol1': 5, 'h1ey': 4, 'wa0gwan': 3, 'y0o': 2}
        arg2 = 3
        exp_arg1 = {'1lol1': 5, 'h1ey': 4, 'wa0gwan': 3}
        act_return = tweets.common_words(arg1, arg2)
        exp_return = None

        msg = "Expected {}, but returned {}".format(exp_return, act_return)
        self.assertEqual(act_return, exp_return, msg)

        msg = ("Expected dictionary to be {}\n, " +
               "but it was\n {}").format(exp_arg1, arg1)
        self.assertEqual(arg1, exp_arg1, msg)   
        
    
    def test_smaller_limit_repetition(self):
        """Test below the limit with Dictionary with lenght of 5 and limit of 3 
        word-count pairs. Where there are 2 occurances of a non-lowest count. 
        There is no tie for n-th spot.
        """

        arg1 = {'1lol1': 5, 'h1ey': 4, 'wa0gwan': 3, 'y0o': 2, 'hi':4}
        arg2 = 3
        exp_arg1 = {'1lol1': 5, 'h1ey': 4, 'hi':4}
        act_return = tweets.common_words(arg1, arg2)
        exp_return = None

        msg = "Expected {}, but returned {}".format(exp_return, act_return)
        self.assertEqual(act_return, exp_return, msg)

        msg = ("Expected dictionary to be {}\n, " +
               "but it was\n {}").format(exp_arg1, arg1)
        self.assertEqual(arg1, exp_arg1, msg)   
        
        
    def test_mutliple_ties(self):
        """Test below the limit with Dictionary with lenght of 5 and limit of 4 
        word-count pairs. Where lowest count occurs twice.
        """

        arg1 = {'hel': 5, 'he': 5, 'wag1': 4, 'yo': 3, '23': 3}
        arg2 = 4
        exp_arg1 = {'hel': 5, 'he': 5, 'wag1': 4}
        act_return = tweets.common_words(arg1, arg2)
        exp_return = None

        msg = "Expected {}, but returned {}".format(exp_return, act_return)
        self.assertEqual(act_return, exp_return, msg)

        msg = ("Expected dictionary to be {}\n, " +
               "but it was\n {}").format(exp_arg1, arg1)
        self.assertEqual(arg1, exp_arg1, msg)
    
    
    def test_lowest_all_tie_count(self):
        """Test below the limit with Dictionary with lenght of 5 and limit of 3
        word-count pairs. Where there is a tie for all 3 spots.
        """

        arg1 = {'hel': 5, 'he': 5, 'wag1': 5, 'yo': 5, '23': 3}
        arg2 = 3
        exp_arg1 = {}
        act_return = tweets.common_words(arg1, arg2)
        exp_return = None

        msg = "Expected {}, but returned {}".format(exp_return, act_return)
        self.assertEqual(act_return, exp_return, msg)

        msg = ("Expected dictionary to be {}\n, " +
               "but it was\n {}").format(exp_arg1, arg1)
        self.assertEqual(arg1, exp_arg1, msg)          

        
if __name__ == '__main__':
    unittest.main(exit=False)
