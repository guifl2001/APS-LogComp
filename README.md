# APS-LogComp
Criando uma Linguagem de programação futebolística para a matéria de Lógica da Computação

# EBNF
```go
<programa> ::= <declaração>*
<declaração> ::= <declaração-variável> | <declaração-função>
<declaração-variável> ::= "var" <identificador> <tipo> "=" <expressão> ";"
<tipo> ::= "int" | "float" | "string" | "bool" | "struct" "{" <campos> "}"
<campos> ::= (<identificador> <tipo> ";")*
<declaração-função> ::= "func" <identificador> "(" <parâmetros> ")" <tipo> <bloco>
<parâmetros> ::= (<identificador> <tipo> ("," <identificador> <tipo>)*)?
<bloco> ::= "{" <declaração>* "}"
<expressão> ::= <expressão-simples>
<expressão-simples> ::= <termo> ("+" <termo> | "-" <termo>)*
<termo> ::= <fator> ("*" <fator> | "/" <fator>)*
<fator> ::= <identificador> | <número> | "(" <expressão-simples> ")"
<identificador> ::= <letra> (<letra> | <dígito>)*
<número> ::= <dígito>+
<letra> ::= "a" | "b" | ... | "z" | "A" | "B" | ... | "Z"
<dígito> ::= "0" | "1" | "2" | ... | "9"

```
