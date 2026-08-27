# 论文评价报告：End-to-End Object Detection with Transformers

- 来源：arxiv；arXiv: 2005.12872
- 综合评分：3.57/5

## 实验指标

| ID | 指标 | 数值 | 方法 | 数据集 | 来源 |
|---|---|---|---|---|---|
| M-000 | AP | 39.0 | Faster RCNN-DC5 | COCO | Table 1 |
| M-001 | AP50 | 60.5 | Faster RCNN-DC5 | COCO | Table 1 |
| M-002 | AP75 | 42.3 | Faster RCNN-DC5 | COCO | Table 1 |
| M-003 | APS | 21.4 | Faster RCNN-DC5 | COCO | Table 1 |
| M-004 | APM | 43.5 | Faster RCNN-DC5 | COCO | Table 1 |
| M-005 | APL | 52.5 | Faster RCNN-DC5 | COCO | Table 1 |
| M-006 | AP | 40.2 | Faster RCNN-FPN | COCO | Table 1 |
| M-007 | AP50 | 61.0 | Faster RCNN-FPN | COCO | Table 1 |
| M-008 | AP75 | 43.8 | Faster RCNN-FPN | COCO | Table 1 |
| M-009 | APS | 24.2 | Faster RCNN-FPN | COCO | Table 1 |
| M-010 | APM | 43.5 | Faster RCNN-FPN | COCO | Table 1 |
| M-011 | APL | 52.0 | Faster RCNN-FPN | COCO | Table 1 |
| M-012 | AP | 42.0 | Faster RCNN-R101-FPN | COCO | Table 1 |
| M-013 | AP50 | 62.5 | Faster RCNN-R101-FPN | COCO | Table 1 |
| M-014 | AP75 | 45.9 | Faster RCNN-R101-FPN | COCO | Table 1 |
| M-015 | APS | 25.2 | Faster RCNN-R101-FPN | COCO | Table 1 |
| M-016 | APM | 45.6 | Faster RCNN-R101-FPN | COCO | Table 1 |
| M-017 | APL | 54.6 | Faster RCNN-R101-FPN | COCO | Table 1 |
| M-018 | AP | 41.1 | Faster RCNN-DC5+ | COCO | Table 1 |
| M-019 | AP50 | 61.4 | Faster RCNN-DC5+ | COCO | Table 1 |
| M-020 | AP75 | 44.3 | Faster RCNN-DC5+ | COCO | Table 1 |
| M-021 | APS | 22.9 | Faster RCNN-DC5+ | COCO | Table 1 |
| M-022 | APM | 45.9 | Faster RCNN-DC5+ | COCO | Table 1 |
| M-023 | APL | 55.0 | Faster RCNN-DC5+ | COCO | Table 1 |
| M-024 | AP | 42.0 | Faster RCNN-FPN+ | COCO | Table 1 |
| M-025 | AP50 | 62.1 | Faster RCNN-FPN+ | COCO | Table 1 |
| M-026 | AP75 | 45.5 | Faster RCNN-FPN+ | COCO | Table 1 |
| M-027 | APS | 26.6 | Faster RCNN-FPN+ | COCO | Table 1 |
| M-028 | APM | 45.9 | Faster RCNN-FPN+ | COCO | Table 1 |
| M-029 | APL | 54.6 | Faster RCNN-FPN+ | COCO | Table 1 |
| M-030 | AP | 42.0 | Ours | COCO | Table 1 |
| M-031 | AP50 | 62.4 | Ours | COCO | Table 1 |
| M-032 | AP75 | 44.2 | Ours | COCO | Table 1 |
| M-033 | APS | 20.5 | Ours | COCO | Table 1 |
| M-034 | APM | 45.8 | Ours | COCO | Table 1 |
| M-035 | APL | 61.1 | Ours | COCO | Table 1 |
| M-036 | AP | 43.3 | Ours | COCO | Table 1 |
| M-037 | AP50 | 63.1 | Ours | COCO | Table 1 |
| M-038 | AP75 | 45.9 | Ours | COCO | Table 1 |
| M-039 | APS | 21.9 | Ours | COCO | Table 1 |
| M-040 | APM | 46.2 | Ours | COCO | Table 1 |
| M-041 | APL | 61.9 | Ours | COCO | Table 1 |
| M-042 | AP | 44.9 | Ours | COCO | Table 1 |
| M-043 | AP50 | 64.3 | Ours | COCO | Table 1 |
| M-044 | AP75 | 47.7 | Ours | COCO | Table 1 |
| M-045 | APS | 23.7 | Ours | COCO | Table 1 |
| M-046 | APM | 49.5 | Ours | COCO | Table 1 |
| M-047 | APL | 63.8 | Ours | COCO | Table 1 |
| M-048 | AP | 45.4 | Ours | COCO | Table 1 |
| M-049 | AP50 | 64.7 | Ours | COCO | Table 1 |
| M-050 | AP75 | 48.0 | Ours | COCO | Table 1 |
| M-051 | APS | 24.0 | Ours | COCO | Table 1 |
| M-052 | APM | 49.0 | Ours | COCO | Table 1 |
| M-053 | APL | 64.5 | Ours | COCO | Table 1 |
| M-054 | AP | 46.2 | Ours | COCO | Table 1 |
| M-055 | AP50 | 65.2 | Ours | COCO | Table 1 |
| M-056 | AP75 | 49.0 | Ours | COCO | Table 1 |
| M-057 | APS | 25.1 | Ours | COCO | Table 1 |
| M-058 | APM | 50.0 | Ours | COCO | Table 1 |
| M-059 | APL | 65.8 | Ours | COCO | Table 1 |

