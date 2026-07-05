#!/usr/bin/env python3
"""
生成每日默写听写练习计划
- 每天半小时：15分钟默写 + 10分钟听写 + 5分钟复习
- 约20-25个单词/天
- 基于艾宾浩斯遗忘曲线安排复习
- 生成HTML练习页面和每日听写文本
"""

import json
import os
import math
from datetime import datetime, timedelta

# ============================================================
# 1. Load vocabulary data
# ============================================================
data_file = r'C:\Users\Admin\WorkBuddy\Claw\vocabulary_data.json'
with open(data_file, 'r', encoding='utf-8') as f:
    words = json.load(f)

# Sort by source (textbook order), then alphabetically
def sort_key(item):
    source = item.get('source', '')
    word = item.get('word', '').lower()
    # Order: 七上, 七下, 八上, 八下
    if '七年级上册' in source:
        s_rank = 0
    elif '七年级下册' in source:
        s_rank = 1
    elif '八年级上册' in source:
        s_rank = 2
    else:
        s_rank = 3
    return (s_rank, word)

words.sort(key=sort_key)

# ============================================================
# 2. Split into daily chunks (20-25 words/day)
# ============================================================
WORDS_PER_DAY = 22  # ~20 new + a few review

# Split words into days
days = []
current_day = []
for w in words:
    if len(current_day) >= WORDS_PER_DAY:
        days.append(current_day)
        current_day = []
    current_day.append(w)
if current_day:
    days.append(current_day)

total_days = len(days)
print(f"Total words: {len(words)}")
print(f"Days: {total_days} (avg {len(words)/total_days:.1f} words/day)")

# ============================================================
# 3. Generate daily plan with Ebbinghaus review schedule
# ============================================================
# Ebbinghaus intervals: day 1, 2, 4, 7, 15
ebbinghaus_intervals = [1, 2, 4, 7, 15]

# Build daily schedule
daily_schedule = []
for day_idx in range(total_days):
    entry = {
        'day': day_idx + 1,
        'new_words': days[day_idx],
        'review_days': [],  # which previous days to review
    }
    # Check which previous day's words need review
    for prev_day in range(day_idx):
        days_ago = day_idx - prev_day
        if days_ago in ebbinghaus_intervals:
            entry['review_days'].append(prev_day + 1)
    daily_schedule.append(entry)

# ============================================================
# 4. Generate dictation text files per day
# ============================================================
output_dir = r'C:\Users\Admin\WorkBuddy\Claw\daily_practice'
os.makedirs(output_dir, exist_ok=True)

# Create subdirectories
dictation_dir = os.path.join(output_dir, 'dictation_texts')
dict_eng_dir = os.path.join(output_dir, 'dictation_english')
dict_cn_dir = os.path.join(output_dir, 'dictation_chinese')
os.makedirs(dictation_dir, exist_ok=True)
os.makedirs(dict_eng_dir, exist_ok=True)
os.makedirs(dict_cn_dir, exist_ok=True)

# Generate per-day text files
for entry in daily_schedule:
    day = entry['day']
    new_words = entry['new_words']
    review_days = entry['review_days']
    
    # Collect review words
    review_words = []
    for rd in review_days:
        review_words.extend(daily_schedule[rd - 1]['new_words'])
    
    # Write Chinese dictation text (看中文写英文 - 默写)
    cn_lines = [f"=== 第{day}天 默写练习（看中文写英文） ===\n"]
    cn_lines.append(f"新词数量: {len(new_words)} | 复习词数量: {len(review_words)}\n\n")
    cn_lines.append("【新词默写】\n")
    for i, w in enumerate(new_words):
        cn_lines.append(f"{i+1:3d}. {w['meaning']}\n")
    
    if review_words:
        cn_lines.append(f"\n【复习词默写（第{','.join(map(str,review_days))}天内容）】\n")
        for i, w in enumerate(review_words):
            cn_lines.append(f"{i+1:3d}. {w['meaning']}\n")
    
    cn_path = os.path.join(dictation_dir, f'day_{day:03d}_默写_看中文写英文.txt')
    with open(cn_path, 'w', encoding='utf-8') as f:
        f.writelines(cn_lines)
    
    # Write English dictation text (看英文写中文)
    en_lines = [f"=== Day {day} Dictation (English → Chinese) ===\n"]
    en_lines.append(f"New: {len(new_words)} | Review: {len(review_words)}\n\n")
    en_lines.append("【New Words】\n")
    for i, w in enumerate(new_words):
        phonetic = f" {w['phonetic']}" if w.get('phonetic') else ''
        pos = f" ({w['pos']})" if w.get('pos') else ''
        en_lines.append(f"{i+1:3d}. {w['word']}{phonetic}{pos}\n")
    
    if review_words:
        en_lines.append(f"\n【Review (Day {','.join(map(str,review_days))})】\n")
        for i, w in enumerate(review_words):
            phonetic = f" {w['phonetic']}" if w.get('phonetic') else ''
            pos = f" ({w['pos']})" if w.get('pos') else ''
            en_lines.append(f"{i+1:3d}. {w['word']}{phonetic}{pos}\n")
    
    en_path = os.path.join(dictation_dir, f'day_{day:03d}_听写_看英文写中文.txt')
    with open(en_path, 'w', encoding='utf-8') as f:
        f.writelines(en_lines)
    
    # Generate answer key
    ans_lines = [f"=== Day {day} Answer Key ===\n\n"]
    ans_lines.append("【New Words】\n")
    for i, w in enumerate(new_words):
        phonetic = f" {w['phonetic']}" if w.get('phonetic') else ''
        pos = f" [{w['pos']}]" if w.get('pos') else ''
        ans_lines.append(f"{i+1:3d}. {w['word']}{phonetic}{pos} — {w['meaning']}\n")
    
    if review_words:
        ans_lines.append(f"\n【Review】\n")
        for i, w in enumerate(review_words):
            phonetic = f" {w['phonetic']}" if w.get('phonetic') else ''
            pos = f" [{w['pos']}]" if w.get('pos') else ''
            ans_lines.append(f"{i+1:3d}. {w['word']}{phonetic}{pos} — {w['meaning']}\n")
    
    ans_path = os.path.join(dictation_dir, f'day_{day:03d}_答案.txt')
    with open(ans_path, 'w', encoding='utf-8') as f:
        f.writelines(ans_lines)

