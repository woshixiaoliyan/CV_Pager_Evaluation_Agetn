# 论文评价报告：End-to-End Object Detection with Transformers

- 来源：arxiv；arXiv: 2005.12872
- 综合评分：3.50/5

## 评价摘要

- 优势：创新性/新颖性 (5.0)、学术贡献度 (5.0)、可复现性 (5.0)
- 不足：统计严谨性与披露 (1.0)、数据集贡献 (0.0)、伦理合规 (0.0)
- 结论：整体评分 3.50/5；主要优势：创新性/新颖性 (5.0)、学术贡献度 (5.0)、可复现性 (5.0)；主要不足：统计严谨性与披露 (1.0)、数据集贡献 (0.0)、伦理合规 (0.0)。

## 实验指标摘要

| 数据集 | 指标 | 变体 | 本方法最优 | 基线最优 | 差值 | 对比方法数 |
|---|---|---|---|---|---|---|
| COCO | AP | AP | - | 45.10 | - | 14 |
| COCO | AP50 | AP50 | - | 79.90 | - | 8 |
| COCO | AP75 | AP75 | - | 55.50 | - | 8 |
| COCO | APL | APL | - | 55.00 | - | 8 |
| COCO | APM | APM | - | 50.50 | - | 8 |
| COCO | APS | APS | - | 33.00 | - | 8 |
| COCO | PQ | PQ | - | 45.10 | - | 7 |
| COCO | PQst | PQst | - | 37.30 | - | 6 |
| COCO | PQth | PQth | - | 51.00 | - | 6 |
| COCO | RQ | RQ | - | 55.50 | - | 7 |
| COCO | RQst | RQst | - | 46.50 | - | 6 |
| COCO | RQth | RQth | - | 60.60 | - | 6 |
| COCO | SQ | SQ | - | 79.90 | - | 7 |
| COCO | SQst | SQst | - | 78.70 | - | 6 |
| COCO | SQth | SQth | - | 83.20 | - | 6 |

> 完整指标与对比明细见 report.json。

## 对比结论摘要

- 无可对比的基线差值。
- [coverage] covers 1 datasets: COCO
- [statistics] no variance/std disclosure detected

## 维度得分

| 维度 | 得分 | 置信度 | 证据 |
|---|---|---|---|
| 创新性/新颖性 | 5.0 | high | We present a new method that views object detection as a direct set prediction problem.；The main ingredients of the new framework, called DEtection TRansformer or DETR, are a set-based global loss that forces unique predictions via bipartite matching, and a transformer encoder-decoder architecture.；Compared to most previous work on direct set prediction, the main features of DETR are the conjunction of the bipartite matching loss and transformers with (non-autoregressive) parallel decoding. |
| 学术贡献度 | 5.0 | high | Our approach streamlines the detection pipeline, effectively removing the need for many hand-designed components like a non-maximum suppression procedure or anchor generation that explicitly encode our prior knowledge about the task.；In our experiments, we show that a simple segmentation head trained on top of a pre-trained DETR outperfoms competitive baselines on Panoptic Segmentation. |
| 技术稳健性 | 3.0 | medium | It obtains, however, lower performances on small objects.；covers 1 datasets: COCO |
| 声明-证据一致性 | 4.0 | high | In our experiments, we show that a simple segmentation head trained on top of a pre-trained DETR outperfoms competitive baselines on Panoptic Segmentation.；It obtains, however, lower performances on small objects. |
| 实验有效性与偏置控制 | 4.0 | high | Training settings for DETR differ from standard object detectors in multiple ways. The new model requires extra-long training schedule and benefits from auxiliary decoding losses in the transformer. |
| 泛化性与部署稳健性 | 3.0 | high | covers 1 datasets: COCO；In our experiments, we show that a simple segmentation head trained on top of a pre-trained DETR outperfoms competitive baselines on Panoptic Segmentation. |
| 统计严谨性与披露 | 1.0 | high | no variance/std disclosure detected |
| 可复现性 | 5.0 | high | Training code and pretrained models are available at https://github.com/facebookresearch/detr.；Unlike most existing detection methods, DETR doesn’t require any customized layers, and thus can be reproduced easily in any framework that contains standard CNN and transformer classes.；Inference code for DETR can be implemented in less than 50 lines in PyTorch. |
| 开放性与资源可得性 | 5.0 | high | Training code and pretrained models are available at https://github.com/facebookresearch/detr. |
| 数据集贡献 | 0.0 | high | covers 1 datasets: COCO |
| 表述清晰度 | 5.0 | high | The overall DETR architecture is surprisingly simple and depicted in Figure 2.；It contains three main components, which we describe below: a CNN backbone to extract a compact feature representation, an encoder-decoder transformer, and a simple feed forward network (FFN) that makes the final detection prediction.；Unlike many modern detectors, DETR can be implemented in any deep learning framework that provides a common CNN backbone and a transformer architecture implementation with just a few hundred lines. |
| 相关工作与引用充分性 | 5.0 | high | Our work build on prior work in several domains: bipartite matching losses for set prediction, encoder-decoder architectures based on the transformer, parallel decoding, and object detection methods.；Transformers were introduced by Vaswani et al. as a new attention-based building block for machine translation.；Most modern object detection methods make predictions relative to some initial guesses. |
| 伦理合规 | 0.0 | high | - |
| 局限性与诚实评估 | 4.0 | high | It obtains, however, lower performances on small objects.；We expect that future work will improve this aspect in the same way the development of FPN did for Faster R-CNN.；Training settings for DETR differ from standard object detectors in multiple ways. The new model requires extra-long training schedule and benefits from auxiliary decoding losses in the transformer. |
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