library(matlab)
stp <- function(x)
{
	primek = primes(x)
	differencia = primek[2:length(primek)]-primek[1:length(primek)-1]
	index = which(differencia==2)
	v1primek = primek[index]
	v2primek = primek[index]+2
	v1pv2 = 1/v1primek+1/v2primek
	return(sum(v1pv2))
}
x=seq(13, 10000000, by=10000)
y=sapply(x,FUN=stp)
plot(x,y,type="b")