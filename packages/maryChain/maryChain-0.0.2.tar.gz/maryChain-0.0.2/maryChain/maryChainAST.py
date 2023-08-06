from abc import ABC, abstractmethod
import importlib
import inspect
import sys, os
import types

core_lib = os.path.dirname(os.path.realpath(__file__)) + '/../Workers'
sys.path.append("/Users/alessioricco/Documents/GitHub/GPTWorkers")
print(sys.path)


def add_module_functions_to_dict(module_name,alias):
    # core.hello()
    try:
        module=importlib.import_module(module_name)
    except ModuleNotFoundError:
        print(f"The module {module_name} was not found.")
        return
    
    FUNCTION_DICT[alias] = {}

    for(name,func) in inspect.getmembers(module,inspect.getmodule):
        if callable(func):
            try:
                args = inspect.getfullargspec(func).args
            except:
                args = []
            FUNCTION_DICT[alias][name]=FunctionDef(name,args,curry(func))



# Now you can add the functions of a module to the FUNCTION_DICT like this:
# add_module_functions_to_dict('aleph')


class Evaluable(ABC):
    """
    Abstract base class for all evaluable entities in the maryChain language.

    This class defines the interface for all classes that can be evaluated in the maryChain language. 
    It is an abstract base class (ABC), which means that it cannot be instantiated directly. 
    Instead, other classes should inherit from this class and implement the abstract methods defined here.

    Each evaluable entity in maryChain is represented by an instance of a class that inherits from Evaluable.
    This class has an abstract method `evaluate`, which should be implemented by all subclasses to define their evaluation semantics.

    The evaluate method of a class representing an evaluable entity in maryChain takes keyword arguments (`kwargs`) 
    which could be used to provide context necessary for evaluation, such as a dictionary of variable names and their values. 
    """

    @abstractmethod
    def evaluate(self, **kwargs):
        """
        Abstract method for evaluating an entity.

        This method is meant to be overridden by each concrete subclass of Evaluable. The overriding method 
        should implement the specific evaluation semantics of the entity it represents.

        Parameters:
        **kwargs: Arbitrary keyword arguments that could be used to provide context necessary for evaluation. 

        Returns:
        The result of evaluating the entity.
        """
        pass


class Expression(Evaluable):
    """
    Abstract base class for all expressions in the maryChain language.
    Inherits from the Evaluable abstract base class.
    """
    pass

class Program(Evaluable):
    def __init__(self, definitions, imports, expression):
        self.definitions = definitions
        self.imports = imports
        self.expression = expression

    def evaluate(self):
        for definition in self.definitions:
            definition.evaluate()

        for import_stmt in self.imports:
            import_stmt.evaluate()

        if self.expression:
            return self.expression.evaluate()

class Import(Expression):
    def __init__(self, module_parts, alias):
        # self.module_name = '.'.join(module_parts)
        self.module_name = module_parts
        self.alias = alias

    def evaluate(self):
        add_module_functions_to_dict(self.module_name, self.alias)



# --------------------------------------------------------------
#  external functions
def print_func(x):
    if isinstance(x, Lazy):
        x = x.evaluate()
    print(x)
    return x

def add_func(x, y):
    if isinstance(x, Lazy):
        x = x.evaluate()
    if isinstance(y, Lazy):
        y = y.evaluate()
    return x + y

def eval_func(x):
    return x.func()

def curry(func):
    """
    This function transforms a given function into a curried function.
    
    Currying is a technique in functional programming where a function with multiple arguments is 
    transformed into a sequence of functions, each with a single argument. 
    For example, a function of two arguments, f(x, y), produces a function of one argument, g(y) = f(x, y), 
    which can be called with one argument to produce the result.

    Parameters:
    func (function): The function to be curried.

    Returns:
    function: The curried version of the original function.
    """
    
    def curried(*args, **kwargs):
        """
        This function represents the curried version of the original function.
        
        It tries to call the original function with the provided arguments. 
        If a TypeError occurs because one argument is missing, it returns a new function that 
        takes one argument and calls the original function with the previously provided arguments 
        and this new argument.
        """
        try:
            return func(*args, **kwargs)
        except TypeError as e:
            if 'missing 1 required positional argument' in str(e):
                return lambda x: func(*args, x, **kwargs)
            else:
                raise e

    return curried  # Return the curried function.


