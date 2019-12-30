#!/bin/sh

maxscreenshots=5
datadir=$HOME/crocoite-data/finished
echo "searching files"
files=`find $datadir -name '*.warc.gz' -type f`
if [ -n "$files" ]; then
	date=`date -I -u`
	rand=`head -c 16 /dev/urandom | sha512sum -b | head -c 6`
	tempdir=`mktemp -d -p "$HOME" tmpupload.XXXXXXX`
	outfile="$tempdir/chromebot-${date}-${rand}.warc.gz"
	jobsfile="$tempdir/jobs.json.gz"
	screenshotInput=`echo "$files" | shuf | head -n $maxscreenshots`
	echo "creating jobfile" && \
	echo "$files" | ./jobinfo.py | gzip > "$jobsfile" && \
	echo "merging warc" && \
	echo "$files" | crocoite-merge-warc "$outfile" && \
	echo "stitching images" && \
	# stitch images
	echo "$screenshotInput" | while read -r L; do
		crocoite-extract-screenshot -f -1 "$L" "`mktemp -p $tempdir screenshot.XXXXX.png`"
	done && \
	find "$tempdir" -type f -name '*.png' | ./stitch.py "$tempdir/preview.jpg" && \
	echo "uploading" && \
	ia upload "chromebot-${date}-${rand}" "$outfile" "$jobsfile" "$tempdir/preview.jpg" -m mediatype:web -m 'subject:archiveteam;crocoite;chromebot' -m 'collection:archiveteam_chromebot' && \
	echo $files | xargs rm -v
	# always remove temp outfile, even if upload failed
	rm -r -v "$tempdir"
	echo "done"
fi

