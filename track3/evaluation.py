import os
import json
import argparse
from collections import defaultdict, OrderedDict
from torchmetrics import SacreBLEUScore
from bert_score import score
import torch
import distance
from transformers import BertTokenizer, BertForMaskedLM

DATA_PATH = './examples'

def read_json(path):
    """读取json文件"""
    with open(path, 'r') as fjson:
        return json.load(fjson, object_pairs_hook=OrderedDict)

def bert_ppl(sentences):
    """bert ppl"""
    tokenizer = BertTokenizer.from_pretrained('bert-base-chinese')
    model = BertForMaskedLM.from_pretrained('bert-base-chinese')
    scores = []
    for s in sentences:
        input_ids = torch.tensor(tokenizer.encode(s)).unsqueeze(0) # [ba, seq_len]
        with torch.no_grad():
            outputs = model(input_ids, labels=input_ids)
            loss = outputs[0]
        scores.append(torch.exp(loss).cpu().item())
    return sum(scores)/len(scores)

def bleu(preds, golds):
    """bleu"""
    bleu = SacreBLEUScore(tokenize='zh')
    golds = [[g] for g in golds]
    return bleu(preds, golds)

def bert_score(preds, golds):
    """bert score"""
    P, R, F1 = score(preds, golds, lang='zh', verbose=True)
    return torch.mean(F1).cpu().item()

def levenshtein(preds, inputs):
    """编辑距离"""
    dist = [distance.levenshtein(p, g) for p, g in zip(preds, inputs)]
    return sum(dist)/len(dist)


if __name__=="__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument("--preds", type=str, default=os.path.join(DATA_PATH, 'pred.json'), help="pred data path")
    parser.add_argument("--golds", type=str, default=os.path.join(DATA_PATH, 'gold.json'), help="gold data path")

    args = parser.parse_args()

    preds = read_json(args.preds)
    golds = read_json(args.golds)

    pred_tags = [p['revisedSent'] for p in preds]
    gold_tags = [g['revisedSent'] for g in golds]
    input_tags = [g['sent'] for g in golds]

    bleu_s = bleu(pred_tags, gold_tags)
    bert_s = bert_score(pred_tags, gold_tags)
    ppl_s = bert_ppl(pred_tags)
    l_s = levenshtein(pred_tags, input_tags)

    print(f"bert ppl score: {ppl_s:2f}")
    print(f"levenshtein score: {l_s:2f}")
    print(f"bleu score: {bleu_s:.4f}")
    print(f"bert score: {bert_s:.4f}")
    
