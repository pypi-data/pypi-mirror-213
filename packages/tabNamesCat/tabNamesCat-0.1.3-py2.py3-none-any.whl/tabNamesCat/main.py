import pickle
import nltk
from nltk.corpus import stopwords
from nltk import stem
from langdetect.detector_factory import DetectorFactory, PROFILES_DIRECTORY
import os
import re


nltk.download('stopwords')
nltk.download('punkt')

stop = stopwords.words('english') + stopwords.words('russian')


def get_factory_for():
    detector = DetectorFactory()
    profiles = []
    for lang in ['en', 'ru']:
        with open(os.path.join(PROFILES_DIRECTORY, lang), 'r', encoding='utf-8') as f:
            profiles.append(f.read())
    detector.load_json_profile(profiles)

    def _detect_langs(text):
        d = detector.create()
        d.append(text)
        return d.get_probabilities()

    def _detect(text):
        d = detector.create()
        d.append(text)
        return d.detect()

    detector.detect_langs = _detect_langs
    detector.detect = _detect
    return detector


stemmer_en = stem.SnowballStemmer('english')
stemmer_ru = stem.SnowballStemmer('russian')
language_detect = get_factory_for()


def stem_word(word):
    try:
        lang = language_detect.detect(word)
        if lang == 'ru':
            return stemmer_ru.stem(word)
        if lang == 'en':
            return stemmer_en.stem(word)
        return word
    except:
        return word


def sentence_clean(sentence):
    sentence = sentence.lower()
    sentence = re.sub("[^a-zA-ZА-Яа-я]", " ", sentence)
    return ' '.join([stem_word(word) for word in sentence.split() if word and word not in stop])


def get_mappings_to_category(reverse=False):
    mappings = {
        2: 'Development',
        6: 'Utilities',
        4: 'Entertainment',
        1: 'Design / Creativity',
        5: 'Management',
        3: 'Education',
        0: 'Communication'
    }
    mappings_reverse = {
        'Development': 2,
        'Utilities': 6,
        'Entertainment': 4,
        'Design / Creativity': 1,
        'Management': 5,
        'Education': 3,
        'Communication': 0
    }
    if reverse:
        return mappings_reverse
    else:
        return mappings


def load_model():
    """
    usage
    vector_clf, clf = load_model()
    X_test = ['анатом html московск физик техническ институт яндекс e learn develop fund coursera googl chrome']
    y_pred = clf.predict(vector_clf.transform(X_test))
    category = map_to_category(y_pred[0])
    :return:
    """
    dir_path = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(dir_path, 'model.pkl'), 'rb') as f:
        clf = pickle.load(f)
    with open(os.path.join(dir_path, 'vector.pkl'), 'rb') as f:
        vector_clf = pickle.load(f)
    return vector_clf, clf
