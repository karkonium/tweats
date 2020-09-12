"""Tweet Analysis"""

from typing import List, Dict, TextIO, Tuple

HASH_SYMBOL = '#'
MENTION_SYMBOL = '@'
URL_START = 'http'

# Order of data in the file
FILE_DATE_INDEX = 0
FILE_LOCATION_INDEX = 1
FILE_SOURCE_INDEX = 2
FILE_FAVOURITE_INDEX = 3
FILE_RETWEET_INDEX = 4

# Order of data in a tweet tuple
TWEET_TEXT_INDEX = 0
TWEET_DATE_INDEX = 1
TWEET_SOURCE_INDEX = 2
TWEET_FAVOURITE_INDEX = 3
TWEET_RETWEET_INDEX = 4

# Helper functions.

def alnum_prefix(text: str) -> str:
    """Return the alphanumeric prefix of text, converted to
    lowercase. That is, return all characters in text from the
    beginning until the first non-alphanumeric character or until the
    end of text, if text does not contain any non-alphanumeric
    characters.

    >>> alnum_prefix('')
    ''
    >>> alnum_prefix('IamIamIam')
    'iamiamiam'
    >>> alnum_prefix('IamIamIam!!')
    'iamiamiam'
    >>> alnum_prefix('IamIamIam!!andMore')
    'iamiamiam'
    >>> alnum_prefix('$$$money')
    ''
    
    """
    index = 0
    while index < len(text) and text[index].isalnum():
        index += 1
    return text[:index].lower()


def clean_word(word: str) -> str:
    """Return all alphanumeric characters from word, in the same order as
    they appear in word, converted to lowercase.

    >>> clean_word('')
    ''
    >>> clean_word('AlreadyClean?')
    'alreadyclean'
    >>> clean_word('very123mes$_sy?')
    'very123messy'

    """
    cleaned_word = ''
    for char in word.lower():
        if char.isalnum():
            cleaned_word = cleaned_word + char
    return cleaned_word


def extract_words(text: str, phrase: str) -> List[str]:
    """Return a list of all strings in text starting with phrase and followed 
    by a alphanumeric character, converted to lowercase, with duplicates 
    included.
       
    >>> extract_words('Hi @UofT do you like @@cats @CATS #meowmeow', '@')
    ['uoft', 'cats']
    >>> extract_words('#cats are #cute #cats @cat meow @meow', '#')
    ['cats', 'cute', 'cats']
    >>> extract_words('@many @cats$extra @meow?!', '@')
    ['many', 'cats', 'meow']
    >>> extract_words('No valid mentions @! here?', '!')
    []
    
    """
    text_lst = text.split()
    result = []
    
    for element in text_lst:
        # using slicing ensures we won't get an indexing error
        if element.startswith(phrase) and element[1:2].isalnum():
            # we don't want the first char
            result += [alnum_prefix(element[1:])]
            
    return result


def get_usernames(text: List[str]) -> List[int]:
    """ Returns all usernames from text.
    
    >>> get_usernames(['UofTSci:\\n', '20181109190529\\n', 'lol:\\n'])
    [0]
    >>> get_usernames(['UofT:\\n', '<<<EOT\\n', 'lol:\\n'])
    [0, 2]
    
    """
    potential = get_indexes(text, ':\n')
    username = []
    for index in potential:
        # aside from the 1st username, all usernames must be precessed by 
        # '<<<EOT' or by another username
        if (index == potential[0] or text[index - 1] == '<<<EOT\n' or \
        (index - 1) in username):
            username += [index]
    return username


def get_indexes(text: List[str], s: str) -> List[int]:
    """Return indexes of all elements that end with s in text

    >>> get_indexes(['UofTSci:\\n', '20181109190529\\n', 'lol:\\n'], ':\\n')
    [0, 2]
    >>> get_indexes(['UofT:\\n??', '<<<EOT\\n', 'lol:\\n??'], '??') 
    [0, 2]
    
    """
    result = []

    for i in range(len(text)):
        if text[i].endswith(s): 
            result += [i]
            
    return result

    
def find_key(dictonary: dict, v: object) -> object:
    """ Return a key in dicationary that has value of v.
    
    Precondition: value occurs in dictionary once
    
    >>> find_key({'a':1, 'b':2,'c':3}, 3)
    'c'
    >>> find_key({1:'a', 2:'b', 3:'c'}, 'c')
    3
    
    """
    for key in dictonary:
        if dictonary[key] == v:
            result = key
    return result


# Required functions


def extract_mentions(text: str) -> List[str]:
    """Return a list of all mentions in text, converted to lowercase, with
    duplicates included.

    >>> extract_mentions('Hi @UofT do you like @cats @CATS #meowmeow')
    ['uoft', 'cats', 'cats']
    >>> extract_mentions('@cats are #cute @cats @cat meow @meow')
    ['cats', 'cats', 'cat', 'meow']
    >>> extract_mentions('@many @cats$extra @meow?!')
    ['many', 'cats', 'meow']
    >>> extract_mentions('No valid mentions @! here?')
    []
    
    """
    
    return extract_words(text, MENTION_SYMBOL) 
    

