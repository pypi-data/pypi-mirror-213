'''BNF
<program> ::= <defn>* <expr>?
<expression> ::= <term>
              | <term> "+" <expression>
              | <term> "-" <expression>
              | <term> "*" <expression>
              | <term> "/" <expression>
              | "(" <expression> ")"
              | <term> "==" <expression>
              | <term> "<" <expression>
              | <term> ">" <expression>
              | <term> "<=" <expression>
              | <term> ">=" <expression>
              | "if" <expression> "then" <expression> "else" <expression>
              | "while" <expression> "do" <expression>
              | "lazy" <expression>
              | "{" <expression> "}"
              | "lambda" "(" <args> ")" <expression>
              | <expression> "|" <expression>

<term> ::= <factor>
        | <string>
        | <number>
        | <boolean>
        | <function_call>

<factor> ::= <number>
           | <string>
           | "true"
           | "false"

<function_call> ::= <function_call> "(" <args> ")"
                  | <identifier> "(" <args> ")"
                  | <identifier>

<args> ::= <arg>
         | <args> "," <arg>

<arg> ::= <expression>
'''

# Importing necessary libraries
from ply import lex, yacc
from maryChain.maryChainAST import Program, BinOp, UnaryOperation, Number, String, Boolean, Identifier, LetIn, LambdaFunction
from maryChain.maryChainAST import FunctionDef, FunctionCall, While, IfThenElse, IfThen, Lazy, Pipe, Import
import maryChain.maryChainAST as AST

# Define the list of tokens that the lexer will recognize
# Define the list of tokens that the lexer will recognize.
# These tokens represent the different types of elements that can appear in the language's syntax.
# Each token corresponds to a specific type of character sequence that can appear in the language's source code.
tokens = (
    # Basic types
    'IDENTIFIER', 'NUMBER', 'STRING', 'BOOLEAN',
    
    # Arithmetic operators
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'EQUALS',
    
    # Parentheses and brackets
    'LPAREN', 'RPAREN', 'LBRACK', 'RBRACK', 
    
    # Comma for argument separation
    'COMMA',
    
    # Control flow keywords
    'IF', 'THEN', 'ELSE', 'WHILE', 'DO', 'TRY', 'CATCH', 'FINALLY', 'LAZY',
    
    # Logical operators
    'AND', 'OR', 'NOT', 
    
    # Other operators
    'PIPE', 'IMPLIES', 
    
    # List functions
    'LEN', 'HEAD', 'TAIL', 'EMPTY', 'FOREACH',
    
    # Type cast functions
    'BOOLEANCAST', 'STRINGCAST', 'INTEGERCAST', 'DOUBLECAST',
    
    # Boolean values and null
    'TRUE', 'FALSE', 'NULL',
    
    # Function definition keyword
    'DEF',
    
    # Comparison operators
    'EQUALITY', 'GREATER', 'LESS', 'GREATEREQUAL', 'LESSEQUAL',
    
    # Dot for method calls or attribute access
    'DOT',
    
    # Braces for block structures
    'LCBRACE', 'RCBRACE',
    
    # Function, let-in, and lambda keywords
    'FUNC', 'LET', 'IN', 'LAMBDA',

    # import libraries
    'IMPORT', 'AS', 'NAMESPACE_OP',

)


# Define a dictionary of reserved words.
# These are words that have a special meaning in the language's syntax and cannot be used as identifiers.
# The keys in this dictionary are the string representations of the reserved words,
# and the values are their corresponding token types (defined above).
reserved = {
    # 'if', 'then', and 'else' are used for if-else control structures.
    'if' : 'IF',
    'then' : 'THEN',
    'else' : 'ELSE',

    # 'while' and 'do' are used for while-do loop control structures.
    'while' : 'WHILE',
    'do' : 'DO',

    # 'try', 'catch', and 'finally' are used for exception handling.
    'try' : 'TRY',
    'catch' : 'CATCH',
    'finally' : 'FINALLY',

    # 'lazy' is used for lazy evaluation.
    'lazy' : 'LAZY',
    
    # 'func' is used to define a function.
    'func' : 'FUNC',

    # 'true' and 'false' are boolean literals.
    'true' : 'TRUE',
    'false' : 'FALSE',

    # 'let' and 'in' are used for variable declarations.
    'let' : 'LET',
    'in' : 'IN',

    # 'lambda' is used for anonymous functions.
    'lambda': 'LAMBDA',
    
    # 'import' is used for importing libraries.
    'import': 'IMPORT',
    'as': 'AS'
    # add other reserved words here
}


