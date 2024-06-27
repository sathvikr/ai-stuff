import math
import random
import string
import sys

POPULATION_SIZE = 500
NUM_CLONES = 1
TOURNAMENT_SIZE = 20
TOURNAMENT_WIN_PROBABILITY = 0.75
CROSSOVER_LOCATIONS = 5
MUTATION_RATE = 0.8


def translate(string, cipher):
    encoded = ""

    for char in string:
        uppercase = char.upper()
        encoded += cipher[uppercase] if uppercase in cipher else uppercase

    return encoded


def create_cipher(pseudo_cipher, source=string.ascii_uppercase):
    return {char.upper(): pseudo_cipher[i].upper() for i, char in enumerate(source)}


def build_ngrams_dict(filename):
    ngrams_dict = {}

    with open(filename) as f:
        for line in f:
            ngram, frequency = line.split()
            ngrams_dict[ngram] = int(frequency)

    return ngrams_dict


def fitness_function(n, encoded_text, candidate_cipher):
    fitness_score = 0
    decoded_text = translate(encoded_text, create_cipher(string.ascii_uppercase, candidate_cipher))
    # print(decoded_text)

    for i in range(len(decoded_text) - n + 1):
        ngram = decoded_text[i:i + n]

        if ngram.isalpha() and ngram in ngrams_dict:
            fitness_score += math.log(ngrams_dict[ngram], 2)

    return fitness_score


def shuffle(s):
    l = list(s)
    random.shuffle(l)

    return "".join(l)


def swap(s, i, j):
    return s[:i] + s[j] + s[i + 1:j] + s[i] + s[j + 1:]


def random_swap(s):
    i = random.randint(0, len(s) - 1)
    j = random.randint(0, len(s) - 1)

    return s if i == j else swap(s, min(i, j), max(i, j))


def hill_climbing(n, encoded_text):
    candidate_cipher = shuffle(string.ascii_uppercase)
    fitness_score = fitness_function(n, encoded_text, candidate_cipher)

    while True:
        new_cipher = random_swap(candidate_cipher)

        if new_cipher != candidate_cipher:
            new_score = fitness_function(n, encoded_text, new_cipher)

            if new_score > fitness_score:
                candidate_cipher = new_cipher
                fitness_score = new_score


def generate_population():
    considered = set()
    population = []
    count = 0

    while count < POPULATION_SIZE:
        cipher = shuffle(string.ascii_uppercase)

        if cipher not in considered:
            considered.add(cipher)
            population.append(cipher)
            count += 1

    return population


def score_generation(generation, n, encoded_text):
    return {cipher: fitness_function(n, encoded_text, cipher) for cipher in generation}


def select_parent(tournament):
    for cipher in tournament:
        if random.random() < TOURNAMENT_WIN_PROBABILITY:
            return cipher

    return None


def fill_child(child, parent2):
    child_set = set(child)

    for i, letter in enumerate(parent2):
        if letter not in child_set:
            child_set.add(letter)

            for j in range(len(child)):
                if child[j] == "":
                    child[j] = letter
                    break

    return child


def breed(parents):
    crossover_count = 0
    index = random.randint(0, 1)
    parent1, parent2 = parents[index], parents[1 - index]
    child = [""] * len(parent1)

    while crossover_count < CROSSOVER_LOCATIONS:
        random_index = random.randint(0, len(child) - 1)

        if child[random_index] == "":
            child[random_index] = parent1[random_index]
            crossover_count += 1

    child = "".join(fill_child(child, parent2))

    if random.random() < MUTATION_RATE:
        child = random_swap(child)

    return "".join(fill_child(child, parent2))


