# MV33 全站对照与适配 · 2026-11-12

## 实现依据

先以 ego lite 读取线上 HTML/DOM，再下载原始 HTML 到 `reference/pages/`，沿原始 CSS 与 `reference/lando-engine.js` 检查 `data-page` 分发器、`mL/cL/lL` 生命周期、On Track `_$/_L`、Off Track `x$/z_`、Calendar `b$/j$/S_`。页面不是按截图另写布局。

参考入口：https://landonorris.com/ 。`on-track`、`off-track`、`calendar` 与两个 legal 页面均成功读取；`partnerships` 当日返回 Not Found，不能据此宣称该页完全还原。

## 差距与处理

| 区域 | 原有差距 | 本次处理 |
| --- | --- | --- |
| 首页导航 | 主要入口打开通用弹层，缺少参考站右上主按钮 | 改为独立地址；恢复源按钮结构，HELMETS 跳转本地档案 |
| 全屏菜单/页尾 | 子页面各用自己的简化导航；额外版本按钮占据菜单空间 | 全部展示页面共用源码导航、菜单和页尾；版本入口集中到档案 |
| On Track | 没有真实子页 | 源码头盔大字开场、三段头盔滚动路径、职业统计、赛季列表、胜场精选、横向摄影、青少年经历、赛道场景、头盔陈列、社交与页尾 |
| Off Track | 通用摄影弹层 | 源码大字开场、照片堆栈翻转、横向项目章节、社交与页尾；替换人物、经历与签名 |
| Calendar | 赛事摄影弹层 | 源码签名标题、赛道信息与 3D 模型切换、2026 列表、2015–2025 历史折叠、倒计时 |
| Racing Worlds | 缺少页面；参考站当前 404 | 以 Off Track 源布局适配真实 racing worlds 内容；明确不是对不可用页面的逐像素复刻 |
| 头盔陈列 | 陈列点击打开通用摄影弹层 | 真实链接指向对应独立详情页；档案保留原始陈列与穿戴揭示 |
| 三维详情 | 独立简化导航和页尾，与首页割裂 | 接入统一导航/菜单/页尾，保留可交互 3D、视角/线框与真实摄影 |
| 2024 Season/USA | 没有详情地址 | 新增独立摄影详情；没有杜撰这两款的可交互三维涂装 |
| Privacy/Terms | 只打开 about 弹层 | 保留法律页排版形式，改写为本网站实际的说明与署名内容，不冒用原站公司与政策 |
| 素材库 | 保留原站旧绿配色 | 随统一色板生成深蓝/橙色 |

## 构建与内容

- `scripts/build.py` 继续拥有首页与 renderer 生成。
- `scripts/build_pages.py` 从保留的原始 DOM 生成 11 个内部路由，复用已完成 Max 适配的首页 shell、社交和页尾。
- `public/pages.css` 只补充页面特定适配；原站共享 CSS、DOM selectors、Webflow 页面 ID、Rive 与 GSAP 控制器继续拥有主要布局和动画。
- `public/page-transition.js` 在 document capture 阶段处理跨文档内部导航，沿用已有 MV 遮罩，支持直接访问/刷新/历史导航。未复制 Taxi 的客户端内容交换；跨页会重新加载文档。
- 赛事数据来自 https://api.jolpi.ca/ergast/f1/ 的 Max Verstappen 结果、排位与积分榜快照，原始响应保留在 `content/`。2026 已完成比赛填入 Max 数据；未核实练习赛与首次参赛年份显示 `—`。不是实时成绩服务。
- On Track 职业统计明确限于 2015–2024。P1 次数根据比赛发车位汇总，标签为 STARTS FROM P1，不冒称官方 pole position 总数。
- 原始旗帜、赛道与装饰资源的新增来源记录在 `reference/pages/resources.json`。

## 实测

使用同一个独立 ego lite 任务 Space（ID 2），未接管用户非空 Space。

- 桌面与约 390px 手机视口逐一访问首页、11 个内部路由；未发现横向溢出、已完成加载的坏图或 HTTP 错误资源。
- 首页、On Track、Off Track、Calendar、Racing Worlds 在约 25%、55%、90% 滚动位置进行画面检查；有些截图包含源站滚动高亮的中间帧，未把它们当作静态排版错误。
- 桌面菜单 Calendar → On Track、手机菜单 Home → Off Track 跨页切换成功；页面 URL 与内容一致。约 768px 平板视口追加检查 On Track、Off Track、Calendar 和 2023 三维详情，未发现横向溢出。
- Calendar 历史折叠展开成功，2024 对应 24 场真实 Max 记录。
- Calendar “下一项”完整动画后由 Las Vegas 切换为 Lusail，`window.landoGL.params.tracksScene.CURRENT` 同步为 `lusail`。
- 两款原有三维详情达到 `ready`；2023 Back 与 Wireframe 实测，线框对象可见。
- 对最终首页、Calendar 和三维详情启用错误/未处理 Promise 拒绝监听，测试时未捕获异常。
- `npm run build` 与 `npm run check` 通过；后者包含全部 13 个 HTML 页面的内部地址、图片/脚本/样式资源和源控制器 hooks 检查。
- 验收截图保留在本地 `.impeccable/review/desktop.png`、`mobile.png`；该目录由仓库既有规则忽略，不作为源代码发布。

## 剩余保真边界

人物照片与内容按 Max 身份替换，构图和行长自然不同。人像深度为推测，签名为 SVG 揭示，头盔为现有近似网格/涂装；不能称为官方扫描或原站 Rive 的逐笔 MV 动画。当前原站 Partnerships 不可用，因此本地该页是有依据的结构适配，不是已验证的逐像素还原。未创建购物、账户或真实邮件订阅系统。未部署或推送这些修改。
