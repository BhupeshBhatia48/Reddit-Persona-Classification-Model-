import praw
import re
from textblob import TextBlob
import openai
import os

# --- CONFIGURATION ---
REDDIT_CLIENT_ID = "jQbsI0B5Pjv_8TADrr4_xA"
REDDIT_CLIENT_SECRET = "1BwwiUPeASBc0YjLg5RakjgPjYvSpQ"
REDDIT_USER_AGENT = "script:reddituserpersona:v1.0 (by u/Shot_Rain_7247)"
OPENAI_API_KEY = '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'  # Replace with your actual OpenAI API key
openai.api_key = OPENAI_API_KEY

# --- INITIALIZE REDDIT INSTANCE ---
reddit = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    user_agent=REDDIT_USER_AGENT
)

# --- INTEREST CATEGORIES ---
INTEREST_KEYWORDS = {
    'Technology': ['tech', 'computer', 'software', 'coding', 'programming', 'app', 'website', 'digital', 'ai', 'machine', 'learning'],
    'Gaming': ['game', 'gaming', 'play', 'player', 'steam', 'xbox', 'playstation', 'nintendo', 'pc', 'console'],
    'Sports': ['sport', 'team', 'player', 'football', 'basketball', 'baseball', 'soccer', 'hockey', 'tennis', 'golf'],
    'Entertainment': ['movie', 'film', 'show', 'series', 'tv', 'music', 'song', 'album', 'artist', 'actor'],
    'Finance': ['money', 'stock', 'invest', 'trading', 'crypto', 'bitcoin', 'market', 'price', 'financial'],
    'Fitness': ['workout', 'gym', 'exercise', 'fitness', 'health', 'diet', 'weight', 'muscle', 'training'],
    'Food': ['food', 'recipe', 'cooking', 'restaurant', 'eat', 'meal', 'chef', 'kitchen', 'delicious'],
    'Travel': ['travel', 'trip', 'vacation', 'hotel', 'flight', 'city', 'country', 'visit', 'tourism'],
    'Education': ['school', 'university', 'college', 'student', 'study', 'learn', 'class', 'teacher', 'degree'],
    'Relationships': ['relationship', 'dating', 'love', 'marriage', 'partner', 'boyfriend', 'girlfriend', 'family']
}

def extract_user_content(username):
    redditor = reddit.redditor(username)
    comments = [comment.body for comment in redditor.comments.new(limit=100)]
    submissions = [post.title + ". " + str(post.selftext) for post in redditor.submissions.new(limit=100)]
    return comments + submissions

def analyze_basic_persona(texts):
    persona = {}
    evidence = {}
    all_text = ' '.join(texts).lower()

    # INTERESTS
    interests_found = []
    for category, keywords in INTEREST_KEYWORDS.items():
        if any(keyword in all_text for keyword in keywords):
            interests_found.append(category)
            for t in texts:
                if any(keyword in t.lower() for keyword in keywords):
                    evidence.setdefault('Interests', []).append(f"{category}: {t.strip()}")
                    break
    if interests_found:
        persona['Interests'] = ', '.join(interests_found)

    # OCCUPATION
    for t in texts:
        if any(kw in t.lower() for kw in ['work as', 'my job', 'i work', 'employed as', 'i am a', 'i’m a']):
            persona['Occupation'] = t.strip()
            evidence['Occupation'] = t.strip()
            break

    # PERSONALITY
    for t in texts:
        polarity = TextBlob(t).sentiment.polarity
        if polarity > 0.5:
            persona['Personality'] = 'Very Positive'
            evidence['Personality'] = t.strip()
            break
        elif polarity < -0.5:
            persona['Personality'] = 'Very Negative'
            evidence['Personality'] = t.strip()
            break

    # WRITING STYLE
    for t in texts:
        if t.isupper():
            persona['Writing Style'] = 'Aggressive / Shouting'
            evidence['Writing Style'] = t.strip()
            break
        elif 'lol' in t.lower() or 'haha' in t.lower():
            persona['Writing Style'] = 'Casual / Humorous'
            evidence['Writing Style'] = t.strip()
            break

    # TONE
    positive, negative = 0, 0
    for t in texts:
        polarity = TextBlob(t).sentiment.polarity
        if polarity > 0.2:
            positive += 1
        elif polarity < -0.2:
            negative += 1
    if positive > negative:
        persona['Tone'] = 'Mostly Positive'
    elif negative > positive:
        persona['Tone'] = 'Mostly Negative'
    else:
        persona['Tone'] = 'Neutral'

    return persona, evidence

def generate_llm_persona(texts):
    prompt = f"""
    You are an expert in profiling Reddit users. Based on the following Reddit posts and comments, create a detailed user persona.
    For each characteristic like Interests, Personality, Occupation, Writing Style, Tone, Age, Gender, Political or Religious Views, or any identifiable traits, include a supporting quote from the user's comments or posts as evidence.

    Reddit user data:
    {' '.join(texts[:50])}  # Limit to first 50 to avoid token overload

    Respond in the following format:
    Trait: <Value>
    Evidence: <Actual Reddit post or comment>
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that builds user personas from Reddit data."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message['content']
    except Exception as e:
        return f"LLM generation failed: {e}"

def write_persona_to_file(username, basic_persona, evidence, llm_persona):
    filename = f"{username}_persona.txt"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("---- BASIC NLP-BASED TRAITS ----\n\n")
        for trait, desc in basic_persona.items():
            f.write(f"{trait}: {desc}\n")
            if trait in evidence:
                if isinstance(evidence[trait], list):
                    for e in evidence[trait]:
                        f.write(f"Evidence: {e}\n")
                else:
                    f.write(f"Evidence: {evidence[trait]}\n")
            f.write("\n")

        f.write("\n---- LLM-BASED ANALYSIS ----\n\n")
        f.write(llm_persona)
    print(f"Persona written to {filename}")

def main():
    url = input("Enter Reddit profile URL: ")
    match = re.match(r"https://www.reddit.com/user/([\w-]+)/?", url)
    if not match:
        print("Invalid Reddit profile URL.")
        return
    username = match.group(1)
    print(f"Extracting data for u/{username}...")
    texts = extract_user_content(username)
    print("Running basic NLP analysis...")
    basic_persona, evidence = analyze_basic_persona(texts)
    print("Sending data to LLM for detailed persona generation...")
    llm_persona = generate_llm_persona(texts)
    write_persona_to_file(username, basic_persona, evidence, llm_persona)

if __name__ == '__main__':
    main()