## 对比结论

- [vs_baseline] AP +3.00 vs Faster RCNN-DC5 (COCO)
- [vs_baseline] AP +1.80 vs Faster RCNN-FPN (COCO)
- [vs_baseline] AP +0.00 vs Faster RCNN-R101-FPN (COCO)
- [vs_baseline] AP +0.90 vs Faster RCNN-DC5+ (COCO)
- [vs_baseline] AP +0.00 vs Faster RCNN-FPN+ (COCO)
- [vs_baseline] AP +4.30 vs Faster RCNN-DC5 (COCO)
- [vs_baseline] AP +3.10 vs Faster RCNN-FPN (COCO)
- [vs_baseline] AP +1.30 vs Faster RCNN-R101-FPN (COCO)
- [vs_baseline] AP +2.20 vs Faster RCNN-DC5+ (COCO)
- [vs_baseline] AP +1.30 vs Faster RCNN-FPN+ (COCO)
- [vs_baseline] AP +5.90 vs Faster RCNN-DC5 (COCO)
- [vs_baseline] AP +4.70 vs Faster RCNN-FPN (COCO)
- [vs_baseline] AP +2.90 vs Faster RCNN-R101-FPN (COCO)
- [vs_baseline] AP +3.80 vs Faster RCNN-DC5+ (COCO)
- [vs_baseline] AP +2.90 vs Faster RCNN-FPN+ (COCO)
- [vs_baseline] AP +6.40 vs Faster RCNN-DC5 (COCO)
- [vs_baseline] AP +5.20 vs Faster RCNN-FPN (COCO)
- [vs_baseline] AP +3.40 vs Faster RCNN-R101-FPN (COCO)
- [vs_baseline] AP +4.30 vs Faster RCNN-DC5+ (COCO)
- [vs_baseline] AP +3.40 vs Faster RCNN-FPN+ (COCO)
- [vs_baseline] AP +7.20 vs Faster RCNN-DC5 (COCO)
- [vs_baseline] AP +6.00 vs Faster RCNN-FPN (COCO)
- [vs_baseline] AP +4.20 vs Faster RCNN-R101-FPN (COCO)
- [vs_baseline] AP +5.10 vs Faster RCNN-DC5+ (COCO)
- [vs_baseline] AP +4.20 vs Faster RCNN-FPN+ (COCO)
- [vs_baseline] AP50 +1.90 vs Faster RCNN-DC5 (COCO)
- [vs_baseline] AP50 +1.40 vs Faster RCNN-FPN (COCO)
- [vs_baseline] AP50 -0.10 vs Faster RCNN-R101-FPN (COCO)
- [vs_baseline] AP50 +1.00 vs Faster RCNN-DC5+ (COCO)
- [vs_baseline] AP50 +0.30 vs Faster RCNN-FPN+ (COCO)
- [vs_baseline] AP50 +2.60 vs Faster RCNN-DC5 (COCO)
- [vs_baseline] AP50 +2.10 vs Faster RCNN-FPN (COCO)
- [vs_baseline] AP50 +0.60 vs Faster RCNN-R101-FPN (COCO)
- [vs_baseline] AP50 +1.70 vs Faster RCNN-DC5+ (COCO)
- [vs_baseline] AP50 +1.00 vs Faster RCNN-FPN+ (COCO)
- [vs_baseline] AP50 +3.80 vs Faster RCNN-DC5 (COCO)
- [vs_baseline] AP50 +3.30 vs Faster RCNN-FPN (COCO)
- [vs_baseline] AP50 +1.80 vs Faster RCNN-R101-FPN (COCO)
- [vs_baseline] AP50 +2.90 vs Faster RCNN-DC5+ (COCO)
- [vs_baseline] AP50 +2.20 vs Faster RCNN-FPN+ (COCO)
- [vs_baseline] AP50 +4.20 vs Faster RCNN-DC5 (COCO)
- [vs_baseline] AP50 +3.70 vs Faster RCNN-FPN (COCO)
- [vs_baseline] AP50 +2.20 vs Faster RCNN-R101-FPN (COCO)
- [vs_baseline] AP50 +3.30 vs Faster RCNN-DC5+ (COCO)
- [vs_baseline] AP50 +2.60 vs Faster RCNN-FPN+ (COCO)
- [vs_baseline] AP50 +4.70 vs Faster RCNN-DC5 (COCO)
- [vs_baseline] AP50 +4.20 vs Faster RCNN-FPN (COCO)
- [vs_baseline] AP50 +2.70 vs Faster RCNN-R101-FPN (COCO)
- [vs_baseline] AP50 +3.80 vs Faster RCNN-DC5+ (COCO)
- [vs_baseline] AP50 +3.10 vs Faster RCNN-FPN+ (COCO)
- [vs_baseline] AP75 +1.90 vs Faster RCNN-DC5 (COCO)
- [vs_baseline] AP75 +0.40 vs Faster RCNN-FPN (COCO)
- [vs_baseline] AP75 -1.70 vs Faster RCNN-R101-FPN (COCO)
- [vs_baseline] AP75 -0.10 vs Faster RCNN-DC5+ (COCO)
- [vs_baseline] AP75 -1.30 vs Faster RCNN-FPN+ (COCO)
- [vs_baseline] AP75 +3.60 vs Faster RCNN-DC5 (COCO)
- [vs_baseline] AP75 +2.10 vs Faster RCNN-FPN (COCO)
- [vs_baseline] AP75 +0.00 vs Faster RCNN-R101-FPN (COCO)
- [vs_baseline] AP75 +1.60 vs Faster RCNN-DC5+ (COCO)
- [vs_baseline] AP75 +0.40 vs Faster RCNN-FPN+ (COCO)
- [vs_baseline] AP75 +5.40 vs Faster RCNN-DC5 (COCO)
- [vs_baseline] AP75 +3.90 vs Faster RCNN-FPN (COCO)
- [vs_baseline] AP75 +1.80 vs Faster RCNN-R101-FPN (COCO)
- [vs_baseline] AP75 +3.40 vs Faster RCNN-DC5+ (COCO)
- [vs_baseline] AP75 +2.20 vs Faster RCNN-FPN+ (COCO)
- [vs_baseline] AP75 +5.70 vs Faster RCNN-DC5 (COCO)
- [vs_baseline] AP75 +4.20 vs Faster RCNN-FPN (COCO)
- [vs_baseline] AP75 +2.10 vs Faster RCNN-R101-FPN (COCO)
- [vs_baseline] AP75 +3.70 vs Faster RCNN-DC5+ (COCO)
- [vs_baseline] AP75 +2.50 vs Faster RCNN-FPN+ (COCO)
- [vs_baseline] AP75 +6.70 vs Faster RCNN-DC5 (COCO)
- [vs_baseline] AP75 +5.20 vs Faster RCNN-FPN (COCO)
- [vs_baseline] AP75 +3.10 vs Faster RCNN-R101-FPN (COCO)
- [vs_baseline] AP75 +4.70 vs Faster RCNN-DC5+ (COCO)
- [vs_baseline] AP75 +3.50 vs Faster RCNN-FPN+ (COCO)
- [vs_baseline] APL +8.60 vs Faster RCNN-DC5 (COCO)
- [vs_baseline] APL +9.10 vs Faster RCNN-FPN (COCO)
- [vs_baseline] APL +6.50 vs Faster RCNN-R101-FPN (COCO)
- [vs_baseline] APL +6.10 vs Faster RCNN-DC5+ (COCO)
- [vs_baseline] APL +6.50 vs Faster RCNN-FPN+ (COCO)
- [vs_baseline] APL +9.40 vs Faster RCNN-DC5 (COCO)
- [vs_baseline] APL +9.90 vs Faster RCNN-FPN (COCO)
- [vs_baseline] APL +7.30 vs Faster RCNN-R101-FPN (COCO)
- [vs_baseline] APL +6.90 vs Faster RCNN-DC5+ (COCO)
- [vs_baseline] APL +7.30 vs Faster RCNN-FPN+ (COCO)
- [vs_baseline] APL +11.30 vs Faster RCNN-DC5 (COCO)
- [vs_baseline] APL +11.80 vs Faster RCNN-FPN (COCO)
- [vs_baseline] APL +9.20 vs Faster RCNN-R101-FPN (COCO)
- [vs_baseline] APL +8.80 vs Faster RCNN-DC5+ (COCO)
- [vs_baseline] APL +9.20 vs Faster RCNN-FPN+ (COCO)
- [vs_baseline] APL +12.00 vs Faster RCNN-DC5 (COCO)
- [vs_baseline] APL +12.50 vs Faster RCNN-FPN (COCO)
- [vs_baseline] APL +9.90 vs Faster RCNN-R101-FPN (COCO)
- [vs_baseline] APL +9.50 vs Faster RCNN-DC5+ (COCO)
- [vs_baseline] APL +9.90 vs Faster RCNN-FPN+ (COCO)
- [vs_baseline] APL +13.30 vs Faster RCNN-DC5 (COCO)
- [vs_baseline] APL +13.80 vs Faster RCNN-FPN (COCO)
- [vs_baseline] APL +11.20 vs Faster RCNN-R101-FPN (COCO)
- [vs_baseline] APL +10.80 vs Faster RCNN-DC5+ (COCO)
- [vs_baseline] APL +11.20 vs Faster RCNN-FPN+ (COCO)
- [vs_baseline] APM +2.30 vs Faster RCNN-DC5 (COCO)
- [vs_baseline] APM +2.30 vs Faster RCNN-FPN (COCO)
- [vs_baseline] APM +0.20 vs Faster RCNN-R101-FPN (COCO)
- [vs_baseline] APM -0.10 vs Faster RCNN-DC5+ (COCO)
- [vs_baseline] APM -0.10 vs Faster RCNN-FPN+ (COCO)
- [vs_baseline] APM +2.70 vs Faster RCNN-DC5 (COCO)
- [vs_baseline] APM +2.70 vs Faster RCNN-FPN (COCO)
- [vs_baseline] APM +0.60 vs Faster RCNN-R101-FPN (COCO)
- [vs_baseline] APM +0.30 vs Faster RCNN-DC5+ (COCO)
- [vs_baseline] APM +0.30 vs Faster RCNN-FPN+ (COCO)
- [vs_baseline] APM +6.00 vs Faster RCNN-DC5 (COCO)
- [vs_baseline] APM +6.00 vs Faster RCNN-FPN (COCO)
- [vs_baseline] APM +3.90 vs Faster RCNN-R101-FPN (COCO)
- [vs_baseline] APM +3.60 vs Faster RCNN-DC5+ (COCO)
- [vs_baseline] APM +3.60 vs Faster RCNN-FPN+ (COCO)
- [vs_baseline] APM +5.50 vs Faster RCNN-DC5 (COCO)
- [vs_baseline] APM +5.50 vs Faster RCNN-FPN (COCO)
- [vs_baseline] APM +3.40 vs Faster RCNN-R101-FPN (COCO)
- [vs_baseline] APM +3.10 vs Faster RCNN-DC5+ (COCO)
- [vs_baseline] APM +3.10 vs Faster RCNN-FPN+ (COCO)
- [vs_baseline] APM +6.50 vs Faster RCNN-DC5 (COCO)
- [vs_baseline] APM +6.50 vs Faster RCNN-FPN (COCO)
- [vs_baseline] APM +4.40 vs Faster RCNN-R101-FPN (COCO)
- [vs_baseline] APM +4.10 vs Faster RCNN-DC5+ (COCO)
- [vs_baseline] APM +4.10 vs Faster RCNN-FPN+ (COCO)
- [vs_baseline] APS -0.90 vs Faster RCNN-DC5 (COCO)
- [vs_baseline] APS -3.70 vs Faster RCNN-FPN (COCO)
- [vs_baseline] APS -4.70 vs Faster RCNN-R101-FPN (COCO)
- [vs_baseline] APS -2.40 vs Faster RCNN-DC5+ (COCO)
- [vs_baseline] APS -6.10 vs Faster RCNN-FPN+ (COCO)
- [vs_baseline] APS +0.50 vs Faster RCNN-DC5 (COCO)
- [vs_baseline] APS -2.30 vs Faster RCNN-FPN (COCO)
- [vs_baseline] APS -3.30 vs Faster RCNN-R101-FPN (COCO)
- [vs_baseline] APS -1.00 vs Faster RCNN-DC5+ (COCO)
- [vs_baseline] APS -4.70 vs Faster RCNN-FPN+ (COCO)
- [vs_baseline] APS +2.30 vs Faster RCNN-DC5 (COCO)
- [vs_baseline] APS -0.50 vs Faster RCNN-FPN (COCO)
- [vs_baseline] APS -1.50 vs Faster RCNN-R101-FPN (COCO)
- [vs_baseline] APS +0.80 vs Faster RCNN-DC5+ (COCO)
- [vs_baseline] APS -2.90 vs Faster RCNN-FPN+ (COCO)
- [vs_baseline] APS +2.60 vs Faster RCNN-DC5 (COCO)
- [vs_baseline] APS -0.20 vs Faster RCNN-FPN (COCO)
- [vs_baseline] APS -1.20 vs Faster RCNN-R101-FPN (COCO)
- [vs_baseline] APS +1.10 vs Faster RCNN-DC5+ (COCO)
- [vs_baseline] APS -2.60 vs Faster RCNN-FPN+ (COCO)
- [vs_baseline] APS +3.70 vs Faster RCNN-DC5 (COCO)
- [vs_baseline] APS +0.90 vs Faster RCNN-FPN (COCO)
- [vs_baseline] APS -0.10 vs Faster RCNN-R101-FPN (COCO)
- [vs_baseline] APS +2.20 vs Faster RCNN-DC5+ (COCO)
- [vs_baseline] APS -1.50 vs Faster RCNN-FPN+ (COCO)
- [coverage] covers 1 datasets: COCO
- [statistics] no variance/std disclosure detected

