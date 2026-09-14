# Color Palette Analysis

Analysis of popular Color Hunt palettes and
fuzzy similarity matching with image color palettes.

## Method

1. Collect 100 popular Color Hunt palettes
2. Extract dominant colors using K-means
3. Calculate RGB Euclidean distance
4. Convert distance to fuzzy similarity
5. Test 24 possible color correspondences
6. Rank palettes by similarity

## Results

Input palette:

#A28465
#271E19
#F9ECE0
#C0BA88

Best matching Color Hunt palette:

#faf3e0
#eabf9f
#b68973
#1e212d

Similarity: 96.56%

## Project structure

data/      - Color Hunt dataset
images/    - Input images
results/   - Analysis results
src/       - Python source code