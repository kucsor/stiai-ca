#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Colectare intrebari tendinta din surse legale

Surse:
  - Hacker News (top stories)
  - Dev.to (top articles)
  - StackOverflow (intrebari active)
"""

import requests
import json
from datetime import datetime
from pathlib import Path

class QuestionCollector:
    def __init__(self, data_dir="data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
    
    def fetch_hackernews_stories(self, limit=5):
        """
        Fetch top stories from Hacker News
        Foloseste API public de la Hacker News
        """
        try:
            url = "https://hn.algolia.com/api/v1/search?tags=front_page&sort=byPopularity&pages=1&perPage=5"
            headers = {'User-Agent': 'HermesQA/1.0 (bot by hermes-agent)'}
            
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            questions = []
            
            for hit in data.get('hits', []):
                questions.append({
                    'source': 'hackernews',
                    'title': hit.get('title', ''),
                    'url': f"https://news.ycombinator.com/item?id={hit.get('objectID', '')}",
                    'points': hit.get('points', 0),
                    'num_comments': hit.get('num_comments', 0),
                    'timestamp': datetime.fromtimestamp(hit.get('created_i', 0)).isoformat() if hit.get('created_i') else None
                })
            
            print(f"Hacker News: Fetch {len(questions)} story-uri")
            return questions
            
        except Exception as e:
            print(f"Hacker News Error: {str(e)}")
            return []
    
    def fetch_devto_articles(self, limit=5):
        """
        Fetch popular articles de la Dev.to
        Foloseste API public de la Dev.to
        """
        try:
            url = "https://dev.to/api/articles?per_page=5&filter=newest"
            headers = {'User-Agent': 'HermesQA/1.0 (bot by hermes-agent)'}
            
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            questions = []
            
            for article in data[:limit]:
                questions.append({
                    'source': 'dev.to',
                    'title': article.get('title', ''),
                    'url': article.get('url', ''),
                    'reactions_count': article.get('reactions_count', 0),
                    'public_reactions_count': article.get('public_reactions_count', 0),
                    'comments_count': article.get('comments_count', 0),
                    'timestamp': article.get('published_at', '')
                })
            
            print(f"Dev.to: Fetch {len(questions)} articole")
            return questions
            
        except Exception as e:
            print(f"Dev.to Error: {str(e)}")
            return []
    
    def fetch_stackoverflow_questions(self, limit=5, tag='python'):
        """
        Fetch intrebari active de la Stack Overflow
        Foloseste oficiala Stack Exchange API
        """
        try:
            url = "https://api.stackexchange.com/2.3/questions"
            params = {
                'order': 'desc',
                'sort': 'creation',
                'tagged': tag,
                'site': 'stackoverflow',
                'pagesize': limit
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            questions = []
            
            for item in data.get('items', []):
                questions.append({
                    'source': 'stackoverflow',
                    'title': item.get('title', ''),
                    'url': f"https://stackoverflow.com/questions/{item.get('question_id', '')}",
                    'tags': item.get('tags', []),
                    'answer_count': item.get('answer_count', 0),
                    'view_count': item.get('view_count', 0),
                    'timestamp': datetime.fromtimestamp(item.get('creation_date', 0)).isoformat()
                })
            
            print(f"Stack Overflow: Fetch {len(questions)} intrebari")
            return questions
            
        except Exception as e:
            print(f"Stack Overflow Error: {str(e)}")
            return []
    
    def collect_all_questions(self):
        """Function principala pentru colectare intrebari"""
        print("=" * 60)
        print("Colectare intrebari")
        print("=" * 60)
        
        all_questions = []
        
        # Colecteaza de la Hacker News
        hn_stories = self.fetch_hackernews_stories(limit=3)
        all_questions.extend(hn_stories)
        
        # Colecteaza de la Dev.to
        devto_articles = self.fetch_devto_articles(limit=3)
        all_questions.extend(devto_articles)
        
        # Colecteaza de la Stack Overflow
        so_questions = self.fetch_stackoverflow_questions(limit=4, tag='python')
        all_questions.extend(so_questions)
        
        # Salveaza la fisier JSON
        output_file = self.data_dir / f"questions_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        output_data = {
            'collected_at': datetime.now().isoformat(),
            'total_questions': len(all_questions),
            'questions': all_questions
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        
        # Si salva ca latest pentru site
        latest_file = self.data_dir / "questions_latest.json"
        with open(latest_file, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        
        print(f"Salvat {len(all_questions)} intrebari la {output_file}")
        print(f"Salvat latest la {latest_file}")
        print("=" * 60)
        
        return output_data

if __name__ == "__main__":
    collector = QuestionCollector()
    result = collector.collect_all_questions()
    print(f"Total intrebari colectate: {result['total_questions']}")
