######    Test   of    variables    ########

data1<-read.table(file.choose(),header=TRUE)
data2<-read.table(file.choose(),header=TRUE)
data3<-read.table(file.choose(),header=TRUE)
data_all<-rbind(data1,data2,data3)
head(data_all)
nrow(data_all)
attach(data_all)
leveneTest(similarity,as.factor(repost))
leveneTest(time_delta,as.factor(repost))
t.test(similarity~repost,data=data,var.equal = FALSE)
t.test(time_delta~repost,data=data,var.equal = FALSE)


##########   FA    ##################
library(psych)
library(MASS)
head(data_all)
ncol(data_all)
x<-data_all[,-c(1,7,20)] 
colnames(x)
R<-cor(scale(x))

eig<-eigen(R)
lambda<-eig$values
eigvectors<-eig$vectors
Lambda<-matrix(rep(lambda,17),nrow=17,byrow=TRUE)
L<-sqrt(Lambda)*eigvectors
Loadings_2<-L[,1:10]
varimax(Loadings_2)
