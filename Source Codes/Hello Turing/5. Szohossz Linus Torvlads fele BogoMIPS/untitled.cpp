#include <stdio.h>
#include <time.h>
#include <strings.h>
#include <string.h>
#include <iostream>

void delay(unsigned long long loops)
{
	for(unsigned long long i = 0; i < loops; i++);
}
int main(void)
{
	std::string alma;
	std::cin >> alma;
	int a = alma.size();
	unsigned long long loops_per_sec = 1, hossz = alma.size();
	while(loops_per_sec <<= 1)
	{
		delay(loops_per_sec);
		if(loops_per_sec >= hossz)
		{
			//loops_per_sec = (loops_per_sec / ticks) * CLOCKS_PER_SEC;
			printf("ok - %llu \n",loops_per_sec);
			return 0;
		}
	}
	printf("failed\n");
	return -1;
}