# Week 1 NLP EDA & Preprocessing

This project analyzes the Cornell Movie Review Polarity Dataset v2.0 (1,000 positive and 1,000 negative processed reviews). Dataset source: https://www.cs.cornell.edu/people/pabo/movie-review-data/

Download and extract the polarity v2.0 archive from Cornell. Expected structure: `review_polarity/txt_sentoken/pos/*.txt` and `review_polarity/txt_sentoken/neg/*.txt`.

Install dependencies: `pip install pandas numpy matplotlib scikit-learn`

Run: `python eda_analysis.py --data_dir ./review_polarity --out_dir ./outputs`

The script generates label and token-length charts, unigram/bigram frequency outputs, per-class term lists, quality flags, a cleaned CSV, and JSON statistics. The cleaner lowercases text, replaces URL/email patterns with placeholders, removes markup and most non-linguistic symbols, and normalizes whitespace. It deliberately preserves negation and selected punctuation. Stopword filtering is limited to frequency summaries.

Do not claim output statistics until the script has been run on the downloaded archive. Record Python/package versions, dataset version, and run date for reproducibility.
