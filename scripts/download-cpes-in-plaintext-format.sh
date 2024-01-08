url="https://github.com/whitfieldsdad/cpe/raw/main/data/cpes.txt.gz"
output_file=$1

function stream {
    wget ${url} --quiet -O - | gzcat
}

if [ -z "$output_file" ]; then
    stream
else
    stream > $output_file
fi
