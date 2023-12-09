%{
#include "parser.tab.h"
%}

%%

int                           { return T_INTEGER_TYPE; }
string                        { return T_STRING_TYPE; }
var                           { return T_VAR; }
=                             { return T_ASSIGN; }
If                            { return T_CONDITIONAL; }
Else                          { return T_ELSE; }
For                           { return T_LOOP; }
or                            { return T_OR; }
and                           { return T_AND; }
Dot                           { return T_DOT; }
Draw                          { return T_DRAW; }
Win                           { return T_WIN; }
Loss                          { return T_LOSS; }
Guardiola                     { return T_GUARDIOLA; }
Mourinho                      { return T_MOURINHO; }
Bellingham                    { return T_BELLINGHAM; }
Camavinga                     { return T_CAMAVINGA; }
not                           { return T_NOT; }

True                          { return T_TRUE; }
False                         { return T_FALSE; }

[a-zA-Z_][a-zA-Z_0-9]*        { return T_IDENTIFIER; }

\"([^\\\"]|\\(.|\n)|[@#$%^&*()_+{}[\]|:;'<>,.?/!~-])*\" { return T_STRING; }

[0-9]+                        { return T_NUMBER; }

.                             { return T_NEW_SENTENCE; }

\n                            { /* handle new lines */ }

[ \t\r]+                      { /* ignore extra whitespace */ }

%%
