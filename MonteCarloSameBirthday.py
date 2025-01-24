#!/usr/bin/env python3
#COMP 3005 In Person
#Assignment 3
#Maya Fry 
#worked with Angelica Shelman and LeeAnn Michael

import random

#First we define a function to run a bernoulli trial 
def birthdayTrial(roomsize):
    while True:
        list365 = [False] * 365
        for i in range(roomsize):
            bday = random.randint(0, 364)
            #This looks for the value at the index of list (list365) 
            # that matches the random birthday
            if list365[bday]:
                return True
            #This will change the value at the index from "False" to "True"
            else:
                list365[bday] = True
        return False

#Now we run the bernoulli experiment, to run multiple trials (n), and to count up
#each time we get two matching birthdays (successes).
def experiment(n, roomsize, successes): 
    successes = 0
    for i in range(n):
        if birthdayTrial(roomsize):
            successes += 1
    return successes

#Here is the whole simulation with global values named at the beginning.
def monte_carlo():
    num_trials = 100000
    num_people = 1
    successes = 0
    while True:
        threshold = int(input("What threshold would you like? (Enter as a percent): "))
        if threshold > 0 and threshold < 101:
            prob_success = 0 #here we name another global value
            while (prob_success <= threshold):
                #this increases the roomsize each time the probability doesn't exceed the threshold
                num_people += 1 
                successes = experiment(num_trials, num_people, successes)
                prob_success = (successes / num_trials) * 100
                print(f"For {num_people} people, the probability of a shared birthday was {successes} / {num_trials} or {prob_success}%.")
            print(f"To achieve at least {threshold}% probability of a match, you need {num_people} people in the room.")
        else:
            print("Error: Not a valid percent.")
            continue
        return threshold

monte_carlo()