# Approaches — Capacity Cut for Latent

**Step 2 of 4.** **Five** approaches. Two changes since the last draft, both worth
stating rather than quietly applying:

- **A scorecard for a captain and an AM to read together was removed.** C8
  settled that nothing is built for AMs, so it had no second reader and no
  reason to exist.
- **Growth Dashboard was missing and is back as E.** It was an approach in the
  first draft; when this set was rebuilt around the axes it disappeared, and
  nothing said so. That is a silent shrink, which is precisely the failure the
  method warns about. Caught on review, not by me. Each is placed on the design axes, says which
success tests it passes, and names the constraints it leans on.

## The axes

Placement is how you get into a page; these are the choices *inside* it.
A set clustered on one point is thin, and the table is what shows that.

| | what is shown | who acts | when surfaced | how framed | depth |
|---|---|---|---|---|---|
| **A** Capacity Cut tab | everything | captain | always | status | DC + FE |
| **B** Alert at the moment of commitment | only the breach | captain | at the decision | warning | summary |
| **C** Pilot-first, on the roster | only the action | captain | always | instruction | FE level |
| **D** Pushed weekly notice | only the breach | system acts, then informs | on the event | warning | summary |
| **E** A reason on Growth Dashboard | only the breach | captain | always, but weekly | **explanation** | summary |

**They are genuinely different by the discriminator** — switching between any
two changes what the captain actually does: *review and plan* (A), *react
while committing a number* (B), *onboard an FE* (C), *wait to be told* (D), and *understand why last week went
the way it did* (E).

> **Placement is an axis too — it is just not the only one.** The previous
> draft over-corrected: having said placement is not the design axis, it
> dropped placement variation altogether, and a whole module went with it.
> A and B sit in DC Capacity, C in Pilot Management, D in the notification
> layer, E in Growth Dashboard. **Vary placement *and* the rest.**

> **The framing span was also short.** It read *status · warning · instruction
> · score*. E is none of those — it is an **explanation**, which is a fifth
> framing and the one Growth Dashboard exists to provide.

## Against the success test

| | T1 which metric | T2 what brings it back | T3 am I close | T4 not a dispute |
|---|---|---|---|---|
| **A** | ✅ | ✅ | ✅ | ✅ |
| **B** | ✅ | ⚠️ partial | ✅ | ✅ |
| **C** | ❌ one metric of four | ⚠️ only the Pilot Load half | ❌ | ✅ |
| **D** | ✅ | ⚠️ partial | ❌ arrives only on breach | ✅ |
| **E** | ✅ | ❌ no room to say a new FE must be hired | ⚠️ only once it has happened | ✅ |

## The approaches

### A · A "Capacity Cut" tab in DC Capacity

**What the captain does**

1. A weekly notice arrives, or they open DC Capacity themselves.
2. They tap the Capacity Cut tab.
3. They read the cut — 20% — and which metric caused it.
4. They scroll to the list of field executives.
5. They see a new FE has to be hired. A lower number will not do.

Two sections: this week's four metrics against their thresholds, and the
field executives over 280 weekly OFD.

**Wins when** the cut is understood as a capacity event, and the captain is
the one who acts. **Costs** a second screen. **Rules out** nothing.
**Leans on** C1, C3, C4, C6.

**Why it can work.** The cut is a capacity event, and this puts it where
capacity already lives — the captain does not have to learn a new place. A tab
costs nothing structurally: two modules already use them, and the module's own
page stays exactly as it is. Most of all it is the only shape with room for a
second section, which is what the hiring rule needs: a number cannot carry it,
a list of people can.

**What would make it fail.** DC Capacity is not a page captains open daily. On
its own it waits to be found — which is why it needs a door, not why it is the
wrong home.

### B · An alert where the capacity number is committed

**What the captain does**

1. They open DC Capacity to set next week's number.
2. They type a capacity figure.
3. An alert tells them a cut is already active.
4. They stop there. Nothing on the page says how to undo it.

