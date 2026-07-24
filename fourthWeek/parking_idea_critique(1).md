# Parking Idea Critique — Convergent Tools Applied Per Group

Ideas grouped loosely by theme. Each group gets: a one-sentence summary, then all seven tools applied. Use this to mix, match, and build one solid concept.

---

## Group 1 — Pre-Departure Visibility
**Summary:** Let a driver check real-time or predicted lot fullness from home or on the way, before they've committed to driving to a specific lot — via a public map, WhatsApp bot, predictive text, portal widget, QR code, or a published reliability score.

### Impact-Effort Matrix
| | Low Effort | High Effort |
|---|---|---|
| **High Impact** | Public live map, WhatsApp bot, portal widget | Predictive night-before model |
| **Low Impact** | QR codes at gates (redundant if map exists) | Reliability score (needs historical data pipeline) |

The public map and WhatsApp bot cluster in the top-left quadrant — build these first. The predictive text is the standout "worth the effort" item since it removes the decision entirely rather than just informing it.

### How-Now-Wow Matrix
- **Now:** WhatsApp bot, public live map — both buildable with off-the-shelf sensor data and a simple front end.
- **How:** Portal widget integration (depends on who owns the student portal codebase — access/politics, not tech, is the blocker).
- **Wow:** Predictive night-before texting ("tomorrow 8am, West Campus 90% full by 7:45") — genuinely novel, reframes parking from reactive to anticipatory.

### Decision Matrix / Weighted Scoring Model
Criteria: Reach (30%), Build Speed (25%), Behaviour Change (25%), Maintenance Cost (20%)

| Idea | Reach | Build Speed | Behaviour Change | Maintenance | Weighted Score |
|---|---|---|---|---|---|
| Public live map | 9 | 8 | 6 | 7 | 7.5 |
| WhatsApp bot | 7 | 9 | 6 | 6 | 7.1 |
| Predictive night-before text | 8 | 4 | 9 | 5 | 6.7 |
| Portal widget | 8 | 5 | 6 | 8 | 6.6 |
| Reliability score | 5 | 5 | 5 | 6 | 5.2 |
| QR codes at gates | 4 | 9 | 3 | 9 | 5.9 |

*(Scores out of 10, illustrative — re-score with your own weights.)*

### Weighted Shortest Job First (WSJF)
WSJF = (Business Value + Time Criticality + Risk Reduction) / Job Size

| Idea | Value | Time Crit. | Risk Reduction | Job Size | WSJF |
|---|---|---|---|---|---|
| WhatsApp bot | 7 | 8 | 5 | 2 | 10.0 |
| Public live map | 8 | 8 | 6 | 3 | 7.3 |
| QR codes | 4 | 5 | 3 | 1 | 12.0 |
| Portal widget | 7 | 6 | 5 | 5 | 3.6 |
| Predictive model | 9 | 7 | 7 | 8 | 2.9 |

QR codes score highest purely because job size is tiny — but they're a *feature of* the map, not a standalone win. Don't let WSJF trick you into shipping a QR code before the destination page exists.

### SWOT Analysis
- **Strengths:** Zero infrastructure change at the lot itself; students self-serve; low ongoing cost once built.
- **Weaknesses:** Only as good as the underlying occupancy data (see Group 4) — garbage in, garbage out.
- **Opportunities:** Becomes the single source of truth other groups' ideas (screens, PA, apps) all pull from.
- **Threats:** If data lags reality by more than a few minutes, students stop trusting it and abandon the tool entirely — trust, once lost, is hard to win back.

### Six Thinking Hats
- **White (facts):** Requires a live occupancy feed (from Group 4) to function at all — this group has zero value without that dependency solved first.
- **Red (feelings):** Students want reassurance before they even leave their room — anxiety reduction, not just time saving.
- **Black (caution):** WhatsApp bot response time and uptime matter — a bot that's slow or wrong once loses credibility fast.
- **Yellow (optimism):** This is the cheapest, highest-leverage layer in the whole idea set — one data feed, many front ends.
- **Green (creativity):** Could extend to "predicted best departure time" rather than just current status.
- **Blue (process):** This should be the *first* thing built, since almost every other group's idea assumes this data pipeline exists.

