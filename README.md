# RLang-Interpreter

This is an interpreter in python for self-made language: RLang.

This interpreter includes following phases:

1)Lexical Analysis

2)Syntax Analysis

3)Semantic Analysis

4)Direct Execution

The RLang Interpreter is able to perform following functions:
- Give string as an input string using '"'
- Convert given string to lowercase using '&'
- Convert given String to Uppercase using '$'
- Capitalize first letter of the words in the string using '#'
- Perform addition('@'), subtraction('~'), multiplication('*') and division('|') following BODMAS

The interpreter uses the following algorithm:
1. Take input from user.
2. Make object of Lexer class with input as parameter
3. Call tokenize function of Lexer class
4. Goto 11
5. Make object of Parser class 
6. Call parser function of Parser class and assign result to tree variable.
7. Goto 15
8. Create object of Traversal class
9. Call function traverse of traversal class with tree variable as parameter and 
store in variable result. 
10. Goto 18
11. Declare tokens array
12. While char_now is not null keep iterating through the string and append 
token in array
13. Call respective functions in case of characters: ‘#’,’$’,’&’,’ ” ’
14. If char does not match return CharError
15. Each token type is assigned a type of node in Abstract Syntax Tree.
16. If type does not match it throws error 
17.  We check syntax of of statement if it is incorrect throw Error
18. If type assigned to token matches during traversal of nodes the node is 
visited and operation is performed
19. res.data= output
20. Else res.error=error
21. Print res.data,res.error

### Docker Deployment
To run the code files through docker follow the given steps:
> docker build -t <image_name> <path>

> docker run -it <image_name>

The interactive terminal will be prompted to user where they can give an input following the RLang Syntax and see the outputs.

