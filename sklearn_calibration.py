import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Step 1: Load the Data
df = pd.read_csv("./data/simple_data.csv")

# Step 2: Preprocess the Data

# Define a function to convert card values to numerical values
def card_to_numeric(card):
    if isinstance(card, str):
        suit = card[0]
        value = card[1:]
        suit_dict = {'S': 1, 'H': 2, 'D': 3, 'C': 4}
        value_dict = {'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}
        if value in value_dict:
            value = value_dict[value]
        else:
            value = int(value)
        return suit_dict[suit] * 100 + value
    elif card is None:
        return 0
    else:
        return card

# Apply the card_to_numeric function to relevant columns
for col in ['hole_card_high', 'hole_card_low', 'community_card_1', 'community_card_2', 'community_card_3', 'community_card_4', 'community_card_5']:
    df[col] = df[col].apply(card_to_numeric)

# Encode categorical variables
le = LabelEncoder()
df['street'] = le.fit_transform(df['street'])
df['action'] = le.fit_transform(df['action'])

# Handle missing values (if any)
df = df.fillna(0)

# Step 3: Feature Engineering
X = df.drop(columns=['action'])
y = df['action']

# Step 4: Model Training
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
decoded_action = le.inverse_transform(y_pred)
print(decoded_action)
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy * 100:.2f}%")

