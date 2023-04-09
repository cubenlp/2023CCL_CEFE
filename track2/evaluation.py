import os
import json
import argparse
from collections import defaultdict, OrderedDict

def read_json(path):
    """读取json文件"""
    with open(path, 'r') as fjson:
        return json.load(fjson, object_pairs_hook=OrderedDict)

DATA_PATH = './examples'

def calc_metrics(tp, p, t, percent=True):
    """
    compute overall precision, recall and FB1 (default values are 0.0)
    if percent is True, return 100 * original decimal value
    """
    precision = tp / p if p else 0
    recall = tp / t if t else 0
    fb1 = 2 * precision * recall / (precision + recall) if precision + recall else 0
    if percent:
        return 100 * precision, 100 * recall, 100 * fb1
    else:
        return precision, recall, fb1

def get_result(correct_counts, true_counts, pred_counts):

    # sum counts
    sum_correct_counts = sum(correct_counts.values())
    sum_true_counts = sum(true_counts.values())
    sum_pred_counts = sum(pred_counts.values())

    chunk_types = sorted(list(set(list(true_counts) + list(pred_counts))))

    # compute overall precision, recall and FB1 (default values are 0.0)
    prec, rec, f1 = calc_metrics(sum_correct_counts, sum_pred_counts, sum_true_counts)
    res = (prec, rec, f1)

    # print overall performance, and performance per type
    print("processed %i labels; " % (sum_true_counts), end='')
    print("found: %i labels; correct: %i.\n" % (sum_pred_counts, sum_correct_counts), end='')
    print("precision: %6.2f%%; recall: %6.2f%%; FB1: %6.2f" % (prec, rec, f1),end="")
    print("  (%d & %d) = %d" % (sum_pred_counts,sum_true_counts,sum_correct_counts))

    # for each type, compute precision, recall and FB1 (default values are 0.0)
    for t in chunk_types:
        prec, rec, f1 = calc_metrics(correct_counts[t], pred_counts[t], true_counts[t])
        print("%17s: " %t , end='')
        print("precision: %6.2f%%; recall: %6.2f%%; FB1: %6.2f" %
                    (prec, rec, f1), end='')
        print("  (%d & %d) = %d" % (pred_counts[t],true_counts[t],correct_counts[t]))

    return res

def MultiLabel_evaluate(pred_seqs, true_seqs):
    assert len(pred_seqs) == len(true_seqs)
    correct_counts = defaultdict(int)
    true_counts = defaultdict(int)
    pred_counts = defaultdict(int)

    for true_tag, pred_tag in zip(true_seqs, pred_seqs):
        if true_tag == []:
            true_tag = ['正确']
        if pred_tag == []:
            pred_tag = ['正确']
        for c in set(true_tag) & set(pred_tag):
            correct_counts[c] += 1
        for t in true_tag:
            true_counts[t] += 1
        for p in pred_tag:
            pred_counts[p] += 1
    
    results = get_result(correct_counts, true_counts, pred_counts)
    return results

def char_detection(pred_results, gold_results):
    assert len(pred_results) == len(gold_results)

    correct_counts = 0
    true_counts = 0
    pred_counts = 0

    for p_result, g_result in zip(pred_results, gold_results):
        p_idx = defaultdict(int)
        g_idx = defaultdict(int)

        for r in p_result:
            p_idx[(r[0], r[1])] = p_idx.get((r[0], r[1]), 0) + 1
        
        for r in g_result:
            g_idx[(r[0], r[1])] = g_idx.get((r[0], r[1]), 0) + 1
        
        true_counts += sum(g_idx.values())
        pred_counts += sum(p_idx.values())

        for key,value in g_idx.items():
            correct_counts += min(value, p_idx.get(key, 0))
    
    results = calc_metrics(correct_counts, pred_counts, true_counts)
    
    return results

def sent_detection(pred_results, gold_results):
    assert len(pred_results) == len(gold_results)
    correct_counts = 0
    true_counts = len([g for g in gold_results if g!=[]])
    pred_counts = len([p for p in pred_results if p!=[]])

    for p_result, g_result in zip(pred_results, gold_results):
        p_idx = defaultdict(int)
        g_idx = defaultdict(int)

        for r in p_result:
            p_idx[(r[0], r[1])] = p_idx.get((r[0], r[1]), 0) + 1
        
        for r in g_result:
            g_idx[(r[0], r[1])] = g_idx.get((r[0], r[1]), 0) + 1

        for key, value in g_idx.items():
            if key not in p_idx.keys() or p_idx[key] != value:
                break
        else:
            correct_counts += 1
    results = calc_metrics(correct_counts, pred_counts, true_counts)
    return results

def char_correction(pred_results, gold_results):
    assert len(pred_results) == len(gold_results)

    correct_counts = 0
    pred_counts = 0
    true_counts = sum([len(g) for g in gold_results])

    for p_result, g_result in zip(pred_results, gold_results):
        p_dict = {}
        g_dict = {}

        for r in p_result:
            p_dict[(r[0], r[1])] = r[-1]
        
        for r in g_result:
            g_dict[(r[0], r[1])] = r[-1]
        
        correct_idx = set(p_dict.keys()) & set(g_dict.keys())
        pred_counts += len(correct_idx)

        for key in correct_idx:
            if p_dict[key] == g_dict[key]:
                correct_counts += 1
    results = calc_metrics(correct_counts, pred_counts, true_counts)
    return results

def sent_correction(pred_results, gold_results):
    assert len(pred_results) == len(gold_results)

    correct_counts = 0
    true_counts = len([g for g in gold_results if g!=[]])
    pred_counts = len([p for p in pred_results if p!=[]])

    for p_result, g_result in zip(pred_results, gold_results):
        p = sorted(p_result, key=lambda x:x[0])
        g = sorted(g_result, key=lambda x:x[0])

        if p == g:
            correct_counts += 1
    
    results = calc_metrics(correct_counts, pred_counts, true_counts)
    return results

if __name__=="__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument("--preds", type=str, default=os.path.join(DATA_PATH, 'pred.json'), help="pred data path")
    parser.add_argument("--golds", type=str, default=os.path.join(DATA_PATH, 'gold.json'), help="gold data path")

    args = parser.parse_args()

    preds = read_json(args.preds)
    golds = read_json(args.golds)

    preds_identify = [p['CgecErrorType'] for p in preds]
    golds_identify = [g['CgecErrorType'] for g in golds]

    # 计算分类效果
    identify_s = MultiLabel_evaluate(preds_identify, golds_identify)

    preds_results = [p['results'] for p in preds]
    golds_results = [g['results'] for g in golds]

    # 计算纠错效果
    char_detection_s = char_detection(preds_results, golds_results)
    sent_detection_s = sent_detection(preds_results, golds_results)

    char_correction_s = char_correction(preds_results, golds_results)
    sent_correction_s = sent_correction(preds_results, golds_results)

    correct_s = 0.8 * (0.8*char_detection_s[-1] + 0.2*char_correction_s[-1]) + 0.2 * (0.8*sent_detection_s[-1] + 0.2*sent_correction_s[-1])

    final_score = 0.5 * identify_s[-1] + 0.5 * correct_s

    print(f"the final score is: {final_score:.2f}")

