#include <stdio.h>
int main()
{
	int tmp = 0,a =1,b = 2;
	printf("%d \n",a);
	printf("%d \n",b);
	tmp = a;
	a = b;
	b = tmp;
	printf("%d \n",a);
	printf("%d \n",b);
}