const fs = require('fs');

const css = `:root{--primary:#1677FF;--primary-dark:#0958D9;--primary-light:#E6F0FF;--success:#00B96B;--success-light:#F6FFED;--warning:#FA8C16;--warning-light:#FFF7E6;--danger:#FF4D4F;--danger-light:#FFF1F0;--bg:#F5F7FA;--card:#FFF;--text:#1A1A1A;--sub:#666;--muted:#999;--border:#E8E8E8;--border-light:#F0F0F0;--radius:12px;--shadow:0 2px 12px rgba(0,0,0,.06)}
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC","Microsoft YaHei",sans-serif;background:var(--bg);color:var(--text);font-size:15px;line-height:1.6;-webkit-font-smoothing:antialiased;min-height:100vh}
.header{background:linear-gradient(135deg,#1677FF,#4096FF);color:#FFF;padding:14px 16px 10px;position:sticky;top:0;z-index:100;box-shadow:0 2px 8px rgba(22,119,255,.2)}
.header-title{font-size:18px;font-weight:700;margin-bottom:10px}
.role-switch{display:flex;gap:4px;background:rgba(255,255,255,.2);border-radius:8px;padding:3px;width:fit-content}
.role-btn{padding:6px 16px;border-radius:6px;font-size:13px;font-weight:500;cursor:pointer;border:none;background:transparent;color:rgba(255,255,255,.8);transition:all .2s}
.role-btn.active{background:#FFF;color:var(--primary);font-weight:600}
.date-bar{display:flex;align-items:center;gap:10px;background:var(--card);border-radius:var(--radius);padding:10px 16px;margin:12px 12px 0;box-shadow:var(--shadow)}
.date-nav{width:34px;height:34px;border-radius:50%;border:none;background:var(--primary-light);color:var(--primary);font-size:18px;cursor:pointer;display:flex;align-items:center;justify-content:center;transition:transform .1s}
.date-nav:active{transform:scale(.9)}
.date-display{text-align:center;flex:1}
.date-display .date-main{font-size:16px;font-weight:600}
.date-display .date-sub{font-size:12px;color:var(--muted)}
#app{padding:12px;padding-bottom:100px;max-width:720px;margin:0 auto}
.name-bar{display:flex;align-items:center;gap:10px;background:var(--card);border-radius:var(--radius);padding:10px 16px;margin-top:12px;box-shadow:var(--shadow)}
.name-bar .name-label{font-size:14px;color:var(--sub);white-space:nowrap}
.name-bar input{flex:1;border:1.5px solid var(--border);border-radius:8px;padding:8px 12px;font-size:15px;background:var(--bg);color:var(--text);outline:none;transition:border-color .2s}
.name-bar input:focus{border-color:var(--primary);background:#FFF}
.session-block{background:var(--card);border-radius:var(--radius);margin-top:12px;box-shadow:var(--shadow);overflow:hidden}
.session-header{display:flex;align-items:center;justify-content:space-between;padding:14px 16px;border-bottom:1px solid var(--border-light)}
.session-header-left{display:flex;align-items:center;gap:10px}
.session-icon{width:36px;height:36px;border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:20px}
.session-icon.morning{background:linear-gradient(135deg,#FFF7E6,#FFE7BA)}
.session-icon.afternoon{background:linear-gradient(135deg,#FFF1F0,#FFCCC7)}
.session-icon.evening{background:linear-gradient(135deg,#F0F5FF,#D6E4FF)}
.session-title{font-size:16px;font-weight:600}
.add-btn{padding:5px 12px;border:1.5px solid var(--primary);border-radius:6px;background:var(--primary-light);color:var(--primary-dark);font-size:13px;font-weight:600;cursor:pointer;transition:all .2s}
.add-btn:active{transform:scale(.96)}
.project-item{background:var(--bg);margin:12px;border-radius:10px;padding:14px;border:1.5px solid var(--border-light)}
.project-item:not(:first-child){margin-top:8px}
.project-item-header{display:flex;align-items:center;justify-content:space-between;margin-bottom:12px}
.project-num{font-size:14px;font-weight:700;color:var(--primary)}
.del-btn{font-size:13px;cursor:pointer;opacity:.6;transition:opacity .15s;background:none;border:none}
.del-btn:hover{opacity:1}
.time-row{display:flex;align-items:center;gap:8px;background:#FFF;border-radius:8px;padding:8px 12px;margin-bottom:12px}
.time-row .tl{font-size:13px;color:var(--sub);white-space:nowrap;font-weight:500}
.time-row input[type=time]{border:1.5px solid var(--border);border-radius:6px;padding:5px 8px;font-size:14px;color:var(--text);background:#FFF;flex:1;min-width:0}
.time-row input[type=time]:focus{outline:none;border-color:var(--primary)}
.time-arrow{color:var(--muted);font-size:13px}
.time-dur{font-size:13px;color:var(--primary);font-weight:600;white-space:nowrap;min-width:55px;text-align:right}
.form-field{margin-bottom:12px}
.form-field:last-child{margin-bottom:0}
.field-label{font-size:13px;font-weight:600;color:var(--sub);margin-bottom:5px;display:flex;align-items:center;gap:4px}
.field-label .req{color:var(--danger);font-size:11px}
textarea{width:100%;border:1.5px solid var(--border);border-radius:8px;padding:8px 12px;font-size:14px;color:var(--text);background:var(--bg);resize:vertical;min-height:65px;line-height:1.5;font-family:inherit;outline:none;transition:border-color .2s}
textarea:focus{border-color:var(--primary);background:#FFF}
.subjects{display:flex;flex-wrap:wrap;gap:7px}
.sub-tag{padding:5px 13px;border:1.5px solid var(--border);border-radius:20px;background:var(--bg);font-size:13px;color:var(--sub);cursor:pointer;transition:all .2s;user-select:none}
.sub-tag.active{border-color:var(--primary);background:var(--primary-light);color:var(--primary-dark);font-weight:600}
.sub-tag:active{transform:scale(.95)}
.ratings{display:flex;gap:8px}
.rating-btn{flex:1;padding:7px 4px;border:1.5px solid var(--border);border-radius:8px;background:var(--bg);font-size:13px;color:var(--sub);cursor:pointer;transition:all .2s;text-align:center;font-weight:500}
.rating-btn.active{border-color:var(--primary);background:var(--primary-light);color:var(--primary-dark);font-weight:600}
.rating-btn:active{transform:scale(.96)}
#bottomBar{position:fixed;bottom:0;left:0;right:0;background:#FFF;border-top:1px solid var(--border-light);padding:10px 16px;display:flex;gap:10px;z-index:100;box-shadow:0 -2px 12px rgba(0,0,0,.06);max-width:720px;margin:0 auto}
#bottomBar .btn{flex:1;height:44px;border-radius:10px;border:none;font-size:14px;font-weight:600;cursor:pointer;transition:all .15s;display:flex;align-items:center;justify-content:center;gap:6px}
.btn:active{transform:scale(.97)}
.btn-outline{background:var(--bg);color:var(--text);border:1.5px solid var(--border)}
.btn-primary{background:var(--primary);color:#FFF}
.btn-primary:disabled{background:#CCC;color:#FFF;cursor:not-allowed}
.btn-success{background:var(--success);color:#FFF}
.empty-msg{text-align:center;padding:32px;color:var(--muted);font-size:14px}
.modal-overlay{position:fixed;inset:0;background:rgba(0,0,0,.5);z-index:200;display:none;align-items:flex-end;justify-content:center}
.modal-overlay.show{display:flex}
.modal{background:#FFF;border-radius:20px 20px 0 0;width:100%;max-width:720px;max-height:85vh;display:flex;flex-direction:column;animation:slideUp .3s ease}
@keyframes slideUp{from{transform:translateY(100%)}to{transform:translateY(0)}}
.modal-header{display:flex;align-items:center;justify-content:space-between;padding:16px 20px;border-bottom:1px solid var(--border-light)}
.modal-title{font-size:18px;font-weight:700}
.modal-close{width:32px;height:32px;border-radius:50%;border:none;background:var(--bg);color:var(--muted);font-size:18px;cursor:pointer;display:flex;align-items:center;justify-content:center}
.modal-body{flex:1;overflow-y:auto;padding:16px 20px}
.preview{background:var(--bg);border-radius:var(--radius);padding:14px;font-size:14px;line-height:1.8;color:var(--text);white-space:pre-wrap;word-break:break-all;border:1px solid var(--border-light);font-family:-apple-system,"PingFang SC","Microsoft YaHei",sans-serif}
.modal-footer{padding:12px 20px;border-top:1px solid var(--border-light);display:flex;gap:10px}
.modal-footer .btn{flex:1;height:44px;border-radius:10px;border:none;font-size:14px;font-weight:600;cursor:pointer}
.modal-footer .btn:active{transform:scale(.97)}
.toast{position:fixed;top:50%;left:50%;transform:translate(-50%,-50%);background:rgba(0,0,0,.75);color:#FFF;padding:12px 24px;border-radius:10px;font-size:15px;z-index:300;opacity:0;transition:opacity .25s;pointer-events:none;white-space:nowrap}
.toast.show{opacity:1}
.stat-bar{display:flex;gap:10px;margin:12px 12px 0}
.stat-chip{flex:1;background:var(--card);border-radius:var(--radius);padding:12px;box-shadow:var(--shadow);text-align:center}
.stat-val{font-size:22px;font-weight:700;color:var(--primary)}
.stat-val.green{color:var(--success)}
.stat-lbl{font-size:12px;color:var(--muted);margin-top:2px}
.member-list{display:flex;flex-direction:column;gap:10px;margin-top:12px}
.member-card{background:var(--card);border-radius:var(--radius);padding:14px;box-shadow:var(--shadow)}
.member-card.done{border:2px solid var(--success)}
.member-card.partial{border:2px solid var(--warning)}
.member-card.empty{border:2px solid var(--border-light)}
.member-top{display:flex;align-items:center;justify-content:space-between}
.member-name{font-size:16px;font-weight:700}
.badge{padding:2px 10px;border-radius:12px;font-size:12px;font-weight:600}
.badge.done{background:var(--success-light);color:var(--success)}
.badge.partial{background:var(--warning-light);color:var(--warning)}
.badge.empty{background:var(--danger-light);color:var(--danger)}
.member-detail{margin-top:10px;padding-top:10px;border-top:1px solid var(--border-light);display:none}
.member-card.expanded .member-detail{display:block}
.detail-session{background:var(--bg);border-radius:8px;padding:10px 12px;margin-bottom:8px}
.detail-session-title{font-size:13px;font-weight:600;color:var(--primary);margin-bottom:4px}
.detail-row{font-size:13px;color:var(--sub);line-height:1.6}
.detail-row span{color:var(--text)}
.history-list{display:flex;flex-direction:column;gap:10px;margin-top:12px}
.history-item{background:var(--card);border-radius:var(--radius);padding:14px;box-shadow:var(--shadow);cursor:pointer;transition:all .15s}
.history-item:active{transform:scale(.98)}
.history-top{display:flex;align-items:center;justify-content:space-between}
.history-date{font-size:16px;font-weight:700}
.history-sessions{display:flex;gap:6px;margin-top:8px}
.history-dot{width:10px;height:10px;border-radius:50%;background:var(--border)}
.history-dot.active{background:var(--success)}
.history-summary{font-size:13px;color:var(--sub);margin-top:6px;line-height:1.5;overflow:hidden;text-overflow:ellipsis;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical}
.empty-state{text-align:center;padding:60px 20px;color:var(--muted)}
.empty-state .empty-icon{font-size:48px;margin-bottom:12px}
.empty-state .empty-text{font-size:15px}
.data-actions{display:flex;gap:8px;margin:12px 12px 0}
.data-btn{flex:1;padding:10px;border:1.5px solid var(--border);border-radius:8px;background:var(--card);font-size:13px;color:var(--sub);cursor:pointer;display:flex;align-items:center;justify-content:center;gap:6px;box-shadow:var(--shadow);transition:all .2s}
.data-btn:active{transform:scale(.97)}
.data-btn.import{border-color:var(--primary);color:var(--primary)}
.teacher-bar{display:flex;align-items:center;gap:10px;background:var(--card);border-radius:var(--radius);padding:10px 16px;margin-top:12px;box-shadow:var(--shadow)}
.teacher-bar .teacher-label{font-size:14px;color:var(--sub);white-space:nowrap}
.teacher-bar input{flex:1;border:1.5px solid var(--border);border-radius:8px;padding:8px 12px;font-size:15px;background:var(--bg);color:var(--text);outline:none}
.teacher-bar input:focus{border-color:var(--primary);background:#FFF}
@media(max-width:480px){#app{padding:10px}.header-title{font-size:16px}}
`;

