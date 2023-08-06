import time
import random
import playsound


class MorseCode:
    def __init__(self, preserve_original=False):
        self.morse_code = {
            'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.', 'G': '--.', 'H': '....', 'I': '..',
            'J': '.---', 'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...',
            'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--', 'Z': '--..',
            '0': '-----', '1': '.----', '2': '..---', '3': '...--', '4': '....-', '5': '.....', '6': '-....',
            '7': '--...', '8': '---..', '9': '----.',
            '.': '.-.-.-', ',': '--..--', '?': '..--..', "'": '.----.', '!': '-.-.--', '/': '-..-.', '(': '-.--.',
            ')': '-.--.-', '&': '.-...',
            ':': '---...', ';': '-.-.-.', '=': '-...-', '+': '.-.-.', '-': '-....-', '_': '..--.-', '"': '.-..-.',
            '$': '...-..-', '@': '.--.-.'
        }
        self.preserve_original = preserve_original

    def encode(self, text):
        """
        Encode text to Morse code.

        :param text: The text to be encoded.
        :return: The Morse code representation of the text.

        Example:
            >>> morse = MorseCode()
            >>> encoded_text = morse.encode('Hello World')
            >>> print(encoded_text)
            '.... . .-.. .-.. --- / .-- --- .-. .-.. -..'

        The `encode` method encodes text into Morse code. It takes a single argument `text` which should be a string representing the text to be encoded. The method returns the Morse code representation of the text as a string.

        Each word in the text is encoded using the `encode_word` method, and the encoded words are joined with a forward slash (/) as a word separator.

        Note that this method is suitable for encoding sentences or multiple words. If you want to encode a single word, you should use the `encode_word` method.

        """
        encoded_text = []
        for word in text.split(' '):
            encoded_text.append(self.encode_word(word))
        return ' / '.join(encoded_text)

    def encode_word(self, word):
        """
        Encode a single word to Morse code.

        :param word: The word to be encoded as Morse code.
        :return: The Morse code representation of the word.

        Example:
            >>> morse = MorseCode()
            >>> encoded_word = morse.encode_word('Hello')
            >>> print(encoded_word)
            '.... . .-.. .-.. ---'

        The `encode_word` method encodes a single word into Morse code. It takes a single argument `word` which should be a string representing the word to be encoded. The method returns the Morse code representation of the word as a string.

        Note that this method is intended for encoding individual words. If you want to encode sentences or multiple words, you should use the `encode` method instead.

        If the preserve_original` flag is set to `True`, the method adds an asterisk (*) before the Morse code representation of each uppercase letter to preserve the original casing in the encoded output.

        """
        encoded_word = []
        for char in word:
            if char.isupper():
                is_upper = True
            else:
                is_upper = False
            if char.upper() in self.morse_code:
                if is_upper and self.preserve_original:
                    encoded_word.append("*" + self.morse_code[char.upper()])
                else:
                    encoded_word.append(self.morse_code[char.upper()])
            else:
                encoded_word.append(char)
        return ' '.join(encoded_word)

    def decode_word(self, word):
        """
        Decode a Morse code representation back to text.

        :param word: The Morse code to be decoded.
        :return: The decoded text.

        Example:
            >>> morse = MorseCode()
            >>> decoded_word = morse.decode_word('.... . .-.. .-.. ---')
            >>> print(decoded_word)
            'hello'

        The `decode_word` method decodes a Morse code representation back into text. It takes a single argument `word` which should be a string representing the Morse code to be decoded. The method returns the decoded text as a string.

        If the `preserve_original` flag is set to `True` and an asterisk (*) is found before a Morse code sequence, the method assumes it was originally an uppercase letter and preserves the casing in the decoded output.

        Note that this method is intended for decoding individual words. If you want to decode sentences or multiple words, you should use the `decode` method instead.

        """
        decoded_word = []
        for c in word.split(' '):
            if str(c).startswith('*'):
                is_upper = True
                c = c[1::]
            else:
                is_upper = False
            for char, code in self.morse_code.items():
                if c == code:
                    if is_upper and self.preserve_original:
                        decoded_word.append(char.upper())
                    else:
                        decoded_word.append(char.lower())


        return ''.join(decoded_word)

    def decode(self, text):
        """
        Decode Morse code back to text.

        :param text: The Morse code to be decoded.
        :return: The decoded text.

        Example:
            >>> morse = MorseCode()
            >>> decoded_text = morse.decode('.... . .-.. .-.. --- / .-- --- .-. .-.. -..')
            >>> print(decoded_text)
            'hello world'

        The `decode` method decodes Morse code back into text. It takes a single argument `text` which should be a string representing the Morse code to be decoded. The method returns the decoded text as a string.

        The Morse code is assumed to have word separators represented by a forward slash (/). Each encoded word is decoded using the `decode_word` method, and the decoded words are joined with a space as a word separator.

        Note that this method is suitable for decoding sentences or multiple words. If you want to decode a single word, you should use the `decode_word` method.

        """
        decoded_text = []
        for word in text.split(' / '):
            decoded_text.append(self.decode_word(word))
        return ' '.join(decoded_text)

    def generate_random_morse(self, length):
        """
        Generate a random Morse code message of the specified length.

        :param length: The length of the random Morse code message to be generated.
        :return: The randomly generated Morse code message.

        Example:
            >>> morse = MorseCode()
            >>> random_morse = morse.generate_random_morse(10)
            >>> print(random_morse)
            '. .- -.-. --- ... -.-- .-. .-.. --- ..-'

        The `generate_random_morse` method generates a random Morse code message of the specified length. It takes a single argument `length` which should be an integer representing the desired length of the Morse code message. The method returns the randomly generated Morse code message as a string.

        The Morse code message consists of randomly chosen Morse code characters from the Morse code dictionary.

        """
        morse_chars = list(self.morse_code.values())
        random_morse_message = ' '.join(random.choices(morse_chars, k=length))
        return random_morse_message

    @staticmethod
    def is_valid_morse_code(morse_text):
        """
        Check if the given input string is a valid Morse code message.

        :param morse_text: The input string to be validated.
        :return: True if the input is a valid Morse code message, False otherwise.

        Example:
            >>> morse = MorseCode()
            >>> is_valid = morse.is_valid_morse_code('.... . .-.. .-.. --- / .-- --- .-. .-.. -..')
            >>> print(is_valid)
            True

        The `is_valid_morse_code` method checks whether the given input string is a valid Morse code message. It takes a single argument `morse_text` which should be a string representing the input to be validated. The method returns True if the input is a valid Morse code message, and False otherwise.

        The method validates the input by checking if each character in the input is either a dot (.), dash (-), or forward slash (/), which are the valid Morse code characters. If any other character is found in the input, the method returns False.

        Note that this method does not perform a comprehensive validation of Morse code syntax or timing. It simply checks for the presence of valid Morse code characters.

        """
        valid_chars = set('.- /')
        for char in morse_text:
            if char not in valid_chars:
                return False
        return True

    @staticmethod
    def analyze_frequency(morse_text):
        """
        Perform frequency analysis on the Morse code message.

        :param morse_text: The Morse code message to be analyzed.
        :return: A dictionary containing the frequency count of each Morse code character.

        Example:
            >>> morse = MorseCode()
            >>> frequency = morse.analyze_frequency('.... . .-.. .-.. --- / .-- --- .-. .-.. -..')
            >>> print(frequency)
            {'.': 4, '-': 6, ' ': 7, '/': 1}

        The `analyze_frequency` method performs frequency analysis on the given Morse code message. It takes a single argument `morse_text` which should be a string representing the Morse code message to be analyzed. The method returns a dictionary containing the frequency count of each Morse code character in the message.

        The method iterates over each character in the Morse code message and updates the frequency count in the dictionary. If a character is already present in the dictionary, its count is incremented by 1. If a character is encountered for the first time, it is added to the dictionary with a count of 1.

        The returned frequency dictionary provides insights into the distribution of Morse code characters in the message, which can be useful for various analyses or visualizations.

        """
        frequency = {}
        for char in morse_text:
            if char in frequency:
                frequency[char] += 1
            else:
                frequency[char] = 1

        return frequency

    @staticmethod
    def visualize_morse_code(morse_text):
        """
        Visualize the Morse code message.

        :param morse_text: The Morse code message to be visualized.
        :return: A string representing the visualization of the Morse code message.

        Example:
            >>> morse = MorseCode()
            >>> visualization = morse.visualize_morse_code('.... . .-.. .-.. --- / .-- --- .-. .-.. -..')
            >>> print(visualization)
            '• • • •   •   •-•-•-   •-•-•-   ---   /   .--   ---   .-.   .-..   ---   ..-   -..'

        The `visualize_morse_code` method converts the given Morse code message into a visual representation. It takes a single argument `morse_text` which should be a string representing the Morse code message to be visualized. The method returns a string representing the visualization of the Morse code message.

        The method iterates over each character in the Morse code message and converts it into a corresponding visual symbol. A dot (.) is represented by '•', a dash (-) is represented by '−', a space is represented by a space character, and a forward slash (/) is represented by a new line character for word spacing.

        The returned visualization provides a visually interpretable representation of the Morse code message, making it easier to understand and analyze.

        """
        visualization = ""
        for char in morse_text:
            if char == '.':
                visualization += '•'  # Dot symbol
            elif char == '-':
                visualization += '−'  # Dash symbol
            elif char == ' ':
                visualization += ' '  # Space symbol
            elif char == '/':
                visualization += '\n'  # New line for word spacing

        return visualization

    @staticmethod
    def calculate_duration(morse_text):
        """
        Calculate the duration of a Morse code message.

        :param morse_text: The Morse code message.
        :return: The duration of the Morse code message in units.

        Example:
            >>> duration = calculate_duration('.... . .-.. .-.. --- / .-- --- .-. .-.. -..')
            >>> print(duration)
            23

        The `calculate_duration` function calculates the duration of a Morse code message. It takes a single argument `morse_text` which should be a string representing the Morse code message. The function returns the duration of the Morse code message in units.

        The function iterates over each character in the Morse code message and adds the corresponding duration to the total duration. A dot (.) has a duration of 1 unit, a dash (-) has a duration of 3 units, a space between characters has a duration of 1 unit, and a space between words has a duration of 7 units.

        The returned duration provides an indication of the overall duration of the Morse code message, which can be useful for timing or synchronization purposes.

        """
        dot_duration = 1  # Duration of a dot (1 unit)
        dash_duration = 3  # Duration of a dash (3 units)
        space_duration = 1  # Duration of a space between characters (1 unit)
        word_space_duration = 7  # Duration of a space between words (7 units)

        duration = 0
        for char in morse_text:
            if char == '.':
                duration += dot_duration
            elif char == '-':
                duration += dash_duration
            elif char == ' ':
                duration += space_duration
            elif char == '/':
                duration += word_space_duration

        return duration

    @staticmethod
    def play_morse_code(morse_text):
        """
        Play Morse code as sound.

        :param morse_text: The Morse code message to be played as sound.

        Example:
            >>> morse = MorseCode()
            >>> morse.play_morse_code('.... . .-.. .-.. --- / .-- --- .-. .-.. -..')

        The `play_morse_code` method plays the given Morse code message as sound. It takes a single argument `morse_text` which should be a string representing the Morse code message to be played.

        The method iterates over each character in the Morse code message. For each dot (.), it plays the sound associated with a dot. For each dash (-), it plays the sound associated with a dash. For any other character, it introduces a pause of 0.5 seconds to create audible gaps between the Morse code elements.

        This method can be used to audibly play Morse code messages, providing a way to listen to and verify Morse code transmissions.

        Note: The implementation of playing the sounds may depend on the specific audio library or platform being used.

        """
        for char in morse_text:
            if char == '.':
                playsound.playsound('dot_sound.wav', True)
            elif char == '-':
                playsound.playsound('dash_sound.wav', True)
            else:
                time.sleep(0.5)  # Pause

