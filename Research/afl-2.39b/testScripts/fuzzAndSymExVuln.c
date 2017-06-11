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
    int *int1;
    int *int2;
    int *int3;
    
    int i;

    //Take input of first integer
    printf("please enter int1\n");
    scanf("%i", int1);
    //Every 5000th input will result in a crash
    
    /*
    for (i = 1; 50; i = i + 1) {
        printf("please enter int2\n");
        scanf("%i", int2);
        if (int2 == 0){
            int1 = int1 -1;
        }else int1 = int1 + 1;
    }*/
    
    if (*int1 == 1000) {
        
        //Take input of second integer
        scanf("%i", int3);
        
        //Every 2^32th input will result in a crash.
        if (*int3 == 123456789){
            
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
