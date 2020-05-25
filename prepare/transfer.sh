mkdir -p ../data/manual_overview/generic
cp -v ~/.scratch/mlebe/manual_overview/generic/coherence_4001_cbv.pdf ../data/manual_overview/generic/ || exit 1
cp -v ~/.scratch/mlebe/manual_overview/generic/4001_ofMcF2_T2w.pdf ../data/manual_overview/generic/ || exit 1
cp -v ~/.scratch/mlebe/manual_overview/generic/4001_ofMcF2_cbv.pdf ../data/manual_overview/generic/ || exit 1
cp ~/.scratch/mlebe/manual_overview/generic/VZ01_baseline_bold.pdf ../data/manual_overview/generic/ || exit 1
cp ~/.scratch/mlebe/manual_overview/generic/VZ01_baseline_T1w.pdf ../data/manual_overview/generic/ || exit 1

mkdir -p ../data/manual_overview/masked
cp -v ~/.scratch/mlebe/manual_overview/masked/coherence_4001_cbv.pdf ../data/manual_overview/masked/ || exit 1
cp -v ~/.scratch/mlebe/manual_overview/masked/4001_ofMcF2_T2w.pdf ../data/manual_overview/masked/ || exit 1
cp -v ~/.scratch/mlebe/manual_overview/masked/4001_ofMcF2_cbv.pdf ../data/manual_overview/masked/ || exit 1
cp ~/.scratch/mlebe/manual_overview/masked/VZ01_baseline_bold.pdf ../data/manual_overview/masked/ || exit 1
cp ~/.scratch/mlebe/manual_overview/masked/VZ01_baseline_T1w.pdf ../data/manual_overview/masked/ || exit 1

cp -v ~/.scratch/mlebe/classifiers/T2/y_test_pred.npy ../data/classifier/ || exit 1
cp -v ~/.scratch/mlebe/classifiers/T2/dice_score.txt ../data/classifier/dice_score.txt || exit 1
cp -v ~/.scratch/mlebe/preprocessing/masked_work/graph.dot ../data/masked_nipype.dot || exit 1
cp -v ~/.scratch/mlebe/preprocessing/generic_work/graph.dot ../data/generic_nipype.dot || True
rsync -avP --exclude='*_cope.nii*' --exclude='*_zstat.nii*' ~/.scratch/mlebe/*l2* ../data/ || exit 1
rsync -avP ~/.scratch/mlebe/data/ ../data || exit 1