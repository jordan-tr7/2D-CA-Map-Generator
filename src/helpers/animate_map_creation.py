"""
Tristan Jordan
4/16/25
This file contains functions to animate the sequence of images 
in the figs/animation directory into a .gif 
"""

import imageio.v2 as imageio # for creating gifs
import os # for file paths
import re # regex for ordering gif frames

IMAGE_FOLDER = "figs/animation"


# function to sort text file names by number
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


# function to empty anim directory
def clear_anim_directory():
    """
    Function to clear all images from the animation directory. Creating
    this because for some gifs a lot of images are created.

    Args: 
        None
    Returns: 
        None, but figs/animation will be cleared of all pngs
    """
    for filename in os.listdir(IMAGE_FOLDER):
        file_path = os.path.join(IMAGE_FOLDER, filename)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
            elif os.path.isdir(file_path):
                print(f"Skipping directory: {file_path}")
        except Exception as e:
            print(f"Error deleting {file_path}: {e}")


# function to animate map creation from a series of pngs
def animate_map_creation(output_file_path, frame_duration, initial_iterations):
    """
    This function takes all of the pngs in figs/animation and converts them
    to a GIF.

    Args:
        output_file_path: string, name of location to save GIF
        frame_duration: int, the duration in milliseconds that frames not equal to the
            initial map creation should last for. Set this separately
            because initial map creation has much fewer frames than later steps.
        initial_iterations: int, the number of iterations used in map creation, used to
            distinguish the slower map creation frames vs. faster frames set by frame_duration.
    
    Returns: 
        None, but a gif will be saved to output_file_path for the animated sequence of imgs in figs/animation
    """
    # get all file names in the animation directory and make sure they're in correct sorted order
    filenames = sort_text_by_number(os.listdir(IMAGE_FOLDER))

    # create gif images for each file name and append them into list
    images = []
    for file in filenames:
        print(os.path.join(IMAGE_FOLDER, file))
        temp = os.path.join(IMAGE_FOLDER, file)
        image = imageio.imread(temp)
        images.append(image)
    
    # we need to create a list to manually set frame duration on each png in the gif. 
    # we do this so that we can make the initial animation sequence slower. All remaining
    # images for steps not in initial_iterations will be set to frame_duration
    frames = initial_iterations * [400]
    subsequent_frames = (len(images) - initial_iterations) * [frame_duration]
    frames.extend(subsequent_frames)

    # save GIF output using imageio.mimsave, image list, and custom duration list for frames. 
    # Updating to add looping to GIF
    imageio.mimsave(output_file_path, images, format = "GIF", duration = frames, loop = 0)
