# Student: William Hellems-Moody
# Date: 9/28/2023 (Updated: 11/19/23)
# Programming Project
# Class: CS 3210

# NOTE: Updated 10-1-23: Added the position of the left parenthesis to the stack, along with updating the error class to include the position of the error for the syntax error, generated.

# NOTE: Updated 11-19-23: Added support for the logical operators such as AND, OR, NOT, etc. for Programming Project 04. Also added support for the logical operators such as >=, <=, >, <, and division by zero error check.

WHM_INT = "WHM_INT"
WHM_FLOAT = "WHM_FLOAT"
WHM_PLUS = "WHM_PLUS"
WHM_MINUS = "WHM_MINUS"
WHM_MUL = "WHM_MUL"
WHM_DIV = "WHM_DIV"
WHM_LPAREN = "WHM_LPAREN"
WHM_RPAREN = "WHM_RPAREN"

DIGITS = "0123456789"

# PROGRAMMING PROJECT 04 for the logical operators such as AND, OR, NOT, etc.
WHM_AND = "WHM_AND"
WHM_OR = "WHM_OR"
WHM_NOT = "WHM_NOT"
WHM_EQUALS = "WHM_EQUALS"

# PROGRAMMING PROJECT 04 for the logical operators such as >=, <=, >, <
WHM_GTE = "WHM_GTE"  # >= Greater than or equal to
WHM_LTE = "WHM_LTE"  # <= Less than or equal to
WHM_GT = "WHM_GT"    # >
WHM_LT = "WHM_LT"    # <
WHM_NE = "WHM_NE"    # != Not equal to
# PROGRAMMING PROJECT 04 for the logical operators



class Error:
    def __init__(self, pos_start, pos_end, error, details):
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.error = error
        self.details = details

    def as_string(self):
        result = f"{self.error}: {self.details}\n"
        result += f"File {self.pos_start.fn}, line {self.pos_start.line + 1}\nColumn {self.pos_start.column}\n"
        # Produce the output
        return result


class IllegalCharError(Error):
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, "Illegal Character", details)

# ****************************
# ADDED CODE FOR PROGRAM 03
# ****************************
# ZERO DIVISION ERROR CHECK
# ****************************
class DivisionByZeroError(Error):
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, "Division Error", details)
        
    def as_string(self):
        result = f"{self.error} \t\t{self.details}"
        # Produce the output without the file, line, and column information
        return result

# ****************************

# Updated 10-2-23: Created a new error class for the syntax error, and added the position of the error.
class InvalidSyntaxError(Error):
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, "Invalid Syntax", details)

class Position:
    def __init__(self, index, line, column, fn, text):
        self.index = index
        self.line = line
        self.column = column
        self.fn = fn
        self.text = text

    def advance(self, current_char=None):
        self.index += 1
        self.column += 1

        if current_char == "\n":
            self.line += 1
            self.column = 0  # Reset column position when a new line is encountered.
        return self

    # NOTE: This is a copy function that returns a new position object.
    def copy(self):
        return Position(self.index, self.line, self.column, self.fn, self.text)

class Token:
    def __init__(self, type, token_value=None, pos_start=None, pos_end=None):
        self.type = type
        self.token_value = token_value

        if pos_start and pos_end:
            self.pos_start = pos_start
            self.pos_end = pos_end
        elif pos_start:
            self.pos_start = pos_start
            self.pos_end = Position(
                pos_start.index + 1,
                pos_start.line,
                pos_start.column + 1,
                pos_start.fn,
                pos_start.text,
            )

        if pos_end:
            self.pos_end = pos_end

    def __repr__(self):
        if self.token_value:
            return f"{self.type}:{self.token_value}"
        return f"{self.type}"


