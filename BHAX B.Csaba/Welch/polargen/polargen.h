#ifndef POLARGEN_H
#define POLARGEN_H

#include <cstdlib>
#include <cmath>
#include <ctime>

class PolarGen
{
	public:
	PolarGen ()
	{
	nincsTarolt = true;
	std::srand (std::time (NULL));
	}
	~PolarGen(){
	}
	double kovetkezo();

	private:
	bool nincsTarolt;
	double Tarolt;

};

#endif