from pathlib import Path
from pypdf import PdfReader
import re, json
paths=[
 r'D:/Desktop/ArcNote/PostGraduate/答题卡/计算机408历年真题/2009-2023计算机408统考真题/2023年计算机408统考真题. .pdf',
 r'D:/Desktop/ArcNote/PostGraduate/答题卡/计算机408历年真题/2009-2023计算机408统考真题/2021年计算机408统考真题. .pdf',
 r'D:/Desktop/ArcNote/PostGraduate/答题卡/计算机408历年真题/2025计算机408真题+解析/2025年计算机408统考真题及答案.pdf',
]
for p in paths:
    print('\n---',p)
    try: r=PdfReader(p)
    except Exception as e: print('ERR',e); continue
    text='\n'.join((pg.extract_text() or '') for pg in r.pages)
    text=re.sub(r'\s+',' ',text)
    for q in [11,12,18,22,23,24,28,32,43,44,45,46]:
        m=re.search(rf'(?<!\d){q}[\.．、]\s*(.*?)(?=(?<!\d){q+1}[\.．、]\s|$)', text)
        if m:
            print(f'Q{q}:',m.group(1)[:220])
        else:
            pos=text.find(str(q))
            print(f'Q{q}: not found pos {pos}')
