# 页尾参考站一致性修正 · 2026-11-12

用户澄清截图问题是“不符合诺里斯的”界面。本次按线上 DOM、保留 HTML 与同视口页尾截图修正，不仅处理商品摄影的抠图毛边。

## 差距与修正

- 原站 `.footer-bg-img` 是穿戴头盔的人物半身透明摄影；本地此前误换成了侧面商品头盔。现替换为 Max 2024 戴盔半身透明照片，并保留原站 48.75rem × 39.875rem 的图像框与底部定位。`object-fit: cover` 保持照片比例，仅裁掉顶部透明留白。
- `.footer-links-col` 新增技术署名撑高整个 `.footer-links-w`，造成两侧导航上移。同视口 1440×900 实测旧本地链接区域高约 326px，原站约 175px。移出技术段落并恢复原站隐藏的 Partnerships 行，保留 4 项导航 + 档案入口；署名继续由 About、说明页、素材库承载。
- 原站背景的抽象轮廓线此前被替换为大块 MV 水印；现恢复原 SVG 轮廓与现有深蓝/橙色色板。
- 恢复源页尾标题的文字/混合字体层级和排版。保留真实 Max 签名替换与 MV 身份色。
- 底部世界标识条恢复较大的标识字高，穿插实际 MV 矢量标志。其余标签仍为项目排版的 racing worlds 名称，不冒称官方合作品牌 logo。
- 全站子页从首页生成同一份页尾，已同步重建。

## 新图片与来源

输出：`public/max/footer-max-worn-2024.png`，RGBA 1330×1183。

原图：`public/max/helmet-worn-2024.jpg`。原始摄影保留不变。来源为 Red Bull Racing 头盔发布照，经 https://ge.globo.com/motor/formula-1/noticia/2024/02/20/f1-2024-veja-capacetes-dos-pilotos-da-temporada.ghtml 刊载；来源台账与素材库已添加该派生文件。使用内置 imagegen 做背景提取，属于 AI 辅助去背景素材，并非新拍摄的摄影或扫描；头盔朝向仍取自源照片，与诺里斯正面姿态并不完全相同。

内置工具原始输出：`/Users/louis/.codex/generated_images/01a1ce7d-be06-7ec1-aff1-ea5756b00468/exec-68265ae8-78fc-489d-b7f5-6d919f5cf267.png`，已复制入仓库消费路径。

Prompt:

> Use case: background-extraction. Edit target: the supplied photograph of Max Verstappen wearing his white red and blue Oracle Red Bull helmet and dark Red Bull racing suit. Create a clean transparent-background cutout for a website footer. Remove ONLY the entire light blue paddock backdrop and white horizontal background bar. Preserve the exact photographed helmet, visor, paint, sponsor lettering, hardware, shoulders, suit, hands if visible, original pose, lighting and proportions, without redrawing or inventing detail. Preserve the torso and shoulder silhouette all the way to the existing bottom crop. Do not turn the head, do not replace with a floating helmet, do not add a shadow or ground. Center the intact photographed person, leaving a little transparent breathing room around head and shoulders. Output a true alpha-transparent PNG. No background, no added words, no retouching or stylization.

构建与 `npm run check` 均通过，后者包含 13 个 HTML 页面的资源和路由检查。桌面/手机最终画面保存在本地 `.impeccable/review/footer-desktop.png` 与 `footer-mobile.png`。未部署。
