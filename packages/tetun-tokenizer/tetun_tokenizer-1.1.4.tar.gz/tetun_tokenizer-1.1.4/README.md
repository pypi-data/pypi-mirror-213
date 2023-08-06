### Tetun Tokenizer

Tetun tokenizer is a Python package used to tokenize an input text into tokens. There are several tokenization techniques we built alongside this package as follows:
1. `TetunStandardTokenizer`: tokenizes the input text into individual tokens based on word boundaries, punctuations, and special characters.
2. `TetunWhiteSpaceTokenizer`: tokenizer: breaks the input text into tokens using whitespace as the delimiter.
3. `TetunSentenceTokenizer`: splits sentences by  its ending delimiters such as period (.), question mark (?), and exclamation mark (!). The period used to represent titles, such as Dr., P.hD., etc., are preserved.
4. `TetunBlankLineTokenizer`: segments the input text based on the presence of blank lines.
5. `TetunSimpleTokenizer`: extracts only strings and numbers from the input text while discarding punctuations and special characters.
6. `TetunWordTokenizer`: extracts only word units from the input text and excludes numbers, punctuation, and special characters.

### Installation

With pip:

```
pip install tetun-tokenizer
```

### Usage

To use the Tetun tokenizer, from the tokenizer module on the Tetun tokenizer package, import a tokenizer feature/class.
The examples of its usage are as follows:

1. Using  `TetunStandardTokenizer` to tokenize the input text.

```python
from tetuntokenizer.tokenizer import TetunStandardTokenizer

tetun_tokenizer = TetunStandardTokenizer()

text = "Ha'u mak ita-nia maluk di'ak. Ha'u iha $0.25 atu fó ba ita."
output = tetun_tokenizer.tokenize(text)
print(output)
```

This will be the output:

```
["Ha'u", 'mak', 'ita-nia', 'maluk', "di'ak", '.', "Ha'u", 'iha', '$', '0.25', 'atu', 'fó', 'ba', 'ita', '.']
```

2. Using `TetunWhiteSpaceTokenizer` to tokenize the input text.

```python
from tetuntokenizer.tokenizer import TetunWhiteSpaceTokenizer

tetun_tokenizer = TetunWhiteSpaceTokenizer()

text = "Ha'u mak ita-nia maluk di'ak. Ha'u iha $0.25 atu fó ba ita."
output = tetun_tokenizer.tokenize(text)
print(output)
```

This will be the output:

```
["Ha'u", 'mak', 'ita-nia', 'maluk', "di'ak.", "Ha'u", 'iha', '$0.25', 'atu', 'fó', 'ba', 'ita.']
```

3. Using `TetunSentenceTokenizer` to tokenize the input text.

```python
from tetuntokenizer.tokenizer import TetunSentenceTokenizer

tetun_tokenizer = TetunSentenceTokenizer()

text = "Ha'u ema-ida ne'ebé baibain de'it. Tebes ga? Ita-nia maluk Dr. ka Ph.D sira hosi U.S.A mós dehan!"
output = tetun_tokenizer.tokenize(text)
print(output)
```

This will be the output:

```
["Ha'u ema-ida ne'ebé baibain de'it.", 'Tebes ga?', 'Ita-nia maluk Dr. ka Ph.D sira hosi U.S.A mós dehan!']
```

4. Using `TetunBlankLineTokenizer` to tokenize the input text.

```python
from tetuntokenizer.tokenizer import TetunBlankLineTokenizer

tetun_tokenizer = TetunBlankLineTokenizer()

text = """
        Ha'u mak ita-nia maluk di'ak.
        Ha'u iha $0.25 atu fó ba ita.
        """
output = tetun_tokenizer.tokenize(text)
print(output)
```

This will be the output:

```
["\n            Ha'u mak ita-nia maluk di'ak.\n            Ha'u iha $0.25 atu fó ba ita.\n            "]
```

5. Using `TetunSimpleTokenizer` to tokenize a given text.

```python
from tetuntokenizer.tokenizer import TetunSimpleTokenizer

tetun_tokenizer = TetunSimpleTokenizer()

text = "Ha'u mak ita-nia maluk di'ak. Ha'u iha $0.25 atu fó ba ita."
output = tetun_tokenizer.tokenize(text)
print(output)
```

This will be the output:

```
["Ha'u", 'mak', 'ita-nia', 'maluk', "di'ak", "Ha'u", 'iha', '0.25', 'atu', 'fó', 'ba', 'ita']
```

6. Using `TetunWordTokenizer` to tokenize the input text.

```python
from tetuntokenizer.tokenizer import TetunWordTokenizer

tetun_tokenizer = TetunWordTokenizer()

text = "Ha'u mak ita-nia maluk di'ak. Ha'u iha $0.25 atu fó ba ita."
output = tetun_tokenizer.tokenize(text)
print(output)
```

This will be the output:

```
["Ha'u", 'mak', 'ita-nia', 'maluk', "di'ak", "Ha'u", 'iha', 'atu', 'fó', 'ba', 'ita']
```

To print the resulting output in the console, with each element on a new line, you can use simply use `join()` as follows:

```
print('\n'.join(output))
```

The output will be:

```
Ha'u
mak
ita-nia
maluk
di'ak
Ha'u
iha
atu
fó
ba
ita
```

You can also use the tokenizer to tokenize a text from a file. Here is an example:

```python
# Assume that we use Path instead of a string for the file path
from pathlib import Path
from tetuntokenizer.tokenizer import TetunSimpleTokenizer


file_path = Path("myfile/example.txt")

try:
    with file_path.open('r', encoding='utf-8') as f:
    contents = [line.strip() for line in f]
except FileNotFoundError:
    print(f"File not found at: {file_path}")

# You can also lowercase the contents before tokenizing them.
lowercase_contents = contents.lower()

tetun_tokenizer = TetunSimpleTokenizer()

output = '\n'.join(tetun_tokenizer.tokenize(str(lowercase_contents)))
print(output)

```

This is the example of the output:

```
ha'u
orgullu
dezenvolve
ha'u-nia
lian
tetun 
...
```

For the source code, visit the [GitHub repository](https://github.com/borulilitimornews/tetun-tokenizer) for this project.
