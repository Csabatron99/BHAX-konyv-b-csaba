kis_szam=10000000
kis=sample(1:3,kis_szam,replace=T)
jatekos=sample(1:3,kis_szam,replace=T)
vezeto=vector(length=kis_szam)
for(i in 1:kis_szam)
{
	if(kis[i]==jatekos[i])
	{
		mibol=setdiff(c(1,2,3),kis[i])
	}
	else
	{
		mibol=setdiff(c(1,2,3),c(kis[i],jatekos[i]))
	}
	vezeto[i]=mibol[sample(1:length(mibol),1)]
}
nemvaltnyer=which(kis==jatekos)
valt=vector(length=kis_szam)
for(i in 1:kis_szam)
{
	holvaltoztat=setdiff(c(1,2,3),c(vezeto[i],jatekos[i]))
	valt[i]=holvaltoztat[sample(1:length(holvaltoztat),1)]
}
valtnyer=which(kis==valt)
sprintf("Kiserletek szama: %i",kis_szam)
length(nemvaltnyer)
length(valtnyer)
length(nemvaltnyer)/length(valtnyer)
length(nemvaltnyer)+length(valtnyer)
