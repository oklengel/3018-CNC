def generate_planfrs():
    depth=float(input("tiefe"))
    repetitions=int(input("Wiederholungen"))
    opposite_x=int(input("X Gegenüber"))
    opposite_y=int(input("Y Gebgenüber"))

    programm=f"G91 ;\n"
    programm+=f"S8000 M3\n"
    programm+=f"G1 Z-{depth} F100\n"
    programm+=f"G1 F45;\n"
    x=0;
    
    for y in range(opposite_y):
        programm+=f"G1 Y{opposite_y}\n"
        programm+=f"G1 Z1\n"
        programm+=f"G0 Y-{opposite_y}\n"
        programm+=f"G1 Z-1\n"

        if(x<opposite_x):
            programm+=f"G1 X1.5\n"
        
    programm+=f"G0 Z+2\n"
    programm+=f"G0 Z{depth}\n"
    programm+=f"M5\n"

    return programm

cnc_code = generate_planfrs()

fname="planfr.nc"
with open(fname, "w") as file:
    file.write(cnc_code)
