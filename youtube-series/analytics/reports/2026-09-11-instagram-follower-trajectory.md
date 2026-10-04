# Instagram follower trajectory: September 11, 2026

Refreshed through the Instagram API at 3:24 PM ET. Current count: 285.
The full default dashboard pull also completed earlier today. No native phone
access is needed to measure account follower totals or this trajectory.

## Observed growth

- September 2 morning: 42 followers.
- September 4: 154.
- September 8: 233.
- September 10: 243.
- September 11, 3:24 PM ET: 285.

Since the September 4 snapshot, the account added 131 net followers, or 85.1%,
over 7.176 days. That averages 18.255 net followers per day. Growth comes in
bursts, with a slower stretch September 8-10 followed by renewed growth.
The snapshot history supports meaningful growth, not steady exponential growth.
These are net changes in account totals, not gross follows or post attribution.

## Conditional projections

Starting at 285 followers, assume a constant number of net additions each day:

| Scenario | Net followers/day | In 30 days | Approximate date reaching 1,000 |
| --- | ---: | ---: | --- |
| Slower illustrative pace | 10 | 585 | November 22 |
| Observed recent-week pace | 18.255 | 833 | October 20 |
| Faster illustrative pace | 30 | 1,185 | October 5 |

The central scenario extrapolates the observed September 4-11 rate; the other
two are sensitivity scenarios, not fitted estimates or confidence bounds.
Future posts, distribution and unfollows can move actual results outside all
three. Sustaining the recent-week pace would mean about six weeks to 1,000;
this is a planning scenario, not a promised arrival date. Do not extrapolate
the latest two-hour burst as a durable daily rate.

## Evidence and reproducibility

- Raw account data: `../private/instagram/latest.json` and timestamped snapshots.
- Dashboard history: `load_audience_history()['Instagram']`.
- Plot generator: `../private/instagram/follower-projection.py`.
- Figure: `../private/instagram/follower-growth-projection-2026-09-11.png`.
- The chart uses exact snapshot timestamps. Connecting lines do not imply
  continuous observation; no missing-day counts were manufactured.
