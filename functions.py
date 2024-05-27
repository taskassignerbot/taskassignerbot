import json
from gensim.models import Word2Vec
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

with open('employees.json', 'r') as json_file:
    employees = json.load(json_file)
employees_names = employees.keys()
print(employees_names)

def extract_name(text):
    words = text.lower().split()
    for word in words:
        for name in employees_names:
            if name in word:
                return name
    return ''

def define_adressee(name):
    if name in employees_names:
        closest_name = name
    else:
        corpus = [['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', ',']]
        model = Word2Vec(corpus, vector_size=20, window=5, min_count=1, sg=0)
        closest_name = get_closest_name(name, model, employees_names)
        return closest_name


def get_closest_name(target_name, model, names):
    target_vector = get_word_vector(target_name, model)
    print(target_vector)
    similarities = []
    
    for name in names:
        name_vector = get_word_vector(name, model)
        similarity = cosine_similarity([target_vector], [name_vector])[0][0]
        similarities.append((name, similarity))
    
    closest_name = sorted(similarities, key=lambda x: x[1], reverse=True)[0][0]
    print(similarities)
    return closest_name

def get_word_vector(word, model):
    vector = np.zeros(model.vector_size)
    for char in word:
        if char in model.wv:
            vector += model.wv[char]
    return vector / len(word)

def compare_words(word1, word2, model):
    vector1 = get_word_vector(word1, model)
    vector2 = get_word_vector(word2, model)
    similarity = cosine_similarity([vector1], [vector2])[0][0]
    return similarity

# def add_employee(new_employee_name, new_employee_id):
#     employees[new_employee_name] = new_employee_id
#     with open('sentences.json', 'w') as json_file:
#         json.dump(employees, json_file, indent=4)