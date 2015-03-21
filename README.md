# MnemoTrain
Scripts and statistical analysis related to the training for memory tournaments    
If you are a wanderer, you should know that these memory feats are not as boring as it seems, have a look on this [wiki](http://mt.artofmemory.com/wiki/Main_Page) to know more about this lost art    
## Notes :  
- I'd be happy if you fork or make use of these scripts, I'd be even more happy if you share your datas. You could get statistical analysis for free !   
- This is not intended to be a high quality repository (messy code, lack of documentation, bad file structure)
- Tested on python2.7 32bits windows. 
- The beloved **mainFeats.py** displays random words, numbers and binaries as well as automated correction, but for the moment does not store any personnal training data as reactionTime_training.py do.   
- spokenNumbers_audio.py won't work for a different OS than windows   
- Audio files are in french.    
- reactionTime_training.py implements a special mode for training reaction time (i.e remember the related image) : if the reaction time is above the desired goal, then the number is pushed back 4 to 7 spots later.      
- The statistical analysis is realised with R, a free and open source data analysis software. The HTML is built with knitr. 
You can have a look on these analysis [this one] (http://htmlpreview.github.io/?https://github.com/brumar/MnemoTrain/blob/master/Training_analysis/Perf_Numer_Analysis.html) or  [this one] (http://htmlpreview.github.io/?https://github.com/brumar/MnemoTrain/blob/master/Training_analysis/Perf_Numer_Analysis_2.html) 

Feel free to adapt these scripts to your needs.