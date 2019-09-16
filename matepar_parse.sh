#!/bin/bash

usage() { printf "\n Parse text with MateParser. Create input for discoure segmenter. \n Usage: $0 [-i <input dir>] [-o <out dir>][-d <executable dir>]  \n -d path to folder containing mateparse executables \n -i directory containing .txt input files \n -o directory where to store output \n \n" 1>&2; exit 1; }

while getopts ":d:i:o:h" v; do
    case "${v}" in
        d)
            d=${OPTARG}
            ;;
        i)
            i=${OPTARG}
            ;;
        h)
			h=${OPTARG}
			;;
		o)
			o=${OPTARG}
			;;
		
        *)
            usage
            ;;
    esac
done
shift $((OPTIND-1))

if [ -z "${d}" ] || [ -z "${i}" ]; then
    usage
fi

echo ""
echo "Creating output dir if not existing..."
echo ""
mkdir -p ${o}

echo "Activate DiscourseSegmenter virtualenv"
echo ""
source ./venv2_dseg/bin/activate

echo "Start processing files..." 
echo ""

for filename in ${i}*.txt; do

	python ${d}/cmd/text_to_mate_input.py "${filename}" ${o}/${filename##*/}.tmp

	java -Xmx2g -cp ${d}/src/anna-3.61.jar is2.util.Split ${o}/${filename##*/}.tmp > ${o}/${filename##*/}.tmp1

	rm ${o}/${filename##*/}.tmp

	java -Xmx2g -cp ${d}/src/anna-3.61.jar is2.lemmatizer.Lemmatizer -model ${d}/models/lemma-ger-3.6.model -test ${o}/${filename##*/}.tmp1 -out ${o}/${filename##*/}.tmp2
	
	rm ${o}/${filename##*/}.tmp1

	java -Xmx3g -classpath ${d}/src/transition-1.30.jar is2.transitionS2a.Parser -model ${d}/models/pet-ger-S2a-40-0.25-0.1-2-2-ht4-hm4-kk0 -test ${o}/${filename##*/}.tmp2 -out ${o}/${filename##*/}.parsed.conll

	rm ${o}/${filename##*/}.tmp2

	discourse_segmenter mateseg segment ${o}/${filename##*/}.parsed.conll > ${o}/${filename##*/}.segmented

done

echo ""
echo "Completed"
deactivate