print(f"Generated {total_days} daily dictation files in: {dictation_dir}")

# ============================================================
# 5. Generate weekly summary and overview
# ============================================================
total_weeks = math.ceil(total_days / 7)

overview_lines = ["=== 英语词汇每日练习总览 ===\n"]
overview_lines.append(f"教材来源: 人教版七上、七下、八上、八下\n")
overview_lines.append(f"总词汇量: {len(words)}\n")
overview_lines.append(f"总天数: {total_days}（约{total_weeks}周）\n")
overview_lines.append(f"每日新词: {WORDS_PER_DAY}个\n")
overview_lines.append(f"每日时间: 约30分钟（15分钟默写 + 10分钟听写 + 5分钟复习）\n\n")
overview_lines.append("=" * 60 + "\n\n")

overview_lines.append("【每周进度表】\n")
overview_lines.append(f"{'周次':<6}{'天数范围':<12}{'新词范围':<12}{'累计词汇':<10}\n")
overview_lines.append("-" * 45 + "\n")

for week in range(total_weeks):
    start_day = week * 7 + 1
    end_day = min((week + 1) * 7, total_days)
    new_count = sum(len(daily_schedule[d-1]['new_words']) for d in range(start_day, end_day+1))
    cumulative = sum(len(daily_schedule[d-1]['new_words']) for d in range(1, end_day+1))
    overview_lines.append(f"第{week+1}周{'':>2}{start_day}-{end_day}天{'':>3}{new_count}个{'':>4}{cumulative}个\n")

overview_lines.append("\n" + "=" * 60 + "\n\n")

overview_lines.append("【艾宾浩斯复习提醒】\n")
overview_lines.append("每天除了学习新词，还需复习以下天数内容：\n")
overview_lines.append("  第1天 → 复习无（第1天只有新词）\n")
overview_lines.append("  第2天 → 复习第1天\n")
overview_lines.append("  第3天 → 复习第2天\n")
overview_lines.append("  第4天 → 复习第3天 + 第1天\n")
overview_lines.append("  第5天 → 复习第4天 + 第2天\n")
overview_lines.append("  ...依此类推\n\n")

overview_lines.append("【30分钟练习流程】\n")
overview_lines.append("  0-15分钟: 默写（看中文释义写出英文单词）\n")
overview_lines.append("  15-25分钟: 听写（听英文写中文/英文）\n")
overview_lines.append("  25-30分钟: 对照答案批改并复习错误单词\n")

overview_path = os.path.join(output_dir, '00_总览_练习计划.txt')
with open(overview_path, 'w', encoding='utf-8') as f:
    f.writelines(overview_lines)

print(f"Overview saved to: {overview_path}")

# ============================================================
# 6. Save daily plan as JSON for HTML generation
# ============================================================
plan_json = []
for entry in daily_schedule:
    plan_json.append({
        'day': entry['day'],
        'new_count': len(entry['new_words']),
        'review_days': entry['review_days'],
        'review_count': sum(len(daily_schedule[rd-1]['new_words']) for rd in entry['review_days']),
        'total_count': len(entry['new_words']) + sum(len(daily_schedule[rd-1]['new_words']) for rd in entry['review_days']),
        'new_words': entry['new_words'],
        'review_words': [],
        'source_books': list(set(w['source'] for w in entry['new_words']))
    })
    # Add review words
    for rd in entry['review_days']:
        plan_json[-1]['review_words'].extend(daily_schedule[rd-1]['new_words'])

plan_path = os.path.join(output_dir, 'daily_plan.json')
with open(plan_path, 'w', encoding='utf-8') as f:
    json.dump(plan_json, f, ensure_ascii=False, indent=2)

print(f"Plan JSON saved to: {plan_path}")
print(f"\nDone! Total {total_days} days of practice generated.")
