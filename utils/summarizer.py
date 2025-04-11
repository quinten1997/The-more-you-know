try:
    from transformers import pipeline
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
except:
    summarizer = None

def summarize_text(text, max_chars=300):
    if not text:
        return ""

    word_count = len(text.split())
    if word_count < 20:
        return text.strip()

    if summarizer:
        try:
            # Dynamically adjust max_length so it’s always slightly larger than input
            max_len = min(75, word_count + 15)
            summary = summarizer(text, max_length=max_len, min_length=15, do_sample=False)
            print(summary[0]['summary_text'])
            return summary[0]['summary_text']
        except:
            pass

    return text[:max_chars] + ("..." if len(text) > max_chars else "")
