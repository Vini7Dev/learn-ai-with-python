import matplotlib.pyplot as plt

def display_image(image):
    image = image.copy()
    image.thumbnail((250, 250))
    plt.imshow(image)
    plt.show()
