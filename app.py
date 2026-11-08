"""Train and use an Indonesian/English SMS scam detector."""
from __future__ import annotations

# Compatibility entry point; canonical implementation is src/detector.py
import argparse, csv, json, re
from pathlib import Path
from joblib import dump, load
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score, f1_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

ROOT = Path(__file__).resolve().parent
RAW = ROOT / "data" / "dataset_raw"
PROCESSED = ROOT / "data" / "dataset_processed" / "messages.csv"
MODEL = ROOT / "models" / "fraud_detector.joblib"
LABELS = {"ham": 0, "normal": 0, "legitimate": 0, "spam": 1, "scam": 1, "fraud": 1, "penipuan": 1, "phishing": 1}

def clean(text: str) -> str:
    text = str(text).lower().replace("\u200b", " ")
    text = re.sub(r"https?://\S+|www\.\S+", " URL ", text)
    text = re.sub(r"\b\d[\d\s+().-]{6,}\d\b", " PHONE ", text)
    return re.sub(r"\s+", " ", text).strip()

def read_rows():
    rows = []
    files = list((RAW / "dataset1").glob("*.csv")) + list((RAW / "dataset2").glob("*.csv")) + list((RAW / "dataset3").glob("SMSSpamCollection"))
    for path in files:
        if path.name == "SMSSpamCollection":
            with path.open(encoding="utf-8", errors="replace") as f:
                for line in f:
                    label, sep, text = line.rstrip("\n").partition("\t")
                    if sep and label.lower() in LABELS and text.strip(): rows.append((clean(text), LABELS[label.lower()]))
        else:
            with path.open(encoding="utf-8-sig", newline="", errors="replace") as f:
                for row in csv.DictReader(f):
                    text = row.get("text") or row.get("Pesan") or ""
                    label = row.get("spam_ham_label") or row.get("Kategori") or row.get("label") or ""
                    if text.strip() and label.lower().strip() in LABELS: rows.append((clean(text), LABELS[label.lower().strip()]))
    return sorted({(text, label) for text, label in rows})

def train():
    rows = read_rows()
    if len(rows) < 20 or len({label for _, label in rows}) < 2: raise RuntimeError("Dataset tidak cukup atau label tidak lengkap")
    PROCESSED.parent.mkdir(parents=True, exist_ok=True)
    with PROCESSED.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f); w.writerow(["text", "label"]); w.writerows(rows)
    texts, labels = zip(*rows)
    x_train, x_test, y_train, y_test = train_test_split(texts, labels, test_size=.2, random_state=42, stratify=labels)
    model = Pipeline([("tfidf", TfidfVectorizer(ngram_range=(1, 2), sublinear_tf=True)), ("classifier", LogisticRegression(max_iter=1000, class_weight="balanced"))])
    model.fit(x_train, y_train); pred = model.predict(x_test)
    result = {"rows": len(rows), "train_rows": len(x_train), "test_rows": len(x_test), "accuracy": accuracy_score(y_test, pred), "f1_penipuan": f1_score(y_test, pred), "report": classification_report(y_test, pred, target_names=["normal", "penipuan"], output_dict=True, zero_division=0)}
    MODEL.parent.mkdir(parents=True, exist_ok=True); dump(model, MODEL)
    (MODEL.parent / "evaluation.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    return result

def predict(message: str):
    if not MODEL.exists(): raise RuntimeError("Model belum ada. Jalankan: python app.py train")
    model = load(MODEL); text = clean(message); label = int(model.predict([text])[0]); probability = model.predict_proba([text])[0][label]
    return {"label": "PENIPUAN" if label else "NORMAL", "confidence": round(float(probability), 4), "message": message}

def main():
    parser = argparse.ArgumentParser(); sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("train"); p = sub.add_parser("predict"); p.add_argument("message")
    args = parser.parse_args(); print(json.dumps(train() if args.command == "train" else predict(args.message), ensure_ascii=False, indent=2))

if __name__ == "__main__": main()