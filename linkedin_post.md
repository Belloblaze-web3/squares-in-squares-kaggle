## Building a validation-first optimization pipeline for Kaggle

I built and submitted a complete solver for Kaggle’s **Squares in Squares** competition—a combinatorial geometry problem where the goal is to pack `n` non-overlapping unit squares into the smallest axis-aligned container.

The interesting part was not just optimization. It was engineering the full workflow:

- deterministic rectangular/grid layouts for a safe complete baseline;
- Separating Axis Theorem checks for rotated-square overlap;
- boundary and schema validation before every export;
- spatial hashing so the full 500,500-row submission could be checked efficiently;
- targeted simulated annealing for selected puzzle sizes;
- reproducible generation, tests, CI, Kaggle upload, and GitHub delivery.

The final baseline submission covered all 1,000 puzzles, passed local geometry validation, and was accepted by Kaggle for evaluation. The local baseline score was **28.937669917**.

The main lesson: in optimization projects, a valid and reproducible baseline is not a compromise—it is the platform that makes experimentation safe.

Repository: https://github.com/Belloblaze-web3/squares-in-squares-kaggle

#DataScience #Optimization #Python #CombinatorialOptimization #Kaggle #MachineLearningEngineering
