# MnemoTrain
Scripts and statistical analysis related to the training for memory tournaments.
Official disciplines are gradually implemented with a fine-grained data storing.
**warning** : abstract images correction is not working because of dumbness.
If you are a wanderer, you should know that these memory feats are not as boring as it seems, have a look on this [wiki](http://mt.artofmemory.com/wiki/Main_Page) to know more about this lost art
## Notes :
- I'd be happy if you fork or make use of these scripts, I'd be even more happy if you share your datas. You could get statistical analysis for free !
- This is not intended to be a high quality repository (messy code, lack of documentation, bad file structure)
- Tested on python2.7 32bits windows. File opening won't work on other os for the moment, so you have to open them manually.
- The beloved **runFeats.py** run all the disciplines (except spoken numbers). Datas (mainly about errors) are stored in a csv file.
- Abstract images and Name and Faces are poorly tested for the moment. Ressources are lacking for these disciplines.
- error.properties and profile.properties, files in the loci directories are intendend to be edited by the user to let the system know his memory systems and is set of journeys.
- Precise Reports are append to feats.csv in rawDatas. Unfortunately, this report is made if there is a memory system related to the discipline declared in profile.properties. Then it blocks out precise reports for image based discipline.
- Many thanks to Timothee Behra for his cards display implementation.
- spokenNumbers_audio.py won't work for a different OS than windows for the moment, and is not implemented as a feat for the moment. Audio files are in French.
- reactionTime_training.py implements a special mode for training reaction time (i.e remember the related image) : if the reaction time is above the desired goal, then the number is pushed back 4 to 7 spots later. This script as been superseded with a more powerfull one (ReactionTimeVector.py) which set smart odds according to the relative difficulty of items.
- The statistical analysis is realised with R, a free and open source data analysis software. The HTML is built with knitr.
You can have a look on these analysis [this one] (http://htmlpreview.github.io/?https://github.com/brumar/MnemoTrain/blob/master/Training_analysis/Perf_Numer_Analysis.html) or  [this one] (http://htmlpreview.github.io/?https://github.com/brumar/MnemoTrain/blob/master/Training_analysis/Perf_Numer_Analysis_2.html). This is the kind of thing I can do for you if you don't know how to use R and if you send me your datas.

## Dependencies :
- Pygame (cards disciplines)
- Jinja2 (abstract images and Name&Faces)

Feel free to let me know your mnemo-needs.

Hopefully I will reduce my commit rythm. Here are some todo notes for my future self and for eventual contributors.
Don't hesitate to contact me if you need.

## Future tasks :
- Allows precise data reporting even if memory system is not specified.
- Manual for users.
- Open file for different OS than windows, display a message if fail to open.
- Implement spoken numbers as a discipline (only as training script for the moment).
- Break disciplines.py in smaller parts.
- Build a common parent class for N&F and abstract images.
- Find better abstract images.
- Time-log card discipline.
- Allowing the user to rehearse his decks in cards.
- Turn cards in png (bmp are slow to load).
- Amend errors in N&F+words for phonetic errors.
- Better html templates for N&F and abstract images.
- Errors as class, not as list. As well as Journeys.
- Reorganize file structure (less files in main directory, a ressources directory, a recall directory, a config directory).
- Add Elements to error properties whenever a new error is added ("do you want to add this type of error?").
- Launch training scripts from runFeats.py.
- For dates, words and N&F, let the user decide to select only items he never saw before (by reading feats.csv).
- Automatic Back up feats.csv.
- Find a way to display remaining memorisation time.
- There is no time limit implemented for card memorisation.
- Better card display in python shell (using unicode for cards).
- Avoid useless overwriting of journey csv files.
- More try/except.
- Loci checker **before** error labelling.
- global options (like directory names, file names, must be stored at a unique place).
- compareSolutionAnswer in Feats class must be break into smaller parts.
- Html Generators must have a parent class.