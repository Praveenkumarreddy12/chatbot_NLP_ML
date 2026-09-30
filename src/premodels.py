import pandas as pd
import re

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer

def clean_text(text):
    text = text.lower()
    text = re.sub(r"http\S+","",text)
    text = re.sub(r"[^a-zA-z\s]","", text)
    text = re.sub(r"\s", " ", text).strip()

    return text


df = pd.read_csv("customer_support_nlp_dataset.csv")


# print(df.head())
# print(df.shape)
# print(df["intent"].value_counts())

df["text"] = df["text"].apply(clean_text)

df = df.sample(frac=1, random_state=42).reset_index(drop=True)


# Save the shuffled dataset
df.to_csv("customer_support_shuffled.csv", index=False)

# Splitting data into train and test


x_train, x_test, y_train, y_test = train_test_split(df["text"],df["intent"], test_size=0.15, random_state= 42)


# Converting text into numbers

vectorizer = TfidfVectorizer(
    max_features= 5000,
    ngram_range= (1,2)
)

x_train_tfidf = vectorizer.fit_transform(x_train)
x_test_tfidf = vectorizer.transform(x_test)