### Decision Tree
```
Do we have (or can we cheaply build) a live occupancy feed?
├── YES → Build public map + WhatsApp bot immediately (low effort, high reach)
│         └── Later: layer predictive texting on top once historical data accumulates
└── NO  → Solve Group 4 (occupancy sensing) FIRST
          └── Then return to this group
```

---

## Group 2 — On-Approach Guidance
**Summary:** Actively guide or inform a driver during the last few minutes of their drive — via a voice-guided app, a short-range radio broadcast, sensor-triggered directional signs on a loop road, or PA announcements near the gate.

### Impact-Effort Matrix
| | Low Effort | High Effort |
|---|---|---|
| **High Impact** | PA announcements | Sensor-triggered loop road signs |
| **Low Impact** | — | Voice-guided app, radio frequency broadcast |

PA announcements are the only genuinely low-effort/high-impact item here. The other three are high-effort for a marginal improvement over what Group 1 and Group 3 already deliver.

### How-Now-Wow Matrix
- **Now:** PA announcements — a speaker and a script, nothing more.
- **How:** Loop road with sensor-triggered signs — needs road redesign or physical sign installation, feasible but a civil-works job.
- **Wow:** Voice-guided companion app — novel, but redundant with Google Maps-style navigation the moment the destination (a specific open lot) is already known from Group 1.

### Decision Matrix / Weighted Scoring Model
Criteria: Reach (25%), Build Speed (30%), Novelty Value (15%), Cost (30%)

| Idea | Reach | Build Speed | Novelty | Cost (inverted) | Weighted Score |
|---|---|---|---|---|---|
| PA announcements | 6 | 9 | 2 | 9 | 6.9 |
| Loop road + sensor signs | 8 | 3 | 6 | 3 | 4.8 |
| Radio frequency broadcast | 5 | 4 | 7 | 4 | 4.8 |
| Voice-guided app | 6 | 3 | 8 | 3 | 4.5 |

### Weighted Shortest Job First (WSJF)
| Idea | Value | Time Crit. | Risk Reduction | Job Size | WSJF |
|---|---|---|---|---|---|
| PA announcements | 5 | 6 | 3 | 1 | 14.0 |
| Loop road signs | 7 | 6 | 5 | 8 | 2.25 |
| Radio broadcast | 5 | 4 | 3 | 7 | 1.7 |
| Voice-guided app | 6 | 4 | 3 | 9 | 1.4 |

PA announcements dominate on job-size alone. The other three carry real infrastructure or engineering cost for benefit that overlaps heavily with cheaper groups.

### SWOT Analysis
- **Strengths:** Reaches drivers at the exact moment of decision (last mile), when Group 1's info might be stale.
- **Weaknesses:** Three of the four ideas require physical infrastructure (roads, radio transmitters, dedicated app) — high sunk cost.
- **Opportunities:** A loop road forces one-way flow, which could also reduce the congestion problem independent of parking info.
- **Threats:** Overlaps with — and risks confusing drivers already looking at — a phone map or dashboard from Group 1/3. Multiple info sources giving slightly different numbers erodes trust in all of them.

### Six Thinking Hats
- **White:** Only PA announcements can be built without new hardware beyond a speaker.
- **Red:** Drivers approaching a gate are often already stressed/late — a calm, simple announcement helps more than a busy app UI would.
- **Black:** A voice app competing for attention while driving is a safety concern, not just a UX one.
- **Yellow:** The loop road idea has a nice side effect — it fixes traffic flow, not just information flow.
- **Green:** Could the loop road signs simply be the same displays from Group 3, just repositioned at junctions instead of lot entrances?
- **Blue:** This group should be sequenced *after* Group 1 and Group 3 — it's reinforcement, not foundation.

### Decision Tree
```
Is there already a loop road / one-way system on campus?
├── YES → Add sensor-triggered signs at existing junctions (moderate effort, high reuse)
└── NO  → Is road redesign in scope for this project?
          ├── YES → Consider it as a longer-term infrastructure bet
          └── NO  → Default to PA announcements only; skip radio/app as redundant
```

---

## Group 3 — At-Lot Signage
**Summary:** Physical, visible displays at or near each lot itself — screens, colour-coded lights, floor LEDs, digital counters, numbered bay markers, or a big board at the main entrance — showing live counts as drivers arrive.

