# MV33 · 维斯塔潘主题前端还原

基于 [Lando Norris / OFF+BRAND](https://landonorris.com/) 的首页 DOM、CSS、浏览器端渲染脚本和 Rive 动画构建的个人学习版本。用户指定高保真保留原站交互，人物、图片、部分文案和链接适配为 Max Verstappen。未部署到公共网站。

## 运行

在本目录执行 `npm start`，浏览器访问 http://127.0.0.1:4173/ 。也可直接执行 `python3 -m http.server 4173 --bind 127.0.0.1 --directory public`。页面运行不需要 Node 依赖安装，Python 3 即可提供静态服务；需使用支持 WebGL 2 / WebAssembly 的浏览器。

素材库：http://127.0.0.1:4173/assets.html 。不要直接以 file:// 打开首页，渲染器需要 HTTP 加载本地模型、字体与 WASM。

需要重新生成页面时，先执行 `python3 -m venv .venv` 和 `.venv/bin/python -m pip install -r requirements.txt`，再运行 `npm run build`。仓库已包含可直接运行的页面和素材，普通预览不需要这一步。

## 文件

- `public/index.html`：保留参考站布局和动画选择器的适配页面。
- `public/engine.js`：原始浏览器动画包的本地适配，保留原有声明。
- `public/mv33.js`、`public/mv33.css`：主题、双语、照片渲染、内容面板与可访问交互。
- `public/texture-bridge.js`：以原始 Max 照片生成运行时 WebGL 贴图；原始摄影文件不变。
- `public/max/`：人物、签名、新闻摄影、商品图及头盔档案候选。
- `assets-manifest.json`：各下载项的源页面、文件地址、SHA-256、大小和状态。
- `max-assets.json`：页面选材清单。
- `reference/`：原站 HTML/CSS/脚本与素材来源页的保留记录，便于比对。
- `scripts/build.py`：从保留的参考 HTML 与素材清单重建页面，需 `.venv` 的 Beautiful Soup。
- `scripts/build_gallery.py`：重建素材展示页。

## 本版已实现

加载过渡、WebGL 背景/头盔线框/切片、鼠标响应、平滑滚动、原站按钮与菜单动画、人物照片叙事、头盔陈列、后半段展示、手机布局、双语说明。菜单、赛事卡片、头盔详情和介绍入口有实际反馈；商店及社交入口外链至对应渠道。已移除原站统计脚本和原站视频自动加载。

## 明确的还原差异

1. **三维头盔不是 Max 专属模型**：当前保留参考站的网格和动画，用 Max 正面商品摄影作投影材质；真实 UV 涂装、结构与光照仍有差异。
2. **人像深度是近似值**：Max 的官方透明照片在运行时生成深度/法线适配；没有本人三维扫描数据。
3. **签名是图片揭示**：签名来源已记录，以原 Rive 滚动输入驱动显示，尚未重建 Max 签名的逐笔矢量动画。
4. **头盔陈列为三款、多角度**：2024 Season、2024 USA、2023 Season，16 个位置展示各角度；另有多年份档案候选图，未冒充为已抠好的商品图。运行时去白底仍可能有轮廓误差。
5. **内容替换会改变行长与图像构图**：双语、姓名、照片和标识与原站天然不同。ON/OFF TRACK 与赛事使用页内面板，尚未复刻独立子页面。
6. **赛事信息为展示样本**：保留圣保罗卡片版式，真实赛程以外链的 F1 官网为准，未接实时接口。

以上是可运行第一版，不能称为与原站所有动画/素材完全一致。

## 素材来源

[F1 车手页](https://www.formula1.com/en/drivers/max-verstappen)、[Verstappen 官网](https://www.verstappen.com/)、[官方新闻](https://news.verstappen.com/)、[Red Bull Shop](https://www.redbullshop.com/en-int/p/RBR24310/)、[Helmet Archive](https://helmetarchive.com/f1/drivers/max-verstappen/)、[Wikimedia 签名文件](https://commons.wikimedia.org/wiki/File:MaxVerstappenSignature.png)。逐文件来源见素材库和台账；来源记录不代表获得额外的再分发授权。

## 验证

`npm run check` 检查三个运行脚本语法。已进行 ego lite 桌面/390px 手机预览、加载失败检查、菜单展开与内容面板交互检查。未进行跨浏览器、真实手机、慢网与长期运行测试。
