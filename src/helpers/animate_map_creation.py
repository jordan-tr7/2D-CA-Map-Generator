"""
Tristan Jordan
4/16/25
This script animates the sequence of images in the figs/animation directory
into a .gif 
"""

import imageio.v2 as imageio 
import os 
import re

IMAGE_FOLDER = "figs/animation"

"""
Note: google searched for: "Python sort text list by number", and adapted the
following response from Google's AI assist to quickly get the numbers out of these
file names for correct order *TAJ 4/15
"""
def sort_text_by_number(text_list):
    def extract_number(text):
        match = re.search(r'\d+', text)
        if match:
            return int(match.group(0))
        return float('inf')  # Assign infinity for no number

    return sorted(text_list, key=extract_number)


def clear_anim_directory():
    for filename in os.listdir(IMAGE_FOLDER):
        file_path = os.path.join(IMAGE_FOLDER, filename)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
            elif os.path.isdir(file_path):
                print(f"Skipping directory: {file_path}")
        except Exception as e:
            print(f"Error deleting {file_path}: {e}")

def animate_map_creation(output_file_path, frame_duration, initial_iterations):
    
    filenames = sort_text_by_number(os.listdir(IMAGE_FOLDER))

    images = []

    for file in filenames:
        print(os.path.join(IMAGE_FOLDER, file))
        temp = os.path.join(IMAGE_FOLDER, file)
        image = imageio.imread(temp)
        images.append(image)
    
    frames = initial_iterations * [269]
    subsequent_frames = (len(images) - initial_iterations) * [frame_duration]

    frames.extend(subsequent_frames)

    imageio.mimsave(output_file_path, images, format = "GIF", duration = frames)

