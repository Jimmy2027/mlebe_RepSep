import os

def find_subjects(dir ='~/.scratch/mlebe/bids'):
    subjects = []
    for o in os.listdir(os.path.expanduser(dir)):
        if o.startswith('sub-'):
            subjects.append(o.strip('sub-'))
    return subjects

def find_sessions(path):
    sessions = []
    for o in os.listdir(path):
        for f in os.listdir(os.path.join(path, o)):
            sessions.append(f.strip('ses-'))
    return list(dict.fromkeys(sessions))

def find_tasks(path):
    tasks = []
    for root, dirs, files in os.walk(path):
        if root.endswith('func'):
            for file in files:
                temp = file.split('_')
                temp.pop(-1)
                dict = {}
                for i in temp:
                    dict[i.split('-')[0]] = i.split('-')[1]
                tasks.append(dict['task'])

    return list(dict.fromkeys(tasks))
