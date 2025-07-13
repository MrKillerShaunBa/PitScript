# PitScript

An esolang where you use F1 lingo to write code. I have made this for the Twist-YSWS event in Hack Club.

This coding language supports variables, operators, user-defined functions and has error handling. It only supports integer data type since speed is a number 🏎️🏎️🏎️. It also has one list whose maximum length is 20 since there are 20 drivers. Each element of the list can be referenced by pointers `p1` to `p20`. The language is case insensitive.

Some rules that must be followed while coding in this language-
- You must always start the code with 'Its lights out and away we go'.
- The code must end with 'retire the car'
- Each command goes in a separate line
- Keep spaces between reserved words, variables and operators.
- List need to be defined between lines containing grid start and grid end.

## Check it out-

https://pitscript.onrender.com

## Installation

```
git clone https://github.com/MrKillerShaunBa/PitScript.git
python pitscript.py <path_to_your_file>.f1
```

The usage is as follows- 
 Syntax | Description | Usage
|:---:|:-----------:|:--------------------:|
| `Radio` | Print command, will print the value if a variable is given otherwise it prints everything after it as it is | `radio <variable or text>` |
| `Grid Start` | Used to start the grid definition | `Grid Start` followed by `p<number> <Value>` |
| `Grid End` | End the grid definition | `Grid End` |
| `Strat` | Define and assing value to a variable | `Strat <var_name> <value>` |
| `Pit` | Used to create user-defined functions | `Pit <func_name> [args]` |
| `Crash` | Used to indicate end of function definition | `Crash` |
| `Box Box` | Call the user-defined functions | `Box Box <func_name> [passed_ards]` |
| `DRS` | Used to enter the try part of error handling | `DRS`|
| `Yellow flag` | Used to define the except part of error handling just after `DRS` |  `Yellow Flag` |
| `Green Flag` | Used to end the try-except block and comes after `Yellow Flag` | `Green Flag` |

## Example programs

### Hello World
```js
ITS LIGHTS OUT AND AWAY WE GO
RADIO Hello World
RETIRE THE CAR
```

### Arithmetic
```js
ITS LIGHTS OUT AND AWAY WE GO
STRAT speed 100
STRAT boost speed * 2
STRAT weight 500
STRAT reduce weight / 5
RADIO hello world
RADIO speed
RADIO boost
RADIO weight
RADIO reduce
RETIRE THE CAR
```

### List
```js
ITS LIGHTS OUT AND AWAY WE GO
strat lewis 44
grid start
p1 100
grid end
radio p1
strat boost p1 * lewis
radio boost
retire the car
```

### User-Defined Function
```js
ITS LIGHTS OUT AND AWAY WE GO
STRAT speed 100
PIT add2 var1
STRAT var1 var1 + 2
CRASH
BOX BOX add2 speed
RADIO speed
RETIRE THE CAR
```

### Error handling
```js
ITS LIGHTS OUT AND AWAY WE GO
DRS
STRAT max 100
STRAT boost speed / 0
RADIO speed
RADIO boost
YELLOW FLAG
RADIO something is wrong I can feel it
GREEN FLAG
RETIRE THE CAR
```
