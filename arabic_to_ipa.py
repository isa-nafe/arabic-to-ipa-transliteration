import re

class ArabicToIPATransliterator:
    def __init__(self):
        self.arabic_to_ipa = {
            'ا': 'aː',
            'ب': 'b',
            'ت': 't',
            'ث': 'θ',
            'ج': 'd͡ʒ',
            'ح': 'ħ',
            'خ': 'x',
            'د': 'd',
            'ذ': 'ð',
            'ر': 'r',
            'ز': 'z',
            'س': 's',
            'ش': 'ʃ',
            'ص': 'sˤ',
            'ض': 'dˤ',
            'ط': 'tˤ',
            'ظ': 'ðˤ',
            'ع': 'ʕ',
            'غ': 'ɣ',
            'ف': 'f',
            'ق': 'q',
            'ك': 'k',
            'ل': 'l',
            'م': 'm',
            'ن': 'n',
            'ه': 'h',
            'و': 'w',
            'ي': 'j',
            'ء': 'ʔ',
            # Diacritics
            'َ': 'a',
            'ُ': 'u',
            'ِ': 'i',
            'ّ': 'ː',
            'ْ': '',  # Sukun (no vowel)
            # Additional letters
            'ى': 'aː',
            'ة': 'h',  # Taa marbouta
        }

    def add_rule(self, arabic_char, ipa_char):
        """Add or modify a transliteration rule."""
        self.arabic_to_ipa[arabic_char] = ipa_char

    def remove_rule(self, arabic_char):
        """Remove a transliteration rule."""
        if arabic_char in self.arabic_to_ipa:
            del self.arabic_to_ipa[arabic_char]

    def transliterate(self, text):
        """Transliterate Arabic text to IPA."""
        # Normalize Arabic text
        text = re.sub(r'[^\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF\s]', '', text)
        
        # Handle special cases
        text = re.sub(r'ال', 'al ', text)  # Definite article
        text = re.sub(r'([تطد])ه', r'\1ah', text)  # Taa marbouta pronunciation
        
        # Transliterate each character
        ipa_text = ''
        for char in text:
            ipa_text += self.arabic_to_ipa.get(char, char)
        
        # Post-processing
        ipa_text = re.sub(r'aː[aiuː]', 'aː', ipa_text)  # Remove short vowels after long 'a'
        ipa_text = re.sub(r'([aiu])w([aiu])', r'\1w\2', ipa_text)  # Handle 'w' between vowels
        ipa_text = re.sub(r'([aiu])j([aiu])', r'\1j\2', ipa_text)  # Handle 'y' between vowels
        
        return ipa_text.strip()

def transliterate_arabic_to_ipa(text):
    """
    Backward compatibility function for the old API.
    """
    transliterator = ArabicToIPATransliterator()
    return transliterator.transliterate(text)

if __name__ == "__main__":
    print("Arabic to IPA Transliterator")
    print("Enter 'q' to quit")
    
    transliterator = ArabicToIPATransliterator()
    
    while True:
        arabic_text = input("\nEnter Arabic text: ")
        if arabic_text.lower() == 'q':
            break
        
        try:
            ipa_text = transliterator.transliterate(arabic_text)
            print(f"IPA: {ipa_text}")
        except Exception as e:
            print(f"An error occurred: {str(e)}")