# def curry(func):
#     def curried(*args, **kwargs):
#         if len(args) + len(kwargs) >= func.__code__.co_argcount:
#             return func(*args, **kwargs)
#         else:
#             # Return a new FunctionDef instance
#             return FunctionDef(func.__name__, func.__code__.co_varnames[len(args):], curried)
#     return curried



# --------------------------------------------------------------
#  environment

ENVIRONMENT = {}

# --------------------------------------------------------------

class FunctionDef:
    """
    Represents a function definition in the maryChain language. Functions can either be user-defined or 
    built-in functions.
    """

    def __init__(self, name, args, body):
        """
        Initialize a function definition with a name, a list of argument names, and a body.
        
        Parameters:
        name (str): The name of the function.
        args (list): The names of the arguments of the function.
        body (expression): The body of the function which can be an expression or a Python callable 
                           (for built-in functions).
        """
        self.name = name
        self.args = args
        self.expected_args = len(args)

        # Check if the body is a function, in which case this is a built-in function
        if callable(body):
            self.is_builtin = True
            self.func = body
        else:
            self.is_builtin = False
            self.body = body

    def evaluate(self, **kwargs):
        """
        Evaluates the function definition by adding it to the global environment and returning itself.
        
        Returns:
        FunctionDef: This function definition.
        """
        if len(self.args) == 0:
            return self.body
        ENVIRONMENT[self.name] = self
        return self

    # def __call__(self, *args):
        """
        Defines how the function definition behaves when called. If the function is built-in, it simply 
        calls the function with the provided arguments. Otherwise, it updates the local environment with 
        the function arguments and evaluates the body of the function in this environment.

        If not all arguments are provided, it returns a new function that takes the remaining arguments.

        Parameters:
        args (list): The arguments to call the function with.

        Returns:
        expression: The result of evaluating the function body.
        """
        # if self.is_builtin:
        #     return self.func(*args)
        
        # if len(args) > len(self.args):
        #     raise TypeError(f"{self.name} takes {len(self.args)} arguments but {len(args)} were given")

        # # Make a copy of the global environment and update it with the function arguments
        # local_env = ENVIRONMENT.copy()
        # local_env.update(zip(self.args, args))

        # if len(args) < len(self.args):
        #     # Not all arguments provided, return a new function that takes the remaining arguments
        #     remaining_args = self.args[len(args):]
        #     return curry(FunctionDef(self.name, remaining_args, self.body).evaluate(local_env))

        # # Evaluate the body of the function in the local environment and return the result
        # return self.body.evaluate(local_env)

    def __call__(self,*args):
        if self.is_builtin:
            return curry(self.func)(*args)
        if len(args)>len(self.args):
            raise TypeError(f"{self.name} takes {len(self.args)} arguments but {len(args)} were given")
        local_env=ENVIRONMENT.copy()
        local_env.update(zip(self.args,args))
        if len(args)<len(self.args):
            remaining_args=self.args[len(args):]
            return curry(FunctionDef(self.name,remaining_args,self.body).evaluate(local_env))
        return self.body.evaluate(local_env)

class FunctionCall(Expression):
    def __init__(self, func, args):
        self.func = func
        self.args = args

    def evaluate(self, **kwargs):
        func = None
        if isinstance(self.func, Identifier):
            # Look up function by name
            name = self.func.name
            if self.func.name in ENVIRONMENT:
                func = ENVIRONMENT[self.func.name]
            else:
                # namespace
                if "." in name:  # Check if func is a qualified function name
                    module_name, func_name = name.split(".")
                    if (module_name not in FUNCTION_DICT) or (func_name not in FUNCTION_DICT[module_name]):
                        raise ValueError(f"Function {self.func} is not defined")
                    func = FUNCTION_DICT[module_name][func_name]
                else:
                    func = FUNCTION_DICT[self.func.name]
        elif isinstance(self.func, FunctionCall):
            # Evaluate inner function call to get function
            func = self.func.evaluate()
        else:
            raise ValueError(f"Function {self.func} is not defined")

        if func.is_builtin:
            # If the function is a built-in function, call it with the provided arguments
            # This will raise an exception if there are too few arguments
            evaluated_args = [arg.evaluate() for arg in self.args]
            return func(*evaluated_args)
        else:
            # If the function is a user-defined function and there are too few arguments, return a new FunctionDef for currying
            if len(self.args) < func.expected_args:
                return FunctionDef(func.name, func.args[len(self.args):], func.body)

            # If there are enough arguments, evaluate the function call as normal
            evaluated_args = [arg.evaluate() for arg in self.args]
            return func(*evaluated_args)


