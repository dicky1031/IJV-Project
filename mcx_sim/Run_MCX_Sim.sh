# ====================== Modify your setting here ====================== #
num_skin_mus=5
num_fat_mus=5
num_muscle_mus=5
num_blood_mus=5
num_skin_mua=5
num_fat_mua=5
num_muscle_mua=7
num_ijv_mua=9
num_cca_mua=9

root="Julie_low_scatter_v2"
subject="Julie"
date="20231012"
PhotonNum=1000000000
VoxelSize=0.25
ijv_type_set=("ijv_large" "ijv_small")
cvThreshold=2.5
repeatTimes=10
NA_enable=1
NA=0.22
# ====================================================================== #

train_sim_start=1
train_sim_end=$(($num_skin_mus*$num_fat_mus*$num_muscle_mus*$num_blood_mus))
test_sim_start=1
test_sim_end=$(($num_skin_mus*$num_fat_mus*$num_muscle_mus*$num_blood_mus/10)) # using 90% train 10% test

echo "Execute bash File name: $0"
echo "################################### run S1 ################################################"
echo "Total mus combination conditions will be $(($num_skin_mus*$num_fat_mus*$num_muscle_mus*$num_blood_mus))"
echo "Total mua combination conditions will be $(($num_skin_mua*$num_fat_mua*$num_muscle_mua*$num_ijv_mua*$num_cca_mua))"
echo "Total conditions will be $(($num_skin_mus*$num_fat_mus*$num_muscle_mus*$num_blood_mus*$num_skin_mua*$num_fat_mua*$num_muscle_mua*$num_ijv_mua*$num_cca_mua))"

python S1_make_simarr.py --num_skin_mus $num_skin_mus --num_fat_mus $num_fat_mus --num_muscle_mus $num_muscle_mus --num_blood_mus $num_blood_mus --num_skin_mua $num_skin_mua --num_fat_mua $num_fat_mua --num_muscle_mua $num_muscle_mua --num_ijv_mua $num_ijv_mua --num_cca_mua $num_cca_mua
echo "################################### finish S1 ################################################"


echo "################################### run S2 ################################################"
echo "Simulation result will under the folder: $root"
echo "Subject name: $subject"
echo "date of ultrasound data: $date"
echo "photon number used: $PhotonNum"
echo "voxelsize: $VoxelSize"
echo "If considering NA, the fiber NA is: $NA"

python S2_make_simfile.py --root $root --subject $subject --date $date --PhotonNum $PhotonNum --VoxelSize $VoxelSize --NA $NA
echo "################################### finish S2 ################################################"


echo "################################### run S3 mcx sim ################################################"
echo "Simulation result will under the folder: $root"
echo "Subject name: $subject"
echo "ijv_type: ${ijv_type_set[@]}"
echo "Generate training set from folder $train_sim_start to $train_sim_end"
echo "Generate testing set from folder $test_sim_start to $test_sim_end"
echo "Stop simulation while CV is under: $cvThreshold%"
echo "You want to first repeat $repeatTimes times then calculate CV"
echo "Considering NA or not: $NA_enable"
echo "If considering NA, the fiber NA is: $NA"

for ijv_type in "${ijv_type_set[@]}"; do
# python S3_run_sim.py --root $root --subject $subject --ijv_type $ijv_type --start $train_sim_start --end $train_sim_end --cvThreshold $cvThreshold --repeatTimes $repeatTimes --datatype train --NA_enable $NA_enable --NA $NA
python S3_run_sim.py --root $root --subject $subject --ijv_type $ijv_type --start $test_sim_start --end $test_sim_end --cvThreshold $cvThreshold --repeatTimes $repeatTimes --datatype test --NA_enable $NA_enable --NA $NA
done
echo "################################### finish S3 ################################################"

# echo "################################### run S4 WMC ################################################"
# for ijv_type in "${ijv_type_set[@]}"; do
# python S4_wmc_generate_dataset.py --root $root --subject $subject --start $train_sim_start --end $train_sim_end --datatype train --ijv_type $ijv_type
# python S4_wmc_generate_dataset.py --root $root --subject $subject --start $test_sim_start --end $test_sim_end --datatype test --ijv_type $ijv_type

# echo "################################### finish S4 ################################################"