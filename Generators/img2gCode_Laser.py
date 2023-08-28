from PIL import Image
import argparse

def rgb_to_intensity(rgb_value):
    rgb_integer = int(rgb_value, 16)
    
    # Extrahiere die einzelnen Farbanteile (Rot, Grün, Blau)
    red = (rgb_integer >> 16) & 0xFF
    green = (rgb_integer >> 8) & 0xFF
    blue = rgb_integer & 0xFF
    
    # Berechne den Durchschnitt der Farbanteile als Intensität
    intensity = (red + green + blue) / (3 * 255)
    
    return intensity

def image_to_gcode(image_path, output_path):
    image = Image.open(image_path)
    width, height = image.size
    
    gcode_lines = []

    # G-Code-Header
    gcode_lines.append("G90 ; Set to absolute positioning")
    gcode_lines.append("G21 ; Set units to millimeters")
    #gcode_lines.append("G28 ; Home all axes")

    # Startpunkt unten links
    start_x = 0
    start_y = 0

    for y in range(height):
        for x in range(width):
            pixel = image.getpixel((x, y))
            intensity = rgb_to_intensity("%02X%02X%02X" % pixel)
            
            # Berechne Laserleistung (z.B. 0% - 100%)
            laser_power = intensity * 100

            # Bewege den Laser zum aktuellen Punkt und setze Laserleistung
            gcode_lines.append(f"G0 X{x + start_x} Y{y + start_y} S{laser_power:.2f}")
            # Aktiviere den Laser (M3)
            gcode_lines.append("M3")
            #Pause?
            # G4 P0.5
            # Deaktiviere den Laser (M5)
            gcode_lines.append("M5")

    #gcode_lines.append("G28 ; Home all axes")
    gcode_lines.append("M30 ; End of program")

    with open(output_path, "w") as f:
        for line in gcode_lines:
            f.write(line + "\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert an image to G-Code for laser engraving")
    parser.add_argument("-i", "--input", required=True, help="Input image file path")
    parser.add_argument("-o", "--output", required=True, help="Output G-Code file path")
    args = parser.parse_args()

    input_image = args.input
    output_gcode = args.output
    
    image_to_gcode(input_image, output_gcode)
    print(f"G-Code wurde in '{output_gcode}' gespeichert.")