class LetIn(Expression):
    """
    This class represents a "let-in" expression in the maryChain language. A let-in expression
    is used to bind a value to an identifier in a certain scope. The syntax is as follows:

        let <identifier> = <expression> in <body>

    After the expression is evaluated, the result is bound to the identifier, and this binding
    is valid within the body of the let-in expression.
    """

    def __init__(self, identifier, value_expression, body):
        """
        Initializes a new instance of the LetIn class.

        Args:
            identifier: The identifier to which the value will be bound.
            value_expression: The expression that will be evaluated to determine the value
                to bind to the identifier.
            body: The body of the let-in expression, where the identifier is bound to the value.
        """
        self.identifier = identifier
        self.value_expression = value_expression
        self.body = body

    def evaluate(self):
        """
        Evaluates the let-in expression.

        This is done by first evaluating the value expression, then creating a new scope where the 
        identifier is bound to the value. The body of the let-in expression is then evaluated in this new 
        scope. Finally, the old scope is restored.

        Returns:
            The result of evaluating the body of the let-in expression.
        """
        # Evaluate the value expression and create a new scope where the identifier is bound to the value.
        value = self.value_expression.evaluate()
        new_env = ENVIRONMENT.copy()
        new_env[self.identifier] = value

        # Evaluate the body in the new scope.
        old_env = ENVIRONMENT
        ENVIRONMENT = new_env
        try:
            return self.body.evaluate()
        finally:
            ENVIRONMENT = old_env  # Restore the old environment



class BinOp(Expression):
    """
    This class represents a binary operation in the maryChain language. A binary operation is 
    an operation that takes two operands and performs a specified operation on them.

    The supported operators are:
        '+'  - addition
        '-'  - subtraction
        '*'  - multiplication
        '/'  - division
        '&&' - logical AND
        '||' - logical OR
        '->' - logical implication
        '>'  - greater than
        '<'  - less than
        '>=' - greater than or equal to
        '<=' - less than or equal to
        '==' - equality (same as)
    """

    def __init__(self, left, op, right):
        """
        Initializes a new instance of the BinOp class.

        Args:
            left: The left operand of the binary operation.
            op: The operator of the binary operation.
            right: The right operand of the binary operation.
        """
        self.left = left
        self.op = op
        self.right = right

    def evaluate(self, **kwargs):
        """
        Evaluates the binary operation and returns the result.

        This is done by first evaluating the left and right operands, then applying the operator to the results.

        Returns:
            The result of the binary operation.

        Raises:
            ValueError: If the operator is not supported.
        """
        if self.op == '+':
            return evaluate(self.left) + evaluate(self.right)
        if self.op == '-':
            return evaluate(self.left) - evaluate(self.right)
        if self.op == '*':
            return evaluate(self.left) * evaluate(self.right)
        if self.op == '/':
            return evaluate(self.left) / evaluate(self.right)
        if self.op == '&&':
            return evaluate(self.left) and evaluate(self.right)
        if self.op == '||':
            return evaluate(self.left) or evaluate(self.right) 
        if self.op == '->':
            return not evaluate(self.left) or evaluate(self.right)
        if self.op == '>':
            return evaluate(self.left) > evaluate(self.right) 
        if self.op == '<':
            return evaluate(self.left) < evaluate(self.right)    
        if self.op == '>=':
            return evaluate(self.left) >= evaluate(self.right)   
        if self.op == '<=':
            return evaluate(self.left) <= evaluate(self.right) 
        if self.op == '==':
            return evaluate(self.left) == evaluate(self.right) 
        raise ValueError(f'Unknown operator: {self.operator}')


