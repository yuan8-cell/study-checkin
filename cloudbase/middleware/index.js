/**
 * 学习打卡系统 - 云托管中转服务
 * 
 * 功能：将前端请求中转到微信云开发云函数
 * 解决浏览器 CORS 限制问题
 * 
 * 部署方式：
 * 1. 将此服务部署到云托管
 * 2. 或部署到自有服务器/腾讯云服务器
 */

const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');

// 配置
const CONFIG = {
  // 微信云开发 SecretId（建议使用环境变量）
  secretId: process.env.TENCENT_SECRET_ID || '',
  secretKey: process.env.TENCENT_SECRET_KEY || '',
  // 云函数配置
  cloudBase: {
    env: process.env.TENCENT_CLOUDBASE_ENV || 'zj-edu-dev-d3grxsted961185b1',
    region: process.env.TENCENT_REGION || 'ap-shanghai'
  }
};

const app = express();
const PORT = process.env.PORT || 8080;

// 中间件
app.use(cors());
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

// 健康检查
app.get('/', (req, res) => {
  res.json({ status: 'ok', service: 'checkin-middleware' });
});

/**
 * 云函数调用封装（实际中转逻辑需在后端环境运行）
 * 说明：静态托管无法直接运行 Node.js 服务，
 * 本文件保留为后端部署参考，前端请改用 tencent-docs skill 直写表格。
 */
async function callCloudFunction(functionName, data) {
  throw new Error('当前为静态托管环境，请改用前端直写腾讯文档表格方案');
}

/**
 * 路由：家长提交打卡
 * POST /api/submit-checkin
 */
app.post('/api/submit-checkin', async (req, res) => {
  try {
    const { date, name, plan, effect, remark, group, role } = req.body;
    
    // 参数验证
    if (!date || !name || !plan) {
      return res.status(400).json({
        success: false,
        error: '缺少必填参数：date, name, plan'
      });
    }
    
    const result = await callCloudFunction('submitCheckin', {
      date,
      name,
      plan,
      effect: effect || '',
      remark: remark || '',
      group: group || '',
      role: role || 'parent'
    });
    
    res.json(result);
  } catch (err) {
    console.error('[submit-checkin] 错误:', err);
    res.status(500).json({
      success: false,
      error: err.message || '服务器内部错误'
    });
  }
});

/**
 * 路由：组长批量提交
 * POST /api/batch-submit
 */
app.post('/api/batch-submit', async (req, res) => {
  try {
    const { records } = req.body;
    
    if (!records || !Array.isArray(records) || records.length === 0) {
      return res.status(400).json({
        success: false,
        error: '缺少批量提交数据：records'
      });
    }
    
    const result = await callCloudFunction('submitCheckin', {
      batch: true,
      records: records.map(r => ({
        date: r.date,
        name: r.name,
        plan: r.plan,
        effect: r.effect || '',
        remark: r.remark || '',
        group: r.group || '',
        role: r.role || 'parent'
      }))
    });
    
    res.json(result);
  } catch (err) {
    console.error('[batch-submit] 错误:', err);
    res.status(500).json({
      success: false,
      error: err.message || '服务器内部错误'
    });
  }
});

/**
 * 路由：组长获取组内数据
 * POST /api/leader-data
 */
app.post('/api/leader-data', async (req, res) => {
  try {
    const { group, date } = req.body;
    
    if (!group) {
      return res.status(400).json({
        success: false,
        error: '缺少必填参数：group'
      });
    }
    
    const result = await callCloudFunction('getLeaderData', { group, date });
    res.json(result);
  } catch (err) {
    console.error('[leader-data] 错误:', err);
    res.status(500).json({
      success: false,
      error: err.message || '服务器内部错误'
    });
  }
});

/**
 * 路由：老师获取看板数据
 * POST /api/teacher-dashboard
 */
app.post('/api/teacher-dashboard', async (req, res) => {
  try {
    const { date, days } = req.body;
    
    const result = await callCloudFunction('getTeacherDashboard', { date, days });
    res.json(result);
  } catch (err) {
    console.error('[teacher-dashboard] 错误:', err);
    res.status(500).json({
      success: false,
      error: err.message || '服务器内部错误'
    });
  }
});

// 启动服务
app.listen(PORT, () => {
  console.log(`🎯 学习打卡中转服务已启动，端口: ${PORT}`);
  console.log(`📡 云函数环境: ${CONFIG.cloudBase.env}`);
});

module.exports = app;