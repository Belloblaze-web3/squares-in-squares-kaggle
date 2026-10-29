from __future__ import annotations
import argparse, math
from .layouts import rectangular_layout
from .geometry import enclosing_side, validate_layout
from .anneal import optimize

def main():
 p=argparse.ArgumentParser(); p.add_argument('--max-n',type=int,default=1000); p.add_argument('--anneal-max-n',type=int,default=0); p.add_argument('--anneal-steps',type=int,default=0); p.add_argument('--seed',type=int,default=0); a=p.parse_args()
 total=0
 for n in range(1,a.max_n+1):
  sq,L=optimize(n,a.anneal_steps,a.seed) if a.anneal_max_n and n<=a.anneal_max_n else rectangular_layout(n)
  assert not validate_layout(sq,L,1e-7)
  score=L/math.sqrt(n)-1; total+=score
  print(f'n={n:4d} L={L:10.6f} score={score:10.6f}')
 print(f'TOTAL {total:.9f}')
if __name__ == '__main__': main()
