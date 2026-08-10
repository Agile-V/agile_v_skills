# Agile V Growth Metrics

This document records repository-level discovery and engagement metrics for maintainers. Metrics are directional, not evidence of product quality, lifecycle conformance, or individual behavior.

## Baseline

**Recorded:** 2026-08-10
**Traffic window:** Prior 14 days as displayed by GitHub on 2026-08-10

| Metric | Total | Unique |
|---|---:|---:|
| Stars | 50 | N/A |
| Forks | 9 | N/A |
| Watchers (subscribers) | 0 | N/A |
| Repository views | 172 | 55 |
| Repository clones | 396 | 179 |

GitHub's REST API uses `subscribers_count` for people watching repository notifications. Do not use `watchers_count`: despite its name, it is an alias of `stargazers_count` in repository responses.

### Referrers

| Referrer | Views | Unique visitors |
|---|---:|---:|
| GitHub | 55 | 13 |
| Google | 12 | 6 |
| ChatGPT | 5 | 5 |
| agile-v.org | 1 | 1 |

Referrer totals are only the sources GitHub reported and do not sum to all traffic. GitHub traffic and referrer data cover a rolling 14-day window, can expire, and may use privacy-preserving aggregation.

## Weekly Measurement

Record metrics on the same weekday and approximate time. Preserve raw API responses outside the repository when historical detail is needed, because GitHub exposes only the recent traffic window.

| Recorded date | Window | Stars | Forks | Subscribers | Views | Unique views | Clones | Unique clones | Notable referrers | Activity/context | Source |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|---|---|
| 2026-08-10 | Prior 14 days | 50 | 9 | 0 | 172 | 55 | 396 | 179 | GitHub 55/13; Google 12/6; ChatGPT 5/5; agile-v.org 1/1 | Baseline | GitHub repository and traffic metrics |
| YYYY-MM-DD | Prior 14 days |  |  |  |  |  |  |  |  | Releases, tutorials, downtime, or other relevant context | GitHub repository and traffic metrics |

For each weekly entry:

- Record cumulative stars, forks, and subscribers as snapshots.
- Record views and clones as rolling 14-day totals, not weekly increments.
- Record both total and unique traffic values.
- Note relevant releases or outreach, but do not claim causation without controlled evidence.
- Keep zeroes as zeroes; do not omit unfavorable or flat results.

## Ratio Caveats

### View-to-Star

If used, calculate `cumulative stars / 14-day views`. At baseline this is `50 / 172 = 29.1%`.

This is not a conversion rate. The numerator is lifetime cumulative stock while the denominator is recent traffic flow; stars may predate the traffic window, repeat views can come from the same visitor, and a star can be added without a counted repository view. For a closer approximation, measure **new stars during a fixed period / unique views during that same period**, while still labeling it an estimate because GitHub does not expose user-level attribution.

### Clone-to-Star

If used, calculate `cumulative stars / 14-day clones`. At baseline this is `50 / 396 = 12.6%`.

This is also not a conversion rate. Automated systems, repeat cloning, CI, mirrors, and existing users may contribute clones; stars and clones are neither matched nor necessarily from the same period. Unique clones reduce repetition but do not establish unique people or intent. Prefer **new stars during a fixed period / unique clones during that period** only as a clearly qualified directional ratio.

Never infer satisfaction, production use, organizational adoption, or user identity from views, clones, stars, forks, subscribers, or referrers.

## 30-Day Targets

Targets are planning goals for the 30 days following the 2026-08-10 baseline, not forecasts or commitments.

| Measure | Baseline | Target by 2026-09-09 | Interpretation |
|---|---:|---:|---|
| Stars | 50 | 65 | Cumulative; seek relevant discovery, not solicited voting |
| Forks | 9 | 12 | Cumulative; forks do not prove active use |
| Subscribers | 0 | 2 | Cumulative notification watchers |
| 14-day views | 172 | 250 | Rolling-window target observed on or before target date |
| 14-day unique views | 55 | 80 | Rolling-window target; privacy-aggregated |
| 14-day clones | 396 | 450 | Rolling-window target; automation may contribute |
| 14-day unique clones | 179 | 200 | Rolling-window target; not necessarily unique people |
| Qualified external references | Not baselined | 3 | Relevant accepted listings, independent mentions, or substantive community discussions with URLs |
| Documentation feedback items resolved | Not baselined | 3 | Reproducible issues or actionable feedback closed with evidence |

Evaluate targets alongside the quality of discussion, issue reports, documentation improvements, and contributor retention. Missing a target is data, not a reason to weaken attribution or community rules.

## Ethical Growth Rules

- Share only in relevant venues and obey each venue's self-promotion and disclosure rules.
- Disclose maintainer, employee, sponsor, or contributor affiliation.
- Do not buy, trade, automate, or directly solicit stars, forks, votes, reviews, or artificial traffic.
- Do not mass-post identical copy, repeatedly repost, astroturf, or use undisclosed accounts.
- Lead with useful documentation, tutorials, release details, and reproducible evidence rather than urgency or hype.
- State limitations: draft skills are preview, compliance support is not certification, and metrics are not quality proof.
- Do not identify, fingerprint, contact, or profile individual visitors from traffic data.
- Use aggregate metrics and retain no secrets, personal data, access tokens, or raw proprietary referral data in this file.
- Correct inaccurate claims promptly and preserve unfavorable measurements.
- Treat community feedback as input, not as permission to contact people outside the venue.

## GitHub CLI Commands

Run these manually from an authenticated maintainer account with repository traffic access. The traffic endpoints generally require push access. Commands are read-only and create no files.

### Repository Snapshot

```bash
gh api repos/Agile-V/agile_v_skills --jq '{recorded_at: now | todate, stars: .stargazers_count, forks: .forks_count, subscribers: .subscribers_count}'
```

### Views and Clones

```bash
gh api repos/Agile-V/agile_v_skills/traffic/views
gh api repos/Agile-V/agile_v_skills/traffic/clones
```

Use `per=day` when daily points are useful within the available window:

```bash
gh api 'repos/Agile-V/agile_v_skills/traffic/views?per=day'
gh api 'repos/Agile-V/agile_v_skills/traffic/clones?per=day'
```

### Referrers and Popular Content

```bash
gh api repos/Agile-V/agile_v_skills/traffic/popular/referrers
gh api repos/Agile-V/agile_v_skills/traffic/popular/paths
```

### Compact Manual Readout

```bash
gh api repos/Agile-V/agile_v_skills --jq '[.stargazers_count, .forks_count, .subscribers_count] | @tsv'
gh api repos/Agile-V/agile_v_skills/traffic/views --jq '[.count, .uniques] | @tsv'
gh api repos/Agile-V/agile_v_skills/traffic/clones --jq '[.count, .uniques] | @tsv'
gh api repos/Agile-V/agile_v_skills/traffic/popular/referrers --jq '.[] | [.referrer, .count, .uniques] | @tsv'
```

API totals can differ from the GitHub web interface because of collection timing, rolling-window boundaries, caching, or aggregation. Record the retrieval date and use one source consistently when comparing periods.
