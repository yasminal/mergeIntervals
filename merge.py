import csv

class Interval:
    def __init__(self, start = None, end = None, mergedIntervals = [], mergedFlag = False):
        self.left = None
        self.right = None
        self.start = start
        self.end = end
        self.mergedFlag = False # Indicates whether an interval has previously been merged before or not
        self.mergedIntervals = []

# minValueNode() finds the earliest interval in the tree
def minValueNode(node): 
    current = node 
    while(current.left is not None): 
        current = current.left  
    return current  

# computeMerged() determines the resulting start and end values
# for two overlapping intervals
def computeMerged(self, node):
    new = Interval()
    new.start = min(node.start, self.start) 
    new.end = max(node.end, self.end)
    new.mergedIntervals = self.mergedIntervals

    if node.mergedFlag == False:
        new.mergedIntervals.append(node)

    elif node.mergedIntervals != []:
        for i in node.mergedIntervals:
            new.mergedIntervals.append(i)

    new.mergedFlag = True

    return new

# isOverlapping() checks whether two given intervals
# overlap over a given merge distance
def isOverlapping(self, interval, mergeDist):  
    if ((self.start < interval.start - mergeDist  and self.end < interval.start - mergeDist) or 
                (self.start > interval.end + mergeDist and self.end > interval.end + mergeDist)):
        return False
    else:
        return True

# findMaxforN() finds the largest value in the tree that's smaller than
# or equal to the start of the new interval to merge
# Adapted from geeksforgeeks.org
def findMaxforN(root, N): 
      
    # Base cases  
    if root is None: 
        return -1
    if root.start == N:  
        return root 
  
    # If root's value is smaller, try in  
    # right subtree  
    elif root.start < N:  
        res = findMaxforN(root.right, N)  
        if res == -1: 
            return root
        else: 
            return res
  
    # If root's key is greater, return  
    # value from left subtree.  
    elif root.start > N:  
        return findMaxforN(root.left, N) 

# inOrderSuccessor() returns the next interval starting after a given interval n
# Adapted from geeksforgeeks.org
def inOrderSuccessor(root, n):  
    if (n.right is not None): 
        return minValueNode(n.right); 
  
    succ = Interval(None, None) 
  
    # Start from root and search for successor down the tree 
    while (root is not None):
        if (n.start < root.start):
            succ = root
            root = root.left
        elif (n.start >= root.start):
            root = root.right
        else:
           break
    return succ

# mergeInterval() merges or inserts new intervals, depending
# on whether they overlap with existing intervals over a specified 
# merge distance
def mergeInterval(root, newInt, mergeDist):
    if (root == None):
        root = insert(root, newInt)            
        return root

    else:
        found = findMaxforN(root, newInt.start)

        if (found == -1): #  This means the new interval needs to be inserted at the beginning
            nextInterval = minValueNode(root) 
            
            ## If new end overlaps with start of next interval, merge
            if (newInt.end >= nextInterval.start - mergeDist): 
                merged = computeMerged(nextInterval, newInt)
                root = delete(root, nextInterval)
                if root:
                    return mergeInterval(root, merged, mergeDist)
                else:
                    return merged

            ## Otherwise: insert
            else:
                root = insert(root, newInt)
            return root

        else:   
            ## Skip if full overlap or enclosing
            if ((found.start <= newInt.start and found.end >= newInt.end)):
                found.mergedIntervals.append(newInt)
                found.mergedFlag = True
                return root ## was: root, changed to found because overlapping didn't add 

            ## Insert new interval if no overlap exists
            if (isOverlapping(found, newInt, mergeDist) is False):
                nextInterval = inOrderSuccessor(root, found)

                if (nextInterval.start is None):
                    root = insert(root, newInt)
                    return root

                ## If new end overlaps with start of next interval, merge
                elif (newInt.end >= nextInterval.start - mergeDist): 
                    merged = computeMerged(nextInterval, newInt)
                    root = delete(root, nextInterval)
                    if root:
                        return mergeInterval(root, merged, mergeDist)
                    else:
                        return merged

                ## Otherwise: insert
                else:
                    root = insert(root, newInt)
                    return root

            ## Otherwise merge values if intervals overlap
            else:
                merged = computeMerged(found, newInt)
                root = delete(root, found)
                if root:
                    return mergeInterval(root, merged, mergeDist)
                else:
                    return merged

