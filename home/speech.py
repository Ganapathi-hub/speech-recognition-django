from unidecode import unidecode
import speech_recognition as sr
from indic_transliteration import sanscript
import pyttsx3
from deep_translator import GoogleTranslator

def transliterate_to_ascii(text):
    # Transliterate text to ASCII
    transliterated_text = unidecode(text)
    return transliterated_text

def transcribe_speech(language):
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        print(f"Speak something in {language}!")
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio, language=f"{language.lower()}-IN")  # Recognize speech
        return text
    except sr.UnknownValueError:
        print("Could not understand speech in the specified language.")
        return None

def translate_text(text, source_language, target_language):
    try:
        translated_text = GoogleTranslator(source=source_language, target=target_language).translate(text)
        return translated_text
    except Exception as e:
        print(f"Error occurred during translation: {e}")
        return None

def transliterate_text(text, source_language, target_language):
    # Define transliteration mappings for each language script
    script_map = {
        "kn": sanscript.KANNADA,
        "hi": sanscript.DEVANAGARI,
        "ml": sanscript.MALAYALAM,
        "ta": sanscript.TAMIL,
        "te": sanscript.TELUGU,
        "bn": sanscript.BENGALI,
        "gu": sanscript.GUJARATI,
        "pa": sanscript.GURMUKHI,
        "or": sanscript.ORIYA,
        "en": None  # No script conversion needed for English
        # Add mappings for other languages as needed
    }

    # Get the source and target script objects
    src_script = script_map.get(source_language.lower())
    dest_script = script_map.get(target_language.lower())

    # Perform transliteration
    if dest_script is not None:
        transliterated_text = sanscript.transliterate(text, src_script, dest_script)
    else:
        transliterated_text = transliterate_to_ascii(text)

    return transliterated_text

def speak_text(text, voice_id=None):
    # Initialize the TTS engine
    engine = pyttsx3.init()

    # Get available voices
    voices = engine.getProperty('voices')

    if voice_id is not None:
        # Set the voice based on the provided voice_id
        engine.setProperty('voice', voice_id)

    # Say the text
    engine.say(text)
    engine.runAndWait()

def get_supported_languages():
    # List of supported languages
    return [
        'af', 'sq', 'am', 'ar', 'hy', 'az', 'eu', 'be', 'bn', 'bs',
        'bg', 'ca', 'ceb', 'ny', 'zh-cn', 'zh-tw', 'co', 'hr', 'cs', 'da', 'nl',
        'en', 'eo', 'et', 'tl', 'fi', 'fr', 'fy', 'gl', 'ka', 'de', 'el', 'gu',
        'ht', 'ha', 'haw', 'he', 'hi', 'hmn', 'hu', 'is', 'ig', 'id', 'ga', 'it',
        'ja', 'jw', 'kn', 'kk', 'km', 'ko', 'ku', 'ky', 'lo', 'la', 'lv', 'lt',
        'lb', 'mk', 'mg', 'ms', 'ml', 'mt', 'mi', 'mr', 'mn', 'my', 'ne', 'no',
        'or', 'ps', 'fa', 'pl', 'pt', 'pa', 'ro', 'ru', 'sm', 'gd', 'sr', 'st',
        'sn', 'sd', 'si', 'sk', 'sl', 'so', 'es', 'su', 'sw', 'sv', 'tg', 'ta',
        'te', 'th', 'tr', 'uk', 'ur', 'ug', 'uz', 'vi', 'cy', 'xh', 'yi', 'yo', 'zu'
    ]

def main():
    # Get supported languages for translation and transliteration
    languages = get_supported_languages()
    transliteration_supported_languages = ["kn", "hi", "ml", "ta", "te", "bn", "gu", "pa", "or", "en"]  # Languages supporting transliteration

    # Ask the user to choose the initial speaking language
    print("Choose the initial speaking language:")
    for i, lang_code in enumerate(languages, 1):
        print(f"{i}. {GoogleTranslator().get_supported_languages(as_dict=True).get(lang_code, lang_code)} ({lang_code})")

    # Validate user input for language selection
    while True:
        try:
            choice = int(input("Enter the number corresponding to the initial speaking language: "))
            if choice < 1 or choice > len(languages):
                raise ValueError
            break
        except ValueError:
            print("Invalid choice. Please enter a valid number.")

    initial_language = languages[choice - 1]

    # Transcribe speech from microphone in the chosen initial speaking language
    speech_text = transcribe_speech(initial_language)

    # Display recognized speech text
    print("Recognized Speech Text:", speech_text)

    if speech_text is not None:
        # Ask the user whether they want translation or transliteration
        print("Choose the action:")
        print("1. Transalate")
        print("2. Transliterate")

        action_choice = input("Enter the number corresponding to the action: ")

        if action_choice == "1":
            # Ask the user to choose the target language for translation
            print("Choose the target language for translation:")
            for i, lang_code in enumerate(languages, 1):
                print(f"{i}. {GoogleTranslator().get_supported_languages(as_dict=True).get(lang_code, lang_code)} ({lang_code})")

            # Validate user input for language selection
            while True:
                try:
                    choice = int(input("Enter the number corresponding to the target language: "))
                    if choice < 1 or choice > len(languages):
                        raise ValueError
                    break
                except ValueError:
                    print("Invalid choice. Please enter a valid number.")

            target_language_translate = languages[choice - 1]

            # Perform translation for the chosen language
            translated_text = translate_text(speech_text, initial_language, target_language_translate)
            if translated_text:
                print(f"Translation to {GoogleTranslator().get_supported_languages(as_dict=True).get(target_language_translate, target_language_translate)} ({target_language_translate}): {translated_text}")
                speak_text(translated_text)  # Speak the translated text
            else:
                print("Translation failed.")

        elif action_choice == "2":
            # Ask the user to choose between English transliteration and other languages
            # Filter out the languages that do not support transliteration
            translit_languages = [lang for lang in languages if lang in transliteration_supported_languages]

            # Ask the user to choose the target language for transliteration
            print("Choose the target language for transliteration:")
            for i, lang_code in enumerate(translit_languages, 1):
                print(f"{i}. {GoogleTranslator().get_supported_languages(as_dict=True).get(lang_code, lang_code)} ({lang_code})")

            # Validate user input for language selection
            while True:
                try:
                    choice = int(input("Enter the number corresponding to the target language: "))
                    if choice < 1 or choice > len(translit_languages):
                        raise ValueError
                    break
                except ValueError:
                    print("Invalid choice. Please enter a valid number.")

            target_language_translit = translit_languages[choice - 1]

            # Perform transliteration for the chosen language
            transliterated_text = transliterate_text(speech_text, initial_language, target_language_translit)
            print(f"Transliteration to {GoogleTranslator().get_supported_languages(as_dict=True).get(target_language_translit, target_language_translit)} ({target_language_translit}): {transliterated_text}")
            speak_text(transliterated_text)  # Speak the transliterated text

if __name__ == "__main__":
    main()
