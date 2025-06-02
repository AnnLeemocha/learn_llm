import requests
from bs4 import BeautifulSoup as BS
from tqdm import tqdm

from collections import Counter, defaultdict

import random

corpus = list()
for pid in tqdm(range(67, 186 + 1)):
    data = {"bid": 12, "id": pid}
    res = requests.post("http://open-lit.com/GETbook.php", data=data)
    res = BS(res.text)
    corpus.append(res.text)

print("=====================================================")

# \u3000 為全形空白
skip_symbols = ["\u3000", "\r", "\t", "\n"]
bigram = defaultdict(Counter)
for data in corpus:
    # 將空白字元移除
    for sym in skip_symbols:
        data = data.replace(sym, "")

    # 以 <BOS> 代表文本開頭，開始統計整份文本
    prev_char = "<BOS>"
    for ch in data:
        bigram[prev_char][ch] += 1
        prev_char = ch

    # 以 <EOS> 代表文本結尾
    ch = "<EOS>"
    bigram[prev_char][ch] += 1

print("=====================================================")

generate = str()
curr_ch = "<BOS>"
while curr_ch != "<EOS>":
    generate += curr_ch
    prob = bigram[curr_ch]
    elements = [k for k in prob]
    weights = [prob[k] for k in prob]
    curr_ch = random.choices(elements, weights=weights, k=1)[0]
print(generate + curr_ch)