No new screen. An inline alert on *Set Your DC Capacity*, at the moment the
captain types a number.

**Wins when** the goal is to stop a bad commitment rather than to explain a
policy. **Costs** everything that does not fit in an alert — the FE table
cannot go here, so T2 is only half answered. **Leans on** C1, C5.

**Why it can work.** It is the only shape that reaches the captain at the
moment of the decision, rather than after it. Nothing is navigated to and
nothing is learned: the alert finds them while they are already typing a
number, which is the one moment the cut has direct consequences.

**What would make it fail.** An alert is a sentence. The hiring rule needs a
list, and there is nowhere under a form field to put one. It also has nothing
to say to a captain who has not been cut, which is most captains most weeks.

### C · Pilot-first, on the roster

**What the captain does**

1. They open Pilot Management.
2. A banner says Pilot Load has breached.
3. They read the two new columns, one field executive at a time.
4. They see exactly who is over 280.

Two columns on Pilot Management — weekly OFD and over/under 280 — and a
banner when Pilot Load is breached.

**Wins when** the belief is that staffing is the only real lever, so put the
metric next to it. **Costs** the other three metrics, which have nowhere to
go. **Rules out** T1 and T3. **Leans on** C4 — and it is the only approach
that makes the hiring rule concrete, because the roster is where a new FE
actually appears.

**Why it can work.** Pilot Load is a problem about people, and this is
the only shape that shows people. A captain reading *9 of 34 over 280* knows
something a percentage cannot tell them — and the roster is the one screen
where hiring a new FE visibly changes the picture, because that is where a new
FE appears.

**What would make it fail.** It explains one metric out of four. A captain cut
for D0 attempt would find nothing here, and would have no reason to look.

### D · A pushed weekly notice

**What the captain does**

1. The notice arrives at the start of the week.
2. They read which metric broke.
3. They tap through to the Capacity Cut tab.

The panel's notification module carries the breach; the detail lives wherever
it already lives.

**Wins when** the problem is that nobody looks in time. It is the only
approach that does not require the captain to come. **Costs** everything
before the breach — it cannot answer T3, because it only exists once the cut
has happened. **Leans on** C1, C5.

**Why it can work.** It is the only shape that does not wait to be
found. Captains live in WhatsApp and check the panel when something sends them
there, so a weekly notice matches how the news actually travels today — and the
panel is where it should land.

**What would make it fail.** Every module already nudges, and nothing says
which matters. Without a reason to outrank the others and a date to stop, this
becomes one more thing to dismiss.

### E · A reason on Growth Dashboard

**What the captain does**

1. They open Growth Dashboard, which they do anyway.
2. They see orders are down.
3. A card says a capacity cut is the reason.
4. They tap through to the Capacity Cut tab.

The cut appears as one more entry in *Your Order Summary*'s reasons, beside
the capacity card already there.

**Wins when** the captain's real question is *why did last week go the way it
did* — and that is the question they already arrive at Growth Dashboard
holding. It is the module most likely to be open, it is weekly like the cut,
and it already names capacity as a reason orders moved.

**Costs** everything after the explanation. Growth Dashboard diagnoses and
points elsewhere, so it can say a cut happened but never what to do about it —
and it cannot say that a lower reading is not enough, which is the subtlest
thing in the KRD (C4).

**Rules out** T2. **Would be a third section** on a module that already has
two, which `section-rules.md` says no screen does. **Leans on** C1, C6.

**Why it can work.** Growth Dashboard is the page captains already open,
and the question it answers — *why did orders drop?* — is the exact question a
cut creates. The cut is one reason among the reasons already shown there, so it
needs no new habit and no new place.

**What would make it fail.** It can name the cause and nothing else. If the
link does not land the captain inside the detail, it tells them they have a
problem and leaves them there.

## Open question — where should this live?

