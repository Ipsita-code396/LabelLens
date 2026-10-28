from gtts import gTTS
import io
import streamlit as st
import easyocr
import numpy as np
import cv2
from PIL import Image, ImageOps
import time
from deep_translator import GoogleTranslator, MyMemoryTranslator

st.set_page_config(page_title="LabelLens", page_icon="🔍")
st.title("LabelLens")
st.caption("Scan a label to get readable text.")

DIGITS = str.maketrans("०१२३४५६७८९", "0123456789")


@st.cache_resource
def load_reader():
    return easyocr.Reader(["en", "hi"])


reader = load_reader()


def preprocess(image):
    img = np.array(image.convert("RGB"))
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    if gray.shape[1] < 1000:
        gray = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    return clahe.apply(gray)


@st.cache_data(show_spinner="Reading label...")
def run_ocr(data: bytes):
    image = ImageOps.exif_transpose(Image.open(io.BytesIO(data)))
    image.thumbnail((1600, 1600))
    processed = preprocess(image)
    results = reader.readtext(processed, detail=1)
    return [(t.translate(DIGITS), float(c)) for _, t, c in results], processed


@st.cache_data(show_spinner="Translating...")
def chunk_text(text, size=450):
    chunks, cur = [], ""
    for w in text.split():
        if len(cur) + len(w) + 1 > size:
            chunks.append(cur)
            cur = w
        else:
            cur = (cur + " " + w).strip()
    if cur:
        chunks.append(cur)
    return chunks


@st.cache_data(show_spinner="Translating...")
def to_hindi(text):
    chunks = chunk_text(text)
    for engine in ("google", "mymemory"):
        try:
            out = []
            for c in chunks:
                if engine == "google":
                    out.append(GoogleTranslator(source="en", target="hi").translate(c))
                else:
                    out.append(MyMemoryTranslator(source="english", target="hindi").translate(c))
                time.sleep(0.4)
            return " ".join(out)
        except Exception:
            continue
    raise RuntimeError("All translators failed")

@st.cache_data(show_spinner="Making audio...")
def make_audio(text, lang_code):
    buf = io.BytesIO()
    gTTS(text[:1500], lang=lang_code).write_to_fp(buf)
    return buf.getvalue()

img = st.camera_input("Scan a label") or st.file_uploader(
    "Or upload a photo", type=["png", "jpg", "jpeg"]
)

if img:
    results, processed = run_ocr(img.getvalue())
    text = " ".join(t for t, c in results if c > 0.3)

    lang = st.radio("Language", ["English", "हिन्दी"], horizontal=True)

    translated = False
    shown = text
    if lang == "हिन्दी" and text:
        try:
            shown = to_hindi(text)
            translated = True
        except Exception:
            st.error("Translation is busy right now. Showing English. Wait a minute and switch again.")

    st.subheader("Label text")
    if not text:
        st.write("No text detected, try a sharper photo.")
    elif translated:
        c1, c2 = st.columns(2)
        c1.markdown("**Original (from label)**")
        c1.write(text)
        c2.markdown("**हिन्दी (translated)**")
        c2.write(shown)
    else:
        st.write(text)

    if any(c <= 0.3 for _, c in results):
        st.warning(
            "Some lines were too unclear to read and are hidden. "
            "Please check the original packaging for those parts."
        )
    st.info("LabelLens only repeats what is printed on the label. Verify with your pharmacist or the original packaging.")

    if text and st.button("🔊 Read aloud"):
        audio = make_audio(shown, "hi" if translated else "en")
        st.audio(audio, format="audio/mp3")

    with st.expander("Raw OCR results (with confidence)"):
        for t, c in results:
            st.write(f"{t}  ({c:.2f})")
    with st.expander("Processed image"):
        st.image(processed)