class Lexer:
    # Implement the following syntax error checks:
    # 1. Check for missing integer or float (e.g. 1 + 2 +).
    # 3. Check for missing operator (e.g. +, -, *, /).
    # 4. Check for missing operand (e.g. 1 + 2 +).
    # 5. Check for missing left parenthesis (e.g. 1 + 2) * 3).
    # 6. Check for missing right parenthesis (e.g. (1 + 2 * 3).

    def __init__(self, fn, text):
        self.fn = fn
        self.text = text
        self.pos = Position(-1, 0, -1, fn, text)
        self.current_char = None
        self.advance()
        self.unmatched_parentheses_stack = []

    def advance(self):
        self.pos.advance(self.current_char)
        self.current_char = (
            self.text[self.pos.index] if self.pos.index < len(self.text) else None
        )

    def make_tokens(self):
        tokens = []
        while self.current_char is not None:
            if self.current_char in " \t":
                self.advance()
                
            # ****************************
            # ADDED CODE FOR PROGRAM 03
            # ****************************
            # URNARY OPERATOR
            # ****************************
            elif self.current_char in '+-':
                # Handle unary operators
                tokens.append(self.make_unary_operator())
            # ****************************
            elif self.current_char in "\n":
                self.advance()
            elif self.current_char in DIGITS:
                tokens.append(self.make_number())

            elif self.current_char in ("+", "-", "*", "/"):
                # ----Expression Cannot Start with an Operator----[✅]
                if (
                    self.pos.index == 0
                    and self.current_char in ("+", "-", "*", "/", ")")
                    and self.text[self.pos.index] not in DIGITS
                ):
                    return [], InvalidSyntaxError(
                        self.pos,
                        self.pos,
                        "The expression cannot start with an operator"
                        + f" {self.current_char}",
                    )
                # ----Expression Cannot End with an Operator----[✅]
                elif (
                    self.pos.index == len(self.text) - 1
                    and self.current_char in ("+", "-", "*", "/", "(")
                    and self.text[self.pos.index] not in DIGITS
                ):
                    return [], InvalidSyntaxError(
                        self.pos,
                        self.pos,
                        "The expression cannot end with an operator"
                        + f" {self.current_char}",
                    )

                # ----Expression Cannot Start with an Operator----[✅]
                elif self.text[self.pos.index - 1] in "+-*/":
                    return [], InvalidSyntaxError(
                        self.pos, self.pos, "Expected integer or float, or parenthesis"
                    )
                else:
                    tokens.append(
                        Token(
                            WHM_PLUS
                            if self.current_char == "+"
                            else WHM_MINUS
                            if self.current_char == "-"
                            else WHM_MUL
                            if self.current_char == "*"
                            else WHM_DIV,
                            pos_start=self.pos,
                        )
                    )
                    self.advance()

            elif self.current_char == "+":
                tokens.append(Token(WHM_PLUS, pos_start=self.pos))
                self.advance()
            # Programming Project 04
            elif self.current_char.isalpha():
                word = self.make_word()
                if word == 'AND':
                    tokens.append(Token(WHM_AND, pos_start=self.pos))
                elif word == 'OR':
                    tokens.append(Token(WHM_OR, pos_start=self.pos))
                elif word == 'NOT':
                    tokens.append(Token(WHM_NOT, pos_start=self.pos))
                else:
                    # Handle undefined words
                    return [], IllegalCharError(self.pos, self.pos, f"'{word}'")
                
                # This represents the relational operators such as >=, <=, >, <
            elif self.current_char == "!":
                pos_start = self.pos.copy()
                self.advance()
                if self.current_char == "=":
                    tokens.append(Token(WHM_NE, pos_start=pos_start))
                    self.advance()
                else:
                    tokens.append(Token(WHM_NOT, pos_start=pos_start))

            elif self.current_char == "!":
                tokens.append(Token(WHM_NOT, pos_start=self.pos))
                self.advance()
            elif self.current_char == "=":
                self.advance()
                if self.current_char == "=":
                    tokens.append(Token(WHM_EQUALS, pos_start=self.pos))
                    self.advance()
            # Additional Conditionals for Programming Project 04
            elif self.current_char == '>':
                pos_start = self.pos.copy()
                self.advance()
                if self.current_char == '=':
                    tokens.append(Token(WHM_GTE, pos_start=pos_start))
                    self.advance()
                else:
                    tokens.append(Token(WHM_GT, pos_start=pos_start))
            elif self.current_char == '<':
                pos_start = self.pos.copy()
                self.advance()
                if self.current_char == '=':
                    tokens.append(Token(WHM_LTE, pos_start=pos_start))
                    self.advance()
                else:
                    tokens.append(Token(WHM_LT, pos_start=pos_start))
                # Additional Conditionals for Programming Project 04
            # Programming Project 04
            elif self.current_char == "-":
                tokens.append(Token(WHM_MINUS, pos_start=self.pos))
                self.advance()
            elif self.current_char == "*":
                tokens.append(Token(WHM_MUL, pos_start=self.pos))
                self.advance()
            elif self.current_char == "/":
                tokens.append(Token(WHM_DIV, pos_start=self.pos))
                self.advance()
            elif self.current_char == "(":
                # Check for missing operator e.g. 1(2+3), of the left value is a number or right parenthesis, then it is an error. ✅
                if tokens and tokens[-1].type in (
                    WHM_INT,
                    WHM_FLOAT,
                    WHM_RPAREN,
                ):
                    return [], InvalidSyntaxError(
                        self.pos,
                        self.pos,
                        "Expected '+', '-', '*', or '/'",
                    )
                self.unmatched_parentheses_stack.append(self.pos)
                tokens.append(Token(WHM_LPAREN, pos_start=self.pos))
                self.advance()
            elif self.current_char == ")":
                if not self.unmatched_parentheses_stack:
                    return [], InvalidSyntaxError(
                        self.pos,
                        self.pos,
                        "Unexpected ')'",
                    )
                self.unmatched_parentheses_stack.pop()
                tokens.append(Token(WHM_RPAREN, pos_start=self.pos))
                self.advance()
            else:
                char = self.current_char
                # self.advance()
                return [], IllegalCharError(self.pos, self.current_char, "'" + char + "'")


        # Check for missing left parenthesis e.g. 1+2)*3) ✅
        if (
            tokens[0].type not in (WHM_INT, WHM_FLOAT, WHM_LPAREN)
            and tokens[1].type == WHM_RPAREN
        ):
            return [], InvalidSyntaxError(
                tokens[0].pos_end,
                tokens[1].pos_start,
                "Expected operator or left parenthesis",
            )

        # Check for missing right parenthesis e.g. ((1+2)*3) ✅
        if self.unmatched_parentheses_stack:
            return [], InvalidSyntaxError(
                self.unmatched_parentheses_stack[-1],
                self.unmatched_parentheses_stack[-1],
                "Expected ')'",
            )

        return tokens, None
    
    def make_word(self):
        word = ''
        while self.current_char is not None and self.current_char.isalpha():
            word += self.current_char
            self.advance()
        # This ensures that the word is not a keyword by converting it to uppercase.
        return word.upper()
    
    # ****************************
    # ADDED CODE FOR PROGRAM 03
    # ****************************
    # URNARY OPERATOR
    # ****************************
    def make_unary_operator(self):
        unary_op = self.current_char
        pos_start = self.pos.copy()
        self.advance()
        return Token(WHM_PLUS if unary_op == '+' else WHM_MINUS, pos_start=pos_start)
    # ****************************

    def make_number(self):
        num_str = ""
        dot_count = 0

        while self.current_char != None and self.current_char in DIGITS + ".":
            if self.current_char == ".":
                if dot_count == 1:
                    break
                dot_count += 1
                num_str += "."
            else:
                num_str += self.current_char
            self.advance()
        if dot_count == 0:
            return Token(WHM_INT, int(num_str), pos_start=self.pos)
        else:
            return Token(WHM_FLOAT, float(num_str), pos_start=self.pos)


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.token_index = -1
        self.advance()

    def advance(self):
        self.token_index += 1
        if self.token_index < len(self.tokens):
            self.current_token = self.tokens[self.token_index]
        return self.current_token

    def factor(self):
        token = self.current_token
        # ****************************
        # ADDED CODE FOR PROGRAM 03
        # ****************************
        # URNARY OPERATOR
        # ****************************
        if token.type in (WHM_PLUS, WHM_MINUS):
            # Handle unary operations
            self.advance()
            factor = self.factor()
            return UnaryOpNode(token, factor)
        # URNARY OPERATOR
        # ****************************
        elif token.type in (WHM_INT, WHM_FLOAT):
            self.advance()
            return NumberNode(token)

        # UPDATED 10-2-23: Moved paren checks to Make_Tokens
        elif token.type == WHM_LPAREN:
            self.advance()
            result = self.expr()
            if self.current_token.type == WHM_RPAREN:
                self.advance()
                return result
            
            

    # Passing the func for readability and simplicity.
    def term(self):
        return self.binary_operation(self.factor, (WHM_MUL, WHM_DIV))

    # # Passing the func for readability and simplicity.
    # def expr(self):
    #     return self.binary_operation(self.term, (WHM_PLUS, WHM_MINUS))

    # PROGRAMMING PROJECT 04
    def expr(self):
        return self.binary_operation(self.comp_expr, (WHM_AND, WHM_OR))

    # Compares the current token type to the passed token types.
    def comp_expr(self):
        if self.current_token.type == WHM_NOT:
            op_token = self.current_token
            self.advance()
            node = self.comp_expr()
            return UnaryOpNode(op_token, node)
        
        # Check for missing operator e.g. 1(2+3), of the left value is a number or right parenthesis, then it is an error. ✅
        node = self.binary_operation(self.arith_expr, (WHM_EQUALS, WHM_NE, WHM_GTE, WHM_LTE, WHM_GT, WHM_LT))

        return node


    # Passing the func for readability and simplicity for arithmetical expressions.
    def arith_expr(self):
        return self.binary_operation(self.term, (WHM_PLUS, WHM_MINUS))

    # PROGRAMMING PROJECT 04

    def binary_operation(self, func, operations):
        left = func()
        while self.current_token.type in operations:
            operation_token = self.current_token
            self.advance()
            right = func()
            left = BinOpNode(left, operation_token, right)
        return left

    def parse(self):
        result = self.expr()
        return result


