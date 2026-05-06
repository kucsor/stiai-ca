#!/usr/bin/env python3
"""Raport orar al proiectului Q&A Educational"""
import json
from datetime import datetime
from pathlib import Path

project_dir = Path('/root/hermes-trending-qa')
data_file = project_dir / 'data' / 'questions_latest.json'

if data_file.exists():
    with open(data_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    questions = data.get('questions', [])
    total = len(questions)
    answered = sum(1 for q in questions if q.get('answer') and len(q.get('answer', '')) > 50)
    
    cats = {}
    for q in questions:
        cat = q.get('category', 'General')
        cats[cat] = cats.get(cat, 0) + 1
    
    cat_lines = '\n'.join([f"  - {k}: {v} intrebari" for k, v in sorted(cats.items())])
    
    report = f"""
RAPORT ORAR - Proiect Q&A Educational
========================================
Timestamp: {datetime.now().strftime('%d.%m.%Y %H:%M')}

Status proiect:
  - Total intrebari: {total}
  - Cu raspunsuri: {answered}/{total}
  - Categorii: {len(cats)}

Categorii:
{cat_lines}

Website: http://localhost:8000
Model: deepseek/deepseek-v4-flash (OpenRouter)

---
Generat automat de Hermes Agent pentru Alex
"""
    print(report)
else:
    print("Fisierul de date nu exista!")