def extract_hashtags(text: str) -> List[str]:
    """Return a list of all hashtags in text, converted to lowercase, with no
    duplicates included.

    >>> extract_hashtags('Hi #UofT do you like #cats #CATS @meowmeow')
    ['uoft', 'cats']
    >>> extract_hashtags('#cats are @cute #cat #cats meow #meow')
    ['cats', 'cat', 'meow']
    >>> extract_hashtags('#many #cats$extra #meow?!')
    ['many', 'cats', 'meow']
    >>> extract_hashtags('No valid mentions #! here?')
    []

    """
    all_hashtags = extract_words(text, HASH_SYMBOL)
    
    unique_hashtags = []
    
    # must ensure there are no duplicates
    for hashtags in all_hashtags:
        if hashtags not in unique_hashtags:
            unique_hashtags += [hashtags]

    return unique_hashtags
    
    
def count_words(text: str, words_to_counts: Dict[str, int]) -> None:
    """Update or add new key-value pairs in words_to_counts based on the 
    freqeuncy of each word in text.
    
    >>> words = {'Angola': 2, 'bo': 2, 'China': 2}
    >>> count_words('', words)
    >>> words == {'Angola': 2, 'bo': 2, 'China': 2}
    True
    >>> words = {'11a': 1, '2bo': 2, '3na': 2, 'd4m': 1, 'e5g': 1}
    >>> count_words('11a #2bo @3#na D^*#^^4-m', words)
    >>> words == {'11a': 2, '2bo': 2, '3na': 2, 'd4m': 2, 'e5g': 1}
    True
    
    """
    text1 = text.split()
    text = text1[:]
    # remove all mentions, hashtags and urls
    for word in text1:
        if (word.startswith(MENTION_SYMBOL) or word.startswith(HASH_SYMBOL) or \
            word.startswith(URL_START)):
            text.remove(word)
            
    # clean all words, no empty string
    keys = []
    for word in text:
        cleaned_word = clean_word(word)
        if cleaned_word != '':
            keys += [cleaned_word.lower()]
    
    # loop over the keys, if new key in dictonary, set up key_value, else 
    # update value
    for key in keys:
        # if key already in list, update that value
        if key in words_to_counts:
            words_to_counts[key] = words_to_counts[key] + 1
        else:
            # if key not in list, add it
            words_to_counts[key] = 1


def common_words(words_to_counts: Dict[str, int], num: int) -> None:
    """Update words_to_counts so it has at most num amount of key-value pairs 
    based on highest frequency of words in words_to_count. If there is a tie
    for the num-th spot all words with the same frequency will be discarded.
    
    Precondition: num > 0 
    
    >>> words = {'Angola': 2, 'bo': 2, 'China': 2}
    >>> common_words(words, 3)
    >>> words
    {'Angola': 2, 'bo': 2, 'China': 2}
    >>> words = {'pop': 2, 'bop': 2, 'cop': 2, 'dop': 1}
    >>> common_words(words, 2)
    >>> words
    {}
    
    """
    # get values list
    counts_list = list(words_to_counts.values())
    counts_list.sort()
    counts_list.reverse()
    # now counts goes from have highest to lowest frequencies
    safe_list = []
    
    # choose num number of values to be in safe_list, since counts is properly 
    # sorted they will be the highest values
    for count in counts_list:
        if len(safe_list) < num:
            safe_list += [count] 
    
    # there was have been a tie for the num-th word if there are more count of 
    # the last element in safe_list than in counts
    if len(counts_list) > 0 and safe_list.count(safe_list[-1]) < \
       counts_list.count(safe_list[-1]):
        i = 0
        last_element_count = safe_list.count(safe_list[-1]) 
        while i < last_element_count:
            safe_list.remove(safe_list[-1])
            i += 1

    # remove all keys whose values aren't in safe_list
    words = list(words_to_counts.keys())
    for word in words:
        if words_to_counts[word] not in safe_list:
            words_to_counts.pop(word)
    