class Number(Expression):
    """
    This class represents a numeric literal in the maryChain language. 

    A numeric literal can be an integer or a floating-point number, and this class can handle both.
    """

    def __init__(self, value):
        """
        Initializes a new instance of the Number class.

        Args:
            value: The numeric value represented by the instance. Can be either an integer or a float.

        Note:
            If the value cannot be converted to an integer, it will be converted to a float.
        """
        self.value = value
        try:
            self.value = int(value)
        except ValueError:
            self.value = float(value)

    def evaluate(self, **kwargs):
        """
        Evaluates the number, which in practice means returning the numeric value.

        Returns:
            The numeric value of the Number instance.
        """
        return self.value


class String(Expression):
    """
    This class represents a string literal in the maryChain language. 

    The `String` class inherits from the `Expression` class and provides methods for the manipulation of string values.
    """

    def __init__(self, value):
        """
        Initializes a new instance of the String class.

        Args:
            value: The string value represented by the instance.
        """
        self.value = value

    def evaluate(self, **kwargs):
        """
        Evaluates the string, which in practice means returning the string value.

        Returns:
            The string value of the String instance.
        """
        return self.value


class Boolean(Expression):
    """
    This class represents a boolean literal in the maryChain language. 

    The `Boolean` class inherits from the `Expression` class and provides methods for the manipulation of boolean values.
    """

    def __init__(self, value):
        """
        Initializes a new instance of the Boolean class.

        Args:
            value: The boolean value represented by the instance.
        """
        self.value = bool(value)

    def evaluate(self, **kwargs):
        """
        Evaluates the boolean, which in practice means returning the boolean value.

        Returns:
            The boolean value of the Boolean instance.
        """
        return self.value


class Identifier(Expression):
    """
    This class represents an Identifier in the maryChain language. 

    The `Identifier` class inherits from the `Expression` class and provides a way to interact with variables
    and function calls.
    """

    def __init__(self, name):
        """
        Initializes a new instance of the Identifier class.

        Args:
            name: The name of the variable or function this identifier refers to.
        """
        self.name = name

    def evaluate(self, **kwargs):
        """
        Evaluates the Identifier. If the identifier name is in the environment, its value is returned. 
        If the name corresponds to a function in the function dictionary, the name is returned. 
        If the name is an instance of a function call, it is evaluated.

        Returns:
            The value of the Identifier if it exists in the environment, its name if it exists in the function dictionary,
            or the result of its evaluation if it is a FunctionCall.
        """
        if self.name in ENVIRONMENT:
            return ENVIRONMENT[self.name]
        if self.name in FUNCTION_DICT:
            return self.name
        if isinstance(self.name, FunctionCall):
            return self.name.evaluate()
        return None


class UnaryOperation(Expression):
    """
    This class represents a unary operation in the maryChain language. 

    The `UnaryOperation` class inherits from the `Expression` class and encapsulates an operator and 
    an operand for operations such as unary minus and logical not.
    """

    def __init__(self, operator, operand):
        """
        Initializes a new instance of the UnaryOperation class.

        Args:
            operator: The operator of the unary operation. It could be '-' for unary minus or 'not' for logical not.
            operand: The operand on which the unary operation is to be performed.
        """
        self.operator = operator
        self.operand = operand

    def evaluate(self, **kwargs):
        """
        Evaluates the UnaryOperation. If the operator is '-', the negation of the operand is returned.
        If the operator is 'not', the logical not of the operand is returned.

        Returns:
            The result of the unary operation on the operand.

        Raises:
            ValueError: If the operator is not recognized.
        """
        if self.operator == '-':
            return -evaluate(self.operand)
        if self.operator == 'not':
            return not evaluate(self.operand)
        raise ValueError(f'Unknown operator: {self.operator}')

class While(Expression):
    """
    This class represents a while loop in the maryChain language. 

    The `While` class inherits from the `Expression` class and encapsulates a condition and a body.
    The body of the while loop is executed as long as the condition evaluates to True.
    """

    def __init__(self, condition, body):
        """
        Initializes a new instance of the While class.

        Args:
            condition: The condition of the while loop. It should be an expression that evaluates to a boolean.
            body: The body of the while loop. It's a sequence of expressions that will be executed 
                  as long as the condition is True.
        """
        self.condition = condition
        self.body = body

    def evaluate(self, **kwargs):
        """
        Evaluates the While loop. The condition is checked before each iteration. 
        If the condition is True, the body is executed, otherwise the loop is exited.

        Returns:
            The result of the last expression evaluated in the body of the loop.

        Raises:
            None
        """
        result = self.condition.evaluate()
        while result != False:
            result = self.body.evaluate()
            if self.condition.evaluate() == False:
                break
        return result

    
