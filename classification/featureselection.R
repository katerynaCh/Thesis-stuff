
#SPLIT THE DATAFRAME IN SMALLER parts
#apis1<-apis[,60001:70517]
#apis1<-cbind(apis1,apis[70518])

apis1<-apis[1:15,]

#
set.seed(123)
boruta.train <- Boruta(Class ~., data = apis1, doTrace = 2)
print(boruta.train)
final.boruta <- TentativeRoughFix(boruta.train)
print(final.boruta)
k1=getSelectedAttributes(final.boruta, withTentative = F)
boruta.df <- attStats(final.boruta)

selected_apis1<-apis1[,k1]
selected_apis1<-cbind(selected_apis1, apis1[70518])
write.csv(selected_apis, file = "selectedfeatures1n.csv")
