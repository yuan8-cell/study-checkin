# 学习打卡系统 - 云函数部署与使用指南

## 📋 环境信息
- **云开发环境ID**: zj-edu-dev-d3grxsted961185b1
- **服务端**: 微信云开发 CloudBase
- **部署位置**: 云函数 + 云托管（可选）
- **前端**: 静态 HTML + JavaScript

---

## 🚀 方案总览

```
家长打卡（前端HTML）
    ↓
方案A：直接上传（无服务器）
    ↓ 导出JSON
组长汇总（本地处理）
    ↓ 上传
云函数 submitCheckin
    ↓
云数据库 checkins
    ↓
老师查看（前端HTML）
```

---

## 📦 部署步骤

### 第一步：安装 CloudBase CLI

```bash
npm install -g @cloudbase/cli
tcb login
```

### 第二步：初始化项目

```bash
# 进入项目目录
cd C:\Users\Admin\WorkBuddy\Claw\cloudbase

# 初始化 CloudBase 项目
tcb init

# 选择已创建的环境：zj-edu-dev-d3grxsted961185b1
```

### 第三步：创建云数据库集合

在 CloudBase 控制台（https://tcb.cloud.tencent.com）：
1. 进入环境 `zj-edu-dev-d3grxsted961185b1`
2. 选择「数据库」
3. 创建集合：`checkins`
4. 添加字段：
   - `date` (String) - 日期 YYYY-MM-DD
   - `name` (String) - 姓名
   - `group` (String) - 组别
   - `plan` (String) - 学习计划
   - `effect` (String) - 学习效果
   - `remark` (String) - 备注
   - `role` (String) - 角色
   - `createdAt` (Date) - 创建时间
   - `updatedAt` (Date) - 更新时间

### 第四步：创建云函数

```bash
# 上传家长提交函数
tcb fn:deploy functions/submitCheckin

# 上传组长查询函数
tcb fn:deploy functions/getLeaderData

# 上传老师看板函数
tcb fn:deploy functions/getTeacherDashboard
```

### 第五步：配置云托管（可选，用于前端中转）

如果需要在浏览器直接调用云函数，需要配置 CORS：

```bash
# 部署中转服务到云托管
cd middleware
npm install
# 然后部署到云托管或自有服务器
```

### 第六步：修改前端代码

在前端 HTML 中添加云端同步功能：

```javascript
// 引入 CloudBase SDK
// <script src="https://img.qcloud.com/open/qcloud/js/cloudbase/3.8.3/cloudbase.js"></script>

// 初始化 CloudBase
const app = cloudbase.init({
  env: 'zj-edu-dev-d3grxsted961185b1'
});

// 调用云函数示例
async function submitCheckin(data) {
  try {
    const result = await app.callFunction({
      name: 'submitCheckin',
      data: data
    });
    return result;
  } catch (err) {
    console.error('提交失败:', err);
    throw err;
  }
}
```

### 第七步：部署前端

将修改后的 HTML 文件部署到：
- 云托管静态服务
- 或任意静态服务器
- 或继续使用 GitHub Pages

---

## 🔧 完整工作流

### 家长打卡流程

```
1. 家长打开页面 → 填写打卡表单
2. 点击"提交打卡" → 调用 submitCheckin 云函数
3. 云函数验证数据 → 写入 checkins 集合
4. 返回成功结果 → 前端显示"打卡成功"
```

### 组长汇总流程

```
1. 组长打开页面 → 切换到组长角色
2. 导入/导出组内数据
3. 点击"批量上传" → 调用 submitCheckin（batch模式）
4. 云函数批量写入 → 返回成功/失败统计
```

### 老师看板流程

```
1. 老师打开页面 → 切换到老师角色
2. 查看组内看板 → 调用 getTeacherDashboard 云函数
3. 云函数查询 checkins 集合 → 返回数据
4. 前端渲染看板 → 展示所有打卡数据
```

---

## ⚠️ 重要说明

### CORS 限制
浏览器直接调用云函数会有跨域问题，必须通过以下任一方式解决：

| 方案 | 难度 | 说明 |
|------|------|------|
| **A. 云托管中转** | ⭐⭐⭐ | 最标准，推荐 |
| **B. 自有服务器** | ⭐⭐ | 需要服务器 |
| **C. 小程序内嵌** | ⭐ | 仅限微信内使用 |

### 数据安全
- 云函数内存储了数据库访问密钥，不应在前端暴露
- 通过云托管中转，前端不直接访问云函数
- 云函数内可添加权限验证

### 免费额度
微信云开发个人版免费额度：
- 云数据库：2GB
- 云函数：100,000 次/月
- 存储：5GB
- 并发：500

**足够支持 30-50 个家庭使用**

---

## 🆘 常见问题

### Q1：云函数调用失败？
A: 检查环境ID是否正确，云函数是否部署成功

### Q2：前端跨域错误？
A: 使用云托管中转服务，不要直接在前端调用云函数

### Q3：数据量增长怎么办？
A: 云数据库自动扩容，免费额度 2GB 约可存 10万条打卡记录

### Q4：能否导出数据？
A: 可以，在 CloudBase 控制台直接导出 Excel

---

## 📞 技术支持

- CloudBase 文档：https://docs.cloudbase.net
- 微信云开发社区：https://developers.weixin.qq.com/community/develop/mixflow