class IfThenElse(Expression):
    """
    This class represents a conditional "if-then-else" statement in the maryChain language.

    The `IfThenElse` class inherits from the `Expression` class and encapsulates a condition,
    an expression to evaluate if the condition is true, and another expression to evaluate if
    the condition is false.
    """

    def __init__(self, condition, true_expr, false_expr):
        """
        Initializes a new instance of the IfThenElse class.

        Args:
            condition: The condition of the if-then-else statement. It should be an expression that evaluates to a boolean.
            true_expr: The expression that will be evaluated if the condition is true.
            false_expr: The expression that will be evaluated if the condition is false.
        """
        self.condition = condition
        self.true_expr = true_expr
        self.false_expr = false_expr

    def evaluate(self, **kwargs):
        """
        Evaluates the IfThenElse statement. 

        The condition is evaluated first. If the condition is True, the true_expr is evaluated and its 
        result is returned. If the condition is False, the false_expr is evaluated and its result is returned.

        Returns:
            The result of the evaluated true_expr if the condition is true, or the result of the evaluated
            false_expr if the condition is false.

        Raises:
            None
        """
        if evaluate(self.condition):
            return evaluate(self.true_expr)
        else:
            return evaluate(self.false_expr)

        
class IfThen(Expression):
    """
    The IfThen class represents a conditional expression in a programming language. 
    It contains a condition and an expression that gets evaluated if the condition is true.
    """

    def __init__(self, condition, true_expr):
        """
        Initialize IfThen with a condition and an expression to be evaluated if the condition is true.

        :param condition: The condition of the 'if' statement.
        :param true_expr: The expression to be evaluated if the condition is true.
        """
        self.condition = condition
        self.true_expr = true_expr

    def evaluate(self, **kwargs):
        """
        Evaluate the IfThen expression. If the condition is true, evaluate and return the true expression. 
        If the condition is false, return the last evaluated result in the environment. 
        If there is no last result in the environment, return None.

        :return: Result of evaluating the true expression if the condition is true, 
                 or the last result in the environment if the condition is false.
        """
        # Evaluate the condition
        if self.condition.evaluate():
            # If the condition is true, evaluate and return the true expression
            return self.true_expr.evaluate()
        elif '%lastresult%' in ENVIRONMENT:
            # If the condition is false, return the last evaluated result in the environment
            return ENVIRONMENT['%lastresult%']
        else:
            # If there is no last result in the environment, return None
            return None  



class Lazy(Expression):
    """
    The Lazy class represents a lazy evaluation of an expression in a programming language. 
    It contains a function and its evaluated state and value.
    """

    def __init__(self, func):
        """
        Initialize Lazy with a function to be lazily evaluated.

        :param func: The function to be evaluated.
        """
        self.func = func
        self.is_evaluated = False  # Indicates if the function has been evaluated
        self.value = None  # Holds the result of the evaluation

    def evaluate(self, **kwargs):
        """
        Evaluate the Lazy expression if it hasn't been evaluated before. 
        The result is cached for future uses.

        :return: Result of evaluating the function.
        """
        # If the function hasn't been evaluated before
        if not self.is_evaluated:
            # If the function is callable
            if callable(self.func):
                # Evaluate and cache the result
                self.value = evaluate(self.func())
            else:
                # If the function is not callable, evaluate and cache the result
                self.value = evaluate(self.func)
            # Mark as evaluated
            self.is_evaluated = True

        # Return the cached value
        return self.value

    def __repr__(self):
        """
        Return a string representation of the Lazy object.
        """
        # If the function has been evaluated
        if self.is_evaluated:
            return f"<Evaluated lazy object with value: {self.value}>"
        else:
            # If the function hasn't been evaluated
            return "<Unevaluated lazy object>"


