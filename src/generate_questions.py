#!/usr/bin/env python3
"""Generator automat de intrebari educationale - DeepSeek API direct"""
import requests, json, os, sys, re
from datetime import datetime
from pathlib import Path

DEEPSEEK_API_KEY = os.environ.get('DEEPSEEK_API_KEY')
if not DEEPSEEK_API_KEY:
    env_file = Path('/root/.hermes/.env')
    if env_file.exists():
        for line in env_file.read_text().splitlines():
            if line.startswith('DEEPSEEK_API_KEY='):
                DEEPSEEK_API_KEY = line.split('=', 1)[1].strip()
if not DEEPSEEK_API_KEY:
    print("ERROR: DEEPSEEK_API_KEY not found"); sys.exit(1)

DEEPSEEK_URL = "https://api.deepseek.com/v1/chat/completions"
CATEGORIES = ["Corp Uman","Corp Uman","Natura si Univers","Natura si Univers","Tehnologie","Tehnologie","Somn si Vis"]

def generate_qa(category, existing=[]):
    prompt = f"""Genereaza o intrebare educationala UNICA in limba romana.

Categoria: {category}
NU repeta intrebarile existente: {chr(10).join(['- '+q[:60] for q in existing[-8:]])}

Formateaza:
Intrebare: [intrebarea, max 120 caractere]
Raspuns: [raspuns simplu, cu analogie, explicatie stiintifica, max 500 cuvinte]"""

    try:
        r = requests.post(DEEPSEEK_URL,
            headers={"Authorization": f"Bearer {DEEPSEEK_API_KEY}", "Content-Type": "application/json"},
            json={"model": "deepseek-chat", "messages": [{"role": "user", "content": prompt}],
                  "max_tokens": 2000, "temperature": 0.85},
            timeout=60)
        if r.status_code != 200:
            return None
        content = r.json()['choices'][0]['message']['content']
        q = re.search(r'Intrebare:\s*(.+?)[\n]', content, re.I)
        a = re.search(r'Raspuns:\s*(.+)', content, re.I | re.DOTALL)
        if q and a:
            return {"question": q.group(1).strip()[:120], "answer": a.group(1).strip(), "category": category}
    except: return None

def main():
    df = Path('/root/hermes-trending-qa/data/questions_latest.json')
    data = json.loads(df.read_text(encoding='utf-8')) if df.exists() else {"questions":[]}
    questions = data.get('questions', [])
    existing = [q.get('question','') for q in questions]
    print(f"Loaded {len(questions)} questions")
    
    count = int(sys.argv[1]) if len(sys.argv)>1 else 5
    new, err = 0, 0
    for i in range(count):
        cat = CATEGORIES[i % len(CATEGORIES)]
        print(f"[{i+1}/{count}] {cat}...", end=" ", flush=True)
        res = generate_qa(cat, existing)
        if res and res['question'] not in existing:
            res['id'] = len(questions) + 1
            res['timestamp'] = datetime.now().isoformat()
            questions.append(res)
            existing.append(res['question'])
            new += 1
            print(f"OK: {res['question'][:50]}")
        else:
            err += 1
            print("SKIP")
    for i,q in enumerate(questions,1): q['id']=i
    data['questions'] = questions
    data['total_questions'] = len(questions)
    data['generated_at'] = datetime.now().isoformat()
    df.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')
    import shutil
    shutil.copy(df, '/root/hermes-trending-qa/public/data/questions_latest.json')
    print(f"\nDone: {len(questions)} total | +{new} new | {err} errors")

if __name__ == "__main__": main()
