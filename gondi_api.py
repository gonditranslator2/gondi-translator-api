from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)

# Load the dataset
file_path = "English_Hindi_Gondi_10000.csv"
df = pd.read_csv(file_path)

@app.route('/')
def home():
    return "Gondi Translator API is running!"

@app.route('/random', methods=['GET'])
def get_random_sentence():
    row = df.sample(n=1).iloc[0]
    return jsonify({"English": row["English"], "Hindi": row["Hindi"], "Gondi": row["Gondi"]})

@app.route('/sentence', methods=['GET'])
def get_sentence():
    query = request.args.get("query", "").lower()
    results = df[(df["English"].str.lower() == query) |
                 (df["Hindi"].str.lower() == query) |
                 (df["Gondi"].str.lower() == query)]

    if results.empty:
        return jsonify({"error": "No match found"}), 404

    sentences = results.to_dict(orient="records")
    return jsonify(sentences)

@app.route('/sentence/<int:idx>', methods=['GET'])
def get_sentence_by_id(idx):
    if 0 <= idx < len(df):
        row = df.iloc[idx]
        return jsonify({"English": row["English"], "Hindi": row["Hindi"], "Gondi": row["Gondi"]})
    else:
        return jsonify({"error": "Index out of range"}), 404

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
