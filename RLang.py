NUMS = '0123456789'

# ERRORS

class Error:
	def __init__(self, loc_start, loc_end, error_name, details):
		self.loc_start = loc_start
		self.loc_end = loc_end
		self.error_name = error_name
		self.details = details

	def convert_to_string(self):
		result = f'{self.error_name}: {self.details}\n'
		return result


class CharError(Error):
	def __init__(self, loc_start, loc_end, details):
		super().__init__(loc_start, loc_end, 'Entered wrong Character', details)

class InvalidSyntax(Error):
	def __init__(self, loc_start, loc_end, details=''):
		super().__init__(loc_start, loc_end, 'Syntax is not valid', details)

# Location


class Location:
	def __init__(self, idx, ln, col):
		self.idx = idx
		self.ln = ln
		self.col = col

	def next(self, char_now=None):
		self.idx += 1
		self.col += 1

		return self

	def temp(self):
		return Location(self.idx, self.ln, self.col)

# TOKENS
INT = 'INT'
FLOAT = 'FLOAT'
STRING = 'STRING'
ADD = 'PLUS'
SUB = 'MINUS'
MLT = 'MUL'
DIV = 'DIV'
LEFT_PAREN = 'LEFT_PAREN'
RIGHT_PAREN = 'RIGHT_PAREN'
END = 'END'

#Tokenization of input
class Token:
	#type of token and its value 
	def __init__(self, type, data=None, loc_start=None, loc_end=None):
		self.type = type
		self.data = data
		 #stores copy of start location and end location then increment end location by 1
		if loc_start:
			self.loc_start = loc_start.temp()
			self.loc_end = loc_start.temp()
			self.loc_end.next()
		#stores copy of end location 
		if loc_end:
			self.loc_end = loc_end.temp()
#how output will be printed -format
	def __repr__(self):
		if self.data:
			return f'{self.type}:{self.data}'
		return f'{self.type}'

# LEXICAL ANALYSIS PHASE

class Lexer:
	#initialize the parameters 
	def __init__(self, str):
		self.str = str
		self.loc = Location(-1, 0, -1)
		self.char_now = None
		self.next()
	#move to next position while 
	def next(self):
		self.loc.next(self.char_now)
		self.char_now = self.str[self.loc.idx] if self.loc.idx < len(
			self.str) else None

	def tokenize(self):
		#take array to keep track of tokens
		tokens = []
		#iterate through input text and append tokens
		while self.char_now != None:
			if self.char_now in ' \t':
				self.next()
			elif self.char_now in NUMS:
				tokens.append(self.convert_to_number())
			elif self.char_now == '$':
				tokens.append(self.caps_string())
			elif self.char_now == '#':
				tokens.append(self.capitalize_first_letter())
			elif self.char_now == '&':
				tokens.append(self.lowercase_string())
			elif self.char_now == '"':
				tokens.append(self.convert_to_string())
			elif self.char_now == '@':
				tokens.append(Token(ADD, loc_start=self.loc))
				self.next()
			elif self.char_now == '~':
				tokens.append(Token(SUB, loc_start=self.loc))
				self.next()
			elif self.char_now == '*':
				tokens.append(Token(MLT, loc_start=self.loc))
				self.next()
			elif self.char_now == '|':
				tokens.append(Token(DIV, loc_start=self.loc))
				self.next()
			elif self.char_now == '(':
				tokens.append(Token(LEFT_PAREN, loc_start=self.loc))
				self.next()
			elif self.char_now == ')':
				tokens.append(Token(RIGHT_PAREN, loc_start=self.loc))
				self.next()

			else:
				loc_start = self.loc.temp()
				char = self.char_now
				self.next()
				return [], CharError(loc_start, self.loc, "'" + char + "'")

		tokens.append(Token(END, loc_start=self.loc))
		return tokens, None
#append int and float
	def convert_to_number(self):
		num_str = ''
		dot_count = 0
		loc_start = self.loc.temp()

		while self.char_now != None and self.char_now in NUMS + '.':
			if self.char_now == '.':
				if dot_count == 1:
					break
				dot_count += 1
			num_str += self.char_now
			self.next()

		if dot_count == 0:
			return Token(INT, int(num_str), loc_start, self.loc)
		else:
			return Token(FLOAT, float(num_str), loc_start, self.loc)
