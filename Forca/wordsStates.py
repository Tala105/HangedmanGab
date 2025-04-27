class WordState:
    def __init__(self, word = ""):
        self.word = word
        self.shown_word = '_' * len(word)
        self.cleaned_word = self.clean_word(word)

    def set_word(self, word: str) -> None:
        self.word = word
        self.cleaned_word = self.clean_word(word)
        self.shown_word = '_' * len(word)

    def clean_word(self, word:str) -> str:
        acentos = {
            'á': 'a', 'ã': 'a', 'â': 'a', 'à': 'a',
            'é': 'e', 'ê': 'e',
            'í': 'i',
            'ó': 'o', 'õ': 'o', 'ô': 'o',
            'ú': 'u',
            'ç': 'c'
        }
        for letter in word:
            if letter in acentos:
                word = word.replace(letter, acentos[letter])
        return word

    def update_shown_word(self, guess: str) -> None:
        self.shown_word = ''.join(
            letter if letter in self.shown_word or letter == guess else '_' for letter in self.word
        )
        

    def show_word(self) -> None:
        print(f"Word: {self.shown_word}")

if __name__ == "__main__":
    word = "orfão"
    word_state = WordState(word)
    print(f"Original word: {word_state.word}")
    print(f"Cleaned word: {word_state.cleaned_word}")
    print(f"Shown word: {word_state.shown_word}")
    word_state.update_shown_word("o")
