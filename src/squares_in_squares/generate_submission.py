from __future__ import annotations
import argparse, csv, os
from .layouts import rectangular_layout
from .geometry import validate_layout
from .anneal import optimize

def generate(output: str, max_n: int = 1000, anneal_max_n: int = 0, anneal_steps: int = 0, seed: int = 0):
    os.makedirs(os.path.dirname(output) or '.', exist_ok=True)
    with open(output, 'w', newline='') as f:
        w = csv.writer(f); w.writerow(['id','n','square_id','x','y','angle'])
        row_id = 0
        for n in range(1, max_n+1):
            if anneal_max_n and n <= anneal_max_n and anneal_steps:
                squares, L = optimize(n, anneal_steps, seed)
            else:
                squares, L = rectangular_layout(n)
            if validate_layout(squares, L, 1e-7):
                raise RuntimeError(f'internal invalid layout for n={n}')
            for sid, s in enumerate(squares):
                w.writerow([row_id, n, sid, f'{s.x:.12f}', f'{s.y:.12f}', f'{s.angle:.12f}'])
                row_id += 1
    return row_id

def main():
    p=argparse.ArgumentParser(); p.add_argument('--output',required=True); p.add_argument('--max-n',type=int,default=1000); p.add_argument('--anneal-max-n',type=int,default=0); p.add_argument('--anneal-steps',type=int,default=0); p.add_argument('--seed',type=int,default=0)
    a=p.parse_args(); print(f'wrote {generate(a.output,a.max_n,a.anneal_max_n,a.anneal_steps,a.seed)} rows')
if __name__ == '__main__': main()