class Pipe(Expression):
    """
    The Pipe class represents a pipeline operation in a programming language.
    A pipeline operation is one where the result of one operation (left) is used as the input to another operation (right).
    """

    def __init__(self, left, right):
        """
        Initialize Pipe with two expressions: left and right.

        :param left: The left expression to be evaluated first.
        :param right: The right expression that takes the result of the left expression as an argument.
        """
        self.left = left
        self.right = right

    def evaluate(self, **kwargs):
        """
        Evaluate the Pipe expression. 
        The left expression is evaluated first and its result is fed as an argument to the right expression.

        :return: Result of evaluating the right expression with the result of the left expression.
        """
        # Evaluate the left expression and store its result in a special variable '%lastresult%'
        ENVIRONMENT['%lastresult%'] = self.left.evaluate()

        # Insert the result of the left expression as the first argument of the right expression
        self.right.args.insert(0, self.left)

        # Evaluate the right expression and return the result
        return self.right.evaluate()


class LambdaFunctionValue(Expression):
    """
    The LambdaFunctionValue class represents a lambda function in a programming language.
    A lambda function is a small anonymous function that can take any number of arguments but can have only one expression.
    """

    def __init__(self, args, body):
        """
        Initialize LambdaFunctionValue with arguments and body of the lambda function.

        :param args: The arguments that the lambda function accepts.
        :param body: The expression that forms the body of the lambda function.
        """
        self.args = args
        self.body = body

    def __call__(self, *args):
        """
        Define the behavior of the LambdaFunctionValue instance when it's 'called' like a function.
        If the number of arguments provided during the call doesn't match the lambda function's arguments,
        a TypeError is raised.

        :param args: The arguments provided during the function call.
        :return: Result of evaluating the lambda function's body with the provided arguments.
        """
        # Check if the number of arguments provided during the call matches the number of arguments the function accepts
        if len(args) != len(self.args):
            raise TypeError("wrong number of arguments")

        # Create a local environment where the arguments are bound to their values
        local_env = ENVIRONMENT.copy()
        local_env.update(zip(self.args, args))

        # Evaluate the function's body in the local environment and return the result
        return self.body.evaluate(local_env)



class LambdaFunction(Expression):
    """
    The LambdaFunction class represents a lambda function definition in a programming language. 
    This class is used to create a lambda function object (LambdaFunctionValue) when evaluated.
    """

    def __init__(self, args, body):
        """
        Initialize LambdaFunction with arguments and body of the lambda function.

        :param args: The arguments that the lambda function accepts.
        :param body: The expression that forms the body of the lambda function.
        """
        self.args = args
        self.body = body

    def evaluate(self):
        """
        Evaluate the lambda function to a LambdaFunctionValue object which can be called like a function.

        :return: A LambdaFunctionValue object that represents the lambda function.
        """
        return LambdaFunctionValue(self.args, self.body)


FUNCTION_DICT = {
    # This dictionary maps function names to FunctionDef instances that implement the function.

    # The 'out' function prints its argument and returns None. 
    # It's implemented with the 'print_func' function and curried to allow partial application.
    'out': FunctionDef('out', ['x'], curry(print_func)),

    # The 'add' function adds its two arguments. 
    # It's implemented with the 'add_func' function and curried to allow partial application.
    'add': FunctionDef('add', ['x', 'y'], curry(add_func)),

    # The 'eval' function evaluates its argument as a maryChain expression. 
    # It's implemented with the 'eval_func' function and curried to allow partial application.
    'eval': FunctionDef('eval', ['x'], curry(eval_func)),
}

# def exec(s):
#     node = None
#     return evaluate(node)

def inject_parsing(parse):
    FUNCTION_DICT['exec'] = FunctionDef('exec', ['s'], curry(lambda x: evaluate(parse(x))))
    return 

def evaluate(node):
    """
    The evaluate function is used to evaluate different types of nodes in an abstract syntax tree (AST).
    It returns the evaluated result of the node.

    :param node: A node in the AST. The node could be a string, integer, float, or an instance of Expression class.
    :return: The evaluated result of the node.
    """
    if node is None:
        return None
    
    if isinstance(node, str):
        # If the node is a string, return the string itself
        return node
    
    if isinstance(node, int):
        # If the node is an integer, return the integer itself
        return node
    
    if isinstance(node, float):
        # If the node is a float, return the float itself
        return node
    
    if isinstance(node, Evaluable):
        # If the node is an instance of Expression class, evaluate the expression and return the result
        return node.evaluate()
    
    # If the node is none of the above types, raise a ValueError
    raise ValueError(f'Unknown node type: {node}')


