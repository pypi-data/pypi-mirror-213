# MorseCodeEnhanced

MorseCodePlus is a Python package that provides functionality for encoding and decoding Morse code.

## Installation

You can install MorseCodePlus using pip:

```shell
pip install morsecode_enhanced
```
 
# Usage

## Encoding

To encode text into Morse code, you can use the encode function:

```python
from morsecode_enhanced import MorseCode

mc = MorseCode()
encoded_word = mc.encode_word('Hello, World!')
print(encodex_word)


```

Output:
```text
.... . .-.. .-.. --- --..-- / .-- --- .-. .-.. -.. -.-.--
```

## Decoding

To decode Morse code into text, you can use the decode function:

```python
from morsecode_enhanced import MorseCode

mc = MorseCode()
decoded_message = mc.decode('.... . .-.. .-.. --- --..-- / .-- --- .-. .-.. -.. -.-.--')
print(decoded_message)

```

Output:
```text
HELLO, WORLD!
```

# More Functionalities

```python
from morsecode_enhanced import MorseCode

mc = MorseCode()
encoded_word = mc.encode_word('Hello')
print(encoded_word)

decoded_word = mc.decode_word('.-..')
print(decoded_word)

random_morse = mc.generate_random_morse(10)

is_valid_morse = mc.is_valid_morse_code(encoded_word)

analyzed = mc.analyze_frequency('.-..')

visualised = mc.visualize_morse_code('.-..')

duration = mc.calculate_duration('.-..')



```

# Contributing

Contributions are welcome! If you find any issues or have suggestions for improvement, please open an issue or submit a pull request on [GitHub](https://github.com/danysrour/MorseCode).

# License

This project is licensed under the [MIT License](https://github.com/danysrour/morsecodeplus.git)

```text

You can now copy this code and use it as your README.md file.
```