import numpy as np
from collections import defaultdict
import random
import re

class NaiveBayesClassifier:
    def __init__(self, alpha=1.0):
        self.alpha = alpha
        self.classes = None
        self.feature_probs = {}
        self.class_probs = {}

    def fit(self, X, y):
        X = np.array(X)
        y = np.array(y)
        self.classes, class_counts = np.unique(y, return_counts=True)
        total_samples = len(y)
        
        for cls, count in zip(self.classes, class_counts):
            self.class_probs[cls] = np.log(count / total_samples)
        
        for i in range(X.shape[1]):
            for cls in self.classes:
                count = X[y == cls, i].sum() + self.alpha
                total_cls_features = np.sum(X[y == cls]) + self.alpha * X.shape[1]
                prob = np.log(count / total_cls_features)
                self.feature_probs.setdefault(cls, {})[i] = prob

    def predict(self, X):
        predictions = []
        for sample in X:
            max_log_prob = -np.inf
            best_class = None
            for cls in self.classes:
                log_prob = self.class_probs[cls]
                for i, exists in enumerate(sample):
                    if exists == 1:
                        log_prob += self.feature_probs[cls][i]
                if log_prob > max_log_prob:
                    max_log_prob = log_prob
                    best_class = cls
            predictions.append(best_class)
        return predictions

def text_to_features(text_list, feature_words):
    X = []
    for text in text_list:
        features = [0] * len(feature_words)
        for i, word in enumerate(feature_words):
            if re.search(r'\b' + re.escape(word) + r'\b', text):
                features[i] = 1
        X.append(features)
    return X

def generate_dataset(n_samples=500):
    feature_words = ["eval", "exec", "rm -rf", "os.system", "subprocess.call"]
    danger_patterns = [
        "{}('print(1)')", "{}('rm -rf /')", "{}('sys.exit(1)')"
    ]
    safe_patterns = [
        "print('Hello')", "x = 5", "for i in range(10): print(i)",
        "def foo(): return 1", "if x > 0: y = 1"
    ]
    
    X_text = []
    y = []
    for _ in range(n_samples // 2):
        keyword = random.choice(feature_words)
        pattern = random.choice(danger_patterns)
        code = pattern.format(keyword)
        X_text.append(code)
        y.append(1)
    for _ in range(n_samples // 2):
        code = random.choice(safe_patterns)
        X_text.append(code)
        y.append(0)

    combined = list(zip(X_text, y))
    random.shuffle(combined)
    X_text, y = zip(*combined)
    return list(X_text), list(y), feature_words

if __name__ == "__main__":
    X_text_train, y_train, feature_words = generate_dataset(500)
    X_train = text_to_features(X_text_train, feature_words)
    nb = NaiveBayesClassifier(alpha=1.0)
    nb.fit(X_train, y_train)

    X_text_test = [
        "eval('print(1)')",
        "for i in range(5): print(i)",
        "os.system('rm -rf /')",
        "x = 10"
    ]
    X_test = text_to_features(X_text_test, feature_words)
    
    predictions = nb.predict(X_test)
    print(f"测试样本: {X_text_test}")
    print(f"预测结果: {predictions}")
    print("\n先验概率(对数):", nb.class_probs)