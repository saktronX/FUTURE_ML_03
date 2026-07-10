skills = [
    "python","java","c++","c","sql","mysql","postgresql",
    "html","css","javascript","react","node.js","express",
    "mongodb","flask","django","git","github","docker",
    "kubernetes","aws","azure","gcp","linux","excel",
    "power bi","tableau","numpy","pandas","matplotlib",
    "scikit-learn","tensorflow","keras","pytorch",
    "machine learning","deep learning","nlp",
    "data analysis","data science","communication",
    "leadership","problem solving","teamwork","project management"
]


def extract_skills(text):
    if not isinstance(text, str):
        return []

    text = text.lower()

    found = []

    for skill in skills:
        if skill in text:
            found.append(skill)

    return sorted(list(set(found)))