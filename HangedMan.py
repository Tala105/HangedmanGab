# pylint: skip-file
import random
import os
from numpy import clip

with open ('Palavras.txt', 'r', encoding="UTF-8") as f:
    words = f.readlines()
words = [word.strip().lower() for word in words]
dificulties = ["easy", "average", "hard"]

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
        # Uso de lambda para criar dicionario em uma linha
        self.wins_per_category = {d: {t: 0 for t in range(5, 11)} for d in dificulties}
        self.wins = self.losses = self.matches = 0

    def set_initial_variables(self) -> None:
        self.hits: list[str] = []
        self.misses: list[str] = []
        self.buffer_string = ""
        
    # Função para escolher a dificulty
    def set_dificulty(self) -> None:
        txt_buffer = "Escolha a dificulty:\n"
        for i, dificulty in enumerate(dificulties):
            txt_buffer += f"{i+1} - {dificulty.capitalize()}\n"
        dificulty = input(txt_buffer)
        while dificulty not in ['1', '2', '3']:
            print("Invalid dificulty!.\n")
            dificulty = input(txt_buffer)
        self.dificulty = int(dificulty)
        self.set_variables_per_dificulty()

    # Função para difinir as variaveis de acordo com a dificuldade escolhida
    def set_variables_per_dificulty(self) -> None:
        attempts = [10, 7, 5]
        self.attempts = attempts[self.dificulty - 1]
        self.word = words[clip(len(words),0,int(random.normalvariate(self.dificulty*len(words)//3, self.dificulty*len(words)//8)))]
        print(f"Chosen dificulty level: {dificulties[self.dificulty - 1].capitalize()}\nattempts: {self.attempts}")
        self.cleaned_word = self.clean_word(self.word)
        self.shown_word = '_' * len(self.word)
        self.acertos = [False] * len(self.word)
        self.category = (dificulties[self.dificulty - 1], len(self.word))


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
                self.show_worda()
                self.show_attempts()
                guess = input("Write your guess: ").strip().lower()

                # Chutou letra 
                if len(guess) == 1:
                    self.guess_letter(guess)
                # Chutou palavra
                elif len(guess) == len(self.word):
                    self.guess_word(guess)
                # Chutou errado(Pembou louco)
                else:
                    self.buffer_string = "Invalid Guess! Guess a letter or the entire word."

                # Verifica se o jogador ganhou ou perdeu
                if all(guess in self.hits for guess in self.word) or guess == self.word:
                    print(f"Congratualtion you guessed the word! '{self.word}'.")
                    self.wins += 1
                    self.wins_per_category[self.category[0]][self.category[1]] += 1
                    break
                if self.attempts == 0:
                    print(f"You lost, the word was '{self.word}'.")
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
        save_data(self)

    # Checa se o guess(letra) está na palavra
    def guess_letter(self, guess:str) -> None:
        if guess in self.hits or guess in self.misses:
            self.buffer_string = "You already guessed that. Try again."
        
        elif guess in self.cleaned_word:
                self.hits.append(guess)
                self.acertos = [True if letra in self.hits else False for letra in self.word]
                self.shown_word = ''.join([letra if acerto else '_' for letra, acerto in zip(self.word, self.acertos)])
                self.buffer_string = "You guessed correctly!"
        else:
            self.misses.append(guess)
            self.attempts -= 1
            self.buffer_string = "Wrong guess! You lost a life."

    # Checa se o guess(palavra) está errado, se estiver correto o loop principal cuida
    def guess_word(self, guess:str) -> None:
        if self.clean_word(guess) != self.cleaned_word:
            self.attempts -= 1
            self.buffer_string = "Wrong guess! You lost a life."
        
    def show_worda(self) -> None:
        print(f"Word: {self.shown_word}")

    def show_attempts(self) -> None:
        print(f"Lives Left: {self.attempts}")
        print(f"Guessed attempted: {', '.join(self.misses + self.hits)}")

    # Retira os acentos/caracteres estranhos da palavra
    def clean_word(self, guesss:str) -> str:
        acentos = {
            'á': 'a', 'ã': 'a', 'â': 'a', 'à': 'a',
            'é': 'e', 'ê': 'e',
            'í': 'i',
            'ó': 'o', 'õ': 'o', 'ô': 'o',
            'ú': 'u',
            'ç': 'c'
        }
        for guess in guesss:
            if guess in acentos:
                guesss[guesss.index(guess)] = acentos[guess]
        return guesss
    
def save_data(jogo: hangedMan) -> None:
    with open("Estatisticas.txt", "a+", encoding="UTF-8") as file2: #13(Long-Lasting Stats)
        file2.seek(0)
        if os.path.getsize("Estatisticas.txt") != 0:
            linhas = file2.readlines()
            wins_antigas = int(linhas[0].split("=")[1].strip())
            losses_antigas = int(linhas[1].split("=")[1].strip())
            wins_per_category_antigas = {d: {t: 0 for t in range(5, 11)} for d in ["easy", "average", "hard"]} #Cancerização Absurda
            i = 3
            for d in ["easy", "average", "hard"]:
                i += 1
                for t in range(5, 11):
                    linha = linhas[i].strip()
                    v = int(linha.split("=")[1].strip())
                    wins_per_category_antigas[d][t] = v
                    i += 1
        else:
            wins_antigas = 0
            losses_antigas = 0
            wins_per_category_antigas = {d: {t: 0 for t in range(5, 11)} for d in ["easy", "average", "hard"]} #O mesmo poderia ser feito para losses

        file2.truncate(0)  # Limpa o conteúdo do arquivo antes de escrever novamente
        wins = jogo.wins + wins_antigas
        losses = jogo.losses + losses_antigas
        matches = wins + losses
        file2.write(f"wins = {wins}\n")
        file2.write(f"losses = {losses}\n")
        file2.write("wins_per_category:\n")
        for d in ["easy", "average", "hard"]:
            file2.write(f"{d}:\n")
            for t in range(5, 11):
                total = jogo.wins_per_category[d][t] + wins_per_category_antigas[d][t]
                file2.write(f"  {t} = {total}\n")
        taxa = (wins) / (matches) * 100
        file2.write(f"taxa_total = {taxa:.2f}\n")

if __name__ == "__main__":
    jogo = hangedMan()
    jogo.play()