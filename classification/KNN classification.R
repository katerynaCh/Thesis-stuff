#import libraries
library(class)
library(dplyr)
library(lubridate)
library(gmodels)
library(ggvis)

#load data from .csv file
selected_apis <- read.csv("C:\\Users\\Kateryna\\Desktop\\Thesis-stuff\\selectedfeatures.csv", header=TRUE)

#define the normalization function
normalize <- function(x) {
num <- x - min(x)
denom <- max(x) - min(x)
return (num/denom)
}

coln = ncol(selected_apis)-1
coln1=coln+1
#normalize data
#selected_apis<- as.data.frame(lapply(selected_apis[,1:coln-1], normalize))

#DIVIDE DATA INTO TRAINING AND TEST SET
set.seed(1234)
#label matrix with 1 with prob 0.067 and 2 with prob 0.33, to separate dataset into 2/3 ratio
ind <- sample(2, nrow(selected_apis), replace=TRUE, prob=c(0.67, 0.33))
#create 2 datasets from tables, without the last column (this is class label)
selected_apis.train1<-selected_apis[ind==1,(1:coln)]
selected_apis.test1<-selected_apis[ind==2,(1:coln)]
selected_apis.train2<-selected_apis[ind==1,1:coln1]
selected_apis.test2<-selected_apis[ind==2,1:coln1]
selected_apis.train2<-selected_apis.train2[,-coln]
selected_apis.test2<-selected_apis.test2[,-coln]

#set class labels for training and test sets
selected_apis.testlabels<-selected_apis[ind==2,coln]
selected_apis.trainlabels<-selected_apis[ind==1,coln]


selected_apis.testlabels.twoway<-selected_apis[ind==2,coln1]
selected_apis.trainlabels.twoway<-selected_apis[ind==1,coln1]
model_pred <- knn(train = selected_apis.train1, test = selected_apis.test1, cl = selected_apis.trainlabels, k=1)
prob <- attr(model_pred, "prob")
CrossTable(x = selected_apis.testlabels, y = model_pred, prop.chisq=FALSE)

model_twoway<-knn.cv(train = selected_apis.train2, test = selected_apis.test2, cl = selected_apis.trainlabels.twoway, k=1)
prob <- attr(model_pred, "prob")
CrossTable(x = selected_apis.testlabels.twoway, y = model_twoway, prop.chisq=FALSE)

