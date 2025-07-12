import re

variables = {}
grid = [0]*20
functions = {}

def isReserved(s):
    if s in ["grid","radio","strat","pit","box","call","its lights out and away we go", "retire the car", "pit","green","box"]:
        return True
    else:
        return False
def parse(code):
    return code.lower().strip().splitlines()

def evaluate_exp(variables,exp):
    parts = exp.strip().split()
    if len(parts) == 1:
        if parts[0].isdigit() == True:
            return int(parts[0])
        else:
            return variables.get(parts[0], 0)
    
    if len(parts) == 3:
        a, op, b= parts
        if a.isdigit() == True:
            a = int(a)
        else:
            a = variables.get(a, 0)
        if b.isdigit() == True:
            b = int(b)
        else:
            b = variables.get(b, 0)

        if op == "+":
            return a + b
        elif op == '-':
            return a - b
        elif op == '*':
            return a * b
        elif op == '/':
            if b == 0:
                raise ZeroDivisionError("Division by zero is not allowed")
            return a // b
        raise SyntaxError(f"Unknown operator: %s"% op)
def start(code, parent_vars = None, funcs = None):
    tokens = parse(code)
    value = 0
    i=1
    if tokens[0] != "its lights out and away we go":
        raise SyntaxError("Race hasnt started bro, use - 'its lights out and away we go'")
    
    if tokens[-1] != "retire the car":
        raise SyntaxError(f"Were you even racing? Use - 'retire the car' to end")
    while i < len(tokens) -1:      
        if tokens[i].startswith("strat "):
            parts = tokens[i].split(maxsplit=2)
            if len(parts) != 3:
                raise SyntaxError("Invalid strategy command")
            _, var_name, var_value = parts
            if isReserved(var_name) == True:
                raise SyntaxError("Invalid variable name %s"% var_name)
            variables[var_name] = evaluate_exp(variables,var_value)

        elif tokens[i].startswith("pit "):
            parts = tokens[i].split()
            fname = parts[1]
            args = parts[2:]
            body = []
            i+=1
            while i < len(tokens) and tokens[i] != "crash":
                body.append(tokens[i])
                i += 1
            if i >= len(tokens) or tokens[i] != "crash":
                raise SyntaxError("Add crash to end pit stop")
            functions[fname] = (args,body)
        
        elif tokens[i].startswith("box box "):
            parts = tokens[i].split()
            fname = parts[2]
            args_passed = parts[3:]

            if fname not in functions:
                raise NameError("Function %s not defined"% fname)
            f_args, f_body = functions[fname]
            if len(f_args) != len(args_passed):
                raise ValueError(f"Function %s expects {len(f_args)} arguments, but {len(args_passed)}"% fname)
            
            local_vars = variables.copy()
            for name, val in zip(f_args, args_passed):
                local_vars[name] = int(val) if val.isdigit() else variables.get(val, 0)
                for j in range(len(f_body)):
                    f_body[j] = f_body[j].replace(name, str(val))
            curr_i = i
            start("its lights out and away we go\n" + "\n".join(f_body) + "\nretire the car", local_vars, functions)
            i = curr_i  
        
        elif tokens[i] == "drs":
            try_body = []
            except_body = []
            i += 1
            while i < len(tokens) and tokens[i] != "yellow flag":
                try_body.append(tokens[i])
                i += 1
            if i >= len(tokens) or tokens[i] != "yellow flag":
                raise SyntaxError("Yellow flag not found after DRS block")
            i += 1
            while i < len(tokens) and tokens[i] != "green flag":
                except_body.append(tokens[i])
                i += 1
            if i >= len(tokens) or tokens[i] != "green flag":
                raise SyntaxError("Green flag not found to end DRS block")
            
            try:
                start("its lights out and away we go\n" + "\n".join(try_body) + "\nretire the car", variables.copy(), functions)
            except Exception as e:
                start("its lights out and away we go\n" + "\n".join(except_body) + "\nretire the car", variables.copy(), functions)
        elif tokens[i] == "grid start":
            i += 1
            while tokens[i] != "grid end":
                pos_str, value_str = tokens[i].split()
                index = int(pos_str[1:]) - 1
                if index < 0 or index > 19:
                    raise IndexError(f"Invalid grid position: {index + 1}")
                value = int(value_str)
                grid[index] = value
                variables[pos_str] = value
                i += 1
                if tokens[i] != "grid end" or re.match(r"^p(\d+)\s+(\d+)$",tokens[i]) == False:
                    raise SyntaxError("Grid end not found")
                
        elif tokens[i].startswith("radio "):
            _,message = tokens[i].split(maxsplit=1)
            if message.startswith("grid"):
                _, pos_str = message.split()
                index = int(pos_str[1:]) - 1
                if index < 0 or index > 19:
                    raise ValueError(f"Invalid grid position: {index + 1}")
                print(grid[index])
            else:
                if message in variables.keys():
                    print(variables[message])
                else:
                    print(message)
        else:
            raise ValueError(f"Unknown radio message: %s"% tokens[i])
        i += 1
command ="""
ITS LIGHTS OUT AND AWAY WE GO
strat speed 100
strat boost speed + 2
grid start
p1 10
grid end
radio grid p1
RADIO hello world
radio speed
radio boost
strat boost boost + p1
radio boost
retire the car
"""
code = """
ITS LIGHTS OUT AND AWAY WE GO
strat speed 100
pit add2 var1
strat var1 var1 + 2
crash
box box add2 speed
radio speed
"""

test = """
ITS LIGHTS OUT AND AWAY WE GO
strat speed 100
pit addnum var1 var2
strat var1 var1 + var2
crash
box box addnum speed 10
radio speed
pit divnum var1 var2
strat var1 var1 / var2
crash
strat weight 50
box box divnum weight 5
radio weight
retire the car
"""

test2= """
ITS LIGHTS OUT AND AWAY WE GO
drs
strat speed 100
strat boost speed / 2
radio speed
radio boost
yellow flag
radio something is wrong I can feel it
green flag
retire the car"""


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python pitscript.py <filename>.f1")
        sys.exit(1)
    
    filename = sys.argv[1]

    if not filename.endswith(".f1"):
        print("Error: Only .f1 files are allowed")
        sys.exit(1)

    try:
        with open(filename, 'r') as f:
            code = f.read()
        start(code)
    except FileNotFoundError:
        print(f"Error: File %s not found"% filename)
    except Exception as e:
        print("Engine failure:", e )