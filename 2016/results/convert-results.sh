#! /bin/bash

for f in *.shtml; do mv "$f" "${f%.*}.md"; done
for f in *-app.md
do
  sed -i 's/<table>/\n#### Parallel Performance\n<table id="parallel" class="result sorted">/g' "$f"
done
for f in *.md
do
  sed -i -E 's/<!--.*value="(.*)"-->/---\nlayout: default\n---\n\{\%- include tablesorter.html -\%\}\n\n## \1\n\n/g' "$f"
  sed -i -E 's/<style>//g' "$f"
  sed -i -E 's/\s*table\{.*//g' "$f"
  sed -i -E 's/\s*border-spacing.*//g' "$f"
  sed -i -E 's/\s*td \{.*//g' "$f"
  sed -i 's/<!--.*-->//g' "$f"
  sed -i 's/<p>//g' "$f"
  sed -i 's/<\/p>/\n\n/g' "$f"
  sed -i 's/<b>/\*\*/g' "$f"
  sed -i 's/<B>/\*\*/g' "$f"
  sed -i 's/<\/b>/\*\*/g' "$f"
  sed -i 's/<\/B>/\*\*/g' "$f"
  sed -i 's/<br\/>/  \n/g' "$f"
  sed -i 's/GMT\*\*/GMT\n\n\*\*/g' "$f"
  sed -i 's/<h3>/\n### /g' "$f"
  sed -i 's/<\/h3>//g' "$f"
  sed -i 's/<h4>/\n#### /g' "$f"
  sed -i 's/<\/h4>//g' "$f"
  sed -i 's/Winners: /Winners/g' "$f"
  sed -i 's/<td>Sequential Performances<\/td>/<th class="center">Sequential Performance<\/th>/g' "$f"
  sed -i 's/<td>Parallel Performances<\/td>/<th class="center">Parallel Performance<\/th>/g' "$f"
  sed -i 's/<tr><td>/<tr class="center"><td>/g' "$f"
  sed -i 's/<\/td><\/table>/<\/td><\/tr><\/table>/g' "$f"
  sed -i 's/<thead><th >/<thead><tr>\n<th>/g' "$f"
  sed -i 's/<thead><tr>/<thead><tr class="center">/g' "$f"
  sed -i 's/<h3> Non-Competitive division <\/h3><style>/<h3> Non-Competitive division <\/h3>/g' "$f"
  sed -i 's/<td>Errors<\/td>/<\/table>\n#### Parallel Performance\n<table id="parallel" class="result sorted">\n<thead><tr>\n<th>Solver<\/th><th>Errors<\/th>/g' "$f"
  sed -i 's/<td>Error Score<\/td>/<th>Error Score<\/th>/g' "$f"
  sed -i 's/<td>Correctly Solved Score<\/td>/<th>Correctly Solved Score<\/th>/g' "$f"
  sed -i 's/<td>CPU time Score<\/td>/<th>CPU Time<\/th>/g' "$f"
  sed -i 's/<td>Correct Score<\/td>/<th>Correct Score<\/th>/g' "$f"
  sed -i 's/<td>CPU Score<\/td>/<th>CPU Score<\/th>/g' "$f"
  sed -i 's/<td>WALL Score<\/td>/<th>WALL Score<\/th>/g' "$f"
  sed -i 's/<td>Overall<\/td>//g' "$f"
  sed -i 's/<td>In Sequential<\/td>//g' "$f"
  sed -i 's/ colspan="[1-9]" align=center>/>/g' "$f"
  sed -i 's/ rowspan="2">/>/g' "$f"
  sed -i 's/<table>/\n#### Sequential Performance\n<table id="sequential" class="result sorted">\n<thead>/g' "$f"
  sed -i 's/><tr>/>\n<tr>/g' "$f"
  sed -i 's/><td>/>\n<td>/g' "$f"
  sed -i 's/><\/tr>/>\n<\/tr>/g' "$f"
  sed -i 's/><\/td>/>\n<\/td>/g' "$f"
  sed -i 's/<\/tr></<\/tr>\n</g' "$f"
  sed -i 's/<td>Solver<\/td>/<th>Solver<\/th>/g' "$f"
  sed -i 's/<td>Parallel performance<\/td>//g' "$f"
  sed -i 's/<td>Sequential performance<\/td>//g' "$f"
  sed -i -E 's/\s+</</g' "$f"
  sed -i -E 's/Benchmarks in this division : ([1-9]*)\*\*\s*/Benchmarks in this division: \1\*\*\n<br\/>\n\*\*Time Limit: 1200s\*\*\n/g' "$f"
  sed -i 's/<td>avg\. CPU time<\/td>/<th>avg\. CPU time <\/th>/g' "$f"
  sed -i 's/<td>avg\. WALL time<\/td>/<th>avg\. WALL time <\/th>/g' "$f"
  sed -i 's/<td>Unsolved benchmarks<\/td>/<th>Unsolved<\/th>/g' "$f"
  sed -i 's/Correctly Solved Score/Correct Score/g' "$f"
  sed -i 's/<td>Reduction Score<\/td>/<th>Reduction Score<\/th>/g' "$f"
  sed -i 's/<th>/<th class="center">/g' "$f"
  sed -i -E 's/<td>([0-9])/<td class="right">\1/g' $f
done
for f in *-app.md
do
  sed -i 's/Time Limit: 1200s/Time Limit: 2400s/g' "$f"
done
for f in *-ucore.md
do
  sed -i 's/Time Limit: 1200s/Time Limit: 2400s/g' "$f"
done

