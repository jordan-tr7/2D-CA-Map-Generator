import imageio.v2 as imageio 
import os 
import re

image_folder = "figs/animation"
output_file_path = "figs/gifs/Simple-map-sparse.gif"

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


def main():
    
    filenames = sort_text_by_number(os.listdir(image_folder))

    images = []

    for file in filenames:
        print(os.path.join(image_folder, file))
        temp = os.path.join(image_folder, file)
        image = imageio.imread(temp)
        images.append(image)
    
    imageio.mimsave(output_file_path, images, format = "GIF", duration = 500)



if __name__ == "__main__":
    main()
