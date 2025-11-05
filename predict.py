import xgboost as xgb
import pandas as pd
import numpy as np
import string

def create_features(command):
    """
    Creates the feature vector for a given command.
    """
    features = {}
    features['command'] = command
    features['num_words'] = len(str(command).split())
    features['mean_word_len'] = np.mean([len(w) for w in str(command).split()])
    features['num_unique_words'] = len(set(str(command).split()))
    features['num_chars'] = len(str(command))
    features['num_words_upper'] = len([w for w in str(command).split() if w.isupper()])
    features['num_punctuations'] = len([c for c in str(command) if c in string.punctuation])

    words = [w for w in command.split(" ")]
    prob = np.unique(words, return_counts=True)[1] / len(words)
    entropy = np.sum(prob**2)
    features['entropy_words'] = np.log(entropy + 0.01)
    features['total_words'] = len(words)
    features['unique_word'] = len(set(words))

    voals = [v for v in command if v in 'aeiou']
    if len(voals) > 0:
        prob = np.unique(voals, return_counts=True)[1] / len(voals)
        entropy = np.sum(prob**2)
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

def predict_command(command_str) :
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

    # Convert to category
    df['command'] = df['command'].astype('category')

    # Create DMatrix
    dmatrix = xgb.DMatrix(df, enable_categorical=True)

    # Predict
    prediction = bst.predict(dmatrix)

    if prediction[0] > 0.5:
        return f"The command \"{command_str}\" is likely bad."
    else:
        return f"The command \"{command_str}\" is likely good."

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        command_to_predict = " ".join(sys.argv[1:])
        predict_command(command_to_predict)
    else:
        print("Please provide a command to predict.")

