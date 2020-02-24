#include <stdio.h>
#include <unistd.h>
#include <omp.h>

int main()
{
	#pragma omp parallel
		{
			for(;;);
		}
	return 0;
}