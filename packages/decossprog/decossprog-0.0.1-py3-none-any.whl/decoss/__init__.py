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




    ''')

def b3():
    print('''
    %{
#include <stdio.h>
int cc=0;
%}
%x CMNT
%%
"/*" {BEGIN CMNT;}
<CMNT>. ; 
<CMNT>"*/" {BEGIN 0; cc++;}
%%
int yywrap() { }
int main(int argc, char *argv[])
{
if(argc!=3)
{
printf("Usage : %s <scr_file> <dest_file>\n",argv[0]);
return 0;
}
yyin=fopen(argv[1],"r");
yyout=fopen(argv[2],"w");
yylex();
printf("\nNumber of multiline comments = %d\n",cc);
return 0;
}

''')

def a4():
    print('''
    %{
#include <stdio.h>
int ext(int);
int a[]={0,0,0,0},valid=1,opnd=0,top=-1,i;
%}
%x oper
%%
["("] {top++;}
[")"] {top--;}
[a-zA-Z0-9]+ {BEGIN oper; opnd++;}
<oper>"+" {if(valid) {valid = 0; i = 0;} else ext(0);}
<oper>"-" {if(valid) {valid = 0; i = 1;} else ext(0);}
<oper>"*" {if(valid) {valid = 0; i = 2;} else ext(0);}
<oper>"/" {if(valid) {valid = 0; i = 3;} else ext(0);}
<oper>"(" {top++;}
<oper>")" {top--;}
<oper>[a-zA-Z0-9]+ {opnd++; if(valid == 0) {valid = 1; a[i]++;} else 
ext(0);}
<oper>"\n" {if(valid == 1 && top == -1) {printf("Valid 
expression\n"); return 0;} else ext(0);}
.\n ext(0);
%%
int yywrap() { }
int ext(int x)
{
printf("\nInvalid expression%d\n",x);
exit(0);
}
int main()
{
printf("\nEnter an arithmetic expression\n");
yylex();
printf("Number of operands = %d\n",opnd);
printf("Number of + = %d\n",a[0]);
printf("Number of - = %d\n",a[1]);
printf("Number of * = %d\n",a[2]);
printf("Number of / = %d\n",a[3]);
return 0;
}

    ''')

def b4():
    print('''
    %{
#include<stdio.h>
%}
ws [ \t\n]
%%
{ws}"and"{ws}|{ws}"AND"{ws} | 
{ws}"or"{ws}|{ws}"OR"{ws} | 
{ws}"but"{ws}|{ws}"BUT"{ws} |
{ws}"because"{ws} |
{ws}"nevertheless"{ws} {printf("compound sentence\n");exit(0);}
. ;
\n return 0;
%%
int yywrap() { }
int main()
{
printf("\nEnter a sentence\n");
yylex();
printf("Simple sentence");
exit(0);
//return 0;
10
}
''')


def a5():
    print('''
    %{
#include<stdio.h>
int idc=0;
%}
e[=][ ]*[0-9]+
ws[ \n\t]*
id[_a-zA-Z][_a-zA-Z0-9]*
decln "int"|"float"|"clear"|"double"|"short"|"long"|"unsigned"
%x defn
%%
{decln} {BEGIN defn;}
<defn>{ws}{id}{ws}\, {idc++;}
<defn>{ws}{id}{ws}\; {BEGIN 0;idc++;}
<defn>{ws}{id}{ws}{e}{ws}\, {idc++;}
<defn>{ws}{id}{ws}{e}{ws}\; {BEGIN 0;idc++;}
<*>\n ;
<*>. ;
%%
int yywrap() { }
int main(int argc,char *argv[])
{
if(argc==2)
{
yyin=fopen(argv[1],"r");
yylex();
printf("\nNumber of identifiers = %d\n",idc);
}
else
{
printf("\nUsage : %s <src_file> \n",argv[0]);
}
return 0;
}

    ''')

def b5():
    print('''
    5b.l
%{
#include "y.tab.h"
%}
%%
[0-9]+ {yylval=atoi(yytext);return NUM;}
[\t] ;
\n return 0;
. return yytext[0];
%%
int yywrap() { }
5b.y
%{#include <stdio.h>%}
%token NUM
%left '+''-'
13
%left '/''*'
%%
expr:e {printf("Valid expression\n"); printf("Result : %d\n",$1); 
return 0;}
e:e'+'e {$$=$1+$3;}
| e'-'e {$$=$1-$3;}
| e'*'e {$$=$1*$3;}
| e'/'e {$$=$1/$3;}
| '('e')' {$$=$2;}
| NUM {$$=$1;}
%%
int main()
{
printf("\nEnter an arithmetic expression\n");
yyparse();
return 0;}
int yyerror()
{
printf("\nInvalid expression\n");
return 0;
}
    ''')

def a6():
    print('''
    %{
#include "y.tab.h"
%}
%%
[0-9]+(\.[0-9]+)? {return NUM;}
[a-zA-Z][_a-zA-Z0-9]* {return ID;}
[\t] ;
\n {return 0;}
. {return yytext[0];}
%%
int yywrap() { }
6a.y
%{
#include<stdio.h>
%}
%token L D NL
%%
var: L E NL {printf("Valid Variable\n");return 0;}
E: E L
| E D
| ;
%%
int yyerror()
{
printf("\n Invalid Variable\n");
16
return 0;
}
int main()
{
printf("\nEnter a variable\n");
yyparse();
}
''')

def b6():
    print('''
    %{
#include "y.tab.h"
%}
%%
[a-z] return L;
[0-9] return D;
\n {return NL;}
18
%%
int yywrap() { }
6b.y
%{
#include<stdio.h>
%}
%token L D NL
%%
var: L E NL {printf("Valid Variable\n");return 0;}
E: E L
| E D
| ;
%%
int yyerror()
{
printf("\n Invalid Variable\n");
return 0;
}
int main()
{
printf("\nEnter a variable\n");
yyparse();
}
''')

def a7():
    print('''
    7a.l
%{
#include "y.tab.h"
%}
%%
[aA] {return A;}
[bB] {return B;}
\n {return NL;}
. {return yytext[0];}
%%
int yywrap() { }
7a.y
%{
#include<stdio.h>
#include<stdlib.h>
%}
%token A B NL
%%
stmt: A A A A A A A A A S B NL {printf("valid string\n"); exit(0);}
;
S: S A
|
;
%%
int yyerror(char *msg)
{
printf("invalid string\n");
exit(0);
}
main()
21
{
printf("enter the string\n");
yyparse();
}
    ''')

def b7():
    print('''
    7b.l
%{
#include "y.tab.h"
%}
%%
[aA] {return A;}
[bB] {return B;}
\n {return NL;}
. {return yytext[0];}
%%
int yywrap() { }
23
7b.y
%{
#include<stdio.h>
#include<stdlib.h>
%}
%token A B NL
%%
stmt: S NL { printf("valid string\n"); exit(0); }
;
S: A S B |
;
%%
int yyerror()
{
printf("invalid string\n");
exit(0);
}
main()
{
printf("enter the string\n");
yyparse();
}''')


def a8():
    print('''
    #include<stdio.h>
#include<conio.h>
#include<string.h>
int k=0,z=0,i=0,j=0,c=0;
char a[16],ac[20],stk[15],act[10];
void check();
void main()
{
puts("GRAMMAR is E->E+E \n E->E*E \n E->(E) \n E->id");
puts("enter input string ");
gets(a);
c=strlen(a);
strcpy(act,"SHIFT->");
puts("stack \t input \t action");
for(k=0,i=0; j<c; k++,i++,j++)
{
if(a[j]=='i' && a[j+1]=='d')
{
stk[i]=a[j];
stk[i+1]=a[j+1];
stk[i+2]='\0';
a[j]=' ';
a[j+1]=' ';
printf("\n$%s\t%s$\t%sid",stk,a,act);
check();
}
else
{
stk[i]=a[j];
stk[i+1]='\0';
a[j]=' ';
printf("\n$%s\t%s$\t%ssymbols",stk,a,act);
check();
}
}
getch();
}
void check()
{
strcpy(ac,"REDUCE TO E");
for(z=0; z<c; z++)
if(stk[z]=='i' && stk[z+1]=='d')
{
stk[z]='E';
stk[z+1]='\0';
printf("\n$%s\t%s$\t%s",stk,a,ac);
j++;
26
}
for(z=0; z<c; z++)
if(stk[z]=='E' && stk[z+1]=='+' && stk[z+2]=='E')
{
stk[z]='E';
stk[z+1]='\0';
stk[z+2]='\0';
printf("\n$%s\t%s$\t%s",stk,a,ac);
i=i-2;
}
for(z=0; z<c; z++)
if(stk[z]=='E' && stk[z+1]=='*' && stk[z+2]=='E')
{
stk[z]='E';
stk[z+1]='\0';
stk[z+1]='\0';
printf("\n$%s\t%s$\t%s",stk,a,ac);
i=i-2;
}
for(z=0; z<c; z++)
if(stk[z]=='(' && stk[z+1]=='E' && stk[z+2]==')')
{
stk[z]='E';
stk[z+1]='\0';
stk[z+1]='\0';
printf("\n$%s\t%s$\t%s",stk,a,ac);
i=i-2;
}
}
    ''')

def a9():
    print('''
    if [ $# != 2 ]
then
echo "Invalid input!!!"
else
p1=`ls -l $1|cut -d " " -f1`
p2=`ls -l $2|cut -d " " -f1`
if [ $p1 == $p2 ]
then
echo "the file permissions are same and it is : "
echo "$p1"
else
echo "The file permissions are different"
echo "$1 : $p1"
echo "$2 : $p2"
fi
fi''')

def b9():
    print('''
    #include<stdio.h>
int main()
{
int ch,rv;
char cmd[10];
rv=fork();
if(rv==0)
{
do
{
printf("\nEnter a command\n");
scanf("%s",cmd);
system(cmd);
printf("\n1 : continue\n0 : exit\n");
scanf("%d",&ch);
}
while(ch!=0);
}
else
{
wait(0);
printf("\nChild terminated\n");
}
return 0;
}

    ''')

def a10():
    print('''
    #include<stdio.h>
 #include <stdlib.h>
 #include <sys/types.h>
 #include <unistd.h>
 int main()
 {
 pid_t child_pid;
 /* Create a child process. */
 child_pid = fork ();
 if (child_pid > 0)
 {
 printf("This is the parent process: %d. Sleep 
for a minute\n",getpid());
 sleep (60);
 }
 else
 {
 printf("This is the child process: %d. Exit 
immediately\n",getpid());
 exit (0);
 }
 system("ps -e -o pid,ppid,stat,comm");
 return 0;
 }
    ''')


def b10():
    print('''
    #include<stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <unistd.h>
#include <sys/wait.h>
int main()
{
pid_t pid1, pid2;
if ((pid1=fork())< 0)
{
printf("Fork error");
}
else if( pid1==0)
{
printf("first child pid=%d\n", getpid());
pid2=fork();
if( pid2 > 0)
 exit(0);
else if(pid2==0)
printf("second child pid = %d\n parent pid=%d\n", 
getpid(), getppid());
exit (0);
}
}

    ''')

def a11():
    print('''
    #include<stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <unistd.h>
#include <sys/wait.h>
int main()
{
pid_t pid1, pid2;
if ((pid1=fork())< 0)
{
printf("Fork error");
}
else if( pid1==0)
{
printf("first child pid=%d\n", getpid());
pid2=fork();
if( pid2 > 0)
 exit(0);
else if(pid2==0)
printf("second child pid = %d\n parent pid=%d\n", 
getpid(), getppid());
exit (0);
}
}
''')

def b11():
    print('''
    #include<stdio.h>
#include<stdlib.h>
#include<fcntl.h>
#include<unistd.h>
#include<sys/types.h>
#include<string.h>
int main(int argc,char *argv[])
{
int fd,num1,num2;
char buf[100];
if(argc==3)
{
mkfifo(argv[1],0666);
fd=open(argv[1],O_WRONLY);
num1=write(fd,argv[2],strlen(argv[2]));
printf("no of bytes written%d\n",num1);
}
if(argc==2)
{
fd=open(argv[1],O_RDONLY);
num2=read(fd,buf,sizeof(buf));
buf[num2]='\0';
printf("the message size %d read is %s",num2,buf);
}
close(fd);
unlink(argv[1]);
return 0;
}

    ''')

def a12():
    print('''
    #include<stdio.h>
#include<omp.h>
int main() {
 int n,a[100],i;
 omp_set_num_threads(2);
 printf("enter the no of terms of fibonacci series which have to be 
generated\n");
 scanf("%d",&n);
 a[0]=0;
 a[1]=1;
 #pragma omp parallel
 {
 #pragma omp single
 for(i=2;i<n;i++)
 {
 a[i]=a[i-2]+a[i-1];
 printf("id of thread involved in the computation of fib no 
%d is=%d\n",i+1,omp_get_thread_num());
 }
 #pragma omp barrier
 #pragma omp single
 {
 printf("the elements of fib series are\n");
 for(i=0;i<n;i++)
 printf("%d,id of the thread displaying this no is = 
%d\n",a[i],omp_get_thread_num());
 }
 }
 return 0;
}

    ''')