**Recommended: A, with two doors.** The deciding reason is unchanged: the cut
acts on the capacity number, so it belongs where the capacity number lives.
Growth Dashboard gets a door, and `dc-capacity` carries a notice when a cut
is live.

**A is still the only approach that passes all four tests**, and the deciding
reason is unchanged: the cut acts on the capacity number, so it belongs where
that number lives.

But E changes the shape of the recommendation rather than the answer.
**E is the best discovery surface we have and the worst home** — most likely
to be open, weekly like the cut, already answering the adjacent question, and
structurally unable to say what to do about any of it. That is the definition
of a door rather than a home, and now it is written down as a rejected
approach with its reason, instead of being a decision I made quietly while
redrawing a table.

So: **A, with two doors** — the capacity card on Growth Dashboard links to the
tab (E as a door), and `dc-capacity` carries a notice when a cut is live.
D also becomes a door rather than an approach.

## Decided

| | |
|---|---|
| **was open** | where should this live? |
| **answered** | **A + E** — the recommendation, taken |
| **what it changed** | A is the **home**: a *Capacity Cut* tab in DC Capacity, carrying all four metrics, the FE list and the reinstatement path. **E is a door, not a second home**: Growth Dashboard's existing capacity card links to the tab. **D becomes a door too** — the notification points at the tab rather than replacing it. **B and C are out.** |

**What "A + E" does not mean.** E is not built as a page. One home, many
doors — the thing itself exists once, in DC Capacity, and Growth Dashboard
gets a link to it. Building the explanation in both places would be two
things to maintain and, before long, two versions of the truth.

**What C's loss costs, recorded so it is not forgotten.** C was the only
approach that made the hiring rule concrete — a newly onboarded FE appearing on the
roster is what actually ends a Pilot Load breach. A can *say* it; C made it
unavoidable. If S5 turns out to be common, borrowing C's two roster columns
into A is the cheapest fix, and this paragraph is where the next person finds
that out.

**Still to do before the design: the shapes.** A and E were chosen from
paragraphs. Step 3 draws all five, because that is what the method is for —
and the choice may survive it or change.

---

## What the shapes showed (step 3)

Drawn, not argued. A situation counts only if the screen has room to show it.

| | shape | situations | tests | verdict |
|---|---|---|---|---|
| **A** | Capacity Cut tab, DC Capacity | **7/7** | **4/4** | home |
| **E** | reason card, Growth Dashboard | 3/7 | 1/4 | door |
| **D** | pushed weekly notice | 1/7 | 1/4 | door |
| **B** | inline alert on the capacity field | 2/7 | 2/4 | out |
| **C** | roster columns, Pilot Management | 1/7 | 1/4 | out |

**The choice survived the drawing. A + E stands.**

Three things the drawings showed that the writing did not:

**Only A has something to show when nothing is wrong.**
B, C and D only exist once a cut has happened. So they are blank for a captain
who has never been cut (S1), one who is close to the line (S2), and a new DC
that is exempt (S6). B cannot answer T3 for the same reason — a captain cannot
ask "am I close?" on a screen that appears only after the answer is yes.
This is what makes A the home. Not the score.

**B beat C.** In writing, C sounded like the better idea. Drawn, B answers two
tests and C answers one. Both are still out. But they were ranked the wrong way
round, and C was the one carried forward.

**E is thin, and that is the risk.** One test out of four. E can say a cut
caused the drop. It cannot say what to do next. Everything depends on its link
opening the Capacity Cut tab. If that link is weak, E is decoration.

### Still carried, still unresolved

**S5 — every metric green, but no new FE.** Only C made this impossible to
miss, because it lists people instead of showing a percentage. C is out. A
picks this up through its field-executive list. That list is now doing real
work: it is the only place the hiring rule becomes visible — capacity returns only
when a new FE is hired (C4). If the design weakens
the list, S5 goes with it.
