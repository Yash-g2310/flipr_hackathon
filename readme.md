# News Aggregator & Blog Publishing System

## 📋 Overview
An automated pipeline that:
1. Scrapes news from websites 
2. Clusters articles into categories (Sports, Entertainment, etc.)
3. Processes through LLM for user interactions
4. Generates & translates blogs
5. Publishes to WordPress

## 🚀 Key Features
- **Smart Scraping**  
  Location-based news scraping (e.g. "Delhi news")
- **AI Clustering**  
  BERT-based categorization into predefined labels
- **LLM Interaction**  
  Natural language queries and blog generation
- **WordPress Integration**  
  Direct publishing with OAuth2 authentication
- **Translation API**  
  MyMemory API integration for multi-language support

## ⚙️ Installation

### 1. Clone Repository
```bash
git clone https://github.com/yourusername/news-clustering-llm.git
cd news-clustering-llm
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Environment
Create `.env` file with:

```ini
# WordPress OAuth2 Credentials
WORDPRESS_CLIENT_ID=<your_client_id>
WORDPRESS_CLIENT_SECRET=<your_client_secret>
WORDPRESS_USERNAME=<wp_username>
WORDPRESS_PASSWORD=<wp_password>
WORDPRESS_REDIRECT_URI=http://localhost:8000/callback

# Translation Service
MYMEMORY_TRANSLATE_KEY=<your_api_key>

# Model Configuration 
MODEL_DIR=bert_model
TF_ENABLE_ONEDNN_OPTS=0
```

### 🔑 Obtaining Credentials

#### WordPress Keys:
1. Create an app at [WordPress Developer Portal](https://developer.wordpress.com/apps/)
2. Get `CLIENT_ID` and `CLIENT_SECRET`
3. Use your WordPress login for `USERNAME/PASSWORD`
4. Set `REDIRECT_URI` to your callback URL

#### Translation API:
1. Register at [MyMemory API](https://mymemory.translated.net/doc/spec.php)
2. Get a free API key for `MYMEMORY_TRANSLATE_KEY`

## 🖥️ Usage

### Start System
```bash
python main.py
```

### Enter Query
```plaintext
> Give me latest news in Delhi
```

### System Will:
- Scrape location-specific news
- Cluster into categories
- Show summarized articles

### Blog Generation
- Confirm to create a blog post → Edit content → Choose translation

### Publishing
Final confirmation publishes to WordPress:

```python
# Sample publishing workflow
if user_confirms:
    publish_to_wordpress(blog_content)
```

## 🔮 Future Roadmap
- Enhanced NLP clustering accuracy
- Multi-source news integration
- Custom blog templates
- Social media auto-posting
- Sentiment analysis layer