#return entered string as only the first letter capital and append as STRING token
	def capitalize_first_letter(self):
		string1 = ""
		loc_start = self.loc.temp()
		self.next()

		while self.char_now != None and (self.char_now != '#'):
			string1 += self.char_now
			self.next()

		self.next()
		return Token(STRING, string1.capitalize(), loc_start, self.loc)
#return entered string as lowercase string and append as STRING token
	def lowercase_string(self):
		string1 = ""
		loc_start = self.loc.temp()
		self.next()

		while self.char_now != None and (self.char_now != '&'):
			string1 += self.char_now
			self.next()

		self.next()
		return Token(STRING, string1.lower(), loc_start, self.loc)
#return entered string as STRING token	
	def convert_to_string(self):
		string1 = ""
		loc_start = self.loc.temp()
		self.next()

		while self.char_now != None and (self.char_now != '"'):
			string1 += self.char_now
			self.next()
		self.next()
		return Token(STRING, string1, loc_start, self.loc)
#return entered string CAPITAL and append as STRING token
	def caps_string(self):
		string = ""
		loc_start = self.loc.temp()
		self.next()

		while self.char_now != None and (self.char_now != '$'):
			string += self.char_now
			self.next()

		self.next()
		return Token(STRING, string.upper(), loc_start, self.loc)

# AST Node types

class NumberNode:
	def __init__(self, tok):
		self.tok = tok

		self.loc_start = self.tok.loc_start
		self.loc_end = self.tok.loc_end

	def __repr__(self):
		return f'{self.tok}'


class StringNode:
	def __init__(self, tok):
		self.tok = tok

		self.loc_start = self.tok.loc_start
		self.loc_end = self.tok.loc_end

	def __repr__(self):
		return f'{self.tok}'


class BinOpNode:
	def __init__(self, left_node, tok_type_op, right_node):
		self.left_node = left_node
		self.tok_type_op = tok_type_op
		self.right_node = right_node

		self.loc_start = self.left_node.loc_start
		self.loc_end = self.right_node.loc_end

	def __repr__(self):
		return f'({self.left_node}, {self.tok_type_op}, {self.right_node})'


class UnaryOpNode:
	def __init__(self, tok_type_op, node):
		self.tok_type_op = tok_type_op
		self.node = node

		self.loc_start = self.tok_type_op.loc_start
		self.loc_end = node.loc_end

	def __repr__(self):
		return f'({self.tok_type_op}, {self.node})'

# Initializing parser result variables for error control
class ParserInit:
	def __init__(self):
		self.error = None
		self.node = None
		self.prev_count = 0
		self.next_count = 0

	def register_forward(self):
		self.prev_count = 1
		self.next_count += 1

	def define(self, res):
		if isinstance(res, ParserInit):
			if res.error: self.error = res.error
			return res.node

		return res

	def succeed(self, node):
		self.node = node
		return self

	def fail(self, error):
		if not self.error or self.prev_count == 0:
			self.error = error
		return self

# Operator Precedence Parser

class Parser:
	def __init__(self, tokens):
		self.tokens = tokens
		self.tok_idx = -1
		self.next()

	def next(self):
		self.tok_idx += 1
		if self.tok_idx < len(self.tokens):
			self.current_tok = self.tokens[self.tok_idx]
		return self.current_tok

	def parse(self):
		res = self.expr()
		if not res.error and self.current_tok.type != END:
			return res.fail(InvalidSyntax(
				self.current_tok.loc_start, self.current_tok.loc_end,
				"Expected '+', '-', '*' or '/'"
			))
		return res
#sets priority for evaluation and type checking
	def factor(self):
		res = ParserInit()
		tok = self.current_tok

		if tok.type in (ADD, SUB):
			res.register_forward()
			self.next()
			factor = res.define(self.factor())
			if res.error: return res
			return res.succeed(UnaryOpNode(tok, factor))
		
		elif tok.type in (INT, FLOAT):
			res.register_forward()
			self.next()
			return res.succeed(NumberNode(tok))
		
		elif tok.type == STRING:
			res.register_forward()
			self.next()
			return res.succeed(StringNode(tok))

		elif tok.type == LEFT_PAREN:
			res.register_forward()
			self.next()
			expr = res.define(self.expr())
			if res.error: return res
			if self.current_tok.type == RIGHT_PAREN:
				res.define(self.next())
				return res.succeed(expr)
			else:
				return res.fail(InvalidSyntax(
					self.current_tok.loc_start, self.current_tok.loc_end,
					"Expected ')'"
				))

		return res.fail(InvalidSyntax(
			tok.loc_start, tok.loc_end,
			"Expected int or float"
		))

	def term(self):
		return self.binary_op(self.factor, (MLT, DIV))

	def expr(self):
		return self.binary_op(self.term, (ADD, SUB))

	def binary_op(self, func, ops):
		res = ParserInit()
		left = res.define(func())
		if res.error: return res

		while self.current_tok.type in ops:
			tok_type_op = self.current_tok
			res.define(self.next())
			right = res.define(func())
			if res.error: return res
			left = BinOpNode(left, tok_type_op, right)

		return res.succeed(left)

