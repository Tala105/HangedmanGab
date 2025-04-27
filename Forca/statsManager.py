import os

class StatsManager:
    def __init__(self, category = ("easy", 5)) -> None:
        self.wins = 0
        self.losses = 0
        self.matches = 0
        self.win_percentage = 0.0
        self.loss_percentage = 0.0
        self.category = category
        # Uso de lambda para criar dicionario em uma linha
        self.wins_per_category = {d: {t: 0 for t in range(5, 11)} for d in ["easy", "average", "hard"]}


    def update_category(self, category: str, word_length: int) -> None:
        self.category = (category, word_length)

    def update_stats(self, result) -> None:
        if result == "win":
            self.wins += 1
            self.wins_per_category[self.category[0]][self.category[1]] += 1
        elif result == "loss":
            self.losses += 1
        self.matches = self.wins + self.losses

        self.calculate_percentages()

    def calculate_percentages(self):
        if self.matches > 0:
            self.win_percentage = (self.wins / self.matches) * 100
            self.loss_percentage = (self.losses / self.matches) * 100
        else:
            self.win_percentage = 0.0
            self.loss_percentage = 0.0

    def load_data(self) -> None:
        with open("Estatisticas.txt", "a+", encoding="UTF-8") as file:
            file.seek(0)
            if os.path.getsize("Estatisticas.txt") != 0:
                linhas = file.readlines()
                wins_antigas = int(linhas[0].split("=")[1].strip())
                losses_antigas = int(linhas[1].split("=")[1].strip())
                wins_per_category_antigas = {d: {t: 0 for t in range(5, 11)} for d in ["easy", "average", "hard"]}
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
                wins_per_category_antigas = {d: {t: 0 for t in range(5, 11)} for d in ["easy", "average", "hard"]}
            self.wins = self.wins + wins_antigas
            self.losses = self.losses + losses_antigas
            self.wins_per_category = {
                d: {t: self.wins_per_category[d][t] + wins_per_category_antigas[d][t] for t in range(5, 11)}
                for d in ["easy", "average", "hard"]
            }
            self.matches = self.wins + self.losses

    def save_data(self) -> None:
        self.load_data()
        with open("Estatisticas.txt", "w", encoding="UTF-8") as file2:
            file2.write(f"wins = {self.wins}\n")
            file2.write(f"losses = {self.losses}\n")
            file2.write("wins_per_category:\n")
            for d in ["easy", "average", "hard"]:
                file2.write(f"{d}:\n")
                for t in range(5, 11):
                    total = self.wins_per_category[d][t]
                    file2.write(f"  {t} = {total}\n")
            taxa = (self.wins) / (self.matches) * 100
            file2.write(f"taxa_total = {taxa:.2f}\n")
