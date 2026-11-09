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

加载过渡、WebGL 背景/头盔线框/切片、鼠标响应、平滑滚动、原站按钮与菜单动画、人物照片叙事、头盔陈列、后半段展示、手机布局、双语说明。菜单、赛事卡片、头盔详情和介绍入口有实际反馈；购物入口已移除；社交入口外链至对应渠道。已移除原站统计脚本和原站视频自动加载。

## 明确的还原差异

1. **三维头盔为独立创作者模型**：现已接入 Maubian 的真实 GLB，实体与线框共用几何。2023、2024 涂装依据多视角摄影重建；不是官方扫描，接缝、轮廓和赞助标识位置仍可能存在差异。
2. **人像深度是近似值**：F1 正面人物经背景移除后，在运行时生成深度/法线适配；没有本人三维扫描数据。
3. **签名是图片揭示**：签名来源已记录，以原 Rive 滚动输入驱动显示，尚未重建 Max 签名的逐笔矢量动画。
4. **头盔陈列为三款、多角度**：2024 Season、2024 USA、2023 Season，16 个位置展示各角度；另有多年份档案候选图，未冒充为已抠好的商品图。运行时去白底仍可能有轮廓误差。
5. **内容替换会改变行长与图像构图**：双语、姓名、照片和标识与原站天然不同。ON/OFF TRACK 与赛事使用页内面板，尚未复刻独立子页面。
6. **赛事信息为展示样本**：保留圣保罗卡片版式，真实赛程以外链的 F1 官网为准，未接实时接口。

以上是可运行第一版，不能称为与原站所有动画/素材完全一致。

## 2026-11-08 更新

已移除所有购物跳转，原商品推广区改为赛车影像。封面接入正面人像，头盔改用 2023 常规款真实正面摄影的透明抠图，保留流体揭示与悬停展开；展开时头盔覆盖头部，人物肩膀和上半身保留。标签页图标与加载过渡使用 MV 标志。上述封面实现取代第一版的外壳投影方案，后续滚动场景及线框仍保留参考几何。

人像与头盔由 imagegen 辅助移除背景，可能有细节偏差，原照保留。素材位置、未接入项和三维模型限制见 [LOCAL-ASSETS.md](LOCAL-ASSETS.md)。

## 2026-11-09：三维头盔与两个独立页面

本次三维方案替代上一节的封面二维抠图方案。首页保留参考站的流体揭示、悬停展开和人物上半身，实体与线框从同一 GLB 生成，并同步变换。MV 标志加入橙色；标签页图标提供深浅两版，随系统配色切换。

- [2023 常规款](http://127.0.0.1:4173/helmets/season-2023/)
- [2024 赞德沃特 · Orange Tribute](http://127.0.0.1:4173/helmets/zandvoort-2024/)

两页提供拖动旋转、滚轮缩放、正面/左右/背面、线框切换及官方多角度原照。方向键转动、Home 恢复正面。2024 款是当年欧洲多站使用的 Orange Tribute，并非荷兰站独占设计。

模型："[Helmet Redbull - Max Verstappen](https://skfb.ly/pEDBZ)" by Maubian / [CC BY 4.0](http://creativecommons.org/licenses/by/4.0/)。用户提供的 46 MB、4k 原始 GLB 保存在本地 `assets/source/max-helmet/original.glb`，不加入 Git；网页版本每款约 2.5 MB。修改包括比例归一、重新展开 UV、依据原照重建涂装和调整材质。原模型涂装含较新的 Gate.io 标识，不能冒充原生 2023 模型。

普通构建运行 `npm run build`，无需 Blender。需要重做模型时，依次用已安装的 Blender 后台执行 `scripts/prepare_helmet.py`、`scripts/bake_helmet_editions.py`、`scripts/export_helmet_editions.py`，再构建页面。原始照片及来源记录均保留；Three.js 0.170.0 在 `public/vendor/three/`，附 MIT LICENSE。

## 素材来源

[F1 车手页](https://www.formula1.com/en/drivers/max-verstappen)、[Verstappen 官网](https://www.verstappen.com/)、[官方新闻](https://news.verstappen.com/)、[Red Bull Shop](https://www.redbullshop.com/en-int/p/RBR24310/)、[Helmet Archive](https://helmetarchive.com/f1/drivers/max-verstappen/)、[Wikimedia 签名文件](https://commons.wikimedia.org/wiki/File:MaxVerstappenSignature.png)。逐文件来源见素材库和台账；来源记录不代表获得额外的再分发授权。

## 验证

`npm run check` 检查三个运行脚本语法。已进行 ego lite 桌面/390px 手机预览、加载失败检查、菜单展开与内容面板交互检查。未进行跨浏览器、真实手机、慢网与长期运行测试。

### Homepage comparison: original component proportions

`/?helmet=source` is a local comparison using the retained OFF+BRAND helmet geometry, native UVs, normal maps and original [6.9, 6.9, 7.1] scale, repainted with reconstructed Max 2023 artwork. It is not a Max/Schuberth scan. The default keeps the Maubian Max mesh, fitted to a similar front width/height ratio. Both use matching model-derived wireframes. Existing edition pages retain the Max mesh.

The homepage now uses RGB from the original 1920px portrait and only opacity from the older extraction. Depth is smooth across the shoulders instead of multiplied by the cutout alpha. This prevents the silhouette from pulling the low-subdivision plane into a sawtooth edge. Original photography is preserved; no facial detail is invented by sharpening or generation.

Rebuild the comparison asset if needed with Blender background scripts `scripts/bake_source_fit_helmet.py`, then `scripts/export_source_fit_helmet.py`, followed by `npm run build`. Ordinary preview needs no rebake.

### Current portrait and Retina quality update (2026-11-09)

The current hero uses `public/max/portrait-studio-source.jpg` (1200×801 native studio photograph), `portrait-studio-alpha.png` (extraction used for opacity only), and offline-inferred `portrait-studio-depth.png`. This replaces the older front-photo RGB/mask composition described above. Facial color comes from the source photograph, not generated portrait pixels. The render uses a 256×256 displaced grid, normals derived with a wider sampling interval to avoid 8-bit stair-stepping, 4096px color texture packing, and a desktop DPR cap of 2 instead of 1.25. The 4096px texture does not claim a 4K source photo or complete 3D scan.

Optional offline preparation: install `requirements-portrait.txt`, download the quantized ONNX weights for `onnx-community/depth-anything-v2-small` (Apache-2.0), then run `.venv/bin/python scripts/estimate_portrait_depth.py --model /path/to/model_quantized.onnx`. The ordinary site loads only the prepared PNG; it does not download or run a model.

The 2023 shell bake now reads original 2250×3000 Red Bull Shop photographs from `assets/source/max-helmet/photos-2023/`, replacing the 900×1200 resized bake inputs. GPU texture sampling is anisotropic, helmet target MSAA is 4x, and shell clearcoat is tuned separately from the visor. Run the existing bake/export scripts only when intentionally rebuilding the model.
