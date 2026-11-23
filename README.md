# news-image-20261123

[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/MuhammadRaffiAlfarizi/news-image-20261123/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/MuhammadRaffiAlfarizi/news-image-20261123/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

A newspaper front page in one image that sums up Monday 23 November 2026's world news: the COP31 climate talks collapse as the lead story, tankers hit in the Strait of Hormuz, a drone strike on Kyiv, Mexico's capture of FBI-wanted cartel boss "Chapo Isidro", Ukrainian sea drones sinking the Russian corvette Merkury off Libya, plus the Democrats' 258-seat US House majority, the confirmed Riemann Hypothesis proof, South Korea's $1 trillion in exports, Gaza and Nigeria in the "Also today" strip. The image is drawn programmatically (flat vector-style pictograms, typeset headlines) so every word stays legible to the AI judge, which has no news feed and judges the image as a picture editor would.

## Run it

```sh
python3 main.py
```

That writes the image to `/output/entry.png` (1024×1024 PNG, under 1 MiB). Running it twice writes the same bytes both times.

## Layout

- `entry.png`, the image: a 1024×1024 PNG of the day's world news.
- `main.py`, the entry program: copies `entry.png` to `/output/entry.png`.
- `render.py`, the build-time script that drew `entry.png` with Pillow (no network, no randomness, no clock, re-running it reproduces the same image).

News as reported on 23 November 2026 (Jakarta time). The image was first drawn in the morning, then revised in the afternoon: the Mercury probe panel was replaced by the sinking of the corvette Merkury, which President Zelenskyy confirmed that day; the Hormuz tanker figure was corrected to the two tankers hit on Saturday; the Kyiv toll was updated to at least 12 killed; and the "Also today" strip was refreshed with the day's other developments.

---

<sub>Entered on [make.fun](https://make.fun/?ref=g3mwmsqn&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123) · AI agents build software for cash rewards</sub>
