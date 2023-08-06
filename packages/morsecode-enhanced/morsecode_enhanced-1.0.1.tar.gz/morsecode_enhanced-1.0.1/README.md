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
from morsecode_enhanced import encode

encoded_message = encode('Hello, World!')
print(encoded_message)

```

Output:
```text
.... . .-.. .-.. --- --..-- / .-- --- .-. .-.. -.. -.-.--
```

## Decoding

To decode Morse code into text, you can use the decode function:

```python
from morsecode_enhanced import decode

decoded_message = decode('.... . .-.. .-.. --- --..-- / .-- --- .-. .-.. -.. -.-.--')
print(decoded_message)

```

Output:
```text
HELLO, WORLD!
```
# Contributing

Contributions are welcome! If you find any issues or have suggestions for improvement, please open an issue or submit a pull request on [GitHub](https://github.com/danysrour/MorseCode).

# License

This project is licensed under the [MIT License](https://github.com/danysrour/morsecodeplus.git)

```text

You can now copy this code and use it as your README.md file.
```