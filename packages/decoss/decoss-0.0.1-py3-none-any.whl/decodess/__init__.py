def a3():
    print('''
    %{
#include <stdio.h>
int wc=0,cc=0,lc=0,bc=0;
char infile[25];
%}
word [a-zA-Z0-9]+
eol [\n]
%%
{word} {wc++; cc+=yyleng;}
{eol} {lc++; cc++;}
[" "] {bc++; cc++;}
[\t] {bc+=8; cc++;}
. {cc++;}
%%
int yywrap() 
{ }
int main()
{
printf("\nRead the input file\n");
scanf("%s",infile);
yyin=fopen(infile,"r");
yylex();
printf("Number of characters = %d\n",cc);
printf("Number of words = %d\n",wc);
printf("Number of spaces = %d\n",bc);
printf("Number of lines = %d\n",lc);
return 0;
fclose(yyin);
}



commands
lex pgm_name.l
gcc lex.yy.c -o pgm_name.exe
pgm_name.exe
    ''')