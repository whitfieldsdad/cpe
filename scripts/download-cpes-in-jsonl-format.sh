url="https://github.com/whitfieldsdad/cpe/raw/main/data/cpes.jsonl.gz"
output_file=$1

function stream {
    wget ${url} --quiet -O - | gzcat | jq '.' -c
}

if [ -z "$output_file" ]; then
    stream
else
    stream > $output_file
fi
