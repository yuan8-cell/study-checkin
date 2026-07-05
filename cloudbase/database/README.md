# 学习打卡系统 - 云数据库设计

## 环境信息
- 环境ID: zj-edu-dev-d3grxsted961185b1
- 数据库: 云开发数据库

## 集合设计

### 1. checkins（打卡记录）
存储所有家长的每日打卡数据

**字段说明：**
| 字段名 | 类型 | 说明 | 必填 |
|--------|------|------|------|
| _id | String | 自动生成ID | - |
| date | String | 打卡日期，格式 YYYY-MM-DD | ✅ |
| name | String | 学生姓名 | ✅ |
| plan | String | 学习计划 | ✅ |
| effect | String | 学习效果 | ✅ |
| remark | String | 备注 | ❌ |
| group | String | 所属组别（如：第一组） | ❌ |
| role | String | 角色（parent/leader/teacher） | ❌ |
| createdAt | Date | 创建时间（自动） | - |
| updatedAt | Date | 更新时间（自动） | - |

**索引配置：**
- 联合索引：`date` + `name`（唯一索引，防重复提交）
- 联合索引：`group` + `date`（组长查询优化）
- 联合索引：`date` + `group` + `name`（老师看板查询优化）

**权限设置：**
- 所有用户可读
- 仅创建者可写（或通过云函数写入）

---

## 数据库初始化脚本

在云开发控制台执行：

```javascript
// 创建 checkins 集合
// 云开发控制台 -> 数据库 -> 创建集合 -> 命名为 "checkins"

// 添加索引（在集合详情页 -> 索引管理）
// 索引1：date_1_name_1（唯一索引）
// 索引2：group_1_date_1
// 索引3：date_1_group_1_name_1

// 设置权限（集合详情页 -> 权限设置）
// 选择"自定义安全规则"，粘贴以下内容：

{
  "read": true,
  "write": "request.auth != null"
}
```

---

## 数据示例

```javascript
{
  "_id": "5f8d0d55e3b4a10001b7e3c2",
  "date": "2026-07-05",
  "name": "张三",
  "plan": "完成数学作业第3-5页，背诵英语单词20个",
  "effect": "数学作业全部正确，英语单词已掌握",
  "remark": "今天表现很好",
  "group": "第一组",
  "role": "parent",
  "createdAt": "2026-07-05T03:30:00.000Z",
  "updatedAt": "2026-07-05T03:30:00.000Z"
}
```