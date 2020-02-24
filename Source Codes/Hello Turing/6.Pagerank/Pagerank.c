#include <stdio.h>
#include <math.h>

void kiir (double tomb[], int db)
{
	int i;
	for (i=0; i<db; i++)
	printf("%lf\n", tomb[i]);
}
double tavolsag(double pagerank[],double pagerank_temp[],int db)
{
	double tav = 0.0;
	int i;
	for(i=0;i<db;i++)
		tav+=(pagerank[i] - pagerank_temp[i])*(pagerank[i] - pagerank_temp[i]);
	sqrt(tav);
	return tav;
}
int main(void)
{
	double L[4][4] = {
		{0.0, 0.0, 1.0 / 3.0, 0.0},
		{1.0, 1.0 / 2.0, 1.0 / 3.0, 1.0},
		{0.0, 1.0 / 2.0, 0.0, 0.0},
		{0.0, 0.0, 1.0 / 3.0, 0.0}
	};
	double PR[4] = {0.0, 0.0, 0.0, 0.0};
	double PRv[4] = {1.0 / 4.0, 1.0 / 4.0, 1.0 / 4.0, 1.0 / 4.0};
	for (;;) 
	{
		for(int i=0;i<4;i++)
		{
			PR[i]=0;
			for (int j=0;j<4;j++)
			{    
				 PR[i] = PR[i]+(PRv[j]*L[i][j]);
			}
		}
		if ( tavolsag(PR,PRv, 4) < 0.00000001)
			break;
		for(int i=0;i<4;i++)
			PRv[i]=PR[i];
	}
	kiir (PR,4);
	return 0;
} 
