%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
%}

%token T_LAMBDA
%token T_ASSIGN
%token T_CONDITIONAL
%token T_LOOP
%token T_ELSE
%token T_IDENTIFIER
%token T_INT
%token T_STRING
%token T_EQUAL
%token T_AND
%token T_OR
%token T_DRAW
%token T_WIN
%token T_LOSS
%token T_GUARDIOLA
%token T_MOURINHO
%token T_FERGUSON
%token T_BELLINGHAM
%token T_CAMAVINGA
%token T_ONSIDE
%token T_OFFSIDE
%token T_NOT
%token T_NUMBER
%token T_STRING_LITERAL

%start sentence

%%

sentence : T_LAMBDA
         | assign
         | conditional
         | loop
         ;

assign : T_IDENTIFIER ',' T_ASSIGN boolean_expression
       ;

conditional : T_CONDITIONAL boolean_expression block T_ELSE block
            | T_CONDITIONAL boolean_expression block
            ;

loop : T_LOOP boolean_expression block
     ;

block : '{' sentence '}'
      ;

boolean_expression : boolean_clause
                  | boolean_expression T_OR boolean_clause
                  ;

boolean_clause : relational_expression
               | boolean_clause T_AND relational_expression
               ;

relational_expression : expression T_DRAW | T_WIN | T_LOSS | T_ONSIDE | T_OFFSIDE expression
                   ;

expression : term
          | expression T_GUARDIOLA | T_MOURINHO | T_FERGUSON term
          ;

term : factor
     | term T_BELLINGHAM | T_CAMAVINGA factor
     ;

factor : T_NUMBER
       | T_STRING_LITERAL
       | T_IDENTIFIER

%%

int main() {
    yyparse();
    return 0;
}

void yyerror(const char *s) {
    fprintf(stderr, "Error: %s\n", s);
}
