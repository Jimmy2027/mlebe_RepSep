import numpy as np
from matplotlib import pyplot as plt
import pickle
seed = 2

path = '/home/hendrik/.scratch/mlebe/classifier'
xfile = open(path + '/x_test_struct.pkl', 'rb')
x_test_struct = pickle.load(xfile)
xfile.close()

yfile = open(path + '/y_test_struct.pkl', 'rb')
y_test_struct = pickle.load(yfile)
yfile.close()

x_test, x_test_affines, x_test_headers, file_names = x_test_struct['x_test'], x_test_struct['x_test_affines'], x_test_struct['x_test_headers'], x_test_struct['file_names']
y_test, y_test_affines, y_test_headers = y_test_struct['y_test'], y_test_struct['y_test_affines'], y_test_struct['y_test_headers']
y_pred = np.load(path + '/y_test_pred.npy', allow_pickle= True)

x_test = np.asarray(x_test)
x_test = np.concatenate(x_test)
np.random.seed(seed)
np.random.shuffle(x_test)
y_test = np.asarray(y_test)
y_test = np.concatenate(y_test)
np.random.seed(seed)
np.random.shuffle(y_test)
y_pred = np.concatenate(y_pred)
np.random.seed(seed)
np.random.shuffle(y_pred)

# x_test = [x_test[3]]
# y_test = [y_test[3]]
# y_pred = [y_pred[3]]
# x_test = [i[1::12] for i in x_test]
# y_test = [i[1::12] for i in y_test]
# y_pred = [i[1::12] for i in y_pred]

# thresholds = [0, 0.9]
# outputs = []
#
# for thr in thresholds:
#     if thr == 0:
#         for img in y_pred:
#             temp = np.squeeze(img)
#             outputs.append([temp])
#     else:
#         for img in y_pred:
#             temp = np.where(np.squeeze(img) > thr, 1, 0)
#             outputs.append([temp])
nbr_images = 13
list = [[x_test[:nbr_images]], [y_test[:nbr_images]], [y_pred[:nbr_images]]]
# for o in outputs:
#     list.append([o[:12]])


for img in range(len(list[0])):
    patches = []
    for l in range(len(list)):
        patch = list[l][img][0, :, :] * 255
        for slice in range(1, list[l][img].shape[0]):
            temp = list[l][img][slice,:,:] * 255
            patch = np.hstack((patch, temp))
        patches.append(patch)
    patch = patches[0]
    for i in range(1, len(patches)):
        patch = np.vstack((patch, patches[i]))
    image = np.vstack(patches)
    plt.figure()
    plt.imshow(image, cmap='gray')
    plt.axis('off')


