#!/usr/bin/env python3
"""
Auto Blog Generator using Google Gemini AI
Generates tech blog posts and saves them as HTML with images from Unsplash
"""

import os
import json
import requests
from datetime import datetime
import google.generativeai as genai
import random

# Configure API Keys
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
UNSPLASH_ACCESS_KEY = os.getenv('UNSPLASH_ACCESS_KEY')

if not GEMINI_API_KEY or not UNSPLASH_ACCESS_KEY:
    raise ValueError("Missing API keys. Set GEMINI_API_KEY and UNSPLASH_ACCESS_KEY environment variables.")

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)

# Tech topics for variety
TECH_TOPICS = [
    "الذكاء الاصطناعي والتعلم الآلي",
    "أمن المعلومات والتشفير",
    "تطوير تطبيقات الموبايل",
    "الحوسبة السحابية",
    "إنترنت الأشياء IoT",
    "البرمجة وتطوير الويب",
    "قواعد البيانات والبيانات الضخمة",
    "تقنيات الشبكات",
    "الواقع الافتراضي والمعزز",
    "البلوكتشين والعملات الرقمية",
    "تطوير لعبات الفيديو",
    "أنظمة التشغيل والأنظمة المدمجة",
    "أتمتة العمليات الآلية",
    "واجهات المستخدم UX/UI",
    "تقنيات البرمجة الحديثة"
]

def get_random_topic():
    """Get a random tech topic"""
    return random.choice(TECH_TOPICS)

def generate_blog_content(topic):
    """
    Generate blog post content using Gemini AI
    Returns: title, description, content
    """
    print(f"🤖 Generating content for topic: {topic}")
    
    prompt = f"""اكتب مقالة تقنية احترافية عن: {topic}

المتطلبات:
- الطول: أكثر من 1500 كلمة
- باللغة العربية
- مقسمة إلى أقسام واضحة مع عناوين فرعية
- تتضمن أمثلة عملية وتطبيقات واقعية
- لغة سهلة وواضحة للجمهور العام والمتخصصين
- ابدأ بمقدمة جذابة
- انهي بخلاصة وتوصيات

الرد يجب أن يكون بصيغة JSON مع المفاتيح التالية:
{{
    "title": "عنوان المقالة",
    "description": "وصف قصير (2-3 أسطر)",
    "content": "محتوى المقالة الكامل"
}}"""
    
    try:
        # استخدام gemini-1.5-flash بدلاً من gemini-pro
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        
        # Extract JSON from response
        response_text = response.text
        # Find JSON in response
        start_idx = response_text.find('{')
        end_idx = response_text.rfind('}') + 1
        json_str = response_text[start_idx:end_idx]
        data = json.loads(json_str)
        return data['title'], data['description'], data['content']
    except Exception as e:
        print(f"Error: {e}")
        return f"مقالة عن {topic}", f"مقالة تقنية حول {topic}", "محتوى المقالة"

def get_image_from_unsplash(query):
    """
    Get image URL from Unsplash based on query
    Returns: image_url
    """
    print(f"🖼️ Fetching image for: {query}")
    
    url = "https://api.unsplash.com/photos/random"
    params = {
        "query": query,
        "client_id": UNSPLASH_ACCESS_KEY,
        "w": 1200,
        "h": 630
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data['urls']['regular']
    except Exception as e:
        print(f"Error fetching image: {e}")
        return None

def create_html_post(title, description, content, image_url, topic):
    """
    Create HTML file for the blog post
    """
    html_content = f"""<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <meta name="description" content="{description}">
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.8;
            color: #333;
            background-color: #f5f5f5;
        }}
        .container {{
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: white;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .header {{
            margin-bottom: 30px;
            border-bottom: 3px solid #007bff;
            padding-bottom: 20px;
        }}
        h1 {{
            color: #007bff;
            margin-bottom: 10px;
            font-size: 2.5em;
        }}
        .meta {{
            color: #666;
            font-size: 0.95em;
            margin-bottom: 10px;
        }}
        .description {{
            color: #555;
            font-size: 1.1em;
            font-style: italic;
            margin-bottom: 20px;
        }}
        .featured-image {{
            width: 100%;
            height: auto;
            border-radius: 8px;
            margin: 20px 0;
        }}
        .content {{
            font-size: 1.05em;
            line-height: 1.9;
        }}
        .content h2 {{
            color: #007bff;
            margin-top: 25px;
            margin-bottom: 15px;
            font-size: 1.8em;
        }}
        .content h3 {{
            color: #0056b3;
            margin-top: 20px;
            margin-bottom: 12px;
            font-size: 1.3em;
        }}
        .content p {{
            margin-bottom: 15px;
            text-align: justify;
        }}
        .content ul, .content ol {{
            margin: 15px 0 15px 30px;
        }}
        .content li {{
            margin-bottom: 10px;
        }}
        .footer {{
            margin-top: 40px;
            padding-top: 20px;
            border-top: 2px solid #eee;
            text-align: center;
            color: #666;
            font-size: 0.9em;
        }}
        .topic-tag {{
            display: inline-block;
            background-color: #007bff;
            color: white;
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 0.9em;
            margin-bottom: 15px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <span class="topic-tag">{topic}</span>
            <h1>{title}</h1>
            <div class="meta">
                <strong>نبض التقنية</strong> | {datetime.now().strftime('%d/%m/%Y')}
            </div>
            <p class="description">{description}</p>
        </div>
        
        {f'<img src="{image_url}" alt="{title}" class="featured-image">' if image_url else ''}
        
        <div class="content">
            {content}
        </div>
        
        <div class="footer">
            <p>تم إنشاء هذا المقال تلقائياً بواسطة نظام نبض التقنية AI</p>
            <p>{datetime.now().strftime('%d/%m/%Y - %H:%M:%S')}</p>
        </div>
    </div>
</body>
</html>"""
    return html_content

def save_post(html_content, title):
    """
    Save the blog post to file
    """
    # Create filename from title and date
    date_str = datetime.now().strftime('%Y-%m-%d')
    safe_title = title.replace('/', '-').replace('\\', '-')[:40]
    filename = f"{date_str}-{safe_title}.html"
    filepath = os.path.join('posts', 'html', filename)
    
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✅ Post saved to: {filepath}")
    return filepath

def main():
    """
    Main function to generate and save blog post
    """
    print("🚀 Starting Auto Blog Generator...")
    
    # Get random topic
    topic = get_random_topic()
    print(f"📌 Selected topic: {topic}")
    
    # Generate content
    title, description, content = generate_blog_content(topic)
    print(f"✅ Content generated: {title}")
    
    # Get image
    image_url = get_image_from_unsplash(topic)
    
    # Create HTML
    html_content = create_html_post(title, description, content, image_url, topic)
    
    # Save post
    filepath = save_post(html_content, title)
    
    print(f"\n✨ Blog post created successfully!")
    print(f"📝 Title: {title}")
    print(f"🖼️ Image: {image_url if image_url else 'No image found'}")
    print(f"📁 File: {filepath}")

if __name__ == "__main__":
    main()
