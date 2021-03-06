library(RWeka)
library(kernlab)
library(Boruta)

#load data from .csv file
selected_apis <- read.csv("C:\\Users\\Kateryna\\Desktop\\Thesis-stuff\\selectedfeatures.csv", header=TRUE)

#define the normalization function
normalize <- function(x) {
  num <- x - min(x)
  denom <- max(x) - min(x)
  return (num/denom)
}


#FEATURE SELECTION STARTS - RUN ONCE
#set.seed(123)
#boruta.train <- Boruta(Class ~., data = trying, doTrace = 2)
#print(boruta.train)
#final.boruta <- TentativeRoughFix(boruta.train)
#print(final.boruta)
#k=getSelectedAttributes(final.boruta, withTentative = F)
#boruta.df <- attStats(final.boruta)
#selected_apis<-apis[,k]
#selected_apis<-cbind(selected_apis, apis[70518])
#write.csv(selected_apis, file = "selectedfeatures.csv")
#FEATURE SELECTION ENDS
coln = ncol(selected_apis)-1
coln1=coln+1

#normalize data
#selected_apis<- as.data.frame(lapply(apis[,1:coln-1], normalize))

#DIVIDE DATA INTO TRAINING AND TEST SET
set.seed(1234)
#label matrix with 1 with prob 0.067 and 2 with prob 0.33, to separate dataset into 2/3 ratio
ind <- sample(2, nrow(selected_apis), replace=TRUE, prob=c(0.67, 0.33))
#create 2 datasets from tables, without the last column (this is class label)
selected_apis.train1<-selected_apis[ind==1,1:coln]
selected_apis.test1<-selected_apis[ind==2,1:coln]

selected_apis.train2<-selected_apis[ind==1,1:coln1]
selected_apis.test2<-selected_apis[ind==2,1:coln1]
selected_apis.train2<-selected_apis.train2[,-coln]
selected_apis.test2<-selected_apis.test2[,-coln]

#set class labels for training and test sets
selected_apis.testlabels<-selected_apis[ind==2,coln]
selected_apis.trainlabels<-selected_apis[ind==1,coln]


selected_apis.testlabels.twoway<-selected_apis[ind==2,coln1]
selected_apis.trainlabels.twoway<-selected_apis[ind==1,coln1]
#J48
fit <- J48(as.factor(Class)~., data=selected_apis.train)
# summarize the fit
summary(fit)
# make predictions
predictions <- predict(fit, selected_apis.test)
# summarize accuracy
CrossTable(selected_apis.testlabels, predictions, type="C-Classification")


fit <- J48(as.factor(Malware)~., data=selected_apis.train2)
# summarize the fit
summary(fit)
# make predictions
predictions <- predict(fit, selected_apis.test2)
# summarize accuracy
CrossTable(selected_apis.testlabels.twoway, predictions, type="C-Classification")