### Impact-Effort Matrix
| | Low Effort | High Effort |
|---|---|---|
| **High Impact** | Colour-coded lights, digital counters above booms | Main-entrance big screen (all lots), per-lot screens |
| **Low Impact** | Numbered bay markers | Floor LEDs per bay |

Colour-coded lights (like a fuel gauge) are the sweet spot: cheap, instantly readable from a distance, no learning curve.

### How-Now-Wow Matrix
- **Now:** Colour-coded entrance lights, digital counters above booms.
- **How:** Main-entrance screen listing every lot — needs a data feed to every lot plus a central display, more integration than novelty.
- **Wow:** Floor LEDs that flash toward an open bay — visually striking but the most expensive per-bay to install and maintain of anything in the whole idea set.

### Decision Matrix / Weighted Scoring Model
Criteria: Visibility Distance (25%), Build Speed (25%), Cost per Lot (25%), Durability (25%)

| Idea | Visibility | Build Speed | Cost per Lot (inverted) | Durability | Weighted Score |
|---|---|---|---|---|---|
| Colour-coded lights | 9 | 8 | 8 | 8 | 8.25 |
| Digital counters (booms) | 7 | 7 | 7 | 7 | 7.0 |
| Main-entrance screen | 8 | 4 | 5 | 8 | 6.25 |
| Numbered bay markers | 4 | 9 | 9 | 9 | 7.75 |
| Per-lot screens (next 2 nearest) | 8 | 5 | 4 | 7 | 6.0 |
| Floor LEDs per bay | 9 | 2 | 2 | 3 | 4.0 |

### Weighted Shortest Job First (WSJF)
| Idea | Value | Time Crit. | Risk Reduction | Job Size | WSJF |
|---|---|---|---|---|---|
| Colour-coded lights | 8 | 7 | 6 | 3 | 7.0 |
| Numbered bay markers | 4 | 3 | 2 | 1 | 9.0 |
| Digital counters | 7 | 6 | 5 | 4 | 4.5 |
| Main-entrance screen | 8 | 6 | 6 | 6 | 3.3 |
| Floor LEDs | 6 | 4 | 3 | 9 | 1.4 |

### SWOT Analysis
- **Strengths:** Works even for drivers who didn't check an app beforehand — a safety net for Group 1's non-adopters.
- **Weaknesses:** Physical hardware means ongoing maintenance (bulbs, sensors, weatherproofing) that software-only solutions avoid.
- **Opportunities:** A single lot-level status feed can drive lights, counters, *and* the app simultaneously — one sensor investment, many outputs.
- **Threats:** Floor LEDs and full per-lot screens risk becoming the expensive, flashy option that doesn't outperform a $50 coloured light for the actual goal (knowing if a lot has *any* space).

