import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io
import os

st.title("😂 Meme Generator")
st.write("Upload an image, add top and bottom text, then download your meme! Lets have fun")
uploaded_file = st.file_uploader("Choose an image which you want to upload", type=["jpg", "png", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")


    top_text = st.text_input("Top Content")
    bottom_text = st.text_input("Bottom Content")
    font_path = "assets/Impact.ttf"  
    if os.path.exists(font_path):
        font_size = int(image.height / 10)
        font = ImageFont.truetype(font_path, font_size)
    else:
        font = ImageFont.load_default()
    def draw_text(draw, text, pos):
        x, y = pos
        outline_range = max(1, int(font.size / 15))
    
        for dx in range(-outline_range, outline_range + 1):
            for dy in range(-outline_range, outline_range + 1):
                draw.text((x + dx, y + dy), text, font=font, fill="black")
       
        draw.text((x, y), text, font=font, fill="white")
    img_editable = image.copy()
    draw = ImageDraw.Draw(img_editable)

    def get_text_size(text):
        bbox = draw.textbbox((0, 0), text, font=font)
        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]
        return w, h

    if top_text:
        w, h = get_text_size(top_text)
        draw_text(draw, top_text, ((image.width - w) / 2, 10))

    if bottom_text:
        w, h = get_text_size(bottom_text)
        draw_text(draw, bottom_text, ((image.width - w) / 2, image.height - h - 10))

    st.image(img_editable, caption="Your Meme", use_container_width=True)
    buf = io.BytesIO()
    img_editable.save(buf, format="PNG")
    byte_im = buf.getvalue()

    st.download_button(
        label="Download Meme",
        data=byte_im,
        file_name="meme.png",
        mime="image/png"
    )
