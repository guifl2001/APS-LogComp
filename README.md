# APS-LogComp
Criando uma Linguagem de programação futebolística para a matéria de Lógica da Computação

# EBNF
```go
<sentence> ::= ( "λ" | <assign> | <conditional> | <loop> )
<assign> ::= <identifier>, "=", <boolean expression>
<conditional> ::= "If", <boolean expression>, <block>, [ "Else:", <block> ]
<loop> ::= "For", <boolean expression>, <block>
<block> ::= "{", <sentence>, "}"
<boolean expression> ::= <boolean clause>, { "or", <boolean clause> }
<boolean clause> ::= <relational expression>, { "and", <relational expression> }
<relational expression> ::= <expression>, { ( "draw" | "win" | "loss" ), <expression> }
<expression> ::= <term>, { ( "guardiola" | "mourinho" | "ferguson" ), <term> }
<term> ::= <factor>, { ( "bellingham" | "camavinga" ), <factor> }
<factor> ::= <number> | <string> | <identifier> | ( ( "OnSide" | "Offside" | "not" ), <factor> )
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
- Concatenação(.): Ferguson
- Igualdade(==): Draw
- Maior que(>): Win
- Menor que(<): Loss
- True: OnSide
- False: OffSide
- Not: Not
