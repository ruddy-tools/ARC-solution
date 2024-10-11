from glob import glob
import csv

def read(fn):
    try:
        with open(fn, 'r') as f:
            return f.read()
    except:
        return ''

def read_csv(fn):
    try:
        with open(fn, 'r') as f:
            return list(csv.reader(f))
    except:
        return []

def process_depth(depth):
    inds = range(0, 419)
    compressed = ''
    features = []
    max_depths = []
    score = [0, 0, 0, 0]

    for i in inds:
        filename = f'output/answer_{i}_{depth}.csv'
        data = read_csv(filename)
        if not data or len(data) < 2:
            compressed += '0'
            continue

        # Assuming the highest score indicates the best result
        best_score = max(float(row[-1].split()[-1]) for row in data[1:])
        
        if best_score > 3:
            s = 3  # Correct
        elif best_score > 2:
            s = 2  # Good candidate
        elif best_score > 1:
            s = 1  # Partial solution
        else:
            s = 0  # No solution
        
        score[s] += 1
        compressed += str(s)

        err_filename = f'store/tmp/{i}_err.txt'
        t = read(err_filename)
        if t:
            try:
                feat = [int(x) for x in t.split('Features:')[1].split('\n')[0].split()]
                features.append([feat, i])
            except (IndexError, ValueError):
                print(f"Warning: Couldn't parse features for task {i}")

            try:
                max_depth = int(t.split('MAXDEPTH:')[1].strip())
                max_depths.append([max_depth, i])
            except (IndexError, ValueError):
                print(f"Warning: Couldn't parse MAXDEPTH for task {i}")

    for i in range(3, 0, -1):
        score[i-1] += score[i]

    print(f"Results for Depth {depth}:")
    print(compressed)
    print()
    print(f"Total  : {score[0]:4d}")
    print(f"Size   : {score[1]:4d}")
    print(f"Cands  : {score[2]:4d}")
    print(f"Correct: {score[3]:3d}")

    print("\nTop 5 Feature Complexities:")
    for feat, i in sorted(features, key=lambda x: sum(x[0]), reverse=True)[:5]:
        print(f"Task {i:3d}: {feat}")

    print("\nTop 5 Max Depths:")
    for depth, i in sorted(max_depths, reverse=True)[:5]:
        print(f"Task {i:3d}: {depth}")

    print("\n" + "="*50 + "\n")

    return score, features, max_depths

def main():
    print("Processing Depth 2 Results:")
    score2, memories2, times2 = process_depth(2)
    
    print("Processing Depth 3 Results:")
    score3, memories3, times3 = process_depth(3)

    print("Comparison of Depth 2 and Depth 3 Results:")
    print(f"{'Metric':<10} {'Depth 2':>10} {'Depth 3':>10}")
    print("-" * 32)
    print(f"{'Total':<10} {score2[0]:>10d} {score3[0]:>10d}")
    print(f"{'Size':<10} {score2[1]:>10d} {score3[1]:>10d}")
    print(f"{'Cands':<10} {score2[2]:>10d} {score3[2]:>10d}")
    print(f"{'Correct':<10} {score2[3]:>10d} {score3[3]:>10d}")

    # You can add more comparative analysis here if needed

if __name__ == "__main__":
    main()
