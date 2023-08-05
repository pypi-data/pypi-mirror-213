import pickle


def map_to_category(value, reverse=False):
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
    if not reverse:
        return mappings[value]
    else:
        return mappings_reverse[value]


def load_model():
    """
    usage
    vector_clf, clf = load_model()
    X_test = ['анатом html московск физик техническ институт яндекс e learn develop fund coursera googl chrome']
    y_pred = clf.predict(vector_clf.transform(X_test))
    category = map_to_category(y_pred[0])
    :return:
    """
    with open('./model.pkl', 'rb') as f:
        clf = pickle.load(f)
    with open('./vector.pkl', 'rb') as f:
        vector_clf = pickle.load(f)
    return vector_clf, clf
