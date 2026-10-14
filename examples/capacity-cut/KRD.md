# Capacity Cut for Latent

*The KRD this demo run was built from, as received. Converted from `Demo 1 Capacity cut for latent.docx` with nothing added or removed.*

The capacity cut framework penalises any Latent DC that fails to hold performance or leans on high-productivity pilots. It runs on the same process as Valmo and is controlled entirely by the central Control Tower

## Benchmark

Each Latent DC is benchmarked against Valmo at hex level, on the hexes the Latent DC serves. Comparing the same hexes removes the area mix effect that a pin-level comparison carries. Each DC is allowed a delta above the benchmark. The delta is relative, not absolute, so it adjusts for seasonality and does not penalise a DC for a network-wide movement it does not control.The delta tightens as a DC matures, because Latent pilots deliver for the first time and are expected to close the gap on the learning curve.

- Mature DCs (8+ weeks) hold a 2pp delta.

- Stable DCs (5–8 weeks) hold a 5pp delta.

- New DCs (under 5 weeks) run on a soft target and are outside the cut.

If cuts do not prove effective and the gap still carries a high impact on RTO, we will tighten the thresholds further.

## Metrics and thresholds

COD RTO is lagging, so the weekly check runs on leading indicators that flag a breach before RTO reflects it, in line with how Valmo runs. Misroute is now a separate metric, and productivity is added to protect the Latent persona.

| Metric | Measured as | Stable | Mature |
|---|---|---|---|
| D0 attempt% | Delta with Valmo D0 attempt on the same hexes the Latent DC serves | 5pp | 2pp |
| COD FAD% | Delta with Valmo COD FAD on the same hexes the Latent DC serves | 5pp | 2pp |
| Misroute within polygon% | Misroute marked inside the polygon, vs Valmo misroute on the same hexes the Latent DC serves | 15% above Valmo | 15% above Valmo |
| Pilot Load% | Active FEs crossing 280 weekly OFD | 20% of active FEs | 20% of active FEs |

- Misroute carries a 15% allowance because a Latent polygon is small, so the chance of a wrong area prediction is higher than on Valmo.

- Productivity protects the persona. Latent pilots are part-time, earning ₹8,000–11,000 a month, and 280 weekly OFD is derived backwards from that band. A DC leaning on a few high-volume pilots carries churn risk, because competition can outbid us on earnings and the remaining pilots cannot clear the load. No pilot is blocked, since pilots do not control their assignment. The cut acts at DC level, where the staffing decision sits, and DC captains are excluded from the count. Both 280 and 20% are configurable per DC.

## How the cut works

- A breach on any metric triggers a 20% capacity cut. The cut is 20% irrespective of which metric breached, and cuts never stack within a week, because every breach points to the same manpower gap.

- Cuts continue weekly to a floor of 100 orders (MVV).

## Reinstatement

- Capacity is reinstated by 25% only when every metric is green. Reinstatement restores the DC to its pre-cut capacity. A 20% cut takes capacity from x to 0.8x; restoring 25% of 0.8x returns it to x.

- For performance metrics, green means the metric is back within threshold.

- For pilot load%, green means the DC has onboarded a new FE (100+ orders and 4+ active days in the week). Productivity metric also falls if the DC's volume falls, since fewer orders means fewer FEs cross 280 OFD. That is not recovery. Green therefore requires a newly onboarded FE, not a lower reading.

- A single red metric blocks reinstatement.

- If any metric is still red when the cooldown ends, the DC takes another 20% cut.

## Ownership with Control Tower

- Parallel engine on the Valmo sheet. We have built a dedicated Latent model that computes cuts for Latent DCs and appends them to the same capacity-cut sheet as Valmo. Actioning follows the Valmo process end to end.

- Exceptions only through CT. There is no kill switch with the Latent ops team. Any foreseeable exception, such as sale and festive days, and any unforeseen event or late actioning, such as rain, is raised by the Latent ops team to CT. CT holds final authority to implement it.

- Alignment. The model has been merged with the Valmo capacity-cut flow and aligned with CT. We will reconvene with CT on the stricter thresholds and the productivity metric, after which the full framework runs with the central team.

## Visibility

A tab on the captain panel will go live in October, before enforcement. It shows FE-level and DC-level metrics, the threshold for each, any warning, and the reason for any cut, so captains and AMs know the policy before it acts on them. Pilots receive no communication, since they cannot act on it.
