import google.generativeai as genai
import string

genai.configure(api_key="AIzaSyBNckU3bCg22Rl1BJ4Nlo0Mzq2GGGiKrz8")
model = genai.GenerativeModel('gemini-1.5-flash')

punctuations = string.punctuation

def process_text(text):

    text = ''.join([letter for letter in text if text not in punctuations])
    try:
        response = model.generate_content(f"""
        Correct following text: {text}, only return corrected version and stem the words, don't write anything else. If there is nothing to correct, return whatever was written in text.
                                      """)
        return response.text
    except:
        return text