python simulate.py True True time > ../output/random-quorum-time.out
python simulate.py False True time > ../output/equal-quorum-time.out

python simulate.py True False time > ../output/random-complete-time.out
python simulate.py False False time > ../output/equal-complete-time.out

python simulate.py True False split > ../output/random-complete-split.out
python simulate.py False False split > ../output/equal-complete-split.out