# Gives data and error as runtime result
class Output:
	def __init__(self):
		self.data = None
		self.error = None

	def define(self, res):
		self.error = res.error
		return res.data

	def succeed(self, data):
		self.data = data
		return self

	def fail(self, error):
		self.error = error
		return self

class Data:
	def __init__(self):
		self.set_loc()
		self.set_text()

	def set_loc(self, loc_start=None, loc_end=None):
		self.loc_start = loc_start
		self.loc_end = loc_end
		return self

	def set_text(self, context=None):
		self.context = context
		return self

class Number(Data):
	def __init__(self, data):
		super().__init__()
		self.data = data
		self.error=None
	def fail(self, error):
		self.error = error
		return self	


	def addition(self, other):
		if isinstance(other, Number):
			return Number(self.data + other.data), None
		else:
			return None, "Operation is not valid"

	def subtraction(self, other):
		if isinstance(other, Number):
			return Number(self.data - other.data), None
		else:
			return None, "Operation is not valid"

	def multiply(self, other):
		if isinstance(other, Number):
			return Number(self.data * other.data), None
		else:
			return None, "Operation is not valid"

	def division(self, other):
		if isinstance(other, Number):
			if other.data == 0:
				return None, Error(
					other.loc_start, other.loc_end,
					'Runtime Error',
					'Division by zero'
				)

			return Number(self.data / other.data), None
		else:
			return None, "Operation is not valid"

	def temp(self):
		temp = Number(self.data)
		temp.set_loc(self.loc_start, self.loc_end)
		return temp

	def __repr__(self):
		return str(self.data)


class String(Data):
	def __init__(self, data):
		super().__init__()
		self.data = data
		self.error=None

	def is_true(self):
		return len(self.data) > 0

	def temp(self):
		temp = String(self.data)
		temp.set_loc(self.loc_start, self.loc_end)
		return temp

	def __repr__(self):
		return f'"{self.data}"'

# TRAVERSAL OF NODES

class Traversal:
	def traverse(self, node):
		method_name = f'traverse{type(node).__name__}'
		method = getattr(self, method_name)
		return method(node)

	def traverseNumberNode(self, node):
		return Output().succeed(
			Number(node.tok.data).set_loc(node.loc_start, node.loc_end)
		)

	def traverseStringNode(self, node):
		return Output().succeed(
			String(node.tok.data).set_loc(node.loc_start, node.loc_end)
		)

	def traverseBinOpNode(self, node):
		res = Output()
		left = res.define(self.traverse(node.left_node))
		if res.error:
			return res
		right = res.define(self.traverse(node.right_node))
		if res.error:
			return res

		if node.tok_type_op.type == ADD:
			result, error = left.addition(right)
		elif node.tok_type_op.type == SUB:
			result, error = left.subtraction(right)
		elif node.tok_type_op.type == MLT:
			result, error = left.multiply(right)
		elif node.tok_type_op.type == DIV:
			result, error = left.division(right)

		if error:
			return res.fail(error) 
		else:
			return res.succeed(result.set_loc(node.loc_start, node.loc_end))

	def traverseUnaryOpNode(self, node):
		res = Output()
		number = res.define(self.traverse(node.node))
		if res.error:
			return res

		error = None

		if node.tok_type_op.type == SUB:
			number, error = number.multiply(Number(-1))

		if error:
			return res.fail(error)
		else:
			return res.succeed(number.set_loc(node.loc_start, node.loc_end))

# RESULT
def result(str):
	# lexical analysis phase
	lexer = Lexer(str)
	tokens, error = lexer.tokenize()
	if error:
		return None, error
	#checks syntax
	parser = Parser(tokens)
	tree = parser.parse()
	if tree.error:
		return None, tree.error
	#type checking : semantic analysis phase
	# Traversing tree and then traverseing every node to get the intermediate code representation
	traverse1 = Traversal()
	result = traverse1.traverse(tree.node)

	return result.data, result.error
