

"""
Kullanıcıdan bir kelime listesi alın ve içlerinde en uzun anagram çiftini bulun. 
(Anagram, harfleri aynı ancak sıralaması farklı kelimelerdir.) 
Örnek: Girdi: ["kedi", "dike", "elmas", "selam", "test", "stet", "masa"] 
Çıktı: ["elma", "alem"] (Çünkü her ikisi de aynı harflerden oluşuyor.)

 Girdi: ["kedi", "dike", "elmas", "selam", "test", "stet", "masa"]
Çıktı: ["elmas", "selam"]

 Girdi: ["kedi", "dike", "elmas", "test", "stet", "masa","selam"]

 temel python sınıfları hariç hazır paketler kullanamak yasak
 for if class fonksiyon listeler kullanılabilir
"""

class LongestAnagramFinder:
    def __init__(self, liste):
        self.liste = liste        

    def anagram(self):
        anagramlar = []
        for i in range(len(self.liste)):
            for j in range(i+1, len(self.liste)):
                if (sorted(self.liste[i]) == sorted(self.liste[j])):
                    anagramlar.append([self.liste[i], self.liste[j]])
                print(sorted(self.liste[i]) , sorted(self.liste[j]))
        return anagramlar

    def longest_pair(self):
        anagramlar = self.anagram()
        max_len = 0
        max_pair = []
        for i in anagramlar:
            if len(i[0]) > max_len:
                max_len = len(i[0])
                max_pair = i
        return max_pair
    

liste = ["kedi", "dike", "eelmas", "selam", "test", "stet", "masa"]
anagram = LongestAnagramFinder(liste)
print(anagram.longest_pair())  # ['elmas', 'selam']



