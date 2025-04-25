import random
import os

with open ('Palavras.txt', 'r') as f:
    palavras = f.readlines()
palavras = [palavra.strip().lower() for palavra in palavras]
dificuldades = ["fácil", "médio", "difícil"]

"""
Fiz uma classe para poder usar variaveis self (contidas na classe) e não ter que passar como parametro
para cada função, assim fica mais fácil de entender e manter o código, não tem que se preocupar com 
diferenças entra variaveis locais e globais.
Todas as variaveis do tipo self.algo estão inclusas no parâmetro self(importa a sí mesma)
"""
class hangedMan:
    def __init__(self):
        self.chutes_acertados = []
        self.chutes_errados = []
        self.set_dificuldade()
        self.buffer_string = ""

    # Função para escolher a dificuldade
    def set_dificuldade(self) -> int:
        txt_buffer = "Escolha a dificuldade:\n"
        for i, dificuldade in enumerate(dificuldades):
            txt_buffer += f"{i+1} - {dificuldade.capitalize()}\n"
        dificuldade = input(txt_buffer)
        while dificuldade not in ['1', '2', '3']:
            print("Dificuldade inválida!.")
            dificuldade = input(txt_buffer)
        self.dificuldade = int(dificuldade)
        self.set_variaveis_por_dificuldade()

    # Função para difinir as variaveis de acordo com a dificuldade escolhida
    def set_variaveis_por_dificuldade(self) -> None:
        tentativas = [10, 7, 5]
        self.tentativas = tentativas[self.dificuldade - 1]
        self.palavra = palavras[int(random.normalvariate(self.dificuldade*len(palavras)//3, 1))]
        self.palavra_clean = self.retirar_acentos(self.palavra)
        self.palavra_exibida = '_' * len(self.palavra)
        self.acertos = [False] * len(self.palavra)
        print(f"Dificuldade escolhida: {dificuldades[self.dificuldade - 1].capitalize()}\nTentativas: {self.tentativas}")


    def jogar(self):
        # Fofidão para iniciar o jogo
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Bem-vindo ao Jogo da Forca!")
        print("Adivinhe a palavra!")
        input("Pressione Enter para começar...")

        # Loop principal do jogo
        while True:
            # Limpa a tela e exibe o estado atual do jogo
            os.system('cls' if os.name == 'nt' else 'clear')
            print(self.buffer_string)
            self.buffer_string = ""
            self.exibir_palavra()
            self.exibir_tentativas()
            chute = input("Digite uma chute: ").strip().lower()

            # Chutou letra 
            if len(chute) == 1:
                self.chutar_letra(chute)
            # Chutou palavra
            elif len(chute) == len(self.palavra):
                self.chutar_palavra(chute)
            # Chutou errado(Pembou louco)
            else:
                self.buffer_string = "Chute inválido! Chute uma letra ou a palavra completa."

            # Verifica se o jogador ganhou ou perdeu
            if all(chute in self.chutes_acertados for chute in self.palavra) or chute == self.palavra:
                print(f"Parabéns! Você acertou a palavra '{self.palavra}'.")
                break
            if self.tentativas == 0:
                print(f"Você perdeu! A palavra era '{self.palavra}'.")
                break

    # Checa se o chute(letra) está na palavra
    def chutar_letra(self, chute:str) -> None:
        if chute in self.chutes_acertados or chute in self.chutes_errados:
            self.buffer_string = "Você já tentou essa chute. Tente outro."
        
        elif chute in self.palavra_clean:
                self.chutes_acertados.append(chute)
                self.acertos = [True if letra in self.chutes_acertados else False for letra in self.palavra]
                self.palavra_exibida = ''.join([letra if acerto else '_' for letra, acerto in zip(self.palavra, self.acertos)])
                self.buffer_string = "Você acertou um chute!"
        else:
            self.chutes_errados.append(chute)
            self.tentativas -= 1
            self.buffer_string = "Chute errado! Você perdeu uma tentativa."

    # Checa se o chute(palavra) está errado, se estiver correto o loop principal cuida
    def chutar_palavra(self, chute:str) -> None:
        if self.retirar_acentos(chute) != self.palavra_clean:
            self.tentativas -= 1
            self.buffer_string = "Chute errado! Você perdeu uma tentativa."
        
    def exibir_palavra(self) -> None:
        print(f"Palavra: {self.palavra_exibida}")

    def exibir_tentativas(self) -> None:
        print(f"Tentativas restantes: {self.tentativas}")
        print(f"chutes Tentadas: {', '.join(self.chutes_errados + self.chutes_acertados)}")

    # Retira os acentos/caracteres estranhos da palavra
    def retirar_acentos(self, chutes:str) -> str:
        acentos = {
            'á': 'a', 'ã': 'a', 'â': 'a', 'à': 'a',
            'é': 'e', 'ê': 'e',
            'í': 'i',
            'ó': 'o', 'õ': 'o', 'ô': 'o',
            'ú': 'u',
            'ç': 'c'
        }
        for chute in chutes:
            if chute in acentos:
                chutes[chutes.index(chute)] = acentos[chute]
        return chutes

if __name__ == "__main__":
    jogo = hangedMan()
    jogo.jogar()