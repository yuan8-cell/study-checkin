// ============================================================
// 学习打卡系统 - 云函数集成脚本
// 环境: 微信云开发 CloudBase
// 环境ID: zj-edu-dev-d3grxsted961185b1
// ============================================================

/**
 * 云函数配置
 * 注意：在纯前端HTML中使用时，需要通过云托管或自有后端中转
 */
const CLOUDBASE_CONFIG = {
  env: 'zj-edu-dev-d3grxsted961185b1'
};

/**
 * 调用云函数的通用方法
 * 注意：由于CORS限制，纯前端需要通过云托管中转
 * 
 * 方案1：使用云托管 HTTP API（推荐）
 * 方案2：使用 tcb-router 等开源方案自行搭建中转
 */
async function callCloudFunction(functionName, data) {
  // 云托管 HTTP 调用地址（由你部署中转服务后填入）
  const url = (window.CLOUD_API_BASE_URL || '') + '/' + functionName;
  
  if (!url || url === '/undefined' || url === '/' + functionName) {
    return { success: false, error: 'CLOUD_API_BASE_URL 未配置' };
  }
  
  try {
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    });
    
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }
    
    return await response.json();
  } catch (err) {
    console.error(`[云函数调用失败] ${functionName}:`, err);
    return { success: false, error: err.message };
  }
}

/**
 * 家长提交打卡（调用云函数）
 */
async function submitToCloud(data) {
  const result = await callCloudFunction('submitCheckin', data);
  return result;
}

/**
 * 组长获取组内数据（调用云函数）
 */
async function getLeaderDataFromCloud(group, date) {
  const result = await callCloudFunction('getLeaderData', { group, date });
  return result;
}

/**
 * 老师获取看板数据（调用云函数）
 */
async function getTeacherDashboardFromCloud(date) {
  const result = await callCloudFunction('getTeacherDashboard', { date });
  return result;
}

/**
 * ============================================================
 * 以下是完整的前端改造方案（需要配合云托管部署）
 * ============================================================
 */

// 方案A：完整的云端同步功能（需要部署云托管）
const CloudSync = {
  // 初始化（需要云托管返回临时凭证）
  init: async function() {
    // 这个需要在后端配置，返回临时access_token
    // 实际部署时由云托管返回
  },
  
  // 家长提交打卡到云端
  submitCheckin: async function(checkinData) {
    // 将本地数据转换为云端格式
    const cloudData = {
      date: checkinData.date,
      name: checkinData.studentName,
      group: checkinData.group || '',
      role: 'parent',
      plan: this.formatPlan(checkinData),
      effect: this.formatEffect(checkinData),
      remark: this.formatRemark(checkinData)
    };
    
    return await callCloudFunction('submitCheckin', cloudData);
  },
  
  // 格式化学习计划
  formatPlan: function(data) {
    const plans = [];
    SESSIONS.forEach(s => {
      const items = data.sessions[s.key] || [];
      items.forEach(item => {
        if (item.plan) {
          plans.push(`[${s.label}] ${item.plan}`);
        }
      });
    });
    return plans.join('\n');
  },
  
  // 格式化学习效果
  formatEffect: function(data) {
    const effects = [];
    SESSIONS.forEach(s => {
      const items = data.sessions[s.key] || [];
      items.forEach(item => {
        if (item.completion || item.rating) {
          const rating = item.rating ? RATING_Map[item.rating] : '';
          effects.push(`[${s.label}] ${item.completion || ''} ${rating}`);
        }
      });
    });
    return effects.join('\n');
  },
  
  // 格式化备注
  formatRemark: function(data) {
    const notes = [];
    SESSIONS.forEach(s => {
      const items = data.sessions[s.key] || [];
      items.forEach(item => {
        if (item.notes) {
          notes.push(`[${s.label}] ${item.notes}`);
        }
      });
    });
    return notes.join('\n');
  },
  
  // 组长批量上传
  batchSubmit: async function(records) {
    return await callCloudFunction('submitCheckin', {
      batch: true,
      records: records.map(r => ({
        date: r.date,
        name: r.studentName,
        group: r.group || '',
        role: 'parent',
        plan: this.formatPlan(r),
        effect: this.formatEffect(r),
        remark: this.formatRemark(r)
      }))
    });
  }
};

/**
 * ============================================================
 * 部署说明
 * ============================================================
 * 
 * 由于浏览器直接调用云函数会有CORS限制，需要选择以下方案：
 * 
 * 方案1：云托管（推荐）
 * - 在 CloudBase 控制台创建云托管服务
 * - 部署一个简单的 Node.js 中转服务
 * - 前端通过云托管的 HTTPS 地址调用
 * 
 * 方案2：使用腾讯云API网关
 * - 配置 API 网关触发云函数
 * - 设置允许的 CORS 源
 * 
 * 方案3：使用 CloudBase Web SDK（需满足特定条件）
 * - 需要在微信开发者工具或特定环境
 * 
 * 具体部署步骤见 deploy/README.md
 */

// 导出供外部使用
if (typeof window !== 'undefined') {
  window.CloudSync = CloudSync;
  window.CLOUDBASE_CONFIG = CLOUDBASE_CONFIG;
}