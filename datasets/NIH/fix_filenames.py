import os

series_path = "raw_dataset/volumes/PANCREAS_0017/1.2.826.0.1.3680043.2.1125.1.63153109893437955319845566142797462/1.2.826.0.1.3680043.2.1125.1.53743992739468671541956667200761612/"
print(len(os.listdir(series_path)))
print(os.listdir(series_path)[:10])


import pydicom

files = [
    os.path.join(series_path, f)
    for f in os.listdir(series_path)
    if f.endswith(".dcm")
]

def get_sort_key(f):
    ds = pydicom.dcmread(f, stop_before_pixels=True)
    return int(ds.InstanceNumber)  # or SliceLocation

files = sorted(files, key=get_sort_key)

vol = [pydicom.dcmread(f).pixel_array for f in files]