def read_tweets(file: TextIO) -> Dict[str, List[tuple]]:
    """Returns a dictionary where the keys are twitter usernames and the 
    values are the user's tweet history in file. Each tweet history is stored
    in a tuple of (tweet text, date, source, favourite count, retweet count).
    
    """
    lines = file.readlines()  
    #only usernames always end in ':\n'
    usernames = get_usernames(lines)
    users_to_tweets = {}
    # between two user names is all of the user's tweet history
    for i in range(len(usernames)):
        if usernames[i] == usernames[-1]:
            users_tweets = lines[usernames[i]:]
        else: 
            users_tweets = lines[usernames[i]:usernames[i + 1]]
        # dividing each tweet's information for the particular user
        tweets_end = get_indexes(users_tweets, '<<<EOT\n')
        tweet_list = []
        start = 1
        for j in tweets_end:
            end = j
            # extracting information from one tweet history
            tweet_data = users_tweets[start:end]
            # getting date, source, favourite count and retweet count 
            tweet_info = tweet_data[0].split(',')
            # getting text of tweet
            tweet_text = ''
            for k in range(1, len(tweet_data)):
                tweet_text += tweet_data[k]
            tweet_list += [(tweet_text.strip(),
                            int(tweet_info[FILE_DATE_INDEX]), 
                            tweet_info[FILE_SOURCE_INDEX], 
                            int(tweet_info[FILE_FAVOURITE_INDEX]), 
                            int(tweet_info[FILE_RETWEET_INDEX][:-1]))]
            start = end + 1
        # putting all information in dictonary where key is lowered username    
        users_to_tweets[users_tweets[0][:-2].lower()] = tweet_list
    return users_to_tweets
    
    
def most_popular(users_to_tweets: Dict[str, List[tuple]], start_date: int, 
                 end_date: int) -> str:
    """Return the username of the Twitter user in users_to_tweets who had the 
    highest popularity (sum of favourite counts and retweet counts for all 
    tweets) on Twitter between the start_date and end_date (inclusive). If two 
    or more users have same populatrity, return the string 'tie'
    
    Precondition: end_date >= start_date
    
    >>> most_popular({'user1':[('1', 110, 'bop', 1, 1), ('1', 112, 'bop', \
    2, 2)],'user2':[('1', 110, 'bop', 2, 2)]}, 109, 111)
    'user2'
    >>> most_popular({'user10':[('1', 110, 'bop', 1, 1), ('1', 112, 'bop', \
    2, 2)],'user20':[('1', 110, 'bop', 2, 2)]}, 1091, 1111)
    'tie'
    
    """
    #For each user
    #get relevant tweets for each user
    users_to_popularity = {}
    for users in users_to_tweets:
        
        users_popularity = 0
        #loop over add each sum to a user's dictionary
        for tweets in users_to_tweets[users]:
            if start_date <= tweets[TWEET_DATE_INDEX] <= end_date:
                users_popularity += (tweets[TWEET_FAVOURITE_INDEX] + 
                                     tweets[TWEET_RETWEET_INDEX])
        users_to_popularity[users] = users_popularity
    
    #get values list and check how many times max occurs
    popularity_values = list(users_to_popularity.values())

    if len(popularity_values) == 0 or \
       popularity_values.count(max(popularity_values)) > 1:
        result = 'tie'
    else:
        result = find_key(users_to_popularity, max(popularity_values))
           
    return result
  

def detect_author(users_to_tweets: Dict[str, List[tuple]], tweet_text: str) -> \
    str:
    """ Return the username of the most likely author of tweet_text, based on
    the hashtags they use in users_to_tweets. If all hashtags in tweet_text are 
    only used by a single user, then return that user's username. Otherwise,
    return the string 'unknown'.
    
    >>> detect_author({'user1': [('#cat rat#', 1, 'pop', 1, 1 ), \
    ('#dog doggy', 1, 'hop', 0, 0)], 'user2': [('#cat', 1, 'dop', 0, 0)]}, \
    'lol #dog')
    'user1'
    >>> detect_author({'user1': [('#cat rat#', 1, 'pop', 1, 1 )], \
    'user2': [('#cat', 1, 'dop', 0, 0)]}, 'lol #rat')
    'unknown'
    
    """
    users_to_hashtags = {}
    wanted_hashtags = extract_hashtags(tweet_text)
    wanted_hashtags.sort()
    
    # Get all hashtags and pair them with their respective users
    for users in users_to_tweets:
        all_tweet_text = ''
        for tweets in users_to_tweets[users]:
                all_tweet_text += (tweets[TWEET_TEXT_INDEX] + ' ')               
        users_to_hashtags[users] = extract_hashtags(all_tweet_text)

    # Revome all hashtags for all users in users_to_hashtags that aren't in 
    # wanted_hashtags
    for users in users_to_hashtags:
        updated_hashtags = []
        for hashtags in users_to_hashtags[users]:
            if hashtags in wanted_hashtags:
                updated_hashtags += [hashtags]
        updated_hashtags.sort()
        users_to_hashtags[users] = updated_hashtags

    users_hashtags_list = list(users_to_hashtags.values())
    
    # There should only be one non-empty hashtags_list and that should have 
    # same value as wanted_hashtags and since they are sorted order 
    # shouldn't matter
    if ((users_hashtags_list.count([]) == len(users_hashtags_list) - 1) and \
        (users_hashtags_list.count(wanted_hashtags) == 1)):
        return find_key(users_to_hashtags, wanted_hashtags)
    else:
        return 'unknown'


if __name__ == '__main__':
    pass

    #import doctest
    #doctest.testmod()