const js = `
var currentRole = 'parent';
var currentTab = 'checkin';
var currentDate = formatDate(new Date());
var SUBJECTS = ['语文','数学','英语','科学','文综'];
var SESSIONS = [
  { key: 'morning', label: '上午', icon: '🌅' },
  { key: 'afternoon', label: '下午', icon: '☀️' },
  { key: 'evening', label: '晚上', icon: '🌙' }
];
var RATINGS = [
  { value: 'great', label: '很好' },
  { value: 'good', label: '还行' },
  { value: 'normal', label: '一般' }
];
var RATING_MAP = { great: '很好', good: '还行', normal: '一般' };

function formatDate(d) {
  var y = d.getFullYear();
  var m = String(d.getMonth() + 1).padStart(2, '0');
  var day = String(d.getDate()).padStart(2, '0');
  return y + '-' + m + '-' + day;
}

function formatDateCN(d) {
  var parts = d.split('-');
  return parseInt(parts[1], 10) + '月' + parseInt(parts[2], 10) + '日';
}

function calcMins(s, e) {
  if (!s || !e) return 0;
  var ps = s.split(':'), pe = e.split(':');
  return (parseInt(pe[0], 10) * 60 + parseInt(pe[1], 10)) - (parseInt(ps[0], 10) * 60 + parseInt(ps[1], 10));
}

function calcDuration(s, e) {
  var m = calcMins(s, e);
  if (m <= 0) return '';
  var h = Math.floor(m / 60), min = m % 60;
  return (h > 0 ? h + '小时' : '') + (min > 0 ? min + '分' : '');
}

function showToast(msg) {
  var t = document.getElementById('toast');
  t.textContent = msg;
  t.classList.add('show');
  setTimeout(function() { t.classList.remove('show'); }, 2200);
}

function esc(s) {
  if (!s) return '';
  return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}

function getStorageKey(date) { return 'studyCheckin_' + date; }
function getGroupKey(date, name) { return 'group_' + date + '_' + name; }

function createEmpty(date) {
  var data = { date: date, studentName: '', sessions: {} };
  SESSIONS.forEach(function(s) { data.sessions[s.key] = []; });
  return data;
}

function loadData(date) {
  var raw = localStorage.getItem(getStorageKey(date));
  if (raw) {
    try {
      var d = JSON.parse(raw);
      SESSIONS.forEach(function(s) {
        if (!d.sessions[s.key] || !Array.isArray(d.sessions[s.key])) d.sessions[s.key] = [];
      });
      return d;
    } catch(e) {}
  }
  return createEmpty(date);
}

function saveData() {
  var name = localStorage.getItem('studentName') || '';
  formData.studentName = name;
  localStorage.setItem(getStorageKey(currentDate), JSON.stringify(formData));
}

function updateGroupIndex(date, studentName) {
  var raw = localStorage.getItem('groupIndex');
  var idx = [];
  if (raw) { try { idx = JSON.parse(raw); } catch(e) { idx = []; } }
  var exists = false;
  for (var i = 0; i < idx.length; i++) {
    if (idx[i].date === date && idx[i].studentName === studentName) { exists = true; break; }
  }
  if (!exists) {
    idx.push({ date: date, studentName: studentName });
    localStorage.setItem('groupIndex', JSON.stringify(idx));
  }
}

function getGroupSubmissions(date) {
  var results = [];
  var raw = localStorage.getItem('groupIndex');
  if (!raw) return results;
  var idx;
  try { idx = JSON.parse(raw); } catch(e) { return results; }
  for (var i = 0; i < idx.length; i++) {
    if (idx[i].date === date) {
      var dataRaw = localStorage.getItem(getGroupKey(idx[i].date, idx[i].studentName));
      if (dataRaw) { try { results.push(JSON.parse(dataRaw)); } catch(e) {} }
    }
  }
  return results;
}

function switchRole(role) {
  currentRole = role;
  renderRoleButtons();
  currentTab = (role === 'parent') ? 'checkin' : 'collect';
  renderCurrentPage();
}

function renderRoleButtons() {
  var btns = document.querySelectorAll('.role-btn');
  for (var i = 0; i < btns.length; i++) {
    var r = btns[i].getAttribute('data-role');
    btns[i].classList.toggle('active', r === currentRole);
  }
}

function renderCurrentPage() {
  if (currentRole === 'parent') {
    if (currentTab === 'checkin') renderCheckinPage();
    else renderHistoryPage();
  } else {
    if (currentTab === 'collect') renderCollectPage();
    else renderCollectHistoryPage();
  }
}

function changeDate(delta) {
  var d = new Date(currentDate);
  d.setDate(d.getDate() + delta);
  currentDate = formatDate(d);
  renderCurrentPage();
}

function updateDateDisplay() {
  var main = document.getElementById('dateMain');
  var sub = document.getElementById('dateSub');
  if (main) main.textContent = formatDateCN(currentDate);
  if (sub) sub.textContent = currentDate;
}

var formData = null;

function isProjectFilled(p) {
  return !!(p.plan || p.completion || p.notes || p.startTime || p.endTime || (p.subjects && p.subjects.length > 0) || p.rating);
}

function countFilled(arr) {
  return arr.filter(function(p) { return isProjectFilled(p); }).length;
}

function renderHeader() {
  var html = '<div class="header">';
  html += '<div class="header-title">📚 学习打卡</div>';
  html += '<div class="role-switch">';
  html += '<button class="role-btn' + (currentRole === 'parent' ? ' active' : '') + '" data-role="parent" onclick="switchRole(\\'parent\\')">👨‍👩‍👧 家长填报</button>';
  html += '<button class="role-btn' + (currentRole === 'leader' ? ' active' : '') + '" data-role="leader" onclick="switchRole(\\'leader\\')">👩‍🏫 组长汇总</button>';
  html += '</div></div>';
  
  html += '<div class="date-bar">';
  html += '<button class="date-nav" onclick="changeDate(-1)">‹</button>';
  html += '<div class="date-display"><div class="date-main" id="dateMain"></div><div class="date-sub" id="dateSub"></div></div>';
  html += '<button class="date-nav" onclick="changeDate(1)">›</button>';
  html += '</div>';
  
  document.getElementById('app').innerHTML = html;
  updateDateDisplay();
}

function renderCheckinPage() {
  renderHeader();
  formData = loadData(currentDate);
  var studentName = localStorage.getItem('studentName') || formData.studentName || '';
  var container = document.getElementById('app');
  var bb = document.getElementById('bottomBar');

  var html = container.innerHTML;
  html += '<div class="name-bar"><span class="name-label">👤 学生</span>';
  html += '<input type="text" placeholder="请输入姓名" value="' + esc(studentName) + '" oninput="localStorage.setItem(\\'studentName\\',this.value)">';
  html += '</div>';

  SESSIONS.forEach(function(s) {
    var items = formData.sessions[s.key] || [];
    html += '<div class="session-block">';
    html += '<div class="session-header"><div class="session-header-left">';
    html += '<div class="session-icon ' + s.key + '">' + s.icon + '</div>';
    html += '<div class="session-title">' + s.label + '</div>';
    html += '</div><button class="add-btn" onclick="addProject(\\'' + s.key + '\\')">➕ 添加项目</button></div>';

    if (items.length === 0) {
      html += '<div class="empty-msg">暂无项目，点击上方「➕ 添加项目」开始填报</div>';
    } else {
      items.forEach(function(item, idx) {
        html += renderProjectItem(s.key, idx, item);
      });
    }
    html += '</div>';
  });

  container.innerHTML = html;
  var totalFilled = SESSIONS.reduce(function(acc, s) {
    return acc + countFilled(formData.sessions[s.key] || []);
  }, 0);

  bb.innerHTML = '<button class="btn btn-outline" onclick="saveDraft()">💾 保存草稿</button>' +
    '<button class="btn btn-success" ' + (totalFilled > 0 ? '' : ' disabled') + ' onclick="submitCheckin()">✔ 提交打卡</button>';
  bb.style.display = 'flex';
}

function renderProjectItem(sessionKey, idx, item) {
  var dur = calcDuration(item.startTime, item.endTime);
  var items = formData.sessions[sessionKey];
  var canDelete = items.length > 1;

  var html = '<div class="project-item" id="proj_' + sessionKey + '_' + idx + '">';
  html += '<div class="project-item-header"><span class="project-num">#' + (idx + 1) + '</span>';
  if (canDelete) html += '<button class="del-btn" onclick="removeProject(\\'' + sessionKey + '\\',' + idx + ')">🗑 删除</button>';
  html += '</div>';

  html += '<div class="time-row"><span class="tl">⏰</span>';
  html += '<input type="time" value="' + (item.startTime || '') + '" onchange="updateProject(\\'' + sessionKey + '\\',' + idx + ',\\'startTime\\',this.value)">';
  html += '<span class="time-arrow">→</span>';
  html += '<input type="time" value="' + (item.endTime || '') + '" onchange="updateProject(\\'' + sessionKey + '\\',' + idx + ',\\'endTime\\',this.value)">';
  html += '<span class="time-dur" id="dur_' + sessionKey + '_' + idx + '">' + (dur || '未填时间') + '</span></div>';

  html += '<div class="form-field"><div class="field-label">📝 学习计划 <span class="req">*</span></div>';
  html += '<textarea placeholder="如：完成数学第3章习题集…" onchange="updateProject(\\'' + sessionKey + '\\',' + idx + ',\\'plan\\',this.value)">' + esc(item.plan || '') + '</textarea></div>';

  html += '<div class="form-field"><div class="field-label">📚 涉及科目</div><div class="subjects">';
  SUBJECTS.forEach(function(sub) {
    var active = item.subjects && item.subjects.indexOf(sub) >= 0;
    html += '<span class="sub-tag' + (active ? ' active' : '') + '" onclick="toggleSubject(\\'' + sessionKey + '\\',' + idx + ',\\'' + sub + '\\')">' + sub + '</span>';
  });
  html += '</div></div>';

  html += '<div class="form-field"><div class="field-label">✅ 完成情况</div>';
  html += '<textarea placeholder="如：完成80%，第5题有难度…" onchange="updateProject(\\'' + sessionKey + '\\',' + idx + ',\\'completion\\',this.value)">' + esc(item.completion || '') + '</textarea></div>';

  html += '<div class="form-field"><div class="field-label">💡 学习效果</div><div class="ratings">';
  RATINGS.forEach(function(r) {
    html += '<button class="rating-btn' + (item.rating === r.value ? ' active' : '') + '" onclick="updateProject(\\'' + sessionKey + '\\',' + idx + ',\\'rating\\',\\'' + r.value + '\\')">' + r.label + '</button>';
  });
  html += '</div></div>';

  html += '<div class="form-field"><div class="field-label">💬 备注（可选）</div>';
  html += '<textarea placeholder="遇到的问题或心得…" onchange="updateProject(\\'' + sessionKey + '\\',' + idx + ',\\'notes\\',this.value)">' + esc(item.notes || '') + '</textarea></div>';

  html += '</div>';
  return html;
}

function addProject(sessionKey) {
  if (!formData.sessions[sessionKey]) formData.sessions[sessionKey] = [];
  formData.sessions[sessionKey].push({ startTime: '', endTime: '', plan: '', subjects: [], completion: '', rating: '', notes: '' });
  saveData(); renderCheckinPage();
}

function removeProject(sessionKey, idx) {
  formData.sessions[sessionKey].splice(idx, 1);
  saveData(); renderCheckinPage();
}

function updateProject(sessionKey, idx, field, value) {
  if (!formData.sessions[sessionKey]) formData.sessions[sessionKey] = [];
  if (!formData.sessions[sessionKey][idx]) return;
  formData.sessions[sessionKey][idx][field] = value;
  saveData();
  if (field === 'startTime' || field === 'endTime') {
    var el = document.getElementById('dur_' + sessionKey + '_' + idx);
    if (el) el.textContent = calcDuration(
      formData.sessions[sessionKey][idx].startTime,
      formData.sessions[sessionKey][idx].endTime
    ) || '未填时间';
  }
}

function toggleSubject(sessionKey, idx, sub) {
  var item = formData.sessions[sessionKey][idx];
  if (!item.subjects) item.subjects = [];
  var i = item.subjects.indexOf(sub);
  if (i >= 0) item.subjects.splice(i, 1); else item.subjects.push(sub);
  saveData();
  var tags = document.querySelectorAll('#proj_' + sessionKey + '_' + idx + ' .sub-tag');
  tags.forEach(function(t) {
    if (t.textContent === sub) t.classList.toggle('active', item.subjects.indexOf(sub) >= 0);
  });
}

function saveDraft() { saveData(); showToast('✔ 草稿已保存'); }

function submitCheckin() {
  var name = localStorage.getItem('studentName') || '';
  if (!name || !name.trim()) { showToast('⚠ 请先填写学生姓名'); return; }
  var totalFilled = SESSIONS.reduce(function(acc, s) {
    return acc + countFilled(formData.sessions[s.key] || []);
  }, 0);
  if (totalFilled === 0) { showToast('⚠ 请至少填写一个时间段'); return; }
  saveData();
  localStorage.setItem(getGroupKey(currentDate, name), JSON.stringify(formData));
  updateGroupIndex(currentDate, name);
  showToast('✔ 打卡已提交到群共享！');
  renderCheckinPage();
}

function renderHistoryPage() {
  renderHeader();
  var container = document.getElementById('app');
  var bb = document.getElementById('bottomBar');
  bb.style.display = 'none';

  var dates = [];
  for (var k in localStorage) {
    var m = k.match(/^studyCheckin_(\\d{4}-\\d{2}-\\d{2})$/);
    if (m && dates.indexOf(m[1]) < 0) dates.push(m[1]);
  }
  dates.sort().reverse();

  var html = container.innerHTML;
  html += '<div class="data-actions">';
  html += '<button class="data-btn import" onclick="document.getElementById(\\'importInput\\').click()">📥 导入数据</button>';
  html += '<button class="data-btn" onclick="exportMyData()">📤 导出我的数据</button></div>';

  if (dates.length === 0) {
    html += '<div class="empty-state"><div class="empty-icon">📅</div><div class="empty-text">暂无历史记录</div></div>';
  } else {
    html += '<div class="history-list">';
    dates.forEach(function(d) {
      var raw = localStorage.getItem('studyCheckin_' + d);
      var data = null;
      if (raw) { try { data = JSON.parse(raw); } catch(e) {} }
      var fc = SESSIONS.reduce(function(a, s) { return a + countFilled((data && data.sessions[s.key]) || []); }, 0);
      var bc = fc === 0 ? 'empty' : 'partial';
      if (fc >= SESSIONS.length) bc = 'done';
      var bt = fc === 0 ? '未打卡' : (fc >= 3 ? '✔ 全部完成' : fc + '/3 时段');
      var summary = ''