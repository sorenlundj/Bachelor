//
//  HybridTestCase.h
//  
//
//  Created by Søren Lund Jensen on 16/05/2017.
//
//  Porpose: To test that the symbolic execution
//  module works with AFL

#include <stdio.h>
#include <string.h>

int main(void)
{
    char login[32];
    char passwd[32];
    
    printf("Login: \n");
    scanf("%s", login);
    printf("Password: \n");
    scanf("%s", passwd);
    
    if (strcmp(login, "root") == 0) {
        if (strcmp(passwd, "1qazxsw2") == 0) {
            printf("Access Granted.\n");
            return 0;
        }
    }
    
    printf("Access Denied.\n");
    return 1;
}