## 维度得分

| 维度 | 得分 | 置信度 | 证据 |
|---|---|---|---|
| 创新性/新颖性 | 5.0 | high | We present a new method that views object detection as a direct set prediction problem.；Our approach streamlines the detection pipeline, effectively removing the need for many hand-designed components like a non-maximum suppression procedure or anchor generation that explicitly encode our prior knowledge about the task.；The main ingredients of the new framework, called DEtection TRansformer or DETR, are a set-based global loss that forces unique predictions via bipartite matching, and a transformer encoder-decoder architecture.；Compared to most previous work on direct set prediction, the main features of DETR are the conjunction of the bipartite matching loss and transformers with (non-autoregressive) parallel decoding.；In contrast, previous work focused on autoregressive decoding with RNNs. |
| 学术贡献度 | 5.0 | high | The main ingredients of the new framework, called DEtection TRansformer or DETR, are a set-based global loss that forces unique predictions via bipartite matching, and a transformer encoder-decoder architecture.；Given a fixed small set of learned object queries, DETR reasons about the relations of the objects and the global image context to directly output the final set of predictions in parallel.；The new model is conceptually simple and does not require a specialized library, unlike many other modern detectors.；The design ethos of DETR easily extend to more complex tasks. |
| 技术稳健性 | 4.0 | high | AP +3.00 vs Faster RCNN-DC5 (COCO)；AP +1.80 vs Faster RCNN-FPN (COCO)；AP +0.00 vs Faster RCNN-R101-FPN (COCO)；AP +0.90 vs Faster RCNN-DC5+ (COCO)；AP +0.00 vs Faster RCNN-FPN+ (COCO)；AP +4.30 vs Faster RCNN-DC5 (COCO)；AP +3.10 vs Faster RCNN-FPN (COCO)；AP +1.30 vs Faster RCNN-R101-FPN (COCO)；AP +2.20 vs Faster RCNN-DC5+ (COCO)；AP +1.30 vs Faster RCNN-FPN+ (COCO)；AP +5.90 vs Faster RCNN-DC5 (COCO)；AP +4.70 vs Faster RCNN-FPN (COCO)；AP +2.90 vs Faster RCNN-R101-FPN (COCO)；AP +3.80 vs Faster RCNN-DC5+ (COCO)；AP +2.90 vs Faster RCNN-FPN+ (COCO)；AP +6.40 vs Faster RCNN-DC5 (COCO)；AP +5.20 vs Faster RCNN-FPN (COCO)；AP +3.40 vs Faster RCNN-R101-FPN (COCO)；AP +4.30 vs Faster RCNN-DC5+ (COCO)；AP +3.40 vs Faster RCNN-FPN+ (COCO)；AP +7.20 vs Faster RCNN-DC5 (COCO)；AP +6.00 vs Faster RCNN-FPN (COCO)；AP +4.20 vs Faster RCNN-R101-FPN (COCO)；AP +5.10 vs Faster RCNN-DC5+ (COCO)；AP +4.20 vs Faster RCNN-FPN+ (COCO)；It obtains, however, lower performances on small objects. |
| 声明-证据一致性 | 5.0 | high | AP +3.00 vs Faster RCNN-DC5 (COCO)；AP +1.80 vs Faster RCNN-FPN (COCO)；AP +0.00 vs Faster RCNN-R101-FPN (COCO)；AP +0.90 vs Faster RCNN-DC5+ (COCO)；AP +0.00 vs Faster RCNN-FPN+ (COCO)；AP +4.30 vs Faster RCNN-DC5 (COCO)；AP +3.10 vs Faster RCNN-FPN (COCO)；AP +1.30 vs Faster RCNN-R101-FPN (COCO)；AP +2.20 vs Faster RCNN-DC5+ (COCO)；AP +1.30 vs Faster RCNN-FPN+ (COCO)；AP +5.90 vs Faster RCNN-DC5 (COCO)；AP +4.70 vs Faster RCNN-FPN (COCO)；AP +2.90 vs Faster RCNN-R101-FPN (COCO)；AP +3.80 vs Faster RCNN-DC5+ (COCO)；AP +2.90 vs Faster RCNN-FPN+ (COCO)；AP +6.40 vs Faster RCNN-DC5 (COCO)；AP +5.20 vs Faster RCNN-FPN (COCO)；AP +3.40 vs Faster RCNN-R101-FPN (COCO)；AP +4.30 vs Faster RCNN-DC5+ (COCO)；AP +3.40 vs Faster RCNN-FPN+ (COCO)；AP +7.20 vs Faster RCNN-DC5 (COCO)；AP +6.00 vs Faster RCNN-FPN (COCO)；AP +4.20 vs Faster RCNN-R101-FPN (COCO)；AP +5.10 vs Faster RCNN-DC5+ (COCO)；AP +4.20 vs Faster RCNN-FPN+ (COCO)；It obtains, however, lower performances on small objects. |
| 实验有效性与偏置控制 | 4.0 | high | AP +3.00 vs Faster RCNN-DC5 (COCO)；AP +1.80 vs Faster RCNN-FPN (COCO)；AP +0.00 vs Faster RCNN-R101-FPN (COCO)；AP +0.90 vs Faster RCNN-DC5+ (COCO)；AP +0.00 vs Faster RCNN-FPN+ (COCO)；AP +4.30 vs Faster RCNN-DC5 (COCO)；AP +3.10 vs Faster RCNN-FPN (COCO)；AP +1.30 vs Faster RCNN-R101-FPN (COCO)；AP +2.20 vs Faster RCNN-DC5+ (COCO)；AP +1.30 vs Faster RCNN-FPN+ (COCO)；AP +5.90 vs Faster RCNN-DC5 (COCO)；AP +4.70 vs Faster RCNN-FPN (COCO)；AP +2.90 vs Faster RCNN-R101-FPN (COCO)；AP +3.80 vs Faster RCNN-DC5+ (COCO)；AP +2.90 vs Faster RCNN-FPN+ (COCO)；AP +6.40 vs Faster RCNN-DC5 (COCO)；AP +5.20 vs Faster RCNN-FPN (COCO)；AP +3.40 vs Faster RCNN-R101-FPN (COCO)；AP +4.30 vs Faster RCNN-DC5+ (COCO)；AP +3.40 vs Faster RCNN-FPN+ (COCO)；AP +7.20 vs Faster RCNN-DC5 (COCO)；AP +6.00 vs Faster RCNN-FPN (COCO)；AP +4.20 vs Faster RCNN-R101-FPN (COCO)；AP +5.10 vs Faster RCNN-DC5+ (COCO)；AP +4.20 vs Faster RCNN-FPN+ (COCO)；The new model requires extra-long training schedule and benefits from auxiliary decoding losses in the transformer. |
| 泛化性与部署稳健性 | 2.0 | high | covers 1 datasets: COCO |
| 统计严谨性与披露 | 1.0 | high | no variance/std disclosure detected |
| 可复现性 | 5.0 | high | Training code and pretrained models are available at https://github.com/facebookresearch/detr.；Unlike most existing detection methods, DETR doesn’t require any customized layers, and thus can be reproduced easily in any framework that contains standard CNN and transformer classes.；Inference code for DETR can be implemented in less than 50 lines in PyTorch. |
| 开放性与资源可得性 | 5.0 | high | Training code and pretrained models are available at https://github.com/facebookresearch/detr.；Unlike most existing detection methods, DETR doesn’t require any customized layers, and thus can be reproduced easily in any framework that contains standard CNN and transformer classes.；Inference code for DETR can be implemented in less than 50 lines in PyTorch. |
| 数据集贡献 | 0.0 | high | - |
| 表述清晰度 | 5.0 | high | The overall DETR architecture is surprisingly simple and depicted in Figure 2.；It contains three main components, which we describe below: a CNN backbone to extract a compact feature representation, an encoder-decoder transformer, and a simple feed forward network (FFN) that makes the final detection prediction.；Unlike many modern detectors, DETR can be implemented in any deep learning framework that provides a common CNN backbone and a transformer architecture implementation with just a few hundred lines.；We hope that the simplicity of our method will attract new researchers to the detection community. |
| 相关工作与引用充分性 | 5.0 | high | Our work build on prior work in several domains: bipartite matching losses for set prediction, encoder-decoder architectures based on the transformer, parallel decoding, and object detection methods.；There is no canonical deep learning model to directly predict sets.；The basic set prediction task is multilabel classification (see e.g., [40,33] for references in the context of computer vision) for which the baseline approach, one-vs-rest, does not apply to problems such as detection where there is an underlying structure between elements (i.e., near-identical boxes).；The first difficulty in these tasks is to avoid near-duplicates.；Most current detectors use postprocessings such as non-maximal suppression to address this issue, but direct set prediction are postprocessing-free.；They need global inference schemes that model interactions between all predicted elements to avoid redundancy.；For constant-size set prediction, dense fully connected networks [9] are sufficient but costly.；A general approach is to use auto-regressive sequence models such as recurrent neural networks [48].；In all cases, the loss function should be invariant by a permutation of the predictions.；The usual solution is to design a loss based on the Hungarian algorithm [20], to find a bipartite matching between ground-truth and prediction.；This enforces permutation-invariance, and guarantees that each target element has a unique match.；We follow the bipartite matching loss approach.；In contrast to most prior work however, we step away from autoregressive models and use transformers with parallel decoding, which we describe below.；Transformers were introduced by Vaswani et al. [47] as a new attention-based building block for machine translation.；Attention mechanisms [2] are neural network layers that aggregate information from the entire input sequence.；Transformers introduced self-attention layers, which, similarly to Non-Local Neural Networks [49], scan through each element of a sequence and update it by aggregating information from the whole sequence.；One of the main advantages of attention-based models is their global computations and perfect memory, which makes them more suitable than RNNs on long sequences.；Transformers are now replacing RNNs in many problems in natural language processing, speech processing and computer vision [8,27,45,34,31].；Transformers were first used in auto-regressive models, following early sequence-to-sequence models [44], generating output tokens one by one.；However, the prohibitive inference cost (proportional to output length, and hard to batch) lead to the development of parallel sequence generation, in the domains of audio [29], machine translation [12,10], word representation learning [8], and more recently speech recognition [6].；We also combine transformers and parallel decoding for their suitable trade-off between computational cost and the ability to perform the global computations required for set prediction.；Most modern object detection methods make predictions relative to some initial guesses.；Two-stage detectors [37,5] predict boxes w.r.t. proposals, whereas single-stage methods make predictions w.r.t. anchors [23] or a grid of possible object centers [53,46].；Recent work [52] demonstrate that the final performance of these systems heavily depends on the exact way these initial guesses are set.；In our model we are able to remove this hand-crafted process and streamline the detection process by directly predicting the set of detections with absolute box prediction w.r.t. the input image rather than an anchor.；Set-based loss. Several object detectors [9,25,35] used the bipartite matching loss.；However, in these early deep learning models, the relation between different prediction was modeled with convolutional or fully-connected layers only and a hand-designed NMS post-processing can improve their performance.；More recent detectors [37,23,53] use non-unique assignment rules between ground truth and predictions together with an NMS.；Learnable NMS methods [16,4] and relation networks [17] explicitly model relations between different predictions with attention.；Using direct set losses, they do not require any post-processing steps.；However, these methods employ additional hand-crafted context features like proposal box coordinates to model relations between detections efficiently, while we look for solutions that reduce the prior knowledge encoded in the model.；Recurrent detectors. Closest to our approach are end-to-end set predictions for object detection [43] and instance segmentation [41,30,36,42].；Similarly to us, they use bipartite-matching losses with encoder-decoder architectures based on CNN activations to directly produce a set of bounding boxes.；These approaches, however, were only evaluated on small datasets and not against modern baselines.；In particular, they are based on autoregressive models (more precisely RNNs), so they do not leverage the recent transformers with parallel decoding. |
| 伦理合规 | 0.0 | high | - |
| 局限性与诚实评估 | 4.0 | high | It obtains, however, lower performances on small objects.；We expect that future work will improve this aspect in the same way the development of FPN did for Faster R-CNN.；The new model requires extra-long training schedule and benefits from auxiliary decoding losses in the transformer. |
| 学科归一化引文影响力 | - | medium | - |
| 引文有效性与边界 | - | medium | - |
| 社会/综合影响力 | - | medium | - |
| 文章级影响力指标 | - | medium | - |
| Altmetrics | - | medium | - |
| 期刊层指标与边界 | - | medium | - |
| 作者层指标 | - | medium | - |
| 组合新颖性 | - | medium | - |
| 作者声望偏差 | - | medium | - |
| 新颖性-影响-性能平衡 | - | medium | - |

## 优势
- 创新性/新颖性 (5.0)
- 学术贡献度 (5.0)
- 声明-证据一致性 (5.0)

## 不足
- 统计严谨性与披露 (1.0)
- 数据集贡献 (0.0)
- 伦理合规 (0.0)

## 综合结论

整体评分 3.57/5；主要优势：创新性/新颖性 (5.0)、学术贡献度 (5.0)、声明-证据一致性 (5.0)；主要不足：统计严谨性与披露 (1.0)、数据集贡献 (0.0)、伦理合规 (0.0)。

## 未评估 / 待审核

- 学科归一化引文影响力：需外部数据，未评估
- 引文有效性与边界：需外部数据，未评估
- 社会/综合影响力：需外部数据，未评估
- 文章级影响力指标：需外部数据，未评估
- Altmetrics：需外部数据，未评估
- 期刊层指标与边界：需外部数据，未评估
- 作者层指标：需外部数据，未评估
- 组合新颖性：争议维度，待人工审核
- 作者声望偏差：争议维度，待人工审核
- 新颖性-影响-性能平衡：争议维度，待人工审核