# isIn() checks if a given interval lies within a list of intervals
# and returns its index or None if not found
def isIn(root, intervals):
    for i in range(len(intervals)):
        if (intervals[i].start == root.start and intervals[i].end == root.end):
            return i
    return None

# removeInterval() removes an interval that was previously merged
def removeInterval(root, interval, mergeDist):

    # find interval to be removed in tree
    found = findMaxforN(root, interval.start)

    # check if interval is part of mergedIntervals list 
    index = isIn(interval, found.mergedIntervals)

    if (index is not None):
        # Remove interval from list of "merged"
        tempIntervals = found.mergedIntervals
        tempIntervals.pop(index)

        # Delete interval that contained the interval to be removed
        root = delete(root, found)

        # Go through all intervals in resulting merged intervals list, merging them as you go (once again)
        for i in tempIntervals:
            root = mergeInterval(root, i, mergeDist)

    return root

# delete() deletes an existing interval node from the tree
# Adapted from geeksforgeeks.org
def delete(root, interval): 

    # print('deleting... ' + str(interval.start), str(interval.end))
    # Base Case 
    if root is None: 
        return root  

    # If the key to be deleted is smaller than the root's 
    # key then it lies in  left subtree 

    if interval.start < root.start: 
        root.left = delete(root.left, interval) 
  
    # If the key to be deleted is greater than the root's key 
    # then it lies in right subtree 
    elif(interval.start > root.start): 
        root.right = delete(root.right, interval) 
  
    # If key is same as root's key, then this is the node 
    # to be deleted 
    else: 
        # print('deleting, finally:')
        # Node with only one child or no child 
        if root.left is None : 
            temp = root.right  
            root = None 
            return temp  
              
        elif root.right is None : 
            temp = root.left  
            root = None
            return temp 
  
        # Node with two children: Get the inorder successor 
        # (smallest in the right subtree) 
        temp = minValueNode(root.right) 
  
        # Copy the inorder successor's content to this node 
        root.start = temp.start 
        root.end = temp.end
        root.mergedIntervals = temp.mergedIntervals
  
        # Delete the inorder successor 
        root.right = delete(root.right, temp) 

    return root 

# insert() inserts a (non-overlapping) interval node into the tree
# Adapted from geeksforgeeks.org ### rebalance tree
def insert(root, interval):
    if root == None: # insert new interval if tree is empty
        root = Interval(interval.start, interval.end, mergedFlag = interval.mergedFlag)  
        if (interval.mergedIntervals == []):
            root.mergedIntervals = [interval]
        else:
            root.mergedIntervals = interval.mergedIntervals
        return root

    if (interval.start < root.start):
        root.left = insert(root.left, interval)
    elif (interval.start > root.start):
        root.right = insert(root.right, interval)

    return root

# PrintTree() prints out the tree inorder
# Adapted from geeksforgeeks.org
def PrintTree(root):

    if root is None:
        print('[]')

    else:
        if root.left is not None:
            PrintTree(root.left)

        print('[' + str(root.start) +',' + str(root.end) + ']', end ='')

        # To print merged subsets
        # for i in root.mergedIntervals:
        #     print('--[' + str(i.start) +',' + str(i.end) + ']', end='\n')

        if root.right is not None:
            PrintTree(root.right)
	
file = open('input.csv', 'r')
reader = csv.reader(file)
headers = next(reader) # Skip header

root = None
mergeDist = 5

for row in reader:
    seq = int(row[0])
    newStart = int(row[1])
    newEnd = int(row[2])
    newNode = Interval(start = newStart, end = newEnd)
    action = row[3]

    if (action == 'ADDED'):
        root = mergeInterval(root, newNode, mergeDist)
        print('[' + str(newNode.start) + ',' + str(newNode.end) + '] added, OUTPUT:', end='')
        PrintTree(root)
        print('\n')

    elif (action == 'REMOVED'):
        root = removeInterval(root, newNode, mergeDist)
        print('[' + str(newNode.start) + ',' + str(newNode.end) + '] removed, OUTPUT: ', end='')
        PrintTree(root)
        print('\n')

file.close()