# Define operator precedence rules.
# These rules dictate the order in which operations are performed when evaluating expressions, 
# i.e., which operations are done first.
# Each rule is a tuple where the first element is the associativity of the operators ('left' or 'right'),
# and the remaining elements are the operator(s) at that level of precedence.
precedence = (
    # The pipe operator has the lowest precedence and is left-associative.
    ('left', 'PIPE'),

    # The logical OR operator is next in line with left associativity.
    ('left', 'OR'),

    # The logical AND operator follows with left associativity.
    ('left', 'AND'),

    # The logical NOT operator is next with left associativity.
    ('left', 'NOT'),

    # The equality and relational operators all have the same level of precedence and are left-associative.
    ('left', 'EQUALITY', 'GREATER', 'LESS', 'GREATEREQUAL', 'LESSEQUAL'),

    # The addition and subtraction operators are at the next level of precedence, also left-associative.
    ('left', 'PLUS', 'MINUS'),

    # The multiplication and division operators are next with higher precedence, left-associative.
    ('left', 'TIMES', 'DIVIDE'),

    # The unary minus operator has the highest precedence and is right-associative.
    ('right', 'UMINUS'),
)


# Define regular expressions for each token
t_DEF = r'def'
# t_PLACEHOLDER = r'_'
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_EQUALS = r'='
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACK = r'\['
t_RBRACK = r'\]'
t_COMMA = r','
t_AND = r'&&'
t_OR = r'\|\|'
t_NOT = r'not'
t_PIPE = r'\|'
t_IMPLIES = r'->'
t_LEN = r'len\(\)'
t_HEAD = r'head\(\)'
t_TAIL = r'tail\(\)'
t_EMPTY = r'empty\(\)'
t_FOREACH = r'foreach\('
t_BOOLEANCAST = r'boolean\(\)'
t_STRINGCAST = r'string\(\)'
t_INTEGERCAST = r'integer\(\)'
t_DOUBLECAST = r'double\(\)'
t_DOT = r'\.'
t_EQUALITY = r'=='
t_GREATER = r'>'
t_LESS = r'<'
t_GREATEREQUAL = r'>='
t_LESSEQUAL = r'<='
t_LCBRACE = r'\{'
t_RCBRACE = r'\}'
t_ignore  = ' \t'
t_IMPORT = 'import'  # Simply match the keyword
t_AS = 'as'
t_NAMESPACE_OP = r'::'

def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*(\.[a-zA-Z_][a-zA-Z_0-9]*)*'
    t.type = reserved.get(t.value, 'IDENTIFIER')    # Check for reserved words
    return t

def t_NUMBER(t):
    r'\d+(\.\d+)?'
    t.value = float(t.value) if '.' in t.value else int(t.value)
    return t

def t_STRING(t):
    r'(\'([^\\\n]|(\\.))*?\'|\"([^\\\n]|(\\.))*?\")'
    t.value = t.value[1:-1]  # remove the quotes
    return t

def t_BOOLEAN(t):
    r'(true|false)'
    t.value = (t.value == 'true')  # convert to Python boolean
    return t

def t_COMMENT(t):
    r'\#.*'
    pass
    # No return value. Token discarded

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    line = t.lexer.lineno
    position = t.lexpos
    value = t.value[0]
    print(f"Illegal character at line {line}, position {position}: {value}")
    t.lexer.skip(1)


