df <- read.csv("/Users/ells/Projects.Mine/coursera-data-at-scale/assignment5/seaflow_21min.csv")
summary(df)
# 18146 synecho examples in pop
# 39184 for 3rd quintile of fsc_small

smp_size <- floor(0.5 * nrow(df))
set.seed(18465)

training_set_index <- sample(
  seq_len(nrow(df)), 
  size = smp_size)

training_set <- df[training_set_index,]
test_set <- df[-training_set_index,]
mean(training_set$time)
# 341.76 for mean of training set time

library(ggplot2)
qplot(pe, chl_small, data = df, color = pop)
# Appears ultra is mixed with nano and pico

library(rpart)
fml <- formula(pop ~ fsc_small + fsc_perp + fsc_big + pe + chl_big + chl_small)
model <- rpart(fml, method="class", data=training_set)
print(model)
# crypto can't be found by this model
# pe < 5001.5 is a high level split for this model

test_predictions <- predict(model, test_set, type="class")
# Now we have class label predictions according to the model

sum(test_set$pop == test_predictions) / nrow(test_set)
# Accuracy of 0.85815

library(randomForest)
model <- randomForest(fml, data=training_set)
print(model)

test_predictions <- predict(model, test_set, type="class")
sum(test_set$pop == test_predictions) / nrow(test_set)
# Accuracy of 0.9202975

importance(model)
# pe and chl_small again stand out as important variables

library(e1071)
model <- svm(fml, data=training_set)
print(model)

test_predictions <- predict(model, test_set, type="class")
sum(test_set$pop == test_predictions) / nrow(test_set)
# Accuracy of 0.9199657

table(test_predictions, test_set$pop)
# Mistaking pico for ultra appears to be the most common mistake

plot(df$time, df$fsc_big, cex=0.01)
# Some suspicious non-continuous data there

# Take out rows with file_id == 208
df_cleaned <- df[!(df$file_id == 208),]

training_set_index <- sample(
  seq_len(nrow(df_cleaned)), 
  size = smp_size)

training_set <- df_cleaned[training_set_index,]
test_set <- df_cleaned[-training_set_index,]
mean(training_set$time)
# Now the mean is 307.3673 for time

# Ok, do the ol' svm model and check accuracy
model <- svm(fml, data=training_set)
test_predictions <- predict(model, test_set, type="class")
sum(test_set$pop == test_predictions) / nrow(test_set)
# Accuracy here is actually 0.9730322, an improvement of 
# 0.0530665 over previous 0.9199657 svm model accuracy