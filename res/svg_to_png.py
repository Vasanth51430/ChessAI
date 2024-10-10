import os
import cairosvg

def convert_svg_to_png(input_dir, output_dir):
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Get a list of SVG files in the input directory
    svg_files = [f for f in os.listdir(input_dir) if f.endswith('.svg')]

    # Convert each SVG file to PNG with transparent background and save in the output directory
    for svg_file in svg_files:
        svg_path = os.path.join(input_dir, svg_file)
        png_file = os.path.splitext(svg_file)[0] + '.png'
        png_path = os.path.join(output_dir, png_file)
        
        # Convert SVG to PNG with transparent background
        cairosvg.svg2png(url=svg_path, write_to=png_path, background_color=None)
        
        print(f"Converted {svg_file} to {png_file}")

# Example usage:
if __name__ == "__main__":
    input_directory = 'res_svg'  # Directory containing SVG files
    output_directory = 'res'  # Directory where PNG files will be saved
    convert_svg_to_png(input_directory, output_directory)
