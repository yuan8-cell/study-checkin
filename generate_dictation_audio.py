#!/usr/bin/env python3
"""
生成每日听写音频 - 使用edge-tts
- 每个单词读两遍（英文），中间停顿1秒
- 读完后停顿3秒供书写
- 中文释义读一遍
- 每日生成一个MP3文件
"""

import json
import os
import asyncio
import edge_tts

OUTPUT_DIR = r'C:\Users\Admin\WorkBuddy\Claw\daily_practice\audio'
PLAN_FILE = r'C:\Users\Admin\WorkBuddy\Claw\daily_practice\daily_plan.json'

os.makedirs(OUTPUT_DIR, exist_ok=True)

with open(PLAN_FILE, 'r', encoding='utf-8') as f:
    plan = json.load(f)

# Only generate audio for first 5 days as demo (96 days would take very long)
# User can generate more later
MAX_DAYS = 5

VOICE_EN = "en-US-AriaNeural"  # English voice
VOICE_CN = "zh-CN-XiaoxiaoNeural"  # Chinese voice

async def generate_day_audio(day_data):
    day = day_data['day']
    new_words = day_data['new_words']
    
    # Build SSML-like text for edge-tts
    # Format: word (pause) word (pause) meaning
    text_parts = []
    
    for i, w in enumerate(new_words):
        word = w['word']
        meaning = w['meaning']
        pos = w.get('pos', '')
        
        # Build the dictation script
        # Number announcement
        text_parts.append(f"Number {i+1}.")
        # Word read twice with pause
        text_parts.append(word)
        text_parts.append(".")  # short pause
        text_parts.append(word)
        text_parts.append(".")  # short pause for writing
        # Chinese meaning
        cn_meaning = meaning.split(';')[0] if ';' in meaning else meaning
        # Remove parenthetical notes
        cn_meaning = cn_meaning.split('(')[0].strip() if '(' in cn_meaning else cn_meaning.strip()
        text_parts.append(f"The Chinese meaning is {cn_meaning}.")
        text_parts.append(".")  # pause before next word
    
    # Combine with pauses
    full_text = " ".join(text_parts)
    
    output_file = os.path.join(OUTPUT_DIR, f'day_{day:03d}_dictation.mp3')
    
    communicate = edge_tts.Communicate(full_text, VOICE_EN)
    await communicate.save(output_file)
    
    print(f"  Day {day}: Generated {output_file} ({len(new_words)} words)")

async def main():
    print(f"Generating audio for first {MAX_DAYS} days...")
    
    for day_data in plan[:MAX_DAYS]:
        await generate_day_audio(day_data)
    
    print(f"\nDone! Audio files saved to: {OUTPUT_DIR}")

if __name__ == '__main__':
    asyncio.run(main())
