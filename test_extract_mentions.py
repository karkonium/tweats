'''Tester for the function extract_mentions in tweets.
'''

import unittest
import tweets

class TestExtractMentions(unittest.TestCase):
    """Tester for the function extract_mentions in tweets.
    """

    def test_empty(self):
        """Empty tweet."""
        arg = ''
        actual = tweets.extract_mentions(arg)
        expected = []
        msg = "Expected {}, but returned {}".format(expected, actual)
        self.assertEqual(actual, expected, msg)


    def test_nonempty_no_mention(self):
        """Non-empty tweet with no mentions.
        """
        arg = 'tweet test case'
        actual = tweets.extract_mentions(arg)
        expected = []
        msg = "Expected {}, but returned {}".format(expected, actual)
        self.assertEqual(actual, expected, msg)
    
    
    def test_cases_order(self):
        """Test with a string with mutliple mentions in different cases
        """
        arg = "hi @HEllO can you hear me @helloo @HELLOOO ok bye!"
        expected = ['hello' , 'helloo', 'hellooo']
        actual = tweets.extract_mentions(arg)
        
        msg = "Expected {}, but returned {}".format(expected, actual)
        self.assertEqual(actual, expected, msg)        
    
    def test_repetition(self):
        """Test with a string with same mention with different endings
        """
        arg = "@HEll0@b can you hear me? @hell0?? @HELL0#ok bye!"
        expected = ['hell0' , 'hell0', 'hell0']
        actual = tweets.extract_mentions(arg)
        
        msg = "Expected {}, but returned {}".format(expected, actual)
        self.assertEqual(actual, expected, msg)   
        
    def test_preceeding_mentions(self):
        """Test with mention/mention symbol perceed by different characters
        """
        arg = "#@Yo can you @ hear @@me? aa@aa 1@#ok bye! \n@last"
        expected = ['last']
        actual = tweets.extract_mentions(arg)
        
        msg = "Expected {}, but returned {}".format(expected, actual)
        self.assertEqual(actual, expected, msg)  
        
    def test_following_mentions(self):
        """Test with mentions/mention symbol followed by different character
        """
        arg = "@# can you @ hear @me? @?? @#ok bye! @@last\n"
        expected = ['me']
        actual = tweets.extract_mentions(arg)
        
        msg = "Expected {}, but returned {}".format(expected, actual)
        self.assertEqual(actual, expected, msg) 
        
    def test_joined_mentions(self):
        """Test with mentions joined with other mentions
        """
        arg = "@hi@hello can you @hear@me? @?@? @ok@bye! @a\n@last\n"
        expected = ['hi', 'hear', 'ok', 'a', 'last']
        actual = tweets.extract_mentions(arg)
        
        msg = "Expected {}, but returned {}".format(expected, actual)
        self.assertEqual(actual, expected, msg)         
        
        
    def test_consecutive(self):
        """Test with consecutively occuring mentions
        """
        arg = "@a @can @you @12lol213 @einow3"
        expected = ['a', 'can', 'you', '12lol213' , 'einow3']
        actual = tweets.extract_mentions(arg)
        
        msg = "Expected {}, but returned {}".format(expected, actual)
        self.assertEqual(actual, expected, msg) 
        
   
        
if __name__ == '__main__':
    unittest.main(exit=False)
