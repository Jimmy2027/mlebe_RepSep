import os
import config

training_save_dir = config.dir  #directory where the training data is stored
classifier_dir = os.path.join(config.scratch_dir, 'classifiers/T2')     #directory where the classifiers are stored for later use

if not os.path.exists(classifier_dir):
    os.makedirs(classifier_dir)
    print('creating dir', os.path.expanduser(classifier_dir))
os.system('cp {a}/*.pkl {b}'.format(a= training_save_dir, b = classifier_dir))
os.system('cp {a}/1_Step/experiment_description.json {b}'.format(a = training_save_dir, b = classifier_dir))
os.system('cp {a}/1_Step/*h5 {b}'.format(a = training_save_dir, b = classifier_dir))
os.system('cp {a}/1_Step/*_augmented.npy {b}'.format(a = training_save_dir, b = classifier_dir))