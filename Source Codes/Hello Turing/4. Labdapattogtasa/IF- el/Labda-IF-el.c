#include <stdio.h>
#include <curses.h>
#include <unistd.h>

int main(void)
{
	WINDOW *window;
	window = initscr();
	int x=0, y=0;
	int xnow=1, ynow=1;
	int mx,my;
	for(;;)
	{
		getmaxyx(window,my,mx);
		mvprintw(y,x,"O");
		refresh();
		usleep(100000);
		clear();
		x=x+xnow;
		y=y+ynow;
		if (x>=mx-1) //Elerte-e a jobb oldalt?
		{
			xnow = xnow*-1;
		}
		if (x<=0) //Elerte-e a bal oldalt?
		{
			xnow = xnow*-1;
		}
		if (y<=0) //Elerte-e a tetejet?
		{
			ynow=ynow*-1;
		}
		if (y>=my-1) //Elerte-e az aljat?
		{
			ynow = ynow*-1;
		}
	}
	return 0;
}