# --------------------------------------------------------------
# Initialize the lexer
lexer = lex.lex()

def p_program(t):
    '''program : definitions imports expression
               | imports expression
               | definitions expression
               | imports
               | definitions
               | expression'''
    """
    Handles the parsing of the whole program.
    
    The function handles the parsing of the program which consists of function definitions,
    imports, and the main expression. Each component is optional and can appear zero or more
    times (for definitions and imports) or at most once (for expression).

    Parameters:
    t: A list where each element represents a component of the syntax being parsed.

    Sets:
    t[0]: A Program object, representing the whole program.
    """

    if len(t) == 2:
        imports = []
        definitions = []
        expression = t[1]
        if isinstance(t[1],list):
            if len(t[1])> 0:
                if isinstance(t[1][0], Import):
                    imports = t[1]
                    expression = None
                elif isinstance(t[1][0], FunctionDef):
                    definitions = t[1]
                    expression = None
            
        t[0] = Program(imports, definitions, expression)

    elif len(t) == 3:
        # is definition or expresssion?
        imports = []
        definitions = []
        if isinstance(t[1],list):
            if len(t[1])> 0:
                if isinstance(t[1][0], Import):
                    imports = t[1]
                elif isinstance(t[1][0], FunctionDef):
                    definitions = t[1]

        t[0] = Program(definitions, imports, t[2])
    elif len(t) == 4:
        t[0] = Program(t[1], t[2], t[3])


def p_expression_let_in(t):
    'expression : LET IDENTIFIER EQUALS expression IN expression'
    """
    Handles the parsing of 'let in' expressions.

    The function handles the 'let' keyword syntax which is used to declare variables.
    In the syntax 'let IDENTIFIER = expression in expression', an IDENTIFIER (variable name)
    is assigned the value of an expression, and this variable is then available within the
    scope of the next expression. This resembles local variable assignment in other programming
    languages.

    Parameters:
    t: A list where each element represents a component of the syntax being parsed. The elements
       correspond to the 'let IDENTIFIER = expression in expression' structure.

    Sets:
    t[0]: A LetIn object, representing the variable assignment and scope for the 'let in'
          construct.
    """
    t[0] = LetIn(t[2], t[4], t[6])



