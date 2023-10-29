import os

subject = "Julie"

#%% make directory for training folder and testing folder of subject
os.makedirs(os.path.join("dataset", subject, 'train'), exist_ok=True)
os.makedirs(os.path.join("dataset", subject, 'test'), exist_ok=True)

