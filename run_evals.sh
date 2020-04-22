
for num_hours in 2 4 8 10 15 20 25 30 50 100
do
	echo $num_hours...
	cat keywords.txt | python evaluation.py $num_hours > keywords_results_$num_hours.tsv
	echo $num_hours done
done
echo DONE
