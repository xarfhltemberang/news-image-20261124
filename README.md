# The World in One Day — Tuesday 24 November 2026

[![make.fun](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/xarfhltemberang/news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/xarfhltemberang/news-image-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124)

A newspaper-front-page infographic summing up the world's news of
Tuesday 24 November 2026, drawn with PIL (Python).

## The day's news

1. **Nvidia brings back Jensen Huang as CEO** — Nvidia reinstated its
   chief after an inquiry into alleged affairs. Shares jumped 31% in a
   day; Trump said: "I made the deal". (BBC)
2. **CrowdStrike buys Zscaler for $43.9bn** — an all-stock deal
   announced Monday creates a cybersecurity giant for the AI era.
   (WSJ / TechCrunch)
3. **Gaza a "toxic wasteland"** — Oxfam and CEOBS found toxic
   contamination across over 99% of Gaza. Air, soil and water may
   stay dangerous for decades. (Oxfam)
4. **Russian strikes kill 14 across Ukraine** — Monday's strikes hit
   homes in Dymer and more. Zelenskyy warned of new attacks as talks
   open in Abu Dhabi. (Reuters / SANA)
5. **DOJ admits it wrongly deported a US citizen** — the Justice Dept
   conceded in court it deported Brian José Morales García to Mexico,
   wrongly calling him undocumented. (Guardian)
6. **O'Hare ground stop snarls Thanksgiving** — the FAA halted
   arrivals at Chicago O'Hare for over an hour Monday over staffing.
   More than 170 flights were delayed as the holiday rush begins.
   (NBC Chicago / FAA)

## Run it

```sh
MAKEFUN_OUTPUT_DIR=out python3 main.py
```

`main.py` copies the pre-rendered `entry.png` to
`$MAKEFUN_OUTPUT_DIR/entry.png` (or `/output/entry.png` by default).
It uses only the Python standard library, needs no network, and is
deterministic — every run writes identical bytes.

The image itself was drawn by `draw.py` (Pillow, DejaVu fonts), kept
in this repository as the record of how `entry.png` was made:

```sh
MAKEFUN_OUTPUT_DIR=. python3 draw.py
```
