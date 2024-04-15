import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, request
import random

app = Flask(__name__)

# Default blog posts
default_blog_posts = [
    {"title": "The Rise of AI in Healthcare", "content": "Lorem ipsum dolor sit amet, consectetur adipiscing elit..."},
    {"title": "Ethical Considerations in AI Development", "content": "Lorem ipsum dolor sit amet, consectetur adipiscing elit..."},
    {"title": "How AI is Transforming Education", "content": "Lorem ipsum dolor sit amet, consectetur adipiscing elit..."}
]

def generate_blog_post(topic):
    # Fetch content from Wikipedia based on the topic
    url = f"https://en.wikipedia.org/wiki/{topic}"
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        # Extract relevant content from the Wikipedia page
        content = ""
        paragraphs = soup.select('p')
        for p in paragraphs:
            content += p.get_text() + "\n"
    else:
        # If fetching fails, generate a default blog post
        post = random.choice(default_blog_posts)
        return post

    # Generate the blog post based on the fetched content
    title = f"Blog Post about {topic}"
    return {"title": title, "content": content}

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        topic = request.form['topic']
        post = generate_blog_post(topic)
    else:
        # Choose a random blog post from default_blog_posts
        post = random.choice(default_blog_posts)
    return render_template('index.html', post=post)

if __name__ == '__main__':
    app.run(debug=True)
