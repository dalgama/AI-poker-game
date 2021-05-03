import os.path
from os import path
from numpy import genfromtxt, savetxt, count_nonzero
from CommonLibrary import CommonMethods as cm

# This funtion returns the freqency of each card suit in the hand.
# Input: List that contains the card rank. (Last value in the list is ignored as it is the hand value).
# Output: Dictionary with the card rank and the frequency ordered in descending order.
def freqOfRank(ranks):
    freq = {}
    # The last element is ignored as its the hand value.
    for item in ranks:
        if (item in freq): 
            freq[item] += 1
        else: 
            freq[item] = 1
    return freq

# This funtion returns the freqency of each card suit in the hand.
# Input: List that contains the card suits. (Last value in the list is ignored as it is the hand value).
# Output: Dictionary with the card suit and the frequency ordered in descending order.
def freqOfSuit(suits):
    freq = {}
    # The last element is ignored as its the hand value.
    for item in suits:
        if (item in freq): 
            freq[item] += 1
        else: 
            freq[item] = 1
    return freq
# This function calculates the freqency of an element in the list.
# Input: A list with elements
# Output: A dictionary of all the elements in the list and thier frequency.
def freqency(list):
    freq = {}
    # The last element is ignored as its the hand value.
    for item in list:
        if (item in freq): 
            freq[item] += 1
        else: 
            freq[item] = 1
    return freq

# This funtion check is the hand is a flush for the given hand (suits)
# Input: the suits of the current hand and number of different suits that should be in the current hand
# Output: a dictionary
def flushTraining(l, size=None):
    freq_S = freqOfSuit(l)
    #get a list of on the freqency of all the suits in the hand and create a dictionary which returns the suit and freqency of each the suits
    freq = freqency(list(freq_S.values()))
    result = list(freq.values())
    #makes the list in descending order.
    result.sort(reverse=True)
    # adds a zero to the list if the length of the result list is smaller than the size if the length of the result list in bigger than the size then we pop the last value.
    if(size is not None):
        while(len(result) < size):
            result += [0]
        while (len(result) > size):
            result.pop()
    return result

# This funtion goes though the ranks and suits of the current hand and checks if the current had is a royal flush.
# Input: the suits and ranks of the current hand.
# Output: Returns 9 if the hand is a royalflush and 0 if not
def royalFlush(suit,rank):
    Flush = ['1.0','10.0','11.0','12.0','13.0']
    current= []
    suitType = "NULL"
    for s in suit:
        if (suitType == "NULL"):
            suitType = str(s)
        if (str(s) != suitType and suitType != "NULL"):
            return 0

    for r in rank:
        if(str(r) not in Flush):
            return 0
        if( r not in current and str(r) in Flush):
            current.append(str(r))

    current.sort()
    if (Flush == current):
        return 9
    else: 
        return 0

# This funtion goes though the ranks and suits of the current hand and checks if the current had is a straight flush.
# Input: the suits and ranks of the current hand.
# Output: Returns 8 if the hand is a straight flush and 0 if not
def straight_Flush(suit,rank):
    diff= []
    suitType = "NULL"
    for s in suit:
        if (suitType == "NULL"):
            suitType = str(s)
        if (str(s) != suitType and suitType != "NULL"):
            return 0
    rank.sort()
    for i in range(len(rank)-1):
        if (rank[i+1] - rank[i] == 1):
            diff.append('1')

    if(all(x == diff[0] for x in diff) == True and len(diff) == 4):   
        return 8
    else:
        return 0

# This funtion goes though the ranks of the current hand and checks if the current had is a four of a kind.
# Input: the ranks of the current hand.
# Output: Returns 7 if the hand is a four of a kind and 0 if not
def four_o_k(rank): 
    counter = 0
      
    for i in rank:
        curr_frequency = count_nonzero(rank == i)
        if(curr_frequency > counter): 
            counter = curr_frequency 
    if (counter == 4):
        return 7
    else:
        return 0 

