import os

for file in os.listdir("tests"):
    path = f"tests/{file}"
    with open(path) as f:
        stuff = f.read()

    new_stuff = stuff + """

char irq(){
    
}
"""
    with open(path, 'w') as f:
        f.write(new_stuff)