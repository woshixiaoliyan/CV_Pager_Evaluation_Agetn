# 论文评价报告：End-to-End Object Detection with Transformers

- 来源：arxiv；arXiv: 2005.12872
- 综合评分：3.36/5

## 评价摘要

- 优势：创新性/新颖性 (5.0)、学术贡献度 (5.0)、可复现性 (5.0)
- 不足：统计严谨性与披露 (1.0)、数据集贡献 (0.0)、伦理合规 (0.0)
- 结论：整体评分 3.36/5；主要优势：创新性/新颖性 (5.0)、学术贡献度 (5.0)、可复现性 (5.0)；主要不足：统计严谨性与披露 (1.0)、数据集贡献 (0.0)、伦理合规 (0.0)。

## 实验指标摘要

| 数据集 | 指标 | 变体 | 本方法最优 | 基线最优 | 差值 | 对比方法数 |
|---|---|---|---|---|---|---|
| COCO val | AP | AP | - | 44.90 | - | 22 |
| COCO val | AP50 | AP50 | - | 64.70 | - | 22 |
| COCO val | AP75 | AP75 | - | 47.80 | - | 10 |
| COCO val | APL | APL | - | 62.30 | - | 17 |
| COCO val | APM | APM | - | 49.50 | - | 17 |
| COCO val | APS | APS | - | 27.20 | - | 17 |
| COCO val | PQ | PQ | - | 43.40 | - | 1 |
| COCO val | PQth | PQth | - | 48.20 | - | 1 |
| COCO val | RQ | RQ | - | 53.80 | - | 1 |
| COCO val | SQ | SQ | - | 79.30 | - | 1 |

⚠ 未能从论文中识别出“本方法”的实验行（可能为抽取遗漏），差值暂缺。

> 完整指标与对比明细见 report.json。

## 对比结论摘要

- 无可对比的基线差值。
- [coverage] covers 1 datasets: COCO val
- [statistics] no variance/std disclosure detected

## 维度得分

