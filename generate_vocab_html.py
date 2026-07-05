#!/usr/bin/env python3
"""
生成交互式词汇学习HTML页面
- 按教材分组浏览
- 点击发音（Web Speech API TTS）
- 悬停查看中文释义
- 收藏复习系统
- 每日练习入口
- 响应式移动端适配
"""

import json
import os

# Load vocabulary data
data_file = r'C:\Users\Admin\WorkBuddy\Claw\vocabulary_data.json'
with open(data_file, 'r', encoding='utf-8') as f:
    words = json.load(f)

# Load daily plan
plan_file = r'C:\Users\Admin\WorkBuddy\Claw\daily_practice\daily_plan.json'
with open(plan_file, 'r', encoding='utf-8') as f:
    plan = json.load(f)

# Group words by source textbook
sources = {}
for w in words:
    src = w.get('source', '未知')
    if src not in sources:
        sources[src] = []
    sources[src].append(w)

# Group words by first letter
letter_groups = {}
for w in words:
    letter = w['word'][0].upper() if w['word'] else '#'
    if not ('A' <= letter <= 'Z'):
        letter = '#'
    if letter not in letter_groups:
        letter_groups[letter] = []
    letter_groups[letter].append(w)

# Build HTML
html_parts = []

html_parts.append('''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>人教版英语词汇表 — 七上七下八上八下</title>
<style>
:root {
  --primary: #4A90D9;
  --primary-dark: #357ABD;
  --bg: #f5f7fa;
  --card-bg: #ffffff;
  --text: #333333;
  --text-light: #666666;
  --border: #e0e6ed;
  --shadow: 0 2px 8px rgba(0,0,0,0.08);
  --shadow-hover: 0 4px 16px rgba(0,0,0,0.12);
  --success: #52c41a;
  --warning: #faad14;
  --danger: #ff4d4f;
  --radius: 12px;
  --transition: all 0.2s ease;
}

* { margin: 0; padding: 0; box-sizing: border-box; }

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  background: var(--bg);
  color: var(--text);
  line-height: 1.6;
  min-height: 100vh;
}

/* Header */
.header {
  background: linear-gradient(135deg, #4A90D9 0%, #357ABD 100%);
  color: white;
  padding: 24px 20px;
  text-align: center;
  position: sticky;
  top: 0;
  z-index: 100;
  box-shadow: 0 2px 12px rgba(74,144,217,0.3);
}
.header h1 { font-size: 1.5rem; margin-bottom: 4px; }
.header .subtitle { font-size: 0.85rem; opacity: 0.85; }

/* Navigation tabs */
.nav-tabs {
  display: flex;
  gap: 8px;
  padding: 12px 20px;
  overflow-x: auto;
  background: white;
  border-bottom: 1px solid var(--border);
  position: sticky;
  top: 100px;
  z-index: 99;
  scrollbar-width: none;
}
.nav-tabs::-webkit-scrollbar { display: none; }
.nav-tab {
  padding: 6px 16px;
  border-radius: 20px;
  border: 1px solid var(--border);
  background: white;
  cursor: pointer;
  font-size: 0.85rem;
  white-space: nowrap;
  transition: var(--transition);
}
.nav-tab:hover { border-color: var(--primary); color: var(--primary); }
.nav-tab.active { background: var(--primary); color: white; border-color: var(--primary); }

/* Alphabet index */
.alpha-index {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
  padding: 10px 20px;
  background: white;
  border-bottom: 1px solid var(--border);
  position: sticky;
  top: 148px;
  z-index: 98;
  justify-content: center;
}
.alpha-btn {
  width: 30px;
  height: 30px;
  border-radius: 6px;
  border: 1px solid var(--border);
  background: white;
  cursor: pointer;
  font-size: 0.8rem;
  font-weight: 600;
  transition: var(--transition);
  display: flex;
  align-items: center;
  justify-content: center;
}
.alpha-btn:hover { background: var(--primary); color: white; border-color: var(--primary); }
.alpha-btn.empty { opacity: 0.3; cursor: default; }
.alpha-btn.empty:hover { background: white; color: var(--text); border-color: var(--border); }

/* Stats bar */
.stats-bar {
  display: flex;
  gap: 16px;
  padding: 12px 20px;
  background: white;
  border-bottom: 1px solid var(--border);
  font-size: 0.85rem;
  color: var(--text-light);
  flex-wrap: wrap;
}
.stat-item { display: flex; align-items: center; gap: 4px; }
.stat-value { color: var(--primary); font-weight: 600; }

/* Main content */
.container {
  max-width: 900px;
  margin: 0 auto;
  padding: 20px;
}

/* Word card */
.word-card {
  background: var(--card-bg);
  border-radius: var(--radius);
  padding: 16px 20px;
  margin-bottom: 10px;
  box-shadow: var(--shadow);
  transition: var(--transition);
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 14px;
  position: relative;
}
.word-card:hover {
  box-shadow: var(--shadow-hover);
  transform: translateY(-1px);
}
.word-card .word-num {
  color: var(--text-light);
  font-size: 0.8rem;
  min-width: 30px;
  text-align: right;
}
.word-card .word-main {
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--primary-dark);
  min-width: 120px;
  cursor: pointer;
}
.word-card .word-phonetic {
  font-size: 0.85rem;
  color: var(--text-light);
  min-width: 100px;
}
.word-card .word-pos {
  font-size: 0.8rem;
  color: var(--primary);
  background: rgba(74,144,217,0.1);
  padding: 2px 8px;
  border-radius: 10px;
  font-style: italic;
}
.word-card .word-meaning {
  flex: 1;
  font-size: 0.9rem;
  color: var(--text);
  line-height: 1.5;
}
.word-card .word-source {
  font-size: 0.75rem;
  color: var(--text-light);
  background: #f0f0f0;
  padding: 2px 8px;
  border-radius: 10px;
  white-space: nowrap;
}

/* Audio button */
.audio-btn {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  border: 2px solid var(--primary);
  background: white;
  cursor: pointer;
  font-size: 1rem;
  transition: var(--transition);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}
.audio-btn:hover { background: var(--primary); }
.audio-btn:active { transform: scale(0.9); }
.audio-btn.speaking { background: var(--primary); animation: pulse 0.6s infinite; }

@keyframes pulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.15); }
}

/* Bookmark */
.bookmark-btn {
  width: 32px;
  height: 32px;
  border: none;
  background: transparent;
  cursor: pointer;
  font-size: 1.2rem;
  transition: var(--transition);
  flex-shrink: 0;
}
.bookmark-btn.bookmarked { color: var(--warning); }

/* Section header */
.section-header {
  font-size: 1.2rem;
  font-weight: 700;
  color: var(--primary-dark);
  padding: 16px 0 8px;
  margin-top: 16px;
  border-bottom: 2px solid var(--primary);
  display: flex;
  align-items: center;
  gap: 8px;
}
.section-header .badge {
  font-size: 0.75rem;
  background: var(--primary);
  color: white;
  padding: 2px 10px;
  border-radius: 10px;
  font-weight: 400;
}

/* Review panel */
.review-panel {
  position: fixed;
  bottom: 20px;
  right: 20px;
  z-index: 200;
}
.review-btn {
  width: 56px;
  height: 56px;
  border-radius: 50%;
  background: var(--primary);
  color: white;
  border: none;
  cursor: pointer;
  font-size: 1.5rem;
  box-shadow: 0 4px 12px rgba(74,144,217,0.4);
  transition: var(--transition);
  position: relative;
}
.review-btn:hover { transform: scale(1.1); }
.review-btn .count {
  position: absolute;
  top: -4px;
  right: -4px;
  background: var(--danger);
  color: white;
  font-size: 0.7rem;
  width: 22px;
  height: 22px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
}

/* Modal */
.modal-overlay {
  display: none;
  position: fixed;
  top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(0,0,0,0.5);
  z-index: 300;
  justify-content: center;
  align-items: center;
}
.modal-overlay.show { display: flex; }
.modal {
  background: white;
  border-radius: var(--radius);
  width: 90%;
  max-width: 500px;
  max-height: 80vh;
  overflow-y: auto;
  box-shadow: 0 8px 32px rgba(0,0,0,0.2);
}
.modal-header {
  padding: 16px 20px;
  border-bottom: 1px solid var(--border);
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: sticky;
  top: 0;
  background: white;
  border-radius: var(--radius) var(--radius) 0 0;
}
.modal-header h3 { font-size: 1.1rem; }
.modal-close {
  width: 32px; height: 32px;
  border: none; background: #f0f0f0;
  border-radius: 50%; cursor: pointer;
  font-size: 1rem; transition: var(--transition);
}
.modal-close:hover { background: #ddd; }
.modal-body { padding: 16px 20px; }
.modal-body .word-card { box-shadow: none; border: 1px solid var(--border); }

/* Daily practice link */
.daily-link {
  display: inline-block;
  margin: 8px 0;
  padding: 8px 16px;
  background: var(--primary);
  color: white;
  border-radius: 20px;
  text-decoration: none;
  font-size: 0.85rem;
  transition: var(--transition);
}
.daily-link:hover { background: var(--primary-dark); }

/* Search */
.search-box {
  width: 100%;
  padding: 10px 16px;
  border: 2px solid var(--border);
  border-radius: 24px;
  font-size: 0.95rem;
  outline: none;
  transition: var(--transition);
  margin-bottom: 16px;
}
.search-box:focus { border-color: var(--primary); }

/* No results */
.no-results {
  text-align: center;
  padding: 40px;
  color: var(--text-light);
}

/* Mobile adjustments */
@media (max-width: 600px) {
  .header h1 { font-size: 1.2rem; }
  .word-card { flex-wrap: wrap; gap: 8px; padding: 12px 14px; }
  .word-card .word-main { min-width: auto; }
  .word-card .word-meaning { flex-basis: 100%; }
  .nav-tabs { top: 86px; }
  .alpha-index { top: 134px; }
}

/* Flashcard mode */
.flashcard-mode .word-card .word-meaning { display: none; }
.flashcard-mode .word-card.reveal .word-meaning { display: block; }

/* Tab content */
.tab-content { display: none; }
.tab-content.active { display: block; }
</style>
</head>
<body>

<div class="header">
  <h1>📚 人教版英语词汇表</h1>
  <div class="subtitle">七年级上 · 七年级下 · 八年级上 · 八年级下</div>
</div>

<div class="nav-tabs" id="navTabs">
  <button class="nav-tab active" data-tab="by-textbook">按教材</button>
  <button class="nav-tab" data-tab="by-alphabet">按字母</button>
  <button class="nav-tab" data-tab="daily">每日练习</button>
  <button class="nav-tab" data-tab="flashcard">闪卡模式</button>
  <button class="nav-tab" data-tab="review">我的收藏</button>
</div>

<div class="stats-bar">
  <div class="stat-item">📖 总词汇: <span class="stat-value" id="statTotal">0</span></div>
  <div class="stat-item">📅 练习天数: <span class="stat-value" id="statDays">0</span></div>
  <div class="stat-item">⭐ 收藏: <span class="stat-value" id="statBookmarks">0</span></div>
  <div class="stat-item">📝 今日进度: <span class="stat-value" id="statProgress">-</span></div>
</div>

<div class="container">

  <!-- Textbook tab -->
  <div class="tab-content active" id="tab-by-textbook">
    <input type="text" class="search-box" id="searchTextbook" placeholder="🔍 搜索单词...">
    <div id="textbookContent"></div>
  </div>

  <!-- Alphabet tab -->
  <div class="tab-content" id="tab-by-alphabet">
    <div class="alpha-index" id="alphaIndex"></div>
    <input type="text" class="search-box" id="searchAlpha" placeholder="🔍 搜索单词...">
    <div id="alphaContent"></div>
  </div>

  <!-- Daily tab -->
  <div class="tab-content" id="tab-daily">
    <h2 style="margin-bottom:16px;">📅 每日练习计划</h2>
    <p style="color:var(--text-light);margin-bottom:16px;">
      共 <strong>{total_days}</strong> 天，每天约 <strong>30分钟</strong>（15分钟默写 + 10分钟听写 + 5分钟复习）<br>
      采用艾宾浩斯遗忘曲线科学复习
    </p>
    <input type="number" class="search-box" id="daySelector" placeholder="输入天数 (1-{total_days})" min="1" max="{total_days}" style="max-width:200px;">
    <button onclick="showDayWords()" style="padding:8px 16px;background:var(--primary);color:white;border:none;border-radius:8px;cursor:pointer;">查看当天单词</button>
    <div id="dailyContent" style="margin-top:16px;"></div>
  </div>

  <!-- Flashcard tab -->
  <div class="tab-content flashcard-mode" id="tab-flashcard">
    <p style="color:var(--text-light);margin-bottom:16px;">点击卡片显示中文释义，测试你的记忆！</p>
    <div id="flashcardContent"></div>
  </div>

  <!-- Review tab -->
  <div class="tab-content" id="tab-review">
    <h2 style="margin-bottom:16px;">⭐ 我的收藏</h2>
    <div id="reviewContent">
      <p class="no-results" id="reviewEmpty">还没有收藏单词，点击单词旁的 ☆ 按钮收藏吧！</p>
    </div>
  </div>

</div>

<div class="review-panel">
  <button class="review-btn" onclick="openReview()" title="我的收藏">
    ⭐<span class="count" id="reviewCount">0</span>
  </button>
</div>

<script>
// ========== DATA ==========
const ALL_WORDS = {all_words_json};
const DAILY_PLAN = {daily_plan_json};
const TOTAL_DAYS = {total_days};

// ========== TTS ==========
function speakWord(word) {{
  if (!('speechSynthesis' in window)) return;
  speechSynthesis.cancel();
  const utter = new SpeechSynthesisUtterance(word);
  utter.lang = 'en-US';
  utter.rate = 0.85;
  utter.pitch = 1;
  speechSynthesis.speak(utter);
}}

// ========== BOOKMARKS ==========
function getBookmarks() {{
  try {{ return JSON.parse(localStorage.getItem('vocab_bookmarks') || '[]'); }}
  catch(e) {{ return []; }}
}}

function toggleBookmark(word) {{
  let bookmarks = getBookmarks();
  const idx = bookmarks.indexOf(word);
  if (idx >= 0) bookmarks.splice(idx, 1);
  else bookmarks.push(word);
  localStorage.setItem('vocab_bookmarks', JSON.stringify(bookmarks));
  updateBookmarkUI();
  renderCurrentTab();
}}

function isBookmarked(word) {{
  return getBookmarks().includes(word);
}}

function updateBookmarkUI() {{
  const count = getBookmarks().length;
  document.getElementById('reviewCount').textContent = count;
  document.getElementById('statBookmarks').textContent = count;
}}

// ========== RENDER WORD CARD ==========
function createWordCard(w, index) {{
  const bookmarked = isBookmarked(w.word);
  return `
    <div class="word-card" id="word-${{index}}">
      <span class="word-num">${{index + 1}}</span>
      <span class="word-main" onclick="speakWord('${{w.word.replace(/'/g, "\\'")}}')" title="点击发音">${{w.word}}</span>
      <span class="word-phonetic">${{w.phonetic || ''}}</span>
      <span class="word-pos">${{w.pos || ''}}</span>
      <span class="word-meaning">${{w.meaning}}</span>
      <span class="word-source">${{w.source}}</span>
      <button class="audio-btn" onclick="speakWord('${{w.word.replace(/'/g, "\\'")}}')" title="发音">🔊</button>
      <button class="bookmark-btn ${{bookmarked ? 'bookmarked' : ''}}" onclick="toggleBookmark('${{w.word.replace(/'/g, "\\'")}}')">${{bookmarked ? '⭐' : '☆'}}</button>
    </div>`;
}}

// ========== RENDER TEXTBOOK VIEW ==========
function renderTextbook(words) {{
  const container = document.getElementById('textbookContent');
  if (!words || words.length === 0) {{
    container.innerHTML = '<p class="no-results">没有找到匹配的单词</p>';
    return;
  }}
  
  // Group by source
  const groups = {{}};
  words.forEach(w => {{
    const src = w.source;
    if (!groups[src]) groups[src] = [];
    groups[src].push(w);
  }});
  
  let html = '';
  for (const [src, groupWords] of Object.entries(groups)) {{
    html += `<div class="section-header">📘 ${{src}} <span class="badge">${{groupWords.length}} 词</span></div>`;
    groupWords.forEach((w, i) => {{
      html += createWordCard(w, words.indexOf(w));
    }});
  }}
  container.innerHTML = html;
}}

// ========== RENDER ALPHABET VIEW ==========
function renderAlphabetIndex() {{
  const letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'.split('');
  const container = document.getElementById('alphaIndex');
  const hasWords = {{}};
  ALL_WORDS.forEach(w => {{
    const l = (w.word[0] || '#').toUpperCase();
    if (l >= 'A' && l <= 'Z') hasWords[l] = true;
  }});
  let html = '';
  letters.forEach(l => {{
    const cls = hasWords[l] ? '' : 'empty';
    html += `<button class="alpha-btn ${{cls}}" onclick="${{hasWords[l] ? "scrollToLetter('"+l+"')" : ""}}">${{l}}</button>`;
  }});
  container.innerHTML = html;
}}

function scrollToLetter(letter) {{
  const el = document.getElementById('letter-' + letter);
  if (el) el.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
}}

function renderAlphabet(words) {{
  const container = document.getElementById('alphaContent');
  if (!words || words.length === 0) {{
    container.innerHTML = '<p class="no-results">没有找到匹配的单词</p>';
    return;
  }}
  
  const groups = {{}};
  words.forEach(w => {{
    const l = (w.word[0] || '#').toUpperCase();
    if (!groups[l]) groups[l] = [];
    groups[l].push(w);
  }});
  
  let html = '';
  const sortedLetters = Object.keys(groups).sort();
  sortedLetters.forEach(l => {{
    html += `<div class="section-header" id="letter-${{l}}">${{l}} <span class="badge">${{groups[l].length}} 词</span></div>`;
    groups[l].forEach((w, i) => {{
      html += createWordCard(w, words.indexOf(w));
    }});
  }});
  container.innerHTML = html;
}}

// ========== DAILY PRACTICE ==========
function showDayWords() {{
  const dayInput = document.getElementById('daySelector');
  const day = parseInt(dayInput.value);
  if (isNaN(day) || day < 1 || day > TOTAL_DAYS) {{
    alert('请输入有效天数 (1-' + TOTAL_DAYS + ')');
    return;
  }}
  
  const dayData = DAILY_PLAN[day - 1];
  const container = document.getElementById('dailyContent');
  
  let html = `<h3 style="margin-bottom:8px;">第 ${{day}} 天</h3>`;
  html += `<p style="color:var(--text-light);margin-bottom:12px;">新词: ${{dayData.new_count}} 个`;
  if (dayData.review_days.length > 0) {{
    html += ` | 复习: 第${{dayData.review_days.join(',')}}天 (${{dayData.review_count}} 个)`;
  }}
  html += `</p>`;
  html += `<p style="color:var(--text-light);margin-bottom:16px;">📖 来源: ${{dayData.source_books.join(', ')}}</p>`;
  
  if (dayData.review_days.length > 0) {{
    html += `<details style="margin-bottom:12px;"><summary style="cursor:pointer;color:var(--warning);">📝 复习词 (${{dayData.review_count}})</summary>`;
    dayData.review_words.forEach((w, i) => {{
      html += createWordCard(w, i);
    }});
    html += `</details>`;
  }}
  
  html += `<div class="section-header">🆕 新词 <span class="badge">${{dayData.new_count}} 词</span></div>`;
  dayData.new_words.forEach((w, i) => {{
    html += createWordCard(w, i);
  }});
  
  html += `<div style="margin-top:16px;padding:12px;background:#f0f7ff;border-radius:8px;font-size:0.85rem;">
    <strong>⏱️ 今日练习安排（约30分钟）：</strong><br>
    ① 默写（15分钟）— 看中文写英文<br>
    ② 听写（10分钟）— 听英文写中文<br>
    ③ 批改复习（5分钟）— 对照答案，重点记忆错误单词
  </div>`;
  
  container.innerHTML = html;
}}

// ========== FLASHCARD MODE ==========
function renderFlashcard() {{
  const container = document.getElementById('flashcardContent');
  // Randomize words
  const shuffled = [...ALL_WORDS].sort(() => Math.random() - 0.5).slice(0, 50);
  let html = '<p style="margin-bottom:12px;">点击卡片显示释义，点击 🔊 发音</p>';
  shuffled.forEach((w, i) => {{
    html += `
      <div class="word-card" onclick="this.classList.toggle('reveal')" style="cursor:pointer;">
        <span class="word-num">${{i + 1}}</span>
        <span class="word-main">${{w.word}}</span>
        <span class="word-phonetic">${{w.phonetic || ''}}</span>
        <span class="word-pos">${{w.pos || ''}}</span>
        <span class="word-meaning">${{w.meaning}}</span>
        <button class="audio-btn" onclick="event.stopPropagation();speakWord('${{w.word.replace(/'/g, "\\'")}}')">🔊</button>
        <button class="bookmark-btn ${{isBookmarked(w.word) ? 'bookmarked' : ''}}" onclick="event.stopPropagation();toggleBookmark('${{w.word.replace(/'/g, "\\'")}}')">${{isBookmarked(w.word) ? '⭐' : '☆'}}</button>
      </div>`;
  }});
  container.innerHTML = html;
}}

// ========== REVIEW ==========
function renderReview() {{
  const bookmarks = getBookmarks();
  const container = document.getElementById('reviewContent');
  const empty = document.getElementById('reviewEmpty');
  
  if (bookmarks.length === 0) {{
    container.innerHTML = '<p class="no-results">还没有收藏单词，点击单词旁的 ☆ 按钮收藏吧！</p>';
    return;
  }}
  
  const reviewWords = ALL_WORDS.filter(w => bookmarks.includes(w.word));
  let html = '';
  reviewWords.forEach((w, i) => {{
    html += createWordCard(w, i);
  }});
  container.innerHTML = html;
}}

// ========== TAB SWITCHING ==========
let currentTab = 'by-textbook';

function switchTab(tabName) {{
  currentTab = tabName;
  document.querySelectorAll('.nav-tab').forEach(t => t.classList.remove('active'));
  document.querySelector(`[data-tab="${{tabName}}"]`).classList.add('active');
  document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
  document.getElementById('tab-' + tabName).classList.add('active');
  
  if (tabName === 'by-alphabet') renderAlphabet(ALL_WORDS);
  if (tabName === 'by-textbook') renderTextbook(ALL_WORDS);
  if (tabName === 'flashcard') renderFlashcard();
  if (tabName === 'review') renderReview();
}}

function renderCurrentTab() {{
  if (currentTab === 'by-textbook') renderTextbook(ALL_WORDS);
  if (currentTab === 'by-alphabet') renderAlphabet(ALL_WORDS);
  if (currentTab === 'flashcard') renderFlashcard();
  if (currentTab === 'review') renderReview();
}}

// ========== SEARCH ==========
document.addEventListener('DOMContentLoaded', () => {{
  // Nav tabs
  document.querySelectorAll('.nav-tab').forEach(tab => {{
    tab.addEventListener('click', () => switchTab(tab.dataset.tab));
  }});
  
  // Search for textbook tab
  document.getElementById('searchTextbook').addEventListener('input', (e) => {{
    const q = e.target.value.toLowerCase().trim();
    if (!q) {{ renderTextbook(ALL_WORDS); return; }}
    const filtered = ALL_WORDS.filter(w =>
      w.word.toLowerCase().includes(q) || w.meaning.includes(q)
    );
    renderTextbook(filtered);
  }});
  
  // Search for alphabet tab
  document.getElementById('searchAlpha').addEventListener('input', (e) => {{
    const q = e.target.value.toLowerCase().trim();
    if (!q) {{ renderAlphabet(ALL_WORDS); return; }}
    const filtered = ALL_WORDS.filter(w =>
      w.word.toLowerCase().includes(q) || w.meaning.includes(q)
    );
    renderAlphabet(filtered);
  }});
  
  // Initialize
  renderTextbook(ALL_WORDS);
  renderAlphabetIndex();
  updateBookmarkUI();
  document.getElementById('statTotal').textContent = ALL_WORDS.length;
  document.getElementById('statDays').textContent = TOTAL_DAYS;
}});
</script>

</body>
</html>'''.replace('{total_days}', str(len(plan))))

# Write HTML
output_path = r'C:\Users\Admin\WorkBuddy\Claw\vocab_html_output\index.html'
os.makedirs(os.path.dirname(output_path), exist_ok=True)

# Write with data embedded
html_str = html_parts[0]
html_str = html_str.replace('{all_words_json}', json.dumps(words, ensure_ascii=False))
html_str = html_str.replace('{daily_plan_json}', json.dumps(plan, ensure_ascii=False))
html_str = html_str.replace('{total_days}', str(len(plan)))

with open(output_path, 'w', encoding='utf-8') as f:
    f.write(html_str)

print(f"HTML generated: {output_path}")
print(f"File size: {os.path.getsize(output_path) / 1024:.0f} KB")
print(f"Words: {len(words)}")
print(f"Daily plan: {len(plan)} days")
