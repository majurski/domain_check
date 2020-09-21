# Script for domain availability check

This script uses Godaddy API, so you will need 
Godaddy developer key and secret
https://developer.godaddy.com/

Original script can be found here:
https://www.8bitavenue.com/godaddy-domain-name-api-in-python/
But the purpose of the original is to check any sequences from list of words.

My interpretation is for all possible words, that can be generated from English alphabet.
This script can be used for checking any number of letters domain and any extensions.

# How to use it:
1. Change the number of cylces for more letters.
for i in alph:
    for b in alph:
        for c in alph:
            for d in alph:
                    word = i + b + c + d
                    keywords.append(word)

2. Add desired domain extensions.txt in the extensions file

Thast`s all.