# This funtion goes though the ranks of the current hand and checks if the current had is a full house.
# Input: the ranks of the current hand.
# Output: Returns 6 if the hand is a full house and 0 if not
def fullHouse(rank):
    counter = 0
    counter2 = 0
    num = rank[0]
    num2 = rank[1]
      
    for r in rank:
        curr_frequency = count_nonzero(rank == r)
        if(curr_frequency > counter): 
            counter = curr_frequency
            num = r

    for i in rank:
        curr_frequency2 = count_nonzero(rank == i)
        if(curr_frequency2 > counter2 and i != num): 
            counter2 = curr_frequency2
            num2 = i

    if ((counter == 2 and counter2 == 3) or (counter == 3 and counter2 == 2)):
        return 6
    else:
        return 0

# This funtion goes though the suits of the current hand and checks if the current had is a flush.
# Input: the suits of the current hand.
# Output: Returns 5 if the hand is a flush and 0 if not
def flushh(suit):
    suitType = "NULL"
    for s in suit:
        if (suitType == "NULL"):
            suitType = str(s)
        if (str(s) != suitType and suitType != "NULL"):
            return 0
    if (suitType != "NULL"):
        return 5
    else:
        return 0

# This funtion goes though the ranks of the current hand and checks if the current had is a straight.
# Input: the ranks of the current hand.
# Output: Returns 4 if the hand is a straight and 0 if not
def straighth(rank):
    diff= []
    rank.sort()
    for i in range(len(rank)-1):
        if (rank[i+1] - rank[i] == 1):
            diff.append('1')

    if(all(x == diff[0] for x in diff) == True and len(diff) == 4):   
        return 4
    else:
        return 0

# This funtion goes though the ranks of the current hand and checks if the current had is a three of a kind.
# Input: the ranks of the current hand.
# Output: Returns 3 if the hand is a three of a kind and 0 if not
def three_o_k(rank): 
    counter = 0
      
    for i in rank:
        curr_frequency = count_nonzero(rank == i)
        if(curr_frequency > counter): 
            counter = curr_frequency 
    if (counter == 3):
        return 3
    else:
        return 0 

# This funtion goes though the ranks of the current hand and checks if the current had is a two pair.
# Input: the ranks of the current hand.
# Output: Returns 2 if the hand is a two pair and 0 if not
def two_pair(rank):
    counter = 0
    counter2 = 0
    num = rank[0]
    num2 = rank[1]
      
    for r in rank:
        curr_frequency = count_nonzero(rank == r)
        if(curr_frequency > counter): 
            counter = curr_frequency
            num = r

    for i in rank:
        curr_frequency2 = count_nonzero(rank == i)
        if(curr_frequency2 > counter2 and i != num): 
            counter2 = curr_frequency2
            num2 = i

    if (counter == 2 and counter2 == 2):
        return 2
    else:
        return 0

# This funtion goes though the ranks of the current hand and checks if the current had is a pair.
# Input: the ranks of the current hand.
# Output: Returns 1 if the hand is a pair and 0 if not
def pair(rank): 
    counter = 0
      
    for i in rank:
        curr_frequency = count_nonzero(rank == i)
        if(curr_frequency > counter): 
            counter = curr_frequency 
    if (counter == 2):
        return 1
    else:
        return 0

