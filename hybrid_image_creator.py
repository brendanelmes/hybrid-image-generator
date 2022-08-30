import cv2
import numpy
import math


# Convolve a 2D kernel with an input image
def convolution(kernel, input_image, kernel_size):

    # Create new black image with dimensions of input image to give black border
    new_image = numpy.zeros_like(input_image)

    # Receive image and kernel dimensions
    image_cols, image_rows, unused_var = input_image.shape
    template_rows = template_cols = kernel_size
    temp_row_half = int(template_rows / 2)
    temp_col_half = int(template_cols / 2)

    # Iterate through pixels within border
    for x in range((temp_row_half + 1), (image_cols - temp_row_half)):
        for y in range((temp_col_half + 1), (image_rows - temp_col_half)):

            # Set initial pixel value to (0,0,0)
            pixel_sum = numpy.zeros(3)

            # Iterate through pixels in kernel
            for i in range(0, template_rows-1):
                for j in range(0, template_cols-1):

                    # Compute cumulative sum of pixel value multiplied by
                    # corresponding kernel weighting
                    pixel_sum = pixel_sum + \
                                (input_image[x + i - temp_row_half - 1]
                                 [y + j - temp_col_half - 1] * kernel[j-1][i-1])

            # Set pixel value to new value
            new_image[x][y] = pixel_sum

    return new_image


# Apply a low-pass filter to an image, given a cutoff value sigma
def low_pass_filter(input_image, sigma):

    # Calculate size of template depending on sigma value
    size = int(8 * sigma + 1)
    if size % 2 == 0:
        size = size + 1

    centre = int(size / 2) + 1

    # Create template according to size
    template = [[0 for x in range(0, size - 1)] for y in range(0, size - 1)]
    template_sum = 0

    # Iterate through the empty template
    for a in range(0, size - 1):
        for b in range(0, size - 1):

            # Using the gaussian operator, compute the values for the template
            template[a][b] = (1 / (2 * math.pi * (sigma ** 2))) * math.exp(
                -((a - centre) ** 2 + (b - centre) ** 2) / (2 * (sigma ** 2)))
            template_sum = template_sum + template[a][b]

    # Iterate through filled template
    for a in range(0, size - 1):
        for b in range(0, size - 1):

            # Normalise the template
            template[a][b] = template[a][b] / template_sum

    # Call convolution function to apply filter to image
    output_image = numpy.array(convolution(template, input_image, size))
    return output_image


def create_hybrid_images(image1, image2, sigma_value):

    # Apply low-pass filter to each image using cutoff values
    lpf_image1 = low_pass_filter(image1, sigma_value)
    lpf_image2 = low_pass_filter(image2, sigma_value)

    # Subtract low-pass filtered images from originals to get
    #  high-pass filtered images
    hpf_image1 = image1 - lpf_image1
    hpf_image2 = image2 - lpf_image2

    # Add low-pass filtered image from each image
    # to the high-pass filtered image of the other
    hybrid_image_1 = lpf_image1 + hpf_image2
    hybrid_image2 = lpf_image2 + hpf_image1

    return hybrid_image_1, hybrid_image2

# Choose a value for sigma
sigma_sigma = 2

# Import two images and resize the second to the size of the first
photo1 = cv2.imread('source-images/volleyball.jpg')
photo2_before_resize = cv2.imread('source-images/basketball.jpeg')
photo2 = cv2.resize(photo2_before_resize, (500, 500))

# Generate the hybrid images
hybrid1, hybrid2 = create_hybrid_images(photo1, photo2, sigma_sigma)

# Display each hybrid image following a key press
cv2.imshow("hybrid image 1", hybrid1)
cv2.waitKey(0)
cv2.imshow("hybrid image 2", hybrid2)
cv2.waitKey(0)
