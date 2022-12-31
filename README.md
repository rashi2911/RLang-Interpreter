# RLang-Interpreter

This is an interpreter in python for self-made language: RLang. The user is provided a user-friendly interface to interact with which is built using Flask.
The interface allows user to enter the input and see its output, the guidelines to use the custom language is also mentioned in the website. The web application is deployed on Docker to package the dependancies used, can be deployed in any devoce and accessed by any user.

## DEMO:

![rlang-1](https://user-images.githubusercontent.com/107244393/210129263-08cddc1b-09c7-4ee3-a795-ac453d182bc5.png)

If the given input is correct:

![rlang-2](https://user-images.githubusercontent.com/107244393/210129272-6fdb8c62-2b86-4866-89ec-95d2c1167380.png)

If the given input has some error:

![rlang-3](https://user-images.githubusercontent.com/107244393/210129287-058ad4b3-090f-46c5-9d5e-5ec54f138322.png)

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

### Flask-Application

Flask web application prompts user to enter an input using POST and GET API methods which are then taken into consideration and the user is directed to the page displaying either an error or the result, given the input.

The templates directory contains the HTML files which the user is redirected to.
### Docker Deployment
To run the code files through docker follow the given steps:
> docker build -t <image_name> <path>

> docker run -p 5000:5000 <image_name>

The interactive terminal will be prompted to user where they can give an input following the RLang Syntax and see the outputs.

