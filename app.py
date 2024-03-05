import streamlit as st
import numpy as np
from PIL import Image
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import io
import base64
import tempfile

path = r'./Montserrat-Bold.otf'
# Function to transform mask image
def transform_format(val):
    if val != 0:
        return 255
    else:
        return 0

def main():
    st.title("Word Cloud Generator")

    # File upload for mask image
    st.sidebar.title("Upload Mask Image")
    mask_image = st.sidebar.file_uploader("Upload mask image", type=["jpg", "jpeg", "png"])

    # Text input for word cloud
    st.sidebar.title("Input Text")
    text = st.sidebar.text_area("Enter your text here", height=200)

    if st.button("Generate Word Cloud"):
        if text:
            # Sample stopwords
            stopwords = set(STOPWORDS)
            stopwords.update(["drink", "now", "wine", "flavor", "flavors"])

            # Load mask image
            if mask_image is not None:
                mask = np.array(Image.open(mask_image).convert('L'))  # Convert to grayscale
                transformed_mask = np.ndarray((mask.shape[0], mask.shape[1]), np.int32)
                for i in range(len(mask)):
                    transformed_mask[i] = list(map(transform_format, mask[i]))

                # Function for changing the color of the text (keeping it black)
                def black_color_func(word=None, font_size=None, position=None, orientation=None, font_path=None,
                                    random_state=None):
                    return "rgb(0, 0, 0)"

                # Create WordCloud object with black color function
                wc = WordCloud(background_color="white", mask=transformed_mask, 
                               font_path = path,
                               stopwords=stopwords,
                               max_words=200, repeat=True, color_func=black_color_func)

                # Generate word cloud
                wc.generate(text.upper())

                # Display the word cloud
                st.image(wc.to_image(), caption='Word Cloud')

                # Option to download the word cloud image
                if st.button('Download Word Cloud Image'):
                    # Save image to a temporary file
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmpfile:
                        wc.to_image().save(tmpfile.name)

                        # Get the base64 representation of the file
                        with open(tmpfile.name, "rb") as image_file:
                            b64_str = base64.b64encode(image_file.read()).decode()

                    # Create a download link
                    href = f'<a href="data:image/png;base64,{b64_str}" download="wordcloud.png">Click here to download</a>'
                    st.markdown(href, unsafe_allow_html=True)
            else:
                st.warning("Please upload a mask image.")
        else:
            st.warning("Please enter some text.")

if __name__ == "__main__":
    main()
