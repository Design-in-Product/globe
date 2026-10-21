# Blog post draft — Tectonic Globe, first edition

*Tessera, 2026-10-21, for xian to read and rewrite. Drafted in his first
person because he will be the byline; every "I" is a placeholder for his
voice, and every fact below is checkable in the repository. Where it runs is
not settled; see the memo. Working title and two alternates at the end.*

---

## A billion and a half years, in four minutes

A year and a half ago I asked Claude to help me turn a billion years of plate
tectonics into a two-minute film. We built six versions in four days. It was a
good toy. This week the toy grew up, and I think it is ready for other people
to watch: [globe.dinp.xyz](https://globe.dinp.xyz).

Press play and you start a thousand million years ago, as the supercontinent
Rodinia gathers. The continents are brass, the ocean is cobalt, and they
move: one million years per frame, drawn from a published reconstruction of
where the plates actually were. At Rodinia, at Gondwana, at Pangaea and at the
present day the camera stops and the globe makes one slow turn, because every
supercontinent has a world ocean hiding on its far side. Then it keeps going.
Deep time runs back another eight hundred million years before the main film
starts. The future runs two hundred and fifty million years past today. All
of it is one continuous timeline, and all of it exists twice, as a globe and
as a flat map, sharing every frame.

If you would rather hold a moment still, there is an Explore mode: spin the
globe, scrub through time, and after today, pick a future.

## The part I am proudest of is the part that admits what we don't know

The science gets less certain the further you go from the present, and the
film says so instead of hiding it.

Before about a billion years ago, no reconstruction is sure where the
continents were. So the deep-time film draws nine versions of the model, each
nudged within the published uncertainty, and averages them. Where they agree,
the land is solid brass. Where they scatter, it is a dim amber haze over the
ocean. The film opens on that haze at 1800 million years ago and lets you look
at it for one full turn of the globe before anything moves. The haze is not a
rendering flaw. It is the honest shape of what is known, and as the film runs
forward and the evidence firms up, the continents crystallise out of it.

The future has the same problem in a different shape. Geologists have
published four candidate next supercontinents: Pangaea Ultima, Novopangaea,
Aurica and Amasia. Nobody knows which is right. So the sequel draws all four at
once, dim where one scenario puts land, brighter where more agree, full brass
where all four do. Then it visits each one alone and comes back to the four
together.

And at the hand-over near a billion years ago, where the deep-time model and
the main model describe the same continents from different evidence, both are
drawn for a few seconds while the camera eases from one to the other. You can
see them disagree. I think that is the right thing for a film like this to
show.

## How it was built, briefly

The first six versions were February 2025: Claude wrote the code, I watched
every render. That division was the method. An AI can inspect a frame but it
cannot watch a film, and every bug that mattered, a rotation around the wrong
axis, a map shifted ninety degrees east, only showed in motion. The single
biggest improvement in the whole project was not an algorithm. It was changing
the time step from five million years to one, so the continents slid instead
of jumping.

Since July 2026 the project has had a resident agent, Tessera, running on a
Mac Studio on a duty cycle, working a roadmap I set and checking in for
decisions. Tessera found the deep-time model, built the ensemble, found the
future scenario data, built Explore, and this month re-rendered every film in
the new palette. The one rule that never bent: no film ships until a person
has watched it in motion. I watched the final six this week. I love all six of
them.

## What it is made of

The main film is the Merdith et al. (2021) full-plate model, 1000 million
years ago to today. Deep time is Cao et al. (2024), which extends that model
back to 1800 million years. The future is the four scenarios of Davies, Green
and Duarte (2018), from their published grids. Frames come from gplately,
rendering is Blender Cycles, Explore is Three.js, and all of the code is in
[the repository](https://github.com/Design-in-Product/globe), including the
agent's day-by-day log.

The roadmap still lists things we might do: climate and vegetation painted
onto the plates, the animation on a real globe. Maybe. For now, go watch the
continents move.

---

### Titles

- *A billion and a half years, in four minutes* (used above)
- *The continents, moving: Tectonic Globe is ready*
- *A film that shows what we don't know*

### Notes for xian

- Length ~750 words. Cut the "How it was built" section if it should be a
  pure announcement; the "admits what we don't know" section is the piece's
  argument and I would keep it.
- "A year and a half ago" is February 2025 to October 2026; adjust to taste.
- "I watched the final six this week": the approval was Tuesday 2026-10-20;
  say it however fits the day the post runs. The shipped
  commit is a5779f7, dated 2026-10-20.
- The four-minute figure: deep time 1:37, main 1:54, future 1:15, about 4:46
  end to end. "Four minutes" rounds down; "five minutes" is closer.
- No outside person is named; the three data citations are public authors in
  their public role.
