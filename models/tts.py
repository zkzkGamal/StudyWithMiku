from diffsinger.infer import DiffSingerInfer

model = DiffSingerInfer(
    acoustic_model="miku_acoustic.pt",
    pitch_model="miku_pitch.pt",
    vocoder="miku_hifigan.pt"
)

if __name__ == "__main__":
    model.infer(
        text="Hello, I am your study assistant!",
        pitch=440,      # A4-like brightness
        speed=1.05
    )