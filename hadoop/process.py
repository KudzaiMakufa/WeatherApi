# #!/usr/bin/python
# import sys
# #Word Count Example
# # input comes from standard input STDIN
# for line in sys.stdin:
#     line = line.strip() #remove leading and trailing whitespaces
#     words = line.split() #split the line into words and returns as a list
#     for word in words:
#     #write the results to standard output STDOUT
#         print('%s    %s' % (word,1) )#Emit the word
import random


file1 = open('merged_file.txt', 'r')
Lines = file1.readlines()
 
count = 0
# Strips the newline character
for line in Lines:
    line = line.strip() #remove leading and trailing whitespaces
    words = line.split() #split the line into words and returns as a list
    for word in words:
    #write the results to standard output STDOUT
        print('%s    %s   %s' % (word,1 , random.randint(15, 30)) )#Emit the word
    count += 1
    