#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>

typedef struct binfa                                //definiáljuk a binfa típust
{
    int ertek;
    struct binfa *bal_nulla;
    struct binfa *jobb_egy;
} BINFA, *BINFA_PTR;

BINFA_PTR uj_elem()
{
    BINFA_PTR p;
    if ((p = (BINFA_PTR) malloc (sizeof (BINFA))) == NULL)
    {
        perror("memoria");
        exit (EXIT_FAILURE);
    }
    return p;
}

int main(int argc, char **argv)
{
    char b;
    BINFA_PTR gyoker = uj_elem ();
    gyoker->ertek = '/';
    gyoker->bal_nulla = gyoker->jobb_egy = NULL;    //bal és jobb gyermeke NULL értéket kapja
    BINFA_PTR fa = gyoker;                          //gyökérre mutat a pointer
    while (read (0, (void *) &b, 1))                //beolvasás
    {
        //write (1, &b, 1);
        if (b == '0')                               
        {
            if (fa->bal_nulla == NULL)              //ha a gyökérnek még nincs bal_nulla gyermeke    
            {   
                fa->bal_nulla = uj_elem ();         //új gyermek létrehozása
                fa->bal_nulla->ertek = 0;           //az értéke 0 lesz
                fa->bal_nulla->bal_nulla = fa->bal_nulla->jobb_egy = NULL; //a létrehozott csomópont bal és jobb gyermekének NULL értéket adunk
                fa = gyoker;                        //a pointer visszaáll a gyökérre
            }
            else    
                fa = fa->bal_nulla;                 //ha van 0-as gyermeke, akkor arra állítjuk rá a pointert
        }
        else                                        //ha c == '1'
        {
            if (fa->jobb_egy == NULL)               //ha nincs 1-es gyermeke, akkor csinálunk neki
            {
                fa->jobb_egy = uj_elem ();          //létrehoz
                fa->jobb_egy->ertek = 1;            //értéke 1 lesz
                fa->jobb_egy->bal_nulla = fa->jobb_egy->jobb_egy = NULL;    //a gyermekeinek NULL értéket adunk
                fa = gyoker;                        //pointer vissza a gyökérre
            }
            else //ha van, akkor ráállitjuk a pointert es rekurzívan újrahívódik a függvény
                fa = fa->jobb_egy;
        }
    }

    void szabadit(BINFA_PTR elem)                   //memória felszabadítás
    {
        if (elem != NULL)
        {
            szabadit (elem->jobb_egy);
            szabadit (elem->bal_nulla);
            free (elem);
        }
    }
}