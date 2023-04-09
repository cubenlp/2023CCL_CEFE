import os
import json
import argparse
from collections import defaultdict, OrderedDict

DATA_PATH = './examples'

def read_json(path):
    """读取json文件"""
    with open(path, 'r') as fjson:
        return json.load(fjson, object_pairs_hook=OrderedDict)

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

if __name__=="__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument("--preds", type=str, default=os.path.join(DATA_PATH, 'pred.json'), help="pred data path")
    parser.add_argument("--golds", type=str, default=os.path.join(DATA_PATH, 'gold.json'), help="gold data path")

    args = parser.parse_args()

    preds = read_json(args.preds)
    golds = read_json(args.golds)

    course_preds_tags = [p['CourseGrainedErrorType'] for p in preds]
    course_golds_tags = [g['CourseGrainedErrorType'] for g in golds]

    course_score = MultiLabel_evaluate(course_preds_tags, course_golds_tags)

    fine_preds_tags = [p['FineGrainedErrorType'] for p in preds]
    fine_golds_tags = [g['FineGrainedErrorType'] for g in golds]

    fine_score = MultiLabel_evaluate(fine_preds_tags, fine_golds_tags)
    
    final_score = 0.5 * course_score[-1] + 0.5 * fine_score[-1]

    print(f"final scores: {final_score:.2f}")