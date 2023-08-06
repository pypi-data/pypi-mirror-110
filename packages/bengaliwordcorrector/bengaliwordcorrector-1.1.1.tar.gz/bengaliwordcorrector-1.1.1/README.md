Bengali Word Corrector
===================

Installation
-------------

    pip install bengaliwordcorrector==1.1.1

Quick Start
-------------
After installation, using bengaliwordcorrector should be fairly straight forward:

**Word Correction**

    from bengaliwordcorrector import correction
    l = ['মেইন্টনেন্স','পরমর্শ','অতক্রম্য','কমিশনরের']
    for i in l:
        print('incorrect word:',i,"correct word:",correction(i))

 **Related Word Suggestions**
 

    from bengaliwordcorrector import suggestions
    l = ['মেইন্টনেন্স','পরমর্শ','অতক্রম্য','কমিশনরের']
    for i in l:
        print("incorrect word:",i,"suggestions:",suggestions(i))
    
