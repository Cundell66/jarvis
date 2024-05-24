import os
import uuid
from dotenv import load_dotenv

from deepgram import (
    DeepgramClient,
    SpeakOptions,
)

load_dotenv()

api_key = os.getenv("DEEPGRAM_API_KEY")



def tts(text):
    sound_dir = "./sounds"

    for f in os.listdir(sound_dir):
        if f.endswith(".wav"):
            os.remove(os.path.join(sound_dir, f))

    print(sound_dir)

    SPEAK_OPTIONS = {"text": text}
    try:
        # STEP 1: Create a Deepgram client using the API key from environment variables
        deepgram = DeepgramClient(api_key=api_key)
        print(api_key)
        # STEP 2: Configure the options (such as model choice, audio configuration, etc.)
        options = SpeakOptions(
            model="aura-stella-en",
            encoding="linear16",
            container="wav"
        )

        # STEP 3: Call the save method on the speak property
        unique_id = str(uuid.uuid4())
        print (unique_id)
        filename = f"./sounds/output_{unique_id}.wav"
        print(filename)

        response = deepgram.speak.v("1").save(filename, SPEAK_OPTIONS, options)
        return filename

    except Exception as e:
        print(f"Exception: {e}")


if __name__ == "__main__":
    tts("this is a test")