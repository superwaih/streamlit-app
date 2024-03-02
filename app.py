import streamlit as st
import numpy as np
from PIL import Image
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import io

# Function to transform mask image
def transform_format(val):
    if val != 0:
        return 255
    else:
        return val

def main():
    st.title("Word Cloud Generator")

    # Sample text
    text = "Leader Visionary Mentor CEO Founder Role-Model Protector Connector Inspiring Motivator Therapist Problem Solver Financier Generous Dedicated Resilient Loving Coach Boss"

    # Sample stopwords
    stopwords = set(STOPWORDS)
    stopwords.update(["drink", "now", "wine", "flavor", "flavors"])

    # Load mask image
    mask_image = Image.open("mask.jpg")
    mask = np.array(mask_image)

    # Transform mask image
    transformed_mask = np.ndarray((mask.shape[0], mask.shape[1]), np.int32)
    for i in range(len(mask)):
        transformed_mask[i] = list(map(transform_format, mask[i]))

    # Function for changing the color of the text
    def one_color_func(word=None, font_size=None, position=None, orientation=None, font_path=None,
                        random_state=None):
        # This HSL is for the green color
        h = 120
        s = 100
        l = 50
        return "hsl({}, {}%, {}%)".format(h, s, l)

    # Create WordCloud object
    wc = WordCloud(background_color="white", mask=transformed_mask, stopwords=stopwords,
                   max_words=200, repeat=True, color_func=one_color_func)

    # Generate word cloud
    wc.generate(text.upper())

    # Convert to image
    img_data = wc.to_image()

    # Display the word cloud
    st.image(img_data, caption='Word Cloud')

    # Option to download the word cloud image
    if st.button('Download Word Cloud Image'):
        # Save image to a BytesIO buffer
        img_buffer = io.BytesIO()
        img_data.save(img_buffer, format='PNG')
        img_bytes = img_buffer.getvalue()

        # Download link
        st.download_button(label='Download Image', data=img_bytes, file_name='wordcloud.png', mime='image/png')

if __name__ == "__main__":
    main()
