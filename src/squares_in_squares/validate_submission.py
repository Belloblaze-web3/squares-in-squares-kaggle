from __future__ import annotations
import argparse, csv, math
from collections import defaultdict
from .geometry import Square, validate_layout, enclosing_side, inside

def _validate_group(n, rows, pairwise):
    errors=[]
    if len(rows)!=n: errors.append(f'n={n}: expected {n} rows, got {len(rows)}'); return errors, None
    rows.sort(); sq=[s for _,s in rows]
    if [sid for sid,_ in rows] != list(range(n)): errors.append(f'n={n}: square_id must be 0..{n-1}')
    L=enclosing_side(sq)
    if pairwise:
        # A unit square's AABB is at most sqrt(2) wide. Hashing centers into
        # 2x2 cells reduces the exact SAT checks to nearby candidates.
        buckets=defaultdict(list)
        for i,s in enumerate(sq): buckets[(int(s.x//2), int(s.y//2))].append(i)
        seen=set()
        for (cx,cy), inds in buckets.items():
            nearby=[]
            for dx in (-1,0,1):
                for dy in (-1,0,1): nearby.extend(buckets.get((cx+dx,cy+dy), []))
            for i in inds:
                for j in nearby:
                    if j>=i or (j,i) in seen: continue
                    seen.add((j,i))
                    from .geometry import overlaps
                    if overlaps(sq[i],sq[j]): errors.append(f'squares {j} and {i} overlap')
    if pairwise:
        errors.extend(f"square {i} violates boundary" for i,s in enumerate(sq) if not inside(s,L,1e-7))
    else:
        errors.extend(validate_layout(sq,L,1e-7))
    return errors, L/math.sqrt(n)-1

def validate_file(path: str, max_n: int = 1000, pairwise: bool = True):
    ids=set(); errors=[]; scores={}; current_n=None; current=[]
    with open(path,newline='') as f:
        r=csv.DictReader(f); expected=['id','n','square_id','x','y','angle']
        if r.fieldnames != expected: errors.append(f'header must be {expected}, got {r.fieldnames}')
        for line,row in enumerate(r,2):
            try:
                rid=int(row['id']); n=int(row['n']); sid=int(row['square_id']); x=float(row['x']); y=float(row['y']); a=float(row['angle'])
                if rid in ids: errors.append(f'line {line}: duplicate id')
                ids.add(rid)
                if current_n is None: current_n=n
                if n != current_n:
                    e, score = _validate_group(current_n,current,pairwise); errors.extend(e)
                    if score is not None: scores[current_n]=score
                    current_n=n; current=[]
                current.append((sid,Square(x,y,a)))
            except Exception as e: errors.append(f'line {line}: parse error {e}')
        if current_n is not None:
            e, score = _validate_group(current_n,current,pairwise); errors.extend(e)
            if score is not None: scores[current_n]=score
    for n in range(1,max_n+1):
        if n not in scores: errors.append(f'n={n}: missing puzzle')
    return errors,scores

def main():
    p=argparse.ArgumentParser(); p.add_argument('path'); p.add_argument('--max-n',type=int,default=1000); p.add_argument('--no-pairwise',action='store_true'); a=p.parse_args()
    errors,scores=validate_file(a.path,a.max_n,not a.no_pairwise)
    print(f'puzzles={len(scores)} total_score={sum(scores.values()):.9f} max_score={max(scores.values(),default=0):.9f}')
    if errors:
        print(f'INVALID: {len(errors)} errors'); print('\n'.join(errors[:20])); raise SystemExit(1)
    print('VALID')
if __name__ == '__main__': main()
