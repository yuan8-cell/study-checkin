// 学习打卡系统 - 老师获取全年级看板数据
// 部署至微信云开发 CloudBase 环境
// 环境ID: zj-edu-dev-d3grxsted961185b1

const cloud = require('@cloudbase/node-sdk')

// 初始化 CloudBase 环境
const app = cloud.init({
  env: 'zj-edu-dev-d3grxsted961185b1'
})

const db = app.database()
const _ = db.command

/**
 * 格式化日期为 YYYY-MM-DD
 */
function formatDate(date) {
  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')
  return `${year}-${month}-${day}`
}

exports.main = async (event, context) => {
  try {
    const { date, days = 7 } = event
    
    // 确定查询的日期范围
    let dateRange = {}
    if (date) {
      dateRange = { date }
    } else {
      const today = new Date()
      const startDate = new Date(today)
      startDate.setDate(today.getDate() - days)
      dateRange = {
        date: _.gte(formatDate(startDate))
      }
    }
    
    // 查询打卡数据
    const result = await db.collection('checkins')
      .where(dateRange)
      .orderBy('date', 'desc')
      .orderBy('group', 'asc')
      .orderBy('name', 'asc')
      .get()
    
    // 统计信息
    const groups = [...new Set(result.data.map(item => item.group))]
    const submittedNames = [...new Set(result.data.map(item => item.name))]
    
    const stats = {
      totalRecords: result.data.length,
      uniqueStudents: submittedNames.length,
      groups: groups,
      date: date || `最近${days}天`,
      dateRange: {
        start: dateRange.date?.gte || null,
        end: date || null
      }
    }
    
    return {
      success: true,
      code: 0,
      data: result.data,
      stats: stats
    }
    
  } catch (err) {
    console.error('[getTeacherDashboard] 错误:', err)
    return {
      success: false,
      error: err.message || '服务器内部错误',
      code: -1
    }
  }
}