python experiment.py True True time > ../output/random-quorum-time.out
python experiment.py False True time > ../output/equal-quorum-time.out

python experiment.py True False time > ../output/random-complete-time.out
python experiment.py False False time > ../output/equal-complete-time.out

python experiment.py True False split > ../output/random-complete-split.out
python experiment.py False False split > ../output/equal-complete-split.out

