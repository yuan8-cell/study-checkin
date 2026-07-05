// 学习打卡系统 - 组长查询组内数据
// 部署至微信云开发 CloudBase 环境
// 环境ID: zj-edu-dev-d3grxsted961185b1

const cloud = require('@cloudbase/node-sdk')

// 初始化 CloudBase 环境
const app = cloud.init({
  env: 'zj-edu-dev-d3grxsted961185b1'
})

const db = app.database()
const _ = db.command

exports.main = async (event, context) => {
  try {
    const { group, date } = event
    
    // 必填字段校验
    if (!group) {
      return {
        success: false,
        error: '缺少必填字段: group',
        code: 400
      }
    }
    
    // 构建查询条件
    const where = {
      group: group
    }
    
    // 如果指定日期，按日期筛选
    if (date) {
      where.date = date
    }
    
    // 查询组内所有打卡数据（按日期降序排列）
    const result = await db.collection('checkins')
      .where(where)
      .orderBy('date', 'desc')
      .orderBy('name', 'asc')
      .get()
    
    // 如果有日期筛选，计算提交统计
    let stats = null
    if (date) {
      stats = {
        total: result.data.length,
        submitted: result.data.length,
        date: date,
        group: group
      }
    }
    
    return {
      success: true,
      code: 0,
      data: result.data,
      stats: stats
    }
    
  } catch (err) {
    console.error('[getLeaderData] 错误:', err)
    return {
      success: false,
      error: err.message || '服务器内部错误',
      code: -1
    }
  }
}