Sure, here is an example of what your README.md could look like:

# MaryChain Parser

MaryChain Parser is a basic lexer and parser written in Python using the Python Lex-Yacc (PLY) library. It uses LR-parsing which is suitable for larger grammars.

## Features

- Mathematical operations: addition, subtraction, multiplication, and division
- Parentheses to dictate the order of operations
- Unary minus operation
- Conditional statements: if-then-else
- Loop construct: while-do
- Function calls with arguments
- Lazy evaluation: expressions are only evaluated when needed
- Pipeline operation: pipes the result of one expression into another
- Placeholder: represents a wildcard or unnamed entity for pattern matching

## Usage

To parse and evaluate a string `s`, use the `eval` function:

```python
result = eval(s)
```

If there is a syntax error in the string, `eval` will print an error message and return `None`. If the string can be parsed successfully, `eval` will return the result of evaluating the parsed Abstract Syntax Tree (AST).

## Technical Details

### Tokens

The lexer recognizes a variety of tokens, such as `NUMBER`, `STRING`, `IDENTIFIER`, and various keywords and symbols.

### Grammar

The parser uses the following grammar:

```
<program> ::= <definition>* <import>* <expression>?

<definition> ::= <identifier> <identifier>* '=' <expression>

<import> ::= 'import' <identifier> 'as' <identifier>

<expression> ::= <boolean>
    | <number>
    | <string>
    | <identifier>
    | <unary>
    | <binary>
    | <function_call>
    | <let_in>
    | <if_then_else>
    | <if_then>
    | <while>
    | <pipe>
    | <lambda_function>

<boolean> ::= 'True' | 'False'

<number> ::= [0-9]+('.'[0-9]+)?

<string> ::= '"' <char>* '"'

<identifier> ::= [a-zA-Z_][a-zA-Z0-9_]*

<unary> ::= ('-' | 'not') <expression>

<binary> ::= <expression> ('+' | '-' | '*' | '/' | '&&' | '||' | '->' | '>' | '<' | '>=' | '<=' | '==') <expression>

<function_call> ::= <identifier> '(' <expression>* ')'

<let_in> ::= 'let' <identifier> '=' <expression> 'in' <expression>

<if_then_else> ::= 'if' <expression> 'then' <expression> 'else' <expression>

<if_then> ::= 'if' <expression> 'then' <expression>

<while> ::= 'while' <expression> <expression>

<pipe> ::= <expression> '|' <expression>

<lambda_function> ::= 'lambda' <identifier>* ':' <expression>

```

Operator precedence and associativity are defined separately in the parser.

### Abstract Syntax Tree (AST)

The parser generates an AST from the input string. Each node in the tree is an instance of a class defined in `maryChainAST.py`, such as `BinOp`, `UnaryOperation`, `Number`, `String`, `Placeholder`, `Identifier`, `FunctionCall`, `While`, `IfThenElse`, `IfThen`, `Lazy`, and `Pipe`.

### Evaluation

The `eval` function evaluates the AST using a visitor pattern: each node class has an `evaluate` method that computes the value of the node based on its child nodes.

Certainly, here is a documentation of MaryChain's semantics:

# MaryChain Language Semantics

The MaryChain language provides a set of constructs and features that allow users to write functional code.

## Language Constructs

1. **Definitions**: The program can include definitions which bind an identifier to a function or value. This function or value can then be used later in the code by referencing the identifier.

    Example: `let sum x y = x + y in sum 5 3`

2. **Import**: The `import` statement allows users to import modules. Imported modules are given an alias which is used to call the module's functions. The alias is used along with the function name separated by a `::` symbol.

    Example: `import numpy as np` and use it as `np::sum(x,y)`

3. **Expressions**: Expressions can be any type of values, identifiers, unary and binary operations, function calls, conditionals (if-then-else or if-then), and control flow structures (such as while). Expressions can be evaluated to give a result.

4. **Function Calls**: Functions can be called with zero or more arguments. User-defined functions, built-in functions, and functions from imported modules can all be called.

    Example: `sum(5, 3)`

5. **Unary Operations**: The unary operations available are negation (`-`) and logical not (`not`).

6. **Binary Operations**: MaryChain supports common arithmetic and logical binary operations.

7. **Let-in Expression**: This construct allows local bindings. It binds an expression to an identifier in the scope of another expression.

8. **If-Then-Else and If-Then**: These are conditional structures. `If-Then-Else` evaluates the first expression if the condition is true, and the second expression if it is false. `If-Then` only evaluates the first expression if the condition is true.

9. **While**: This is a control flow structure that evaluates an expression while a condition is true.

10. **Pipe Operator**: The pipe operator (`->`) allows users to chain function calls in a clear and readable way. The output of the first function call is passed as the input to the second function call.

11. **Lambda Functions**: Users can create anonymous functions (also known as lambda functions) with the `lambda` keyword.

## Evaluation Semantics

Evaluation semantics in MaryChain are mostly similar to those in traditional functional programming languages. Here are some specifics:

1. **Lazy Evaluation**: Expressions are evaluated in a lazy manner. This means that an expression is not evaluated until its value is needed. This is particularly important when dealing with infinite data structures or long-running computations.

2. **Environment**: The environment is a mapping of identifiers to their current values. When a new value is bound to an identifier using a `let-in` expression, a new environment is created where the identifier maps to the new value. The old environment is restored after the `let-in` expression is evaluated.

3. **Function Application**: When a function is called, the arguments are evaluated from left to right. The function body is then evaluated in a new environment where the function parameters are bound to the evaluated arguments.

4. **Control Flow**: `if-then-else` and `while` structures are evaluated in the usual way. The condition is evaluated first, and depending on its value, the corresponding expression(s) is/are evaluated. In a `while` structure, the body is evaluated repeatedly as long as the condition is true.

5. **Pipe Operator**: When using the pipe operator (`|`), the expression on the left is evaluated first. Its value is then passed as an argument to the function call on the right.

