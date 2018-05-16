for YEAR in $(seq 1897 2016)
do
	mv Year${YEAR}ParsedBoston* ParsedBoston${YEAR}.txt
done
