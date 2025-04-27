# pylint: skip-file
import random
import os
from numpy import clip
from wordsStates import WordState
from statsManager import StatsManager

with open ('Palavras.txt', 'r', encoding="UTF-8") as f:
    words = f.readlines()

words = [word.strip().lower() for word in words]
dificulties = ["easy", "average", "hard"]
word_state = WordState()
stats_manager = StatsManager()

"""
Fiz uma classe para poder usar variaveis self (contidas na classe) e não ter que passar como parametro
para cada função, assim fica mais fácil de entender e manter o código, não tem que se preocupar com 
diferenças entra variaveis locais e globais.
Todas as variaveis do tipo self.algo estão inclusas no parâmetro self(importa a sí mesma)
"""
class hangedMan:
    def __init__(self):
        self.set_initial_variables()
        self.set_dificulty()

    def set_initial_variables(self) -> None:
        self.hits: list[str] = []
        self.misses: list[str] = []
        self.buffer_string = ""
        
    # Função para escolher a dificulty
    def set_dificulty(self) -> None:
        txt_buffer = "Choose a dificulty level:\n"
        for i, dificulty in enumerate(dificulties):
            txt_buffer += f"{i+1} - {dificulty.capitalize()}\n"
        dificulty = input(txt_buffer)
        # Checa se a dificuldade é valida. Se não for, pede novamente
        while dificulty not in ['1', '2', '3']:
            print("Invalid choice!.\n")
            dificulty = input(txt_buffer)
        self.dificulty = int(dificulty)
        self.set_variables_per_dificulty()

    # Função para difinir as variaveis de acordo com a dificuldade escolhida
    def set_variables_per_dificulty(self) -> None:
        attempts = [10, 7, 5]
        self.attempts = attempts[self.dificulty - 1]
        word = words[clip(len(words),0,int(random.normalvariate(self.dificulty*len(words)//3, self.dificulty*len(words)//8)))]
        word_state.set_word(word)
        print(f"Chosen dificulty level: {dificulties[self.dificulty - 1].capitalize()}\nattempts: {self.attempts}")
        self.correct_guesses = [False] * len(word_state.word)
        stats_manager.update_category(dificulties[self.dificulty - 1], len(word))


    def play(self):
        # Fofidão para iniciar o jogo
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Welcomed to the HangedMan Game!")
        print("Guess the word before the man dies by strangulation!")
        input("Press enter to start...")

        # Loop principal do jogo
        while True:
            while True:
                # Limpa a tela e exibe o estado atual do jogo
                os.system('cls' if os.name == 'nt' else 'clear')
                print(self.buffer_string)
                self.buffer_string = ""
                self.show_word()
                self.show_attempts()
                guess = input("Write your guess: ").strip().lower()

                # Chutou letter 
                if len(guess) == 1:
                    self.guess_letter(guess)
                # Chutou palavra
                elif len(guess) == len(word_state.word):
                    self.guess_word(guess)
                # Chutou errado(Pembou louco)
                else:
                    self.buffer_string = "Invalid Guess! Guess a letter or the entire word."

                # Verifica se o jogador ganhou ou perdeu
                if all(guess in self.hits for guess in word_state.word) or guess == word_state.word:
                    print(f"Congratualtion you guessed the word! '{word_state.word}'.")
                    stats_manager.update_stats("win")
                    break
                if self.attempts == 0:
                    stats_manager.update_stats("loss")
                    print(f"You lost, the word was '{word_state.word}'.")
                    break
            play_again = input("Want to play again? (y/n): ").strip().lower()
            if play_again == 'y':
                self.set_dificulty()
                self.set_initial_variables()
            elif play_again == 'n':
                print("Thanks for Playing!")
                break
            else:
                print("Invalid input, exiting game.")
                break
        stats_manager.save_data()

    # Checa se o chute(letra) está na palavra
    def guess_letter(self, guess:str) -> None:
        if guess in self.hits or guess in self.misses:
            self.buffer_string = "You already guessed that. Try again."
        elif guess in word_state.cleaned_word:
            self.hits.append(guess)
            word_state.update_shown_word(guess)
            self.buffer_string = "You guessed correctly!"
        else:
            self.misses.append(guess)
            self.attempts -= 1
            self.buffer_string = "Wrong guess! You lost a life."

    # Checa se o chute(palavra) está errado, se estiver correto o loop principal cuida
    def guess_word(self, guess:str) -> None:
        if word_state.clean_word(guess) != word_state.cleaned_word:
            self.attempts -= 1
            self.buffer_string = "Wrong guess! You lost a life."
            
    def show_word(self) -> None:
        word_state.show_word()


    def show_attempts(self) -> None:
        print(f"Lives Left: {self.attempts}")
        print(f"Guessed attempted: {', '.join(self.misses + self.hits)}")
    

if __name__ == "__main__":
    jogo = hangedMan()
    jogo.play()