| 维度 | 得分 | 置信度 | 证据 |
|---|---|---|---|
| 创新性/新颖性 | 5.0 | high | We present a new method that views object detection as a direct set prediction problem.；Our approach streamlines the detection pipeline, effectively removing the need for many hand-designed components like a non-maximum suppression procedure or anchor generation that explicitly encode our prior knowledge about the task.；The main ingredients of the new framework, called DEtection TRansformer or DETR, are a set-based global loss that forces unique predictions via bipartite matching, and a transformer encoder-decoder architecture.；Compared to most previous work on direct set prediction, the main features of DETR are the conjunction of the bipartite matching loss and transformers with (non-autoregressive) parallel decoding. |
| 学术贡献度 | 5.0 | high | We present a new method that views object detection as a direct set prediction problem.；Our approach streamlines the detection pipeline, effectively removing the need for many hand-designed components like a non-maximum suppression procedure or anchor generation that explicitly encode our prior knowledge about the task.；The main ingredients of the new framework, called DEtection TRansformer or DETR, are a set-based global loss that forces unique predictions via bipartite matching, and a transformer encoder-decoder architecture. |
| 技术稳健性 | 3.0 | medium | It obtains, however, lower performances on small objects.；We expect that future work will improve this aspect in the same way the development of FPN did for Faster R-CNN. |
| 声明-证据一致性 | 4.0 | high | It obtains, however, lower performances on small objects.；The new model requires extra-long training schedule and benefits from auxiliary decoding losses in the transformer. |
| 实验有效性与偏置控制 | 3.0 | medium | The new model requires extra-long training schedule and benefits from auxiliary decoding losses in the transformer. |
| 泛化性与部署稳健性 | 2.0 | high | covers 1 datasets: COCO val |
| 统计严谨性与披露 | 1.0 | high | no variance/std disclosure detected |
| 可复现性 | 5.0 | high | Training code and pretrained models are available at https://github.com/facebookresearch/detr.；Unlike most existing detection methods, DETR doesn’t require any customized layers, and thus can be reproduced easily in any framework that contains standard CNN and transformer classes.；Inference code for DETR can be implemented in less than 50 lines in PyTorch. |
| 开放性与资源可得性 | 5.0 | high | Training code and pretrained models are available at https://github.com/facebookresearch/detr.；Unlike most existing detection methods, DETR doesn’t require any customized layers, and thus can be reproduced easily in any framework that contains standard CNN and transformer classes. |
| 数据集贡献 | 0.0 | high | - |
| 表述清晰度 | 5.0 | high | The overall DETR architecture is surprisingly simple and depicted in Figure 2.；It contains three main components, which we describe below: a CNN backbone to extract a compact feature representation, an encoder-decoder transformer, and a simple feed forward network (FFN) that makes the final detection prediction.；Unlike many modern detectors, DETR can be implemented in any deep learning framework that provides a common CNN backbone and a transformer architecture implementation with just a few hundred lines. |
| 相关工作与引用充分性 | 5.0 | high | Our work build on prior work in several domains: bipartite matching losses for set prediction, encoder-decoder architectures based on the transformer, parallel decoding, and object detection methods.；There is no canonical deep learning model to directly predict sets.；The first difficulty in these tasks is to avoid near-duplicates.；Most current detectors use postprocessings such as non-maximal suppression to address this issue, but direct set prediction are postprocessing-free.；They need global inference schemes that model interactions between all predicted elements to avoid redundancy.；For constant-size set prediction, dense fully connected networks are sufficient but costly.；A general approach is to use auto-regressive sequence models such as recurrent neural networks.；In all cases, the loss function should be invariant by a permutation of the predictions.；The usual solution is to design a loss based on the Hungarian algorithm, to find a bipartite matching between ground-truth and prediction.；This enforces permutation-invariance, and guarantees that each target element has a unique match.；We follow the bipartite matching loss approach.；In contrast to most prior work however, we step away from autoregressive models and use transformers with parallel decoding, which we describe below.；Transformers were introduced by Vaswani et al. as a new attention-based building block for machine translation.；Attention mechanisms are neural network layers that aggregate information from the entire input sequence.；Transformers introduced self-attention layers, which, similarly to Non-Local Neural Networks, scan through each element of a sequence and update it by aggregating information from the whole sequence.；One of the main advantages of attention-based models is their global computations and perfect memory, which makes them more suitable than RNNs on long sequences.；Transformers are now replacing RNNs in many problems in natural language processing, speech processing and computer vision.；Transformers were first used in auto-regressive models, following early sequence-to-sequence models, generating output tokens one by one.；However, the prohibitive inference cost (proportional to output length, and hard to batch) lead to the development of parallel sequence generation, in the domains of audio, machine translation, word representation learning, and more recently speech recognition.；We also combine transformers and parallel decoding for their suitable trade-off between computational cost and the ability to perform the global computations required for set prediction.；Most modern object detection methods make predictions relative to some initial guesses.；Two-stage detectors predict boxes w.r.t. proposals, whereas single-stage methods make predictions w.r.t. anchors or a grid of possible object centers.；Recent work demonstrate that the final performance of these systems heavily depends on the exact way these initial guesses are set.；Several object detectors used the bipartite matching loss.；However, in these early deep learning models, the relation between different prediction was modeled with convolutional or fully-connected layers only and a hand-designed NMS post-processing can improve their performance.；More recent detectors use non-unique assignment rules between ground truth and predictions together with an NMS.；Learnable NMS methods and relation networks explicitly model relations between different predictions with attention.；Using direct set losses, they do not require any post-processing steps.；However, these methods employ additional hand-crafted context features like proposal box coordinates to model relations between detections efficiently, while we look for solutions that reduce the prior knowledge encoded in the model.；Closest to our approach are end-to-end set predictions for object detection and instance segmentation.；Similarly to us, they use bipartite-matching losses with encoder-decoder architectures based on CNN activations to directly produce a set of bounding boxes.；These approaches, however, were only evaluated on small datasets and not against modern baselines.；In particular, they are based on autoregressive models (more precisely RNNs), so they do not leverage the recent transformers with parallel decoding. |
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