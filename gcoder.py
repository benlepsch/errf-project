# how far to turn the conveyor belt after printing (mm along y axis)
cycle_amt = 200

# max distance to move continuously before breaking it up into smaller move commands
max_cont_move = 500

# range for random values to add to cycle_amt
# final distance is cycle_amt + randint(rrange[0], rrange[1])
rrange = (1, 15)

# speed to turn conveyor belt after printing (mm/min)
belt_speed = 1800

# default values for looping gcode w/ m808
repeating = True
repeat_reps = 2



'''
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
from random import randint
import re

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

def modify():
    global fpath, cycle_amt, repeating, repeat_reps
    
    # verify output is .gcode
    output_name = output_path_input_var.get()
    if not output_name[-6:] == '.gcode':
        output_name += '.gcode'

    # open input file
    infile = open(fpath, 'r')
    output = ('M808 L' + str(repeat_reps)) if repeating else ''
    
    # remove "home all" lines
    for line in infile.read().split('\n'):
        # G28 = home, replace with `G28 X Z`
        if 'G28' in line:
            # also check for like 'G28 X0 Y0'
            output += re.sub(r'G28( X[0-9]*)?( Y[0-9]*)?( Z[0-9]*)?', 'G28 X0 Z0', line)
        else:
            output += line
        
        output += '\n'
    infile.close()

    # move conveyor belt a lot
    # G0 Y100 => sets Y axis to 100mm
    # if G0 is too fast, G1 allows u to set feed rate: G1 Y100 F1800 => move to 100mm at 1800mm/min
    move_dist = cycle_amt + randint(rrange[0], rrange[1])
    move_cmd = ''
    # split up longer moves into multiple 500 mm moves
    while move_dist > max_cont_move:
        move_cmd += 'G1 Y' + str(move_dist) + ' F' + str(belt_speed) + '\n'
        move_dist -= max_cont_move
    move_cmd += 'G1 Y' + str(move_dist) + ' F' + str(belt_speed) + '\n'

    loop_cmd = 'M808\n' if repeating else ''

    finish_regex =  r'''(M400                                      ; wait for moves to finish
M140 S[0-9]+.?[0-9]+ ; start bed cooling
M104 S0                                   ; disable hotend
M107                                      ; disable fans
G92 E5                                    ; set extruder to 5mm for retract on print end
M117 Cooling please wait                  ; progress indicator message on LCD
G1 X5 Y5 Z158 E0 F10000                   ; move to cooling position
G1 E5                                     ; re-prime extruder
M190 R[0-9]+.?[0-9]+ ; wait for bed to cool down to removal temp
M77					  ; Stop GLCD Timer
G1 X145 F1000                             ; move extruder out of the way
G1 Y175 F1000                             ; present finished print
M140 S[0-9]+.?[0-9]+; keep temperature or cool down
M84                                       ; disable steppers
G90                                       ; absolute positioning
M117 Print Complete.                      ; print complete message)'''
    output = re.sub(finish_regex, move_cmd + loop_cmd + r'\1', output)

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