# This funtion generates the features for the given hand.
# Input: the current hand and which set it is given (training or test)
# Output: a list will integers.
def generateFeatures(hand,set):
    #Separates the ranks and suits from the hand
    hand_suits, hand_ranks, handvalue = cm.separateRankAndSuit(hand)
    Hand = 0

    # check if the hand is a flush
    sh = flushTraining(hand_suits, 4)
    flush = int(sh[0] == 1 and sh[1] == 0)

    freq = freqOfRank(hand_ranks)
    h = list(freq.values())
    #Sorted from highest to lowest
    h.sort(reverse=True)
    # The most common card regardless of suit.
    Rank1 = h[0]
    # The second most common card regardless of suit.
    Rank2 = h[1]

    hand_ranks.sort()
    # High is the highest card in the hand
    # Low is the lowest card in the hand.
    if(1 in hand_ranks):
        highest = 1
        lowest = hand_ranks[0]
        if lowest == 1:
            lowest = hand_ranks[1]
    else:

        highest = hand_ranks[-1]
        lowest = hand_ranks[0]

    normalized = [(r - lowest + 13)%13 for r in hand_ranks]
    normalized.sort()
    straight = normalized[-1] == 4
    if (set == "test"):
        # the code below chercks if what the current hand is (eg. pairs, two_pair) and assigns it the value assigned to that specific hand in the dataset.
        pair_h = pair(hand_ranks)
        if(pair_h > Hand):
            Hand = pair_h

        t_pair = two_pair(hand_ranks)
        if(t_pair > Hand):
            Hand = t_pair

        three_o_k_h = three_o_k(hand_ranks)
        if(three_o_k_h  > Hand):
            Hand = three_o_k_h 

        straight_h = straighth(hand_ranks)
        if(straight_h > Hand):
            Hand = straight_h

        flush_h = flushh(hand_suits)
        if(flush_h > Hand):
            Hand = flush_h

        fullHouse_h = fullHouse(hand_ranks)
        if(fullHouse_h > Hand):
            Hand = fullHouse_h

        four_o_k_h = four_o_k(hand_ranks)
        if(four_o_k_h > Hand):
            Hand = four_o_k_h

        straight_Flush_h = straight_Flush(hand_suits, hand_ranks)
        if(straight_Flush_h > Hand):
            Hand = straight_Flush_h

        royalFlush_h = royalFlush(hand_suits, hand_ranks)
        if(royalFlush_h > Hand):
            Hand = royalFlush_h

        return [flush, Rank1, Rank2, highest, lowest, straight,Hand]
    else:
        return [flush, Rank1, Rank2, highest, lowest, straight]

# This funtion creates the two files with all the features which will be later used for training the model.
# Input:None
# Output: None
def createFeatureFiles():
    # ________________________________Training set_____________________________________________
    # Column title row is ignored
    train_dataset = genfromtxt(open('Data/train.csv','r'), delimiter=',', dtype='f8')[1:]
    #list to store all the features for each row in the training set.
    ptrain = []
    # Appends all the features for the train set, created from the generateFeatures function.
    for x in train_dataset:
        y = x[-1]
        train_features = generateFeatures(x[:-1], "train")
        ptrain.append(train_features+[y])
    # Creating and saving all the features created above into a "new" file which will later be used for training and testing the model.
    if(path.exists("Data/trainFeatures.csv") == False):
        savetxt("Data/trainFeatures.csv",ptrain, delimiter=',', fmt='%d,%d,%d,%d,%d,%d,%d', 
            header='Flush,Rank1,Rank2,Highest,Lowest,Straight,Hand', comments = '')

    # Handler to prevent overwriting any file with the same name.
    else:
        print("!! A file with this name already exists in this file path mate, call me back when it's gone !!")
        return
    # ________________________________Test set_____________________________________________
    # Column title row is ignored
    test_dataset = genfromtxt(open('Data/test.csv','r'), delimiter=',', dtype='f8')[1:]
    #list to store all the features for each row in the test set.
    ptest = []
    # Appends all the features for the test set, created from the generateFeatures function.
    for x in test_dataset:
        test_features = generateFeatures(x[1:], "test")
        id = x[0]
        ptest.append([id]+test_features)

    # Creating an saving all the features created above into a "new" file which will later be used for training and testing the model.
    if(path.exists("Data/testFeatures.csv") == False):
        savetxt("Data/testFeatures.csv",ptest, delimiter=',', fmt='%d,%d,%d,%d,%d,%d,%d,%d', 
            header='id,Flush,Rank1,Rank2,Highest,Lowest,Straight,Hand', comments = '')

    # Handler to prevent overwriting any file with the same name.
    else:
        print("!! A file with this name already exists in this file path mate, call me back when it's gone !!")
        return

