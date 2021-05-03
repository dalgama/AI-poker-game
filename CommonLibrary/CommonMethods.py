import operator as op
import collections


#This method separates out the hand into suits and ranks.
#Input: The poker hand.
#Output: Two lists in a tuple.
def separateRankAndSuit(hand, trainingSet = True):
    #The first number in the slice is the starting index, the second number is the step value.
    if (trainingSet):
        suits = hand[0::2]
        ranks = hand[1::2]
        handValue = suits[-1]
        suits  = suits[:-1]
        return suits, ranks, handValue
    
    suits = hand[1::2]
    ranks = hand[2::2]
    
    return suits, ranks, -1


#This method checks the absolute difference between the value of adjacent cards
#Input: The list of suits and ranks
#Output: A list of the absolute difference between the current and previous card (0 for first index)
def absoluteDifference(hand):
    #Initiliaze an array of 4 elems (initially set to 0)
    absDif = [0]*(len(hand)-1)
    #make sure to sort the hand first
    hand = sorted(hand)
    for i in range(1, len(hand)):
        absDif[i-1] = abs(hand[i]-hand[i-1])

    return absDif

# Test if the elements in the hand are ascending or descending (with respect to suit or rank)
# Input: hand (ranks or suits)
# Output: boolean value indicating whether the cards are ascending or descending 
def elemsAscDesc(hand, isRank=True):
    #make sure to sort the hand first
    absDifLow = absoluteDifference(hand)

    # if there is an ace in the hand, we must also test with aces high
    if (isRank):
        for i in range(0, len(hand)):
            if (hand[i] == 1):
                hand[i] = 14

    absDifHigh = absoluteDifference(hand)

    FLAG1 = True
    FLAG2 = True
    for i in range(1, len(absDifLow)):
        # check to make sure that they are equal and that at least 1 of them is equal to 1
        if (absDifLow[i] != 1):
            FLAG1 = False
        if (absDifHigh[i] != 1):
            FLAG2 = False

    return (FLAG1 or FLAG2)

# Returns whether or not the high card in the hand is an ace. This allows us to separate a Royal Flush from a straight flush.
# Input: hand (ranks or suits)
# Output: Boolean value representing whether or not a ace is present in the deck.
def acePresent(hand):
    if 1 in hand:
        return True
    return False

# Returns the number of zeros present in the absDif array (pairs)
# Input: hand (ranks or suits)
# Output: The number of zeros present in the absoluteDifference array
def numZeros(hand):
    absDif = absoluteDifference(hand)
    count = 0
    for elem in absDif:
        if (elem == 0):
            count += 1
    return count

# Returns the index of all the zeros in the given absoluteDifference array
# Input: hand (ranks or suits)
# Output: The number of zeros present in the absoluteDifference array
def indexOfZeros(absDif):
    indexList = []
    for i in range(0, len(absDif)):
        if (absDif[i] == 0):
            indexList.append(i)
    return indexList

# Returns a boolean that is True if the Zeros in the array are separated and false if not
# Input: hand (ranks or suits)
# Output: The number of zeros present in the absoluteDifference array
def separationOfZeros(hand):
    absDif = absoluteDifference(hand)
    if numZeros(hand) > 1:
        indexListAbsDif = absoluteDifference(indexOfZeros(absDif))
        for elem in indexListAbsDif:
            if (elem != 1):
                return True
    return False

def freqOfRank(ranks):
    freq = {}
    # The last element is ignored as its the hand value.
    for item in ranks:
        if (item in freq): 
            freq[item] += 1
        else: 
            freq[item] = 1

    # Ordering the dictionary in descending order.
    sorted_items=sorted(freq.items(),key = lambda x : x[1], reverse=True)
    sorted_dict = collections.OrderedDict(sorted_items)

    return sorted_dict

# This funtion returns the freqency of each card suit in the hand.
# Input: List that contains the card suits and card ranks. (Last value in the list is ignored as it is the hand value).
# Output: Dictionary with the card suit and the frequency ordered in descending order.
def freqOfSuit(suits):
    freq = {}
    # The last element is ignored as its the hand value.
    for item in suits:
        if (item in freq): 
            freq[item] += 1
        else: 
            freq[item] = 1

    # Ordering the dictionary in descending order.
    sorted_items = sorted(freq.items(),key = lambda x : x[1],reverse=True)
    sorted_dict = collections.OrderedDict(sorted_items)

    return sorted_dict