class NumberNode:
    def __init__(self, token):
        self.token = token

    def __repr__(self):
        return f"{self.token}"


class BinOpNode:
    def __init__(self, left_node, op_token, right_node):
        self.left_node = left_node
        self.op_token = op_token
        self.right_node = right_node

    def __repr__(self):
        return f"({self.left_node}, {self.op_token}, {self.right_node})"

# ****************************
# ADDED CODE FOR PROGRAM 03
# ****************************
# ********************
# UNARY OPERATION NODE
# ********************
class UnaryOpNode:
    # Handle the unary operations such as NOT, MINUS, etc.
    def __init__(self, op_token, node):
        self.op_token = op_token
        self.node = node

    def __repr__(self):
        return f"({self.op_token}, {self.node})"

# ********************


# ****************************
# ADDED CODE FOR PROGRAM 03
# ****************************
# ********************
# EVALUATOR CLASS - EVALUATES THE AST
# ********************
class Evaluator:
    # Should visit the nodes in the AST and return the result of the expression based on the node type.
    def visit(self, node):
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name)
        return method(node)
    
    # PROGRAMMING PROJECT 04
    def visit(self, node):
        if node is None:
            return self.visit_NoneType(node)

        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name)
        return method(node)

    def visit_NoneType(self, node):
        # Handle the None node case, possibly return an error message or None
        return "Syntax Error: Invalid expression"
    # PROGRAMMING PROJECT 04

    def visit_NumberNode(self, node):
        return node.token.token_value

    def visit_BinOpNode(self, node):
        left = self.visit(node.left_node)
        right = self.visit(node.right_node)

        # Check if left or right is an error message (string)
        if isinstance(left, str) or isinstance(right, str):
            return "Error in operation"  # Replace with the specific error message

        # Check for division by zero and logic to handle the operations such as AND, OR, NOT, etc.
        if node.op_token.type == WHM_AND:
            return bool(left) and bool(right)
        elif node.op_token.type == WHM_OR:
            return bool(left) or bool(right)
        elif node.op_token.type == WHM_EQUALS:
            return left == right
        elif node.op_token.type == WHM_GTE:
            return left >= right
        elif node.op_token.type == WHM_LTE:
            return left <= right
        elif node.op_token.type == WHM_GT:
            return left > right
        elif node.op_token.type == WHM_LT:
            return left < right
        elif node.op_token.type == WHM_NE:
            return left != right
        elif node.op_token.type == WHM_PLUS:
            return left + right
        elif node.op_token.type == WHM_MINUS:
            return left - right
        elif node.op_token.type == WHM_MUL:
            return left * right
        elif node.op_token.type == WHM_DIV:
            if right == 0:
                return DivisionByZeroError(node.op_token.pos_start, node.op_token.pos_end, "Cannot divide by zero").as_string()
            return left / right

    def visit_UnaryOpNode(self, node):
        number = self.visit(node.node)
        if node.op_token.type == WHM_NOT:
            # Convert the result to a boolean and then apply the NOT operation
            return not bool(number)
        elif node.op_token.type == WHM_MINUS:
            return -number
        elif node.op_token.type == WHM_PLUS:
            return number
# ********************


# PROGRAMMING PROJECT 04 (Edited to match the output of the module requirements)
def run(fn, text):
    lexer = Lexer(fn, text)
    tokens, error = lexer.make_tokens()

    if error:
        # Structure the error message as specified in the instructions
        if isinstance(error, IllegalCharError):
            return f"{text}  \t\t\tUnexpected token {error.details} at position {error.pos_start.index + 1}", None
        elif isinstance(error, DivisionByZeroError):
            return f"{text}  \t\t\t{error.details}", None
        elif isinstance(error, InvalidSyntaxError):
            return f"{text}  \t\t\tInvalid Syntax at position {error.pos_start.index + 1}", None
        else:
            return error.as_string(), None
    else:
        # Generate the AST
        parser = Parser(tokens)
        ast = parser.parse()

        # Evaluate the AST if there are no errors
        if ast is None or isinstance(ast, Error):
            error = ast or Error()
            return error.as_string(), None

        evaluator = Evaluator()
        result = evaluator.visit(ast)

        if isinstance(result, Error):
            return result.as_string(), None

        # Print the structure of the result as specified in the instructions if there are no errors.
        return f"{text} = {result}", None

# PROGRAMMING PROJECT 04 (Edited to match the output of the module requirements)