### Six Thinking Hats
- **White:** You explicitly noted granularity doesn't need to go to the individual-bay level — this cuts floor LEDs and numbered bay markers down in priority immediately, since they solve a more precise problem than the one stated.
- **Red:** A simple green/amber/red light at a distance feels calm and clear; a screen full of numbers while driving feels like a chore to read.
- **Black:** Any lit signage needs a maintenance budget line, or it degrades into broken lights that erode trust (same risk as Group 1's data-lag problem).
- **Yellow:** Colour-coded lights are the cheapest idea in the *entire* document relative to impact.
- **Green:** Could the main-entrance screen just be a physical mirror of the Group 1 public map, so there's only one data source to maintain?
- **Blue:** Sequence this after the occupancy feed (Group 4) exists, in parallel with Group 1 — same data, different display surface.

### Decision Tree
```
Does the project need bay-level precision, or just lot-level "has space / doesn't"?
├── Lot-level only (as you specified) → Colour-coded lights + digital counters
│                                        Skip floor LEDs and numbered bay markers
└── Bay-level needed → Reconsider scope; floor LEDs/numbered markers become viable
```

---

## Group 4 — Occupancy Sensing (the Data Layer)
**Summary:** How the system actually knows a lot's live count — exit-boom sensors decrementing a counter, license plate recognition, overhead cameras, a "my bay is free" self-report button, or periodic photo capture at peak times.

### Impact-Effort Matrix
| | Low Effort | High Effort |
|---|---|---|
| **High Impact** | Exit-boom sensor counter | License plate recognition |
| **Low Impact** | "My bay is free" button (relies on user compliance) | Overhead cameras, periodic photo capture |

The exit-boom counter is the clear starting point: it's the mechanism you already sketched in your own notes ("An exit-boom sensor that decrements a live counter the instant a car leaves") and needs no new recognition technology, just entry/exit counting.

### How-Now-Wow Matrix
- **Now:** Exit-boom sensor + entry sensor pair — simple in/out counting, proven technology (same as any paid parking garage).
- **How:** License plate recognition — more complex, but unlocks extra features later (see and elsewhere) beyond just counting.
- **Wow:** Overhead cameras with computer-vision occupancy counting — most flexible (could eventually go bay-level if scope changes) but the most technically ambitious.

### Decision Matrix / Weighted Scoring Model
Criteria: Accuracy (30%), Build Speed (25%), Cost (25%), Scalability to New Lots (20%)

| Idea | Accuracy | Build Speed | Cost (inverted) | Scalability | Weighted Score |
|---|---|---|---|---|---|
| Entry/exit boom sensors | 9 | 8 | 8 | 8 | 8.35 |
| License plate recognition | 9 | 5 | 4 | 7 | 6.6 |
| Overhead cameras | 8 | 4 | 3 | 6 | 5.5 |
| "My bay is free" button | 4 | 9 | 9 | 9 | 7.1 |
| Periodic photo capture | 5 | 6 | 6 | 5 | 5.5 |

### Weighted Shortest Job First (WSJF)
| Idea | Value | Time Crit. | Risk Reduction | Job Size | WSJF |
|---|---|---|---|---|---|
| Entry/exit boom sensors | 10 | 10 | 9 | 4 | 7.25 |
| "My bay is free" button | 4 | 5 | 3 | 2 | 6.0 |
| License plate recognition | 8 | 6 | 6 | 8 | 2.5 |
| Overhead cameras | 7 | 5 | 5 | 9 | 1.9 |
| Photo capture | 4 | 3 | 3 | 5 | 2.0 |

Boom sensors score highest on both value and urgency — every other group's idea in this document is a consumer of this data, so it's the true dependency root.

### SWOT Analysis
- **Strengths:** This is the one group where getting it right unblocks *every other group* — the highest-leverage decision in the whole document.
- **Weaknesses:** Self-report buttons are unreliable at scale (students forget, or don't bother) — can't be the *sole* source of truth.
- **Opportunities:** Boom sensors are boring, proven tech — lowest risk of the whole project, which is valuable precisely because everything else depends on it working.
- **Threats:** If this layer is wrong even occasionally, it poisons trust in every downstream display (map, lights, screens) simultaneously — a single point of failure for the entire concept.

### Six Thinking Hats
- **White:** You already scoped this correctly in your own notes — lot-level in/out counting, not bay-level tracking. That constraint makes boom sensors sufficient; cameras/plate recognition would be solving a harder problem than the one stated.
- **Red:** Nobody feels good campaigning for "just install some sensors" — it's invisible plumbing — but it's the part that makes every visible, exciting idea (lights, apps, screens) actually true rather than a guess.
- **Black:** A miscounted boom sensor (e.g., two cars passing close together) compounds every time it's wrong; needs a periodic manual recalibration or reset mechanism.
- **Yellow:** This is genuinely the cheapest, most reliable, most reusable single investment in the entire idea set.
- **Green:** Could combine boom sensors (for the reliable baseline count) with the self-report button (for early departure warnings before the car physically exits) — belt and suspenders.
- **Blue:** Build this first, full stop. It's not really a "creative idea" to compare against the others on inspiration — it's the infrastructure everything else stands on.

### Decision Tree
```
Do existing lots already have boom gates / entry-exit barriers?
├── YES → Add simple in/out sensors to existing booms — fastest path (aligns with your own note)
└── NO  → Would installing boom gates also help with access control / security?
          ├── YES → Bundle the sensor install with a security/access upgrade (shared cost)
          └── NO  → Consider overhead cameras as a no-new-hardware-at-the-gate alternative
```

---

## Group 5 — Booking / Reservation Systems
**Summary:** Guarantee a spot in advance rather than relying on live information alone — a fixed number of guaranteed bays per lot, tiered permits (guaranteed vs. first-come), a daily advance-booking option, or a promised fallback lot if the first two choices are full.

### Impact-Effort Matrix
| | Low Effort | High Effort |
|---|---|---|
| **High Impact** | Guaranteed fallback lot promise | Tiered permits (guaranteed vs. standard) |
| **Low Impact** | — | Guaranteed bay booking system, daily advance booking |

Both "high effort" cells require a new allocation/booking system with rules, enforcement, and likely a fairness or fee policy — genuinely the most operationally complex group in the entire document.

### How-Now-Wow Matrix
- **Now:** Guaranteed fallback lot promise — a policy decision plus signage, no new booking infrastructure required.
- **How:** Tiered permits — requires a permit system (may already partially exist) extended with a "guaranteed" tier.
- **Wow:** Daily advance booking system — most flexible for students, but the most complex to build fairly (what happens with no-shows? cancellations?).

### Decision Matrix / Weighted Scoring Model
Criteria: Fairness (30%), Build Complexity (25%), Student Value (25%), Enforcement Ease (20%)

| Idea | Fairness | Build Complexity (inverted) | Student Value | Enforcement Ease | Weighted Score |
|---|---|---|---|---|---|
| Guaranteed fallback lot | 7 | 8 | 7 | 8 | 7.45 |
| Tiered permits | 5 | 5 | 8 | 6 | 6.0 |
| Daily advance booking | 6 | 3 | 9 | 4 | 5.5 |
| Guaranteed bay booking (fixed spots) | 4 | 4 | 7 | 5 | 5.05 |

### Weighted Shortest Job First (WSJF)
| Idea | Value | Time Crit. | Risk Reduction | Job Size | WSJF |
|---|---|---|---|---|---|
| Guaranteed fallback lot | 7 | 6 | 8 | 3 | 7.0 |
| Tiered permits | 8 | 5 | 5 | 7 | 2.6 |
| Daily advance booking | 8 | 5 | 6 | 9 | 2.1 |
| Guaranteed bay booking | 6 | 4 | 5 | 8 | 1.9 |

### SWOT Analysis
- **Strengths:** Removes uncertainty entirely for the students who most need it (e.g., those with mobility needs or tight schedules) rather than just informing uncertainty.
- **Weaknesses:** Any reservation system raises a fairness question the moment demand exceeds guaranteed supply — who gets the guaranteed tier, and why?
- **Opportunities:** Could be funded by tiered pricing, turning a cost centre into a self-sustaining feature.
- **Threats:** Reservation no-shows waste a bay that a live-information system (Groups 1–3) would have correctly shown as available — the two philosophies (guarantee vs. inform) can work against each other if not designed together.

### Six Thinking Hats
- **White:** This is the only group that fundamentally changes the *allocation* of parking rather than just the *information about* parking — a structurally different intervention from every other group.
- **Red:** Guaranteed access feels like fairness to some and privilege to others — this is the most politically sensitive group in the document.
- **Black:** Reservation no-show rates need a policy (release the bay after N minutes? charge a no-show fee?) or the guaranteed tier quietly becomes a source of empty, wasted bays.
- **Yellow:** Even a small guaranteed tier (say 10% of bays) removes the worst-case anxiety for the people most affected by parking stress, without needing to solve the problem for everyone.
- **Green:** A "guaranteed fallback lot" could literally be the park-and-ride shuttle from Group 6 — same idea, framed as a promise instead of an overflow.
- **Blue:** This group is a policy decision layered on top of the data layer (Group 4) — build the sensing and information system first, then decide if/how much of the supply to pre-allocate.

### Decision Tree
```
Is a fee or fairness policy for guaranteed access acceptable to stakeholders?
├── YES → Start with guaranteed fallback lot (lowest complexity, high reassurance)
│         └── Expand to tiered permits once demand data (from Group 4) shows how much guaranteed
│             capacity is actually needed
└── NO  → Skip reservation systems entirely; rely on Groups 1–3 (information) and Group 6
          (demand-shaping) instead
```

---

## Group 6 — Demand-Shaping (Non-Tech)
**Summary:** Reduce or redistribute demand itself rather than just informing drivers about it — staggered lecture start times, an overflow lot that auto-activates at capacity, a park-and-ride shuttle from off-campus, and carpool matching.

### Impact-Effort Matrix
| | Low Effort | High Effort |
|---|---|---|
| **High Impact** | Auto-activating overflow lot | Staggered lecture times, park-and-ride shuttle |
| **Low Impact** | — | Carpool matching |

This is the one group where the highest-impact idea (staggered lecture times) is also organisationally the hardest — it's not a parking-team decision, it's a timetabling/faculty-wide one.

### How-Now-Wow Matrix
- **Now:** Auto-activating overflow lot with signage — a policy + signage change, minimal new infrastructure if the lot physically exists already.
- **How:** Park-and-ride shuttle — needs a vehicle, driver, and schedule, but it's a known, well-understood solution pattern (universities do this already elsewhere).
- **Wow:** Staggered lecture start times — the single most impactful idea in the *entire document* if achievable, because it reduces peak demand at the source rather than managing it after the fact; also the hardest to action since it's outside a parking project's usual authority.

### Decision Matrix / Weighted Scoring Model
Criteria: Demand Reduction (35%), Organisational Feasibility (30%), Cost (20%), Speed to Implement (15%)

| Idea | Demand Reduction | Org. Feasibility | Cost (inverted) | Speed | Weighted Score |
|---|---|---|---|---|---|
| Staggered lecture times | 9 | 3 | 8 | 3 | 6.2 |
| Auto-activating overflow lot | 6 | 8 | 6 | 8 | 6.9 |
| Park-and-ride shuttle | 7 | 6 | 4 | 5 | 5.85 |
| Carpool matching | 5 | 7 | 8 | 6 | 6.15 |

### Weighted Shortest Job First (WSJF)
| Idea | Value | Time Crit. | Risk Reduction | Job Size | WSJF |
|---|---|---|---|---|---|
| Auto-activating overflow lot | 7 | 7 | 6 | 3 | 6.7 |
| Carpool matching | 5 | 4 | 4 | 4 | 3.25 |
| Park-and-ride shuttle | 8 | 6 | 6 | 7 | 2.9 |
| Staggered lecture times | 10 | 5 | 8 | 10 | 2.3 |

WSJF penalises staggered lecture times heavily for job size (cross-faculty coordination), even though its raw value is highest — a good illustration of why WSJF alone shouldn't be the only tool used to kill a high-value idea.

### SWOT Analysis
- **Strengths:** Only group that addresses the root cause (too many cars wanting the same lot at the same time) rather than the symptom (not knowing where a space is).
- **Weaknesses:** Three of four ideas require cooperation from people outside a "parking project" team — faculty timetablers, a shuttle operator/budget holder, students' own willingness to carpool.
- **Opportunities:** Even a partial win (e.g., 15% of students opting into carpool matching) reduces pressure on every other group's system.
- **Threats:** If sold as *the* answer, staggered lecture times can stall the whole project waiting on a decision that isn't yours to make — the earlier "solid place to stop diverging" conclusion in your own notes was right to treat this as the outlier, not the starting point.

### Six Thinking Hats
- **White:** Your own effort-impact reasoning already flagged park-and-ride as "the one genuine big bet" — worth trusting that instinct rather than re-deriving it from scratch.
- **Red:** Carpool matching only works if students actually trust and like their matched partner — a logistics fix with a real social/comfort dimension.
- **Black:** Staggered lecture times risks becoming a permanent "someday" item that never gets prioritised by the people who control timetabling.
- **Yellow:** An auto-activating overflow lot is a small, self-contained win that doesn't need anyone's permission outside the parking team.
- **Green:** Could the park-and-ride shuttle *be* the guaranteed fallback lot from Group 5 — one physical solution serving two conceptual purposes?
- **Blue:** Treat staggered lecture times as a parallel, longer-horizon conversation to start now but not depend on — build the overflow lot and shuttle as the near-term demand-shaping wins.

### Decision Tree
```
Can the parking project team unilaterally implement this, or does it need external sign-off?
├── Unilateral (overflow lot, carpool matching) → Build now, in parallel with the info system
└── Needs external sign-off (staggered lectures, shuttle budget)
          → Start the conversation now, but plan the whole system to work
            WITHOUT it, so the project doesn't stall waiting for a "yes"
```

---

## Group 7 — Operational / Security Tools
**Summary:** Give operational staff, not just drivers, visibility or new capability — a live feed of parking availability for security, and a ride-share style valet drop-off where someone else parks the car.

### Impact-Effort Matrix
| | Low Effort | High Effort |
|---|---|---|
| **High Impact** | Live feed to security | — |
| **Low Impact** | — | Valet-style drop-off service |

Only two ideas here, and they sit at opposite ends: the security feed is a near-free byproduct of Group 4's data layer, while valet drop-off is a genuinely new service requiring staff.

### How-Now-Wow Matrix
- **Now:** Security live feed — literally just giving an existing team a screen with the same data Group 1/3 already produce.
- **How:** N/A (no middle item in this small group).
- **Wow:** Valet-style drop-off — solves the problem completely for the driver (they never search at all) but is a staffing and liability commitment, not really a "parking information" idea anymore.

### Decision Matrix / Weighted Scoring Model
Criteria: Marginal Cost (35%), Value to Operations (30%), Driver Value (20%), Complexity (15%)

| Idea | Marginal Cost (inverted) | Value to Ops | Driver Value | Complexity (inverted) | Weighted Score |
|---|---|---|---|---|---|
| Live feed to security | 10 | 8 | 3 | 9 | 8.1 |
| Valet-style drop-off | 2 | 5 | 9 | 2 | 4.6 |

### Weighted Shortest Job First (WSJF)
| Idea | Value | Time Crit. | Risk Reduction | Job Size | WSJF |
|---|---|---|---|---|---|
| Live feed to security | 6 | 5 | 7 | 1 | 18.0 |
| Valet-style drop-off | 6 | 3 | 4 | 9 | 1.4 |

The security feed is almost a "free win" once Group 4 exists — it's not really a separate project, just an additional screen for an existing data feed.

### SWOT Analysis
- **Strengths:** Security feed has essentially zero marginal cost once occupancy data exists; helps security direct traffic verbally during peak congestion.
- **Weaknesses:** Valet drop-off introduces liability (who's responsible if a staff-driven car is damaged?) and a staffing cost that scales with usage, unlike every other idea in this document.
- **Opportunities:** Security could become an active fallback channel — e.g., if the app is down, security radios out lot status manually using their live feed.
- **Threats:** Valet drop-off, while high driver-value, is really a different *kind* of project (staffing/operations) rather than an extension of the information system — including it may dilute focus.

### Six Thinking Hats
- **White:** The security feed requires no new idea generation at all — it's a distribution decision once Group 4's data exists.
- **Red:** Drivers under time pressure would love valet drop-off, but it's worth being honest that this is a different scale of commitment than everything else in this document.
- **Black:** Valet drop-off's liability question alone could stall it indefinitely if not addressed early.
- **Yellow:** The security feed is arguably the single best "quick win to prove the system works" — cheap, useful, low-risk, and validates the data pipeline with a real internal user.
- **Green:** Security's live feed could double as the manual override/backup for Group 1's public map if sensors ever fail — human-in-the-loop redundancy.
- **Blue:** Ship the security feed as a first internal user of Group 4's data, before exposing it publicly — a natural staging step and de-risking exercise.

### Decision Tree
```
Does Group 4 (occupancy data) already exist or is it being built?
├── YES → Give security a live feed screen immediately — near-zero extra cost
└── NO  → Defer; the security feed isn't independently useful without the underlying data

Is a paid valet-style service in scope/budget for this project?
├── YES → Treat as its own workstream (staffing, liability, pricing) — separate from the
          information-system project
└── NO  → Drop from consideration; overlaps too little with the core "how do I find a
          space" problem to justify inclusion here
```

---

## Cross-Group Takeaways

- **Group 4 (occupancy sensing) is the true dependency root.** Nearly every other group either displays, predicts, or acts on the data it produces. Prioritise it first regardless of which specific ideas you pick elsewhere.
- **Groups 1 and 3 are two display surfaces for the same underlying feed** — a phone/web view and a physical on-site view. Building them together, off one data source, avoids the "which number do I trust" problem flagged repeatedly in the SWOT/Black Hat sections above.
- **Group 6's staggered lecture times keeps scoring high on value and low on feasibility across every tool** — worth raising as a parallel conversation, but don't let the project wait on it.
- **Group 5 (booking) and Group 6 (park-and-ride/shuttle) can merge** — a "guaranteed fallback lot" is functionally the same promise as a park-and-ride shuttle, just described differently.
- **Group 7's security feed is close to a free win** once Group 4 exists, and doubles as a good first real-world test of the data pipeline before it goes public.
