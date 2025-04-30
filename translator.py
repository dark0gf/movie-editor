import os
import deepl

# Initialize DeepL translator
# You should set your DeepL API key as an environment variable: DEEPL_API_KEY
def get_translator():
    """
    Initialize and return a DeepL translator instance.
    
    Returns:
        deepl.Translator: A configured DeepL translator instance
    
    Raises:
        ValueError: If the DEEPL_API_KEY environment variable is not set
    """
    api_key = os.environ.get('DEEPL_API_KEY')
    if not api_key:
        raise ValueError("DEEPL_API_KEY environment variable is not set. Please set it to your DeepL API key.")
    
    return deepl.Translator(api_key)

def translate_text(text, target_lang='ES', source_lang=None):
    """
    Translate text using DeepL API.
    
    Args:
        text (str): Text to translate
        target_lang (str): Target language code (default: 'ES' for Spanish)
        source_lang (str, optional): Source language code. If None, DeepL will auto-detect.
    
    Returns:
        str: Translated text
        
    Example:
        >>> translate_text("Hello world", target_lang="ES")
        'Hola mundo'
    """
    try:
        translator = get_translator()
        result = translator.translate_text(
            text, 
            target_lang=target_lang,
            source_lang=source_lang
        )
        return result.text
    except Exception as e:
        print(f"Translation error: {e}")
        # Return original text if translation fails
        return text