# LabelLens 🔍

**Making confusing labels understandable.**

Scan a medicine, food or household product label with a camera. LabelLens reads the small print, shows it clearly, translates it between English and Hindi, and reads it aloud.

> **Safety principle:** LabelLens only repeats what is printed on the label. It never invents medical instructions or changes prescribed doses. Always verify with your pharmacist or the original packaging.

---

## The problem

Small, dense print on medicine, food and household labels is hard to read, especially for older adults and people with low vision. Many labels are English-only, so people who are more comfortable in Hindi can miss important details like directions, storage conditions, warnings and expiry dates. The problem goes unnoticed because people quietly struggle, guess, or ask someone else.

## Target users

- Older adults
- People with low vision
- Hindi-speaking users who find English labels difficult
- Caregivers buying products for family members

## Features

- 📷 Camera scan or photo upload
- 🔤 OCR in English and Hindi (EasyOCR)
- 🖼️ Image preprocessing (grayscale, contrast boost, upscaling, rotation fix) for small print
- 🔢 Digit cleanup (Hindi-model digits converted to normal digits in English text)
- 🌐 English ⇄ Hindi toggle with the original and translation shown side by side
- 🔊 Read aloud (text-to-speech) in English or Hindi
- ⚠️ Safety layer: low-confidence lines are hidden and flagged ("check the original packaging"), plus a "verify with your pharmacist" note
- ⚡ Cached results, so switching language or re-uploading the same photo is fast

## Tech stack

| Purpose | Tool |
|---|---|
| App / UI | Streamlit |
| OCR (English + Hindi) | EasyOCR |
| Image processing | OpenCV, Pillow |
| Translation | deep-translator (Google, with MyMemory fallback) |
| Text-to-speech | gTTS |
| Language | Python |

## How it works

```
Photo -> Preprocess -> OCR -> Confidence filter -> Translate -> Read aloud
```

1. The image is rotated correctly, resized, converted to grayscale and contrast-enhanced.
2. EasyOCR reads the text with a confidence score for each line.
3. Lines below the confidence threshold are hidden and the user is warned.
4. The text can be translated to Hindi, shown beside the original.
5. The text can be played as audio.

## Getting started

**Requirements:** Python 3.10 or newer, and an internet connection (translation and text-to-speech need it).

```bash
# 1. Clone the repo
git clone https://github.com/<your-username>/<your-repo>.git
cd <your-repo>

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
streamlit run app.py
```

Open http://localhost:8501 in your browser.

> The first run downloads the EasyOCR models (a few hundred MB), so it can take a few minutes. After that it starts quickly.

### requirements.txt

```
streamlit
easyocr
opencv-python-headless
pillow
numpy
deep-translator
gTTS
```

## Usage

1. Take a photo with the camera box, or upload a photo of a label.
2. Wait for the label text to appear.
3. Switch between **English** and **हिन्दी**.
4. Click **🔊 Read aloud** to listen.

**Tips for a good scan:** hold the label flat and parallel to the camera, use bright even light, keep the phone steady, and fill the frame with the print. White labels work better than dark or glossy ones.

## Current progress

- ✅ Camera and upload scanning
- ✅ OCR tested on real products (lotion and hair serum labels)
- ✅ Preprocessing and digit cleanup
- ✅ Low-confidence filter with warning
- ✅ English ⇄ Hindi translation with side-by-side original
- ✅ Read aloud in English and Hindi

## Known limitations

- Blurry, tilted, dark or glossy labels reduce OCR accuracy. Sharp phone photos work much better than webcams.
- Ingredient names may stay in English or be translated imperfectly, and OCR typos can pass through. This is why the original text is always shown beside the translation.
- Free translation and text-to-speech services can be rate-limited on shared networks.
- OCR runs on the CPU, so processing can take several seconds per image.

## Roadmap

- Plain-language explanation of label sections, based only on the label text
- Better handling of ingredient names in translation
- Large-text and high-contrast mode for low-vision users
- Mobile-friendly interface
- Testing on more medicine labels

## Team

Built for a 24-hour hackathon by **<INFINITE LOOP>**:

- Kaushiki Gupta
- <Ipsita Kirati>
- <Vaishnavi Rastogi>
- <Mahi Singh>

## Disclaimer

LabelLens is an accessibility aid, not a medical device. It does not give medical advice. Always check the original packaging and consult a pharmacist or doctor for medicine instructions.
