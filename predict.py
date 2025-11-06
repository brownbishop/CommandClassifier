import xgboost as xgb
import pandas as pd
import numpy as np
import string

def create_features(command):
    """
    Creates the feature vector for a given command.
    """
    features = {}
    words = str(command).split()
    num_words = len(words)

    features['num_words'] = num_words
    if num_words > 0:
        features['mean_word_len'] = np.mean([len(w) for w in words])
    else:
        features['mean_word_len'] = 0
    features['num_unique_words'] = len(set(words))
    features['num_chars'] = len(str(command))
    features['num_words_upper'] = len([w for w in words if w.isupper()])
    features['num_punctuations'] = len([c for c in str(command) if c in string.punctuation])

    if num_words > 0:
        prob = np.unique(words, return_counts=True)[1] / num_words
        entropy = np.sum(prob**2)
        features['entropy_words'] = np.log(entropy + 0.01)
    else:
        features['entropy_words'] = 0
    features['total_words'] = num_words
    features['unique_word'] = len(set(words))

    voals = [v for v in command if v in 'aeiou']
    features['total_voals'] = len(voals)
    features['unique_voals'] = len(set(voals))
    if len(voals) > 0:
        prob = np.unique(voals, return_counts=True)[1] / len(voals)
        entropy = np.sum(prob**2)
        features['entropy_voals'] = np.log(entropy + 0.01)
    else:
        features['entropy_voals'] = 0

    cons = [v for v in command if v not in 'aeiou']
    features['total_cons'] = len(cons)
    features['unique_cons'] = len(set(cons))
    if len(cons) > 0:
        prob = np.unique(cons, return_counts=True)[1] / len(cons)
        entropy = np.sum(prob**2)
        features['entropy_cons'] = np.log(entropy + 0.01)
    else:
        features['entropy_cons'] = 0
    
    return features

def predict_command(command_str):
    """
    Predicts if a command is good or bad.
    """
    # Create a Booster
    bst = xgb.Booster()

    # Load the model
    bst.load_model("commands-predictor-model.json")

    # Create features
    features = create_features(command_str)

    # Create a dataframe
    df = pd.DataFrame([features])
    
    feature_columns = [
        'num_words', 'mean_word_len', 'num_unique_words', 'num_chars',
        'num_words_upper', 'num_punctuations', 'entropy_words', 'total_words',
        'unique_word', 'total_voals', 'unique_voals', 'entropy_voals',
        'total_cons', 'unique_cons', 'entropy_cons'
    ]
    df = df[feature_columns]

    # Create DMatrix
    dmatrix = xgb.DMatrix(df)

    # Predict
    prediction = bst.predict(dmatrix)

    if prediction[0] > 0.5:
        return f"The command \"{command_str}\" is likely dangerous."
    else:
        return f"The command \"{command_str}\" is likely harmless."

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        command_to_predict = " ".join(sys.argv[1:])
        out = predict_command(command_to_predict)
        print(out)
    else:
        print("Please provide a command to predict.")