//
//  fuzzAndSymExVuln.c
//
//
//  Created by Søren Lund Jensen on 14/05/2017.
//
//  Purpose: A program to test fuzzing, combined with symbolic execution.

#include "fuzzAndSymExVuln.h"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>


int main(void)
{
    int int1[32];
    int int2[32];
    div_t d;

    //Take input of first integer
    scanf("%i", int1);
    //Every 5000th input will result in a crash
    d = div(*int1, 5000);
    
    if (d.rem == 0) {
        
        //Take input of second integer
        scanf("%i", int2);
        
        //Every 2^32th input will result in a crash.
        if (*int2 == 123456789){
            
            //Crash here
            abort();
            return 0;
        }
        
        //Don't crash here
        return 0;
    }
    
    //Don't crash here
    return 0;
}
