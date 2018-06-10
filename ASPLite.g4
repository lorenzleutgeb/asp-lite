grammar ASPLite;

/* The ASP-Lite grammar in ANTLR v4 based on
 * https://www.mat.unical.it/aspcomp2013/files/ASP-CORE-2.01c.pdf
 * (sections 4 and 5, pages 10-12).
 * https://github.com/alpha-asp/Alpha/blob/master/src/main/antlr/at/ac/tuwien/kr/alpha/antlr/ASPCore2.g4
 */

program : rule+;

rule : head ('\n' body)?;

head : disjunction; // | choice

disjunction : classical_literal (OR disjunction)?;

body : naf_literal ('\n' naf_literal)?;

naf_literal : NAF? (classical_literal | builtin_atom);

classical_literal : MINUS? ID terms;

builtin_atom : binop term term;

terms : term terms?;

term : ID                                   # term_const
     | ID (PAREN_OPEN terms? PAREN_CLOSE)   # term_func
     | NUMBER                               # term_number
     | QUOTED_STRING                        # term_string
     | VARIABLE                             # term_variable
     | ANONYMOUS_VARIABLE                   # term_anonymousVariable
     | PAREN_OPEN term PAREN_CLOSE          # term_parenthesisedTerm
     | MINUS term                           # term_minusTerm
     | arithop term term                    # term_binopTerm
     | interval                             # term_interval; // syntax extension

interval : lower = (NUMBER | VARIABLE) DOT DOT upper = (NUMBER | VARIABLE); // NOT Core2 syntax, but widespread
binop : EQUAL | UNEQUAL | LESS | GREATER | LESS_OR_EQ | GREATER_OR_EQ;
arithop : PLUS | MINUS | TIMES | DIV;


ANONYMOUS_VARIABLE : '_';
DOT : '.';
COMMA : ',';
QUERY_MARK : '?';
COLON : ':';
SEMICOLON : ';';
OR : '|';
NAF : 'not';
CONS : ':-';
WCONS : ':~';
PLUS : '+';
MINUS : '-';
TIMES : '*';
DIV : '/';
AT : '@';
SHARP : '#'; // NOT Core2 syntax but gringo
AMPERSAND : '&';
QUOTE : '"';

PAREN_OPEN : '(';
PAREN_CLOSE : ')';
SQUARE_OPEN : '[';
SQUARE_CLOSE : ']';
CURLY_OPEN : '{';
CURLY_CLOSE : '}';
EQUAL : '=';
UNEQUAL : '<>' | '!=';
LESS : '<';
GREATER : '>';
LESS_OR_EQ : '<=';
GREATER_OR_EQ : '>=';

AGGREGATE_COUNT : '#count';
AGGREGATE_MAX : '#max';
AGGREGATE_MIN : '#min';
AGGREGATE_SUM : '#sum';

ID : ('a'..'z') ( 'A'..'Z' | 'a'..'z' | '0'..'9' | '_' )*;
VARIABLE : ('A'..'Z') ( 'A'..'Z' | 'a'..'z' | '0'..'9' | '_' )*;
NUMBER : '0' | ('1'..'9') ('0'..'9')*;
QUOTED_STRING : QUOTE ( '\\"' | . )*? QUOTE;

COMMENT : '%' ~[\r\n]* -> channel(HIDDEN);
MULTI_LINE_COMMEN : '%*' .*? '*%' -> channel(HIDDEN);
BLANK : [ \t\r\n\f]+ -> channel(HIDDEN);
