import os
import sys
import threading
import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox
import joblib
import pandas as pd

# ---- Auto install required packages ----
REQUIRED_PACKAGES = ["transformers", "torch", "sklearn", "tkintertable"]
import subprocess
import importlib

for pkg in REQUIRED_PACKAGES:
    try:
        importlib.import_module(pkg)
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])

from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# ---- Cache directories ----
CACHE_DIR = "cached_models"
os.makedirs(CACHE_DIR, exist_ok=True)

LR_MODEL_PATH = os.path.join(CACHE_DIR, "lr_model.pkl")
VEC_PATH = os.path.join(CACHE_DIR, "tfidf_vectorizer.pkl")
BERT_MODEL_NAME = "distilbert-base-uncased-finetuned-sst-2-english"
BERT_DIR = os.path.join(CACHE_DIR, "bert_model")


# ---- Lightweight Model Loader (TF-IDF + LogisticRegression placeholder) ----
def load_lightweight_model():
    # If not already trained, train on a tiny fake dataset (placeholder)
    if not os.path.exists(LR_MODEL_PATH) or not os.path.exists(VEC_PATH):
        print("Training lightweight model (placeholder quick train)...")
        texts = [
            "Congratulations! You won a prize",
            "Your account has been hacked",
            "Meeting scheduled at 10 AM",
            "Lunch with team tomorrow",
        ]
        labels = [1, 1, 0, 0]  # 1=phishing/spam, 0=legit

        vec = TfidfVectorizer()
        X = vec.fit_transform(texts)
        model = LogisticRegression()
        model.fit(X, labels)

        joblib.dump(model, LR_MODEL_PATH)
        joblib.dump(vec, VEC_PATH)
    else:
        print("Loading cached lightweight model...")

    model = joblib.load(LR_MODEL_PATH)
    vec = joblib.load(VEC_PATH)
    return vec, model

# ---- BERT Model Loader ----
def load_bert_model():
    if not os.path.exists(BERT_DIR):
        print("Downloading BERT model (first run)...")
    tokenizer = AutoTokenizer.from_pretrained(BERT_MODEL_NAME, cache_dir=BERT_DIR)
    model = AutoModelForSequenceClassification.from_pretrained(BERT_MODEL_NAME, cache_dir=BERT_DIR)
    clf = pipeline("text-classification", model=model, tokenizer=tokenizer)
    return clf

# ---- Prediction functions ----
def predict_lr(text, vec, model):
    X = vec.transform([text])
    pred = model.predict(X)[0]
    return "Phishing" if pred == 1 else "Legit"

def predict_bert(text, bert_pipeline):
    result = bert_pipeline(text[:512])[0]  # truncate long text
    # convert positive/negative to phishing/legit for demo
    label = result['label']
    return "Phishing" if label.upper() == "POSITIVE" else "Legit"

# ---- GUI Application ----
class EmailClassifierGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Email Phishing Classifier (LR + BERT)")
        self.root.geometry("800x600")

        # Load models
        self.vec, self.lr_model = load_lightweight_model()
        self.bert_pipeline = load_bert_model()

        # UI Elements
        tk.Label(root, text="Paste Email Text:").pack(pady=5)
        self.text_input = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=10)
        self.text_input.pack(padx=10, pady=5, fill=tk.BOTH)

        tk.Button(root, text="Classify Text", command=self.classify_text).pack(pady=5)

        tk.Label(root, text="OR Upload File:").pack(pady=5)
        tk.Button(root, text="Select File", command=self.select_file).pack(pady=5)

        tk.Label(root, text="Results:").pack(pady=5)
        self.result_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=10, state='disabled')
        self.result_box.pack(padx=10, pady=5, fill=tk.BOTH)

    def log_result(self, msg):
        self.result_box.config(state='normal')
        self.result_box.insert(tk.END, msg + "\n")
        self.result_box.config(state='disabled')

    def classify_text(self):
        text = self.text_input.get("1.0", tk.END).strip()
        if not text:
            messagebox.showwarning("Input Needed", "Please paste some text first.")
            return
        threading.Thread(target=self.run_predictions, args=(text,)).start()

    def select_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("All Files", "*.*"), ("CSV Files", "*.csv"), ("Text Files", "*.txt")])
        if file_path:
            try:
                if file_path.lower().endswith(".csv"):
                    df = pd.read_csv(file_path, header=None, nrows=1)
                    # Auto-detect first non-numeric text column
                    for col in df.columns:
                        if isinstance(df[col][0], str):
                            column_index = col
                            break
                    text = pd.read_csv(file_path, header=None)[column_index].astype(str).str.cat(sep="\n")
                else:
                    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                        text = f.read()
                threading.Thread(target=self.run_predictions, args=(text,)).start()
            except Exception as e:
                messagebox.showerror("File Error", f"Failed to read file: {e}")

    def run_predictions(self, text):
        self.log_result("Classifying...\n")
        # Run both models in parallel threads
        lr_result = [None]
        bert_result = [None]

        def run_lr():
            lr_result[0] = predict_lr(text, self.vec, self.lr_model)

        def run_bert():
            bert_result[0] = predict_bert(text, self.bert_pipeline)

        t1 = threading.Thread(target=run_lr)
        t2 = threading.Thread(target=run_bert)
        t1.start(); t2.start()
        t1.join(); t2.join()

        self.log_result(f"Lightweight LR Model: {lr_result[0]}")
        self.log_result(f"BERT Model: {bert_result[0]}")
        self.log_result("-" * 40)


# ---- Run GUI ----
if __name__ == "__main__":
    root = tk.Tk()
    app = EmailClassifierGUI(root)
    root.mainloop()