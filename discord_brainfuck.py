import sys

help = "python3 discord_brainfuck.py [file_here.dbf] [bot token]"

if len(sys.argv) != 3:
    print(help)
    exit(0)

f = open(sys.argv[1], 'r')
all_code = f.read()
f.close()

cells = [0]
current_cell = 0

def insert_to_cell(cell: int, value: int):
    if cell > len(cells):
        for c in range(len(cells)-cell):
            cells.append(0)
    try:
        cells[cell] = value
    except:
        cells.append(value)

def get_from_cell(cell: int):
    try:
        return cells[cell]
    except IndexError:
        return 0

def increment_cell_value(cell: int):
    insert_to_cell(cell, get_from_cell(cell)+1)

def decrement_cell_value(cell: int):
    insert_to_cell(cell, get_from_cell(cell)-1)

def print_cells():
    to_print = ""
    for cell in cells:
        to_print += f"[{cell}]"
    print(to_print)

commands = []
loops = []

index = 0
def interpret(code: str, index: int):
    global current_cell
    while index+1 != len(code):
        char = code[index]
        if char == ">":
            current_cell+=1
        elif char == "<":
            current_cell-=1
        elif char == "+":
            increment_cell_value(current_cell)
        elif char == "-":
            decrement_cell_value(current_cell)
        elif char == "[":
            loops.insert(0, index+1)
        elif char == "]":
            if get_from_cell(current_cell) > 0:
                index = loops[0]
                continue
            else:
                loops.remove(loops[0])
        elif char == ",":
            insert_to_cell(current_cell, ord(input("")[0]))
        elif char == "$":
            commands.append({"trigger": "", "response": ""})
        elif char == "*":
            commands[len(commands)-1]["trigger"] += chr(get_from_cell(current_cell))
        elif char == "!":
            commands[len(commands)-1]["response"] += chr(get_from_cell(current_cell))
        elif char == ".":
            print(chr(get_from_cell(current_cell)), end = "")
        index+=1

interpret(all_code, 0)
#print(commands)

for command in commands:
    print(f"Added command {command['trigger']}")

# Discord Bot

import discord

client = discord.Client()

@client.event
async def on_message(message):
    for command in commands:
        if message.content == command["trigger"]:
            await message.channel.send(command["response"])
            return

client.run(open(sys.argv[2], "r").read())