def selection(current_generation, n, encoded_text):
    scored_generation = score_generation(current_generation, n, encoded_text)
    ranked_generation = sorted(current_generation, key=lambda cipher: -scored_generation[cipher])
    next_generation = ranked_generation[:NUM_CLONES]

    print(translate(encoded_text, create_cipher(string.ascii_uppercase, ranked_generation[0])))

    while len(next_generation) < POPULATION_SIZE:
        distinct_ciphers = random.sample(ranked_generation, 2 * TOURNAMENT_SIZE)
        tournaments = distinct_ciphers[:len(distinct_ciphers) // 2], distinct_ciphers[len(distinct_ciphers) // 2:]
        tournaments = sorted(tournaments[0], key=lambda cipher: -scored_generation[cipher]), \
                      sorted(tournaments[1], key=lambda cipher: -scored_generation[cipher])

        parents = select_parent(tournaments[0]), select_parent(tournaments[1])
        next_generation.append(breed(parents))

    return next_generation


def genetic_algorithm(n, encoded_text):
    population = generate_population()
    count = 0

    while count < 500:
        print("Generation:", count)
        population = selection(population, n, encoded_text)

        count += 1


# encoded_text = """PF HACYHTTRQ VF N PBYYRPGVBA PF HACYHTTRQ VF N PBYYRPGVBA PF HACYHTTRQ VF N PBYYRPGVBA PF HACYHTTRQ VF N PBYYRPGVBA PF HACYHTTRQ VF N PBYYRPGVBA PF HACYHTTRQ VF N PBYYRPGVBA PF HACYHTTRQ VF N PBYYRPGVBA PF HACYHTTRQ VF N PBYYRPGVBA PF HACYHTTRQ VF N PBYYRPGVBA PF HACYHTTRQ VF N PF HACYHTTRQ VF N PBYYRPGVBA PF HACYHTTRQ VF N PBYYRPGVBA PF HACYHTTRQ VF N PBYYRPGVBA PF HACYHTTRQ VF N PBYYRPGVBA PF HACYHTTRQ VF N PF HACYHTTRQ VF N PBYYRPGVBA PF HACYHTTRQ VF N PBYYRPGVBA PF HACYHTTRQ VF N PBYYRPGVBA PF HACYHTTRQ VF N PBYYRPGVBA PF HACYHTTRQ VF N PF HACYHTTRQ VF N PBYYRPGVBA PF HACYHTTRQ VF N PBYYRPGVBA PF HACYHTTRQ VF N PBYYRPGVBA PF HACYHTTRQ VF N PBYYRPGVBA PF HACYHTTRQ VF N PF HACYHTTRQ VF N PBYYRPGVBA PF HACYHTTRQ VF N PBYYRPGVBA PF HACYHTTRQ VF N PBYYRPGVBA PF HACYHTTRQ VF N PBYYRPGVBA PF HACYHTTRQ VF N PF HACYHTTRQ VF N PBYYRPGVBA PF HACYHTTRQ VF N PBYYRPGVBA PF HACYHTTRQ VF N PBYYRPGVBA PF HACYHTTRQ VF N PBYYRPGVBA PF HACYHTTRQ VF N PF HACYHTTRQ VF N PBYYRPGVBA PF HACYHTTRQ VF N PBYYRPGVBA PF HACYHTTRQ VF N PBYYRPGVBA PF HACYHTTRQ VF N PBYYRPGVBA PF HACYHTTRQ VF N PF HACYHTTRQ VF N PBYYRPGVBA PF HACYHTTRQ VF N PBYYRPGVBA PF HACYHTTRQ VF N PBYYRPGVBA PF HACYHTTRQ VF N PBYYRPGVBA PF HACYHTTRQ VF N"""
encoded_text = """PF HACYHTTRQ VF N PBYYRPGVBA BS SERR YRNEAVAT NPGVIVGVRF GUNG GRNPU PBZCHGRE FPVRAPR GUEBHTU RATNTVAT
TNZRF NAQ CHMMYRF GUNG HFR PNEQF, FGEVAT, PENLBAF NAQ YBGF BS EHAAVAT NEBHAQ. JR BEVTVANYYL QRIRYBCRQ
GUVF FB GUNG LBHAT FGHQRAGF PBHYQ QVIR URNQ-SVEFG VAGB PBZCHGRE FPVRAPR, RKCREVRAPVAT GUR XVAQF BS
DHRFGVBAF NAQ PUNYYRATRF GUNG PBZCHGRE FPVRAGVFGF RKCREVRAPR, OHG JVGUBHG UNIVAT GB YRNEA CEBTENZZVAT
SVEFG. GUR PBYYRPGVBA JNF BEVTVANYYL VAGRAQRQ NF N ERFBHEPR SBE BHGERNPU NAQ RKGRAFVBA, OHG JVGU GUR
NQBCGVBA BS PBZCHGVAT NAQ PBZCHGNGVBANY GUVAXVAT VAGB ZNAL PYNFFEBBZF NEBHAQ GUR JBEYQ, VG VF ABJ JVQRYL
HFRQ SBE GRNPUVAT. GUR ZNGREVNY UNF ORRA HFRQ VA ZNAL PBAGRKGF BHGFVQR GUR PYNFFEBBZ NF JRYY, VAPYHQVAT
FPVRAPR FUBJF, GNYXF SBE FRAVBE PVGVMRAF, NAQ FCRPVNY RIRAGF. GUNAXF GB TRAREBHF FCBAFBEFUVCF JR UNIR
ORRA NOYR GB PERNGR NFFBPVNGRQ ERFBHEPRF FHPU NF GUR IVQRBF, JUVPU NER VAGRAQRQ GB URYC GRNPUREF FRR UBJ
GUR NPGVIVGVRF JBEX (CYRNFR QBA'G FUBJ GURZ GB LBHE PYNFFRF – YRG GURZ RKCREVRAPR GUR NPGVIVGVRF
GURZFRYIRF!). NYY BS GUR NPGVIVGVRF GUNG JR CEBIVQR NER BCRA FBHEPR – GURL NER ERYRNFRQ HAQRE N PERNGVIR
PBZZBAF NGGEVOHGVBA-FUNERNYVXR YVPRAPR, FB LBH PNA PBCL, FUNER NAQ ZBQVSL GUR ZNGREVNY. SBE NA
RKCYNANGVBA BA GUR PBAARPGVBAF ORGJRRA PF HACYHTTRQ NAQ PBZCHGNGVBANY GUVAXVAT FXVYYF, FRR BHE
PBZCHGNGVBANY GUVAXVAT NAQ PF HACYHTTRQ CNTR. GB IVRJ GUR GRNZ BS PBAGEVOHGBEF JUB JBEX BA GUVF
CEBWRPG, FRR BHE CRBCYR CNTR. SBE QRGNVYF BA UBJ GB PBAGNPG HF, FRR BHE PBAGNPG HF CNTR. SBE ZBER
VASBEZNGVBA NOBHG GUR CEVAPVCYRF ORUVAQ PF HACYHTTRQ, FRR BHE CEVAPVCYRF CNTR."""
# encoded_text = """WZQY XZINYLQPL LPQNYPN LZPQNKR"""
ngrams_dict = build_ngrams_dict("ngrams.txt")
# genetic_algorithm(3, encoded_text)
genetic_algorithm(3, encoded_text)
