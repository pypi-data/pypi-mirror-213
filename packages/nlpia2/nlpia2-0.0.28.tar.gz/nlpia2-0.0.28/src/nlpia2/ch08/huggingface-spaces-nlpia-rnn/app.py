# app.py
import gradio
import sys

from pipeline import predict_nationality


def greet_nationality(name):
    nationality = predict_nationality(name)
    return f"Hello {name}!!\n Your name seems to be from {nationality}. Am I right?"


if __name__ == '__main__':
    iface = gradio.Interface(
        fn=greet_nationality, inputs="text", outputs="text")
    share = len(sys.argv) > 1 and any(('share' in a.lower() for a in sys.argv[1:]))
    iface.launch(share=share)
