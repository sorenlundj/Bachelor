//
//  symExVuln.c
//  
//
//  Created by Søren Lund Jensen on 15/05/2017.
//
//  Purpose: A program to test symbolic execution.

#include "symExVuln.h"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>


int main(void)
{
    int int1[32];
    //Take input of second integer
    scanf("%i", int1);
        
    //Every 2^32th input will result in a crash.
    if (*int1 == 123456789){
        
        //Crash here
        abort();
        return 0;
    }
    
    //Don't crash here
    return 0;
}
