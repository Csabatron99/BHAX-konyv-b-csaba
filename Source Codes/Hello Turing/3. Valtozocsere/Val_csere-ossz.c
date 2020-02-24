#include <stdio.h>
int main()
{
	int a =1 ,b = 2;
	printf("%d \n",a);
	printf("%d \n",b);
	a = a + b;
	b = a - b;
	a = a - b;
	printf("%d \n",a);
	printf("%d \n",b);
}