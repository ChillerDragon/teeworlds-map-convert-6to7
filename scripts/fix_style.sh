#!/bin/bash

err() {
	echo "[-] $1"
}

arg_dry=0

if [ "$1" == "--dry-run" ]
then
	arg_dry=1
fi

for mapping in ./mappings/*.json
do
	if ! expected="$(jq . "$mapping")"
	then
		err "Error: invalid json '$mapping'"
		exit 1
	fi
	if [ "$expected" != "$(cat "$mapping")" ]
	then
		if [ "$arg_dry" == "1" ]
		then
			err "Error: wrong json style '$mapping'"
			err "       please run $(tput bold)./scripts/fix_style.sh$(tput sgr0) to fix it"
			exit 1
		else
			echo "$expected" > "$mapping"
		fi
	fi
done

