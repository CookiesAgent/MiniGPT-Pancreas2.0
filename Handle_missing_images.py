import os
import re
import shutil
from collections import defaultdict

SLICES_DIR = "datasets/TC/slices_same_size"

pattern = re.compile(r"(PANCREAS_\d+)_slice_(\d+)\.png")

# -----------------------------
# 1. Collect files per volume
# -----------------------------
volumes = defaultdict(dict)

for fname in os.listdir(SLICES_DIR):
    match = pattern.match(fname)
    if not match:
        continue

    vol = match.group(1)
    idx = int(match.group(2))
    volumes[vol][idx] = fname

# -----------------------------
# 2. Fill missing slices
# -----------------------------
for vol, slices in volumes.items():
    indices = sorted(slices.keys())

    if not indices:
        continue

    min_idx, max_idx = indices[0], indices[-1]

    for i in range(min_idx, max_idx + 1):
        if i in slices:
            continue

        # find previous available slice
        prev = i - 1
        while prev not in slices and prev >= min_idx:
            prev -= 1

        if prev < min_idx:
            print(f"[WARN] No previous slice for {vol} at {i}, skipping")
            continue

        src_file = os.path.join(SLICES_DIR, slices[prev])
        dst_file = os.path.join(
            SLICES_DIR,
            f"{vol}_slice_{i}.png"
        )

        shutil.copy(src_file, dst_file)

        print(f"[FILLED] {dst_file} from {slices[prev]}")

print("Done filling missing slices.")