# 赛道2：中小学作文字符级错误识别与纠正
## 1 排行榜

### Track2测试集B排行榜

&emsp;&emsp;我们提供了各参赛队伍在错误类型识别和错误纠正的效果供大家参考，具体包括F1_score（各指标加权F1）、Identify（错误类型识别F1）、Correct（错误纠正F1）、Char_detection（字粒度检测F1）、Char_correction（字粒度纠正F1）、Sent_detection（句粒度检测F1）、Sent_correction（句粒度纠正F1），最终按照F1_score分数进行排名。

&emsp;&emsp;结果统计截止至2023年6月9日，榜单更新时间：2023年6月13日。

| Team Name | Email | F1_score | Identify | Correct | Char_detection | Char_correction | Sent_detection | Sent_correction |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 切忌不要改队 | yix***@ir.hit.edu.cn | 67.33 | 74.22 | 60.44 | 62.28 | 62.76 | 55.86 | 40.02 |
| yang | 231***@qq.com | 59.85 | 67.08 | 52.61 | 53.86 | 55.01 | 49.81 | 34.28 |

&emsp;&emsp;2023年6月9日提交结果：

| Team Name | Email | F1_score | Identify | Correct | Char_detection | Char_correction | Sent_detection | Sent_correction |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| yang | 231***@qq.com | 59.44 | 67.30 | 51.57 | 52.50 | 55.77 | 48.16 | 33.46 |
| 切忌不要改队 | yix***@ir.hit.edu.cn | 66.75 | 73.16 | 60.33 | 62.23 | 61.95 | 56.24 | 39.81 |

&emsp;&emsp;2023年6月8日提交结果：

| Team Name | Email | F1_score | Identify | Correct | Char_detection | Char_correction | Sent_detection | Sent_correction |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| yang | 231***@qq.com | 59.89 | 67.30 | 52.48 | 53.32 | 56.61 | 49.50 | 34.31 |

&emsp;&emsp;2023年6月7日提交结果：

| Team Name | Email | F1_score | Identify | Correct | Char_detection | Char_correction | Sent_detection | Sent_correction |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| yang | 231***@qq.com | 49.84 | 58.15 | 41.52 | 41.09 | 47.72 | 40.50 | 27.72 |

### 测试集A排行榜

| Team Name | Email | F1_score | Identify | Correct | Char_detection | Char_correction | Sent_detection | Sent_correction |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| yang | 231***@qq.com | 54.42 | 56.73 | 52.12 | 53.49 | 54.93 | 48.29 | 34.32 |
| 切忌不要改队 | yix***@ir.hit.edu.cn | 19.99 | 36.77 | 3.21 | 4.00 | 2.06 | 1.85 | 0.58 |

## 2 任务简述

- 任务描述：

&emsp;&emsp;中小学作文字符级错误识别与纠正任务旨在自动检测并修改作文中的标点、错别字、缺字漏字等错误，能够反映作者语言使用的规范性，是自然语言处理领域的一项重要任务，也是作文流畅性评价的一项重要工作。以往的文本错误识别与纠错任务数据集通常是基于规则生成的伪数据，或是外国语言学者撰写的文本，对于以中文为母语的用户来说缺乏准确性。因此，一个来源于实际场景，并从更多方面整合影响作文流畅性基本因素的字符级错误识别与纠正任务具有重要研究意义。本次评测任务从缺字漏字、错别字错误、缺少标点、错用标点四个角度研究中小学作文字符级错误的识别与纠正问题。

- 任务定义：

&emsp;&emsp;中小学作文字符级错误主要聚焦于四个方面：缺字漏字、错别字错误、缺少标点、错用标点，字符级错误类别识别任务为多标签分类任务。字符级错误识别与纠正以作文句子作为输入，输出错误类别和修改方式三元组，三元组内容包含所在原句位置、要执行的操作（A-增加，R-替换，D-删除）、及对应位置修改结果；错误类别定义及示例如下表2所示：

![表2 中小学作文字符级错误识别与纠正赛道错误类型](https://github.com/paopaobubbletang/test/blob/main/%E8%A1%A82%E4%B8%AD%E5%B0%8F%E5%AD%A6%E4%BD%9C%E6%96%87%E5%AD%97%E7%AC%A6%E7%BA%A7%E9%94%99%E8%AF%AF%E8%AF%86%E5%88%AB%E4%B8%8E%E7%BA%A0%E6%AD%A3%E8%B5%9B%E9%81%93%E9%94%99%E8%AF%AF%E7%B1%BB%E5%9E%8B.png#{height="50%";width="50%";})
<p align="center">表2 中小学作文字符级错误识别与纠正赛道错误类型</p>

## 3 结果提交格式

```json
{
    "sent_id":"3201",
    "sent":"他把我推了推说：“我不需要你们的帮，我觉得我自己可以拼好。”",
    "CgecErrorType":["缺字漏字"],
    "results":[(17,'A','助')]
}
```
