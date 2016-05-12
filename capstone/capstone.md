## Predicting Detroit blighted buildings from reported incidents

*The ultimate explanation of my approach with this problem is the code at https://github.com/davidells/datasci_course_materials/blob/answers/capstone/capstone.ipynb*


### Defining Buildings

Firstly, I have some text extraction functions to parse out (lat, lng) information for 
each sort of incident, and I'm dropping some outliers that fall outside of the expected 
area of Detroit. 
 
Buildings are defined as a cluster of incidents, rather than as a specific building
extent defined by a rectangle or circle area. Admittedly, I got this idea when reviewing
another student's answers to the first assignment. I am using scikit-learn's DBSCAN
clustering algorithm to define the incident clusters, and using the output to power
the function that returns a building id for a given (lat, lng) pair.

The clustering algorithm with the tuned parameters gives me about 166k defined buildings.
To label the buildings according to their blight status (the thing we're ultimately
trying to predict), I'm using the data from detroit-demolition-permits.tsv, considering
every incident from that file as indication of blight status. This gives me around 4.5k
blighted buildings.


### Dataset selection

My selection of a dataset to learn on uses all the blighted buildings, and a same sized
sample of non-blighted buildings. This vastly reduces the full set of buildings to look
at from around 166k to just around 9k.


### Feature selection

My approach now is to just gather up a lot of different features to use for a 
classification algorithm, so I look at the different dimensions available in the 
incident data. Currently I'm using the following features, all aggregated per building:

 * number of 311 calls
 * number of 311 calls by issue_type

 * number of blights
 * number of blights by ViolationCode
 * number of blights by PaymentStatus
 * sum of blights JudgmentAmt

 * number of crimes
 * number of crimes by when the crime happens (night or day)
 * number of crimes by CATEGORY

Some of the other features I'd like to explore (but haven't yet) are:

 * number of unique 311 issue types
 * number of unique crime CATEGORY
 * number of unique incident types (crimes, calls, blights)
 * number of incidents within a 1-month(?) period
 * number of *other* demos in broader area (define broader area)


### Classification and accuracy

Using the above features and the blight status for my selected buildings, I am using
scikit-learn's RandomForestClassifier for the classification task, having tweaked the
number of estimators, the depth of the decision trees it creates, and the number of
features used in each random decision tree. With 10-fold cross validation, I'm getting
an average score of around 82.5% pretty consistently. With some earlier feature sets,
I was only getting around %70, but tweaking the features I was using seemed to help
quite a bit.

### Feature importance 

Beyond that, I'm taking an additional single fit of the whole dataset with the
RandomForestClassifier in order to look at the reported feature importances, as I
was curious to know what features were guiding the prediction more than others. The
following features stood out as important:

 * number of crimes
 * total number of incidents
 * number of crimes by when a crime happened
 * number of blight violations
 * number of unpaid blight violations
 * number of 311 call incidents
 * sum of blight violation fines


... and a few specific categories of crimes and blight violations from there.

This makes some intuitive sense, as you'd figure blights are more likely in high
crime areas -- lots of crime could seem to signal abandonment of a building. It was
interesting to see when a crime happens surfacing as an important feature. Additionally
the time at which a crime happened seemed to help signal problems. 

### Concerns and final thoughts

Once concern I have in this approach is that the prediction is more a result of the
clustering algorithm that defined buildings rather than the classification task. It may
be that high crime rates are predicting blighted buildings only because lots of crimes
close to each other promote a bigger cluster that is more likely to include a blighted
building just by virtue of spanning a bigger area as a cluster.

So, the classifier looks OK "on paper" which is encouraging, with the rate of accuracy
above 4 out of 5 correctly classified buildings in a 10 fold cross validation, but
there are some subtleties that should be explored, and might be exposed with further
datasets of incidents, or at least with more attention paid to the temporal dimensions
of the incident data.


