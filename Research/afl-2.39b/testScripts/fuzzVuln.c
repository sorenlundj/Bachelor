//
//  fuzzVuln.c
//  
//
//  Created by Søren Lund Jensen on 17/05/2017.
//
//  Purpose: A program, to test fuzzing.

#include "fuzzVuln.h"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>


int main(void)
{
    int int1[32];
    div_t d;
    //Take input of an integer

    scanf("%i", int1);
    //Every 5000th input will result in a crash
    d = div(*int1, 5000);

    if (d.rem == 0) {
        //Crash here
        abort();
        return 0;
    }
    
    //Don't crash here
    return 0;
}
