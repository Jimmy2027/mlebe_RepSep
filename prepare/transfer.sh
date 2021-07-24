while getopts s:d: option
do
case "${option}"
in
s) scratch_dir=${OPTARG};;
d) destination_dir=${OPTARG};;
esac
done

python make_dataselection.py || exit 1

echo "moving data from ${scratch_dir} to ${destination_dir}"
mkdir -p ${destination_dir}/manual_overview/generic
cp -v ${scratch_dir}/manual_overview/generic/coherence_4001_cbv.pdf ${destination_dir}/manual_overview/generic/
cp -v ${scratch_dir}/manual_overview/generic/4001_ofMcF2_T2w.pdf ${destination_dir}/manual_overview/generic/
cp -v ${scratch_dir}/manual_overview/generic/4001_ofMcF2_cbv.pdf ${destination_dir}/manual_overview/generic/
#cp ${scratch_dir}/manual_overview_new/generic/VZ01_baseline_bold.pdf ${destination_dir}/manual_overview_new/generic/ || exit 1
#cp ${scratch_dir}/manual_overview_new/generic/VZ01_baseline_T1w.pdf ${destination_dir}/manual_overview_new/generic/ || exit 1

mkdir -p ${destination_dir}/manual_overview/masked
cp -v ${scratch_dir}/manual_overview/masked/coherence_4001_cbv.pdf ${destination_dir}/manual_overview/masked/
cp -v ${scratch_dir}/manual_overview/masked/4001_ofMcF2_T2w.pdf ${destination_dir}/manual_overview/masked/
cp -v ${scratch_dir}/manual_overview/masked/4001_ofMcF2_cbv.pdf ${destination_dir}/manual_overview/masked/
#cp ${scratch_dir}/manual_overview_new/masked/VZ01_baseline_bold.pdf ${destination_dir}/manual_overview_new/masked/ || exit 1
#cp ${scratch_dir}/manual_overview_new/masked/VZ01_baseline_T1w.pdf ${destination_dir}/manual_overview_new/masked/ || exit 1

rsync -avP --exclude='*_cope.nii*' --exclude='*_zstat.nii*' ${scratch_dir}/*l2* ${destination_dir}/

cp ${scratch_dir}/config.json ${destination_dir}/
cp -r ${scratch_dir}/data/* ${destination_dir}/
# temp
#mkdir -p ${destination_dir}/classifier
#cp -v ${scratch_dir}/classifiers/T2/y_test.npy ${destination_dir}/classifier/
#cp -v ${scratch_dir}/classifiers/T2/y_pred.npy ${destination_dir}/classifier/
#cp -v ${scratch_dir}/classifiers/T2/x_test.npy ${destination_dir}/classifier/
