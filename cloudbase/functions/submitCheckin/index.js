// 学习打卡系统 - 云函数入口
// 部署至微信云开发 CloudBase 环境
// 环境ID: zj-edu-dev-d3grxsted961185b1

const cloud = require('@cloudbase/node-sdk')

// 初始化 CloudBase 环境
const app = cloud.init({
  env: 'zj-edu-dev-d3grxsted961185b1'
})

const db = app.database()
const _ = db.command
const $ = db.command.aggregate

// 主入口
exports.main = async (event, context) => {
  try {
    // 批量提交模式（组长汇总）
    if (event.batch === true && Array.isArray(event.records)) {
      return await handleBatchSubmit(event.records)
    }
    
    // 单条提交模式（家长）
    return await handleSingleSubmit(event)
    
  } catch (error) {
    return {
      success: false,
      errorCode: 500,
      errorMessage: error.message || '服务器内部错误'
    }
  }
}

// 处理单条提交
async function handleSingleSubmit(data) {
  const { date, name, plan, effect, remark = '', group = '', role = 'parent' } = data
  
  // 验证必填字段
  if (!date || !name) {
    return {
      success: false,
      errorCode: 400,
      errorMessage: '日期和姓名不能为空'
    }
  }
  
  // 构建记录
  const record = {
    date,
    name,
    plan: plan || '',
    effect: effect || '',
    remark,
    group,
    role,
    createTime: db.serverDate(),
    updateTime: db.serverDate()
  }
  
  // 写入数据库
  const result = await db.collection('checkins').add({
    data: record
  })
  
  return {
    success: true,
    data: {
      id: result.id,
      ...record
    },
    message: '打卡成功'
  }
}

// 处理批量提交
async function handleBatchSubmit(records) {
  const results = {
    successCount: 0,
    failCount: 0,
    errors: []
  }
  
  for (const record of records) {
    try {
      const result = await handleSingleSubmit(record)
      if (result.success) {
        results.successCount++
      } else {
        results.failCount++
        results.errors.push(result.errorMessage)
      }
    } catch (e) {
      results.failCount++
      results.errors.push(e.message)
    }
  }
  
  return {
    success: results.failCount === 0,
    data: results,
    message: `成功 ${results.successCount} 条，失败 ${results.failCount} 条`
  }
}