def p_expression_binop(t):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression'''
    """
    Handles the parsing of binary operations.

    The function handles the basic binary mathematical operations: addition, subtraction,
    multiplication, and division. For a given operation 'expression OPERATOR expression', it
    constructs a BinOp object with the two expressions and the operator as arguments.

    Parameters:
    t: A list where each element represents a component of the syntax being parsed. The elements
       correspond to the 'expression OPERATOR expression' structure.

    Sets:
    t[0]: A BinOp object, representing the binary operation.
    """
    t[0] = BinOp(t[1], t[2], t[3])


# --------------------------------------------------------------
#  import
def p_namespace(p):
    '''namespace : IDENTIFIER
                 | namespace DOT IDENTIFIER'''
    if len(p) == 2:
        # If namespace is a single identifier, make it a one-element list
        p[0] = [p[1]]
    else:
        # If namespace is another namespace followed by an identifier, 
        # append the identifier to the list of identifiers in the namespace
        p[0] = p[1] + [p[3]]

def p_import(t):
    'import : IMPORT IDENTIFIER AS IDENTIFIER'
    print("Import statement detected: ", t[2], t[4])
    t[0] = Import(t[2], t[4])

def p_imports(t):
    '''
    imports : import
            | imports import
    '''
    # if there's only one import statement
    if len(t) == 2:
        t[0] = [t[1]]
    # if there's more than one import statement
    else:
        t[1].append(t[2])
        t[0] = t[1]


# Rule for unary minus operation
def p_expression_uminus(t):
    'expression : MINUS expression %prec UMINUS'
    t[0] = UnaryOperation('-', t[2])  # Represent unary minus as a UnaryOperation.

def p_expression_paren(t):
    'expression : LPAREN expression RPAREN'
    t[0] = t[2]  # No change here, parentheses do not change the AST.

def p_term_factor(t):
    'term : factor'
    t[0] = t[1]  # No change here, we are just passing up the node.

def p_factor_string(t):
    'factor : STRING'
    t[0] = String(t[1])  # Wrap the string in a String node.

def p_factor_num(t):
    'factor : NUMBER'
    t[0] = Number(t[1])  # This will try to cast to int first, then float

def p_factor_boolean(t):
    '''factor : TRUE
              | FALSE'''
    t[0] = Boolean(t[1] == 'true')  # This will try to cast to boolean

# --------------------------------------------------------------
#  while

def p_expression_while(t):
    'expression : WHILE expression DO expression'
    t[0] = While(t[2], t[4])

# --------------------------------------------------------------
#  if then else

def p_expression_if_then_else(t):
    'expression : IF expression THEN expression ELSE expression'
    """
    Handles the parsing of if-then-else expressions.

    The function processes if-then-else constructs in the language. For an input of the form
    'IF expression THEN expression ELSE expression', it constructs an IfThenElse object with the 
    conditional expression, the expression to evaluate if the condition is true, and the expression 
    to evaluate if the condition is false, as arguments.

    Parameters:
    t: A list where each element represents a component of the syntax being parsed. The elements
       correspond to the 'IF expression THEN expression ELSE expression' structure.

    Sets:
    t[0]: An IfThenElse object, representing the if-then-else construct.
    """
    t[0] = IfThenElse(t[2], t[4], t[6])


def p_expression_if_then(t):
    'expression : IF expression THEN expression'
    """
    Handles the parsing of if-then expressions.

    The function processes if-then constructs in the language. For an input of the form
    'IF expression THEN expression', it constructs an IfThen object with the 
    conditional expression and the expression to evaluate if the condition is true, as arguments.

    Parameters:
    t: A list where each element represents a component of the syntax being parsed. The elements
       correspond to the 'IF expression THEN expression' structure.

    Sets:
    t[0]: An IfThen object, representing the if-then construct.
    """
    t[0] = IfThen(t[2], t[4])


# --------------------------------------------------------------
#  Lazy

def p_lazy_expr(t):
    'expression : LAZY expression'
    """
    Handles the parsing of 'LAZY expression' constructs in the language.

    The function processes constructs beginning with 'LAZY'. For an input of the form
    'LAZY expression', it constructs a Lazy object with the expression as an argument.

    Parameters:
    t: A list where each element represents a component of the syntax being parsed. The elements
       correspond to the 'LAZY expression' structure.

    Sets:
    t[0]: A Lazy object, representing the lazy evaluation construct.
    """
    t[0] = Lazy(t[2])  # Wrap the expression in a Lazy node.


def p_expression_braces(t):
    'expression : LCBRACE expression RCBRACE'
    """
    Handles the parsing of expressions within braces in the language.

    The function processes constructs that are enclosed within braces '{}'. For an input of the form
    '{expression}', it constructs a Lazy object with the expression as an argument.

    Parameters:
    t: A list where each element represents a component of the syntax being parsed. The elements
       correspond to the '{expression}' structure.

    Sets:
    t[0]: A Lazy object, representing the expression enclosed in braces.
    """
    t[0] = Lazy(t[2])  # Wrap the expression in a Lazy node.


def p_expression_lambda(t):
    'expression : LAMBDA LPAREN args RPAREN expression'
    """
    Handles the parsing of lambda expressions in the language.

    The function processes constructs of the form 'lambda (args) expression'. It creates a LambdaFunction 
    object with the arguments and the body expression as parameters.

    Parameters:
    t: A list where each element represents a component of the syntax being parsed. The elements
       correspond to the 'lambda (args) expression' structure.

    Sets:
    t[0]: A LambdaFunction object, representing the lambda expression.
    """
    t[0] = LambdaFunction(t[3], t[5])  # Create a new LambdaFunction node.


def p_expression_pipe(p):
    'expression : expression PIPE expression'
    """
    Handles the parsing of pipe operations in the language.

    The function processes constructs of the form 'expression | expression'. It creates a Pipe 
    object with the left and right expressions as parameters.

    Parameters:
    p: A list where each element represents a component of the syntax being parsed. The elements
       correspond to the 'expression | expression' structure.

    Sets:
    p[0]: A Pipe object, representing the pipe operation.
    """
    p[0] = Pipe(p[1], p[3])  # Create a new Pipe node.

def p_expression_func_call(t):
    'expression : function_call'
    """
    Handles the parsing of function calls in the language.

    The function processes constructs where a function is called. It sets the parsed function call
    as the expression's value.

    Parameters:
    t: A list where each element represents a component of the syntax being parsed. The elements
       correspond to the 'function_call' structure.

    Sets:
    t[0]: The parsed function call.
    """
    t[0] = t[1]  # Set the function call as the value of the expression.


def p_expression_term(t):
    'expression : term'
    """
    Processes the parsing of an individual term in the language.

    This function is used to parse individual terms, which are the simplest element 
    of an expression in the language. When a term is encountered, the value of the 
    term is set as the value of the expression.

    Parameters:
    t: A list where each element represents a component of the syntax being parsed. 
       The elements correspond to the 'term' structure.

    Sets:
    t[0]: The parsed term.
    """
    t[0] = t[1]  # Set the term as the value of the expression.


def p_error(t):
    """
    Handles syntax errors in the parsed code.

    This function is invoked when a syntax error is detected in the parsed code. 
    It can handle two types of errors: one where an unexpected token is encountered, 
    and one where the parser reaches the end of the file unexpectedly (EOF). For the 
    former, the function prints the line and position of the error, as well as the 
    offending token and its value.

    Parameters:
    t: A PLY token instance containing information about the token that resulted in 
       an error, or None if the error was due to reaching EOF unexpectedly.

    Returns:
    None
    """
    if t is None:  # If the error is due to EOF.
        print("Syntax error at EOF")
    else:  # If the error is due to an unexpected token.
        line = t.lexer.lineno  # Line number where the error occurred.
        position = t.lexpos  # Position in the file where the error occurred.
        token = t.type  # Type of the offending token.
        value = t.value  # Value of the offending token.
        print(f"Syntax error at line {line}, position {position}")
        print(f"Offending token: {token}")
        print(f"Offending value: {value}")



# -------------------------------------------------------------------
# Rule for function calls

def p_function_definition(t):
    'function_definition : FUNC IDENTIFIER LPAREN args RPAREN LCBRACE expression RCBRACE'
    """
    Parses function definition expressions.

    This function parses a function definition, which consists of the 'func' keyword,
    followed by an identifier (the function's name), parentheses enclosing arguments 
    (if any), and a block of code enclosed in curly braces. 

    After successful parsing, a FunctionDef object is constructed with the function name, 
    arguments, and the expression (body of the function) as arguments.

    Parameters:
    t: A PLY lex token instance. It is a tuple where t[2] is the function's name, t[4] is 
       the function's arguments, and t[7] is the body of the function (an expression).

    Returns:
    None
    """
    # FunctionDef is a hypothetical class to store function definitions. This will need to be 
    # defined elsewhere in your code. It takes the function name, the arguments, and the body 
    # of the function (an expression).
    t[0] = FunctionDef(t[2], t[4], t[7]) 

def p_definitions(t):
    '''
    definitions : function_definition
                | definitions function_definition
    '''
    # if there's only one function definition
    if len(t) == 2:
        t[0] = [t[1]]
    # if there's more than one function definition
    else:
        t[1].append(t[2])
        t[0] = t[1]


# def p_function_call(t):
    '''function_call : function_call LPAREN args RPAREN
                     | IDENTIFIER LPAREN args RPAREN
                     | IDENTIFIER'''
    """
    Parses function call expressions.

    This function parses a function call, which may be a simple function call with or without 
    arguments, or a chained function call with or without arguments. It constructs a FunctionCall 
    object with the function's name and arguments.

    Parameters:
    t: A PLY lex token instance. If it is a simple function call, t[1] is the function's name 
       and t[3] are the function's arguments. If it is a chained function call, t[1] is the 
       previous function call, and t[3] are the arguments of the next function in the chain.

    Returns:
    None
    """
    # # Check if there are arguments in the function call, if not set it to an empty list
    # args = [] if len(t) == 2 else t[3]
    # # Get the function name (it can be an identifier or another function call in case of function chaining)
    # function_name = t[1]
    # # FunctionCall and Identifier are hypothetical classes to store function calls and identifiers.
    # # These will need to be defined elsewhere in your code. FunctionCall takes the function name 
    # # (wrapped in an Identifier instance) and the arguments of the function.
    # t[0] = FunctionCall(Identifier(function_name), args) 


def p_function_call(t):
    '''function_call : function_call LPAREN args RPAREN
                     | IDENTIFIER LPAREN args RPAREN
                     | IDENTIFIER'''
    if len(t) == 4 and isinstance(t[2], FunctionCall):
        # Function call following another function call
        # Treat it as currying
        t[0] = FunctionCall(t[2], [t[4]])
    elif len(t) == 2:
        # Single function call
        args = []
        function_name = t[1]
        t[0] = FunctionCall(Identifier(function_name), args)
    else:
        # Function call with arguments
        args = t[3]
        function_name = t[1]
        t[0] = FunctionCall(Identifier(function_name), args)


def p_args(t):
    '''args : args COMMA arg
            | arg
            | '''
    """
    Parses arguments of a function or lambda.

    This function parses the arguments passed to a function call or a lambda function in the source code. 
    The arguments could be none, one, or many. It returns a list of arguments.

    Parameters:
    t: A PLY lex token instance. In the case of multiple arguments, t[1] is the list of arguments parsed 
       so far, and t[3] is the next argument. In the case of a single argument, t[1] is the argument. 

    Returns:
    None
    """
    if len(t) == 1:
        # No arguments are passed in the function call or lambda function
        t[0] = []
    elif len(t) == 2:
        # Only one argument is passed
        t[0] = [t[1]]
    else:
        # Multiple arguments are passed
        t[1].append(t[3])  # Append the next argument to the list of arguments
        t[0] = t[1]  # Set the list of arguments as the parsed result


def p_arg(t):
    '''arg : expression'''
    """
    Parses a single argument.

    This function is responsible for parsing a single argument in a function call or a lambda function 
    in the source code. It takes the expression as an argument and returns it.

    Parameters:
    t: A PLY lex token instance. t[1] is the parsed expression representing the argument.

    Returns:
    None
    """
    # The expression parsed is the argument
    t[0] = t[1]


# -------------------------------------------------------------------
# Initialize the parser
parser = yacc.yacc()
AST.inject_parsing(parser.parse)
# -------------------------------------------------------------------

def eval(s):
    """
    Evaluates a given string as a maryChain program.

    This function takes a string representation of a program written in the maryChain language,
    parses it into an abstract syntax tree (AST), and then evaluates it. If the result of the evaluation is a Lazy node,
    it is further evaluated to get the final result. 

    Parameters:
    s (str): The string to be evaluated as a maryChain program.

    Returns:
    result: The final result of evaluating the maryChain program. It can be a value of any data type supported in maryChain, 
    or None if there was a syntax error in the program.
    """
    # Parse the input string to an AST using the defined parser
    ast = parser.parse(s)

    # If there was a syntax error, print an error message and return None
    if ast is None:
        print("Syntax Error")
        return None

    # Otherwise, evaluate the AST using the evaluate method of the AST class
    result = AST.evaluate(ast)

    # If the result is a Lazy node, evaluate it to get the final result
    if isinstance(result, Lazy):
        result = result.evaluate()

    # Return the result of the evaluation
    return result
