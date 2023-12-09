# APS-LogComp
Criando uma Linguagem de programação futebolística para a matéria de Lógica da Computação

# EBNF
```go
<sentence> ::= ( "λ" | <assign> | <conditional> | <loop> )
<assign> ::= "var", <identifier>, "=", <boolean expression>
<conditional> ::= "If", <boolean expression>, <block>, [ "Else:", <block> ]
<loop> ::= "For", <boolean expression>, <block>
<block> ::= "{", <sentence>, "}"
<boolean expression> ::= <boolean clause>, { "or", <boolean clause> }
<boolean clause> ::= <relational expression>, { "and", <relational expression> }
<relational expression> ::= <expression>, { ( "draw" | "win" | "loss" ), <expression> }
<expression> ::= <term>, { ( "guardiola" | "mourinho" | "dot" ), <term> }
<term> ::= <factor>, { ( "bellingham" | "camavinga" ), <factor> }
<factor> ::= <number> | <string> | <identifier> | ( ( "True" | "False" | "not" ), <factor> )
<identifier> ::= <letter>, { <letter> | <digit> }*
<number> ::= <digit>+
<string> ::= '"' { "λ" | <letter> | <digit> }* '"'
<letter> ::= "a" | "b" | ... | "z" | "A" | "B" | ... | "Z"
<digit> ::= "0" | "1" | "2" | ... | "9"
```

# Legenda

- Multiplicação(*): Bellingham
- Divisão(/): Camavinga
- Adição(+): Guardiola
- Subtração(-): Mourinho
- Igualdade(==): Draw
- Maior que(>): Win
- Menor que(<): Loss
