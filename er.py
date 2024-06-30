from PIL import Image

# Open an image file
image = Image.open('Resources/board_pokemon_find.png')

# Resize image to a specific width and height
new_width = 3300
new_height = 1854
resized_image = image.resize((new_width, new_height))

# Save resized image
resized_image.save('Resources/resized_example.png')

# Optionally, show the resized image
resized_image.show()