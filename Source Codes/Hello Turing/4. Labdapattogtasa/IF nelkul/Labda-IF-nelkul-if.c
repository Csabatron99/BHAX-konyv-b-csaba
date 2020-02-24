#include <stdio.h>
#include <stdlib.h>
#include <curses.h>
#include <unistd.h>

int main(void)
{
	WINDOW *window;
	window = initscr();
	int xj=0, xk=0, yj=0, yk=0;
	int mx,my;
	nodelay(window, true);
	getmaxyx(window,my,mx);
	my=my*2;mx=mx*2;
	for(;;)
	{
		xj = (xj-1)%mx;
		xk = (xk+1)%mx;
		yj = (yj-1)%my;
		yk = (yk+1)%my;
		clear();
		mvprintw(abs((yj+(my-yk)) / 2),abs((xj+(mx-xk)) / 2), "O");
		refresh();
		usleep(100000);
	}
	return 0;
}