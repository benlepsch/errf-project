'''
Ben Lepsch

program will:
- take a gcode file
- remove home all command, replace with home x and z
- at end of gcode move conveyor belt one full rotation + a little bit extra to even out wear

so
open a dialog box

    |----------------------------------------|
    | GCODE fixer                          X |
    |----------------------------------------|
    | Select File: <Browse>                  |
    |                                        |
    | Output path + filename:                |
    | (input box here, set default path?)    |
    |                                        |
    | <Fix GCODE>       <Open Config File>   |
    |----------------------------------------|

something to this effect
i am thinking config file so you can change conveyor belt full rotation value
could also just do this as a preset at first

'''

from tkinter import *
from tkinter import filedialog

# -----------------------  Browse Files  ------------------------- #

fpath = ''

def file_explorer():
    global fpath
    filename = filedialog.askopenfilename(initialdir="/", title="Select a .gcode file", filetypes=(("GCODE files","*.gcode"),("All files","*.*")))
    # print(filename) # C:/Users/ben lepsch/Documents/errf-project/test.gcode
                      # C:/Users/ben lepsch/Documents/errf-project/test-FIXED.gcode
    fpath = filename
    selected_file_display.delete('1.0', END)
    selected_file_display.insert(END, filename)
    if not (output_path_input_var.get() == ''):
        output_path_input.delete(0, END)
    output_path_input.insert(0, filename[:-6] + '-FIXED.gcode')

# ----------------------  Gcode Modifying  ----------------------- #

# how far to turn the conveyor belt for 1 rotation + a little
# actually how many millimeters its moving along y axis
cycle_amt = 200

def modify():
    global fpath, cycle_amt
    
    # verify output is .gcode
    output_name = output_path_input_var.get()
    if not output_name[-6:] == '.gcode':
        output_name += '.gcode'

    # open input file
    infile = open(fpath, 'r')
    output = ''
    
    # remove "home all" lines
    for line in infile.read().split('\n'):
        # G28 = home, replace with `G28 X Z`
        # could check to see if its homing y axis but this is easier
        if line.split(' ')[0] == 'G28':
            output += 'G28 X Z'
        else:
            output += line
        
        output += '\n'
    infile.close()

    # move conveyor belt a lot
    # G0 Y100 => sets Y axis to 100mm
    # if G0 is too fast, G1 allows u to set feed rate: G1 Y100 F1800 => move to 100mm at 1800mm/min
    output += 'G0 Y' + str(cycle_amt) + '\n'

    # then should i try to set it so it thinks its back at Y=0?
    # actually i'm not sure i can
    # hopefully it'll be fine if it restarts between prints and doesn't home Y axis

    # write output
    outfile = open(output_name, 'w')
    outfile.write(output)
    outfile.close()

    # todo: something so the user knows it finished

    


# -------------------------  GRAPHICS  --------------------------- #

window = Tk()
window.title('Gcode Fixer')

# defenition
selected_label = Label(window, text='Selected File:')
browse_files = Button(window, text='Browse Files', command=file_explorer)
selected_file_display = Text(window, height=1, width=100)

output_path_label = Label(window, text='Output file:')
output_path_input_var = StringVar(value='')
output_path_input = Entry(window, textvariable=output_path_input_var, width=100)

go_button = Button(window, text='Fix File', command=modify)

# gridding (griddy)
selected_label.grid(row=0, column=0)
browse_files.grid(row=1, column=1)
selected_file_display.grid(row=1, column=0)

output_path_label.grid(row=3, column=0)
output_path_input.grid(row=4, column=0)

go_button.grid(row=4, column=1)

window.mainloop()