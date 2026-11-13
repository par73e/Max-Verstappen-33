# 头盔陈列方向、尺度与悬停修正 · 2026-11-12

## 来源与定位

按项目规则先读取 https://landonorris.com/ 对应头盔网格 DOM，并检查 `reference/lando-home.html` 中 `[data-helmet-item]` 的 mask、`.helmet-grid-item-reveal-img` 的 ellipse/scale 过渡，以及 `reference/lando-engine.js` 的 `ZZ()` 滚动错位。

参考站各款使用统一朝右的三分之四视图，并以透明图片本身的留白控制视觉尺寸。本地此前把三款产品的不同角度铺成 16 项，正面/背面/左右方向混杂；还在浏览器中以白色阈值 flood-fill 抠图，造成边缘缺口、白边、主线程工作和 data URL 上传。悬停图仍是 lazy 图片，现场检查时前四张的 `complete` 为 false，且本地额外叠加了 0.5 秒延迟。

## 改动

- `content/helmet-archive.json` 明确列出 Season 2024、USA 2024、Orange Tribute 2024、Season 2023 四款真实设计。多角度照片继续在各自详情页中保留，不再作为重复陈列卡片。
- 三分之四视图统一朝右；通过 alpha 边界计算 CSS 位置，主体最大宽度为卡片 64%、最大高度为 54%，居中略上移。原四列框架、缺口轮廓、caption 和错位滚动 hooks 保留。
- 四张源摄影均通过内置 imagegen 提取透明背景。原图保留；所选 PNG 保存在 `assets/derived/helmet-archive/`，运行时使用 `public/max/archive/` 中宽 768px 的高质量透明 WebP。四张 WebP 合计约 409 KiB。
- 去掉运行时抠图和 data URL，白色盔壳不再被背景阈值算法误删。
- 悬停照片 eager 加载并显式 `decode()`。没有解码成功时保留基础陈列图；解码完成仍会检查当前鼠标/焦点意图，避免已经移出后突然显示。
- 移除额外半秒延迟和竞争的 CSS hover reveal。改用一对同步、可反向播放的 Web Animations：窗口从上向下移动，照片反向移动抵消位移，保持照片配准。650ms 过渡可以从中途收回/继续，不先重置为第一帧。
- 保留静态卡片 mask；揭示边缘改为合成层的位移窗口，不再逐帧修改椭圆 clip-path。支持键盘 focus-visible 和 prefers-reduced-motion。

## 素材与提示词

| 设计 | 原图 | 所选内置 imagegen 输出 |
| --- | --- | --- |
| Season 2024 | `public/max/helmet-00-01.jpg` | `exec-dfbdf238-9867-4d6d-9ef7-b27c66259d30.png` |
| USA 2024 | `public/max/helmet-02-02.jpg` | `exec-b1780cd4-5ba7-4d90-9658-08945efc16a2.png` |
| Season 2023 | `public/max/helmet-04-01.jpg` | `exec-bd8db6d5-8745-42bf-b9ee-62a6f859a233.png` |
| Orange Tribute 2024 | `public/max/orange-2024-03.jpg` | `exec-8d23bf74-9ad7-4098-b054-dcef7fb74598.png` |

内置输出目录：`/Users/louis/.codex/generated_images/01a1ce7d-be06-7ec1-aff1-ea5756b00468/`。Orange 第一版未采用；一次三维渲染比较也未采用，最终四项均使用摄影去背景版。AI 辅助去背景可能带来局部细节变化，不宣称官方产品扫描或原始摄影像素完全不变。

三款通用提示词（`<edition>` 分别代入 season-2024、usa-2024、season-2023）：

> Use case: background-extraction. Edit target: the supplied photograph of a Max Verstappen racing helmet, <edition>. Create a clean high-quality alpha-transparent helmet cutout for a website product archive. Remove only the white/grey studio backdrop, background graphics, floor shadow, and the white foam display pad if present underneath the helmet. Preserve the exact helmet silhouette, three-quarter view facing RIGHT, original camera angle, visor color, reflections, shell, vents, transparent hardware, all sponsor lettering and paint details. Do not turn, mirror, redraw or recolor the helmet. Keep every genuine white shell edge solid; remove white fringe outside the silhouette; smooth naturally anti-aliased edges, no ragged horizontal gouges or white halo. Entire helmet visible and centered with generous transparent margin. Output a true alpha-transparent PNG, no floor, no added shadow or stand. Keep original photographic detail.

Orange 所选提示词：

> Background-extraction correction. Input is an ORANGE Max Verstappen helmet photograph on a white studio floor with a grey MV graphic behind it. Extract ONLY the intact helmet itself. The entire outside region must be fully transparent alpha=0, including all floor shadows, colored glow, backdrop graphics and the tiny background copyright caption. There must be no smoky fringe, no halo, no black backdrop. Keep every helmet pixel visually faithful: original right-facing three-quarter pose, orange paint, black speckles, white outlines, Heineken/Oracle/Red Bull lettering, visor reflections, hardware and genuine helmet edges. Remove the floor and any stand but preserve the helmet base. Flat photographic product cutout, no added lighting effects, no added shadows or glow. Transparent PNG with a small clean transparent margin.

## 验证

- 构建、JS 语法检查、13 个 HTML 页面路由/资源检查通过。
- 桌面检查四项照片方向、尺寸和边缘，实际鼠标悬停展开后离开可回到 closed。
- 页面内以 220ms 移出、380ms 重入采样 1.4 秒：41 个动画帧，状态依次包含 opening、closing、open，窗口/照片位移抵消误差为 0；位移逐步变化，没有跳到终点。最大采样间隔约 51ms，不能由此宣称所有硬件上恒定 60fps。
- 验收时原 ego Space 消失，取得用户明确授权后创建新空白 Space 继续，没有接管用户已有非空 Space。
- 截图保存在本地 `.impeccable/review/helmet-archive-desktop.png` 与 `helmet-archive-mobile.png`。

未部署、未提交或推送。

## 2026-11-13 最终手机适配

源码手机端的 `max-width: 12rem` 会对透明留白较多的橙色素材二次限宽，已在标准化陈列图上取消该限制。按最终 WebP alpha 边界计算，四款主体高度均为卡片的 54%。键盘焦点、减少动态模式、真实鼠标移入移出及 Orange Tribute 详情导航均已通过；手机端四项正常且无横向溢出。

最终手机截图在 390×844 下确认四项 `max-width` 均为 none，无横向溢出；最终桌面图保留稳定网格状态，避免把页面滚动到后续章节的画面误记为陈列截图。
