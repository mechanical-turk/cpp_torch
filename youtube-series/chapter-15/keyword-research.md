# Chapter 15 keyword and SEO research

Dated 2026-10-28. Pre-script step required by the long-form playbook. Script:
[script.md](script.md). Review: [script-review.md](script-review.md).

## What the episode delivers

Chapter 14 ended (captions, final minute): "we will look into training on more data. We will look
at momentum and velocity and we will also look at hopefully the Adam optimizer." This episode
delivers momentum (velocity) and Adam, implemented in the same `main.cpp`, measured against plain
stochastic gradient descent on MNIST. It does not deliver more training data; that promise moves to
a later episode and is recorded as a scope change in `script-review.md`. It does not derive Adam's
theory, cover AdamW, weight decay, schedulers or Nesterov momentum.

## Evidence available and unavailable

- Owned search and traffic data for this topic: unavailable. No YouTube Studio search-term export
  exists for an optimizer episode yet. No query volume, competition or ranking claim is made.
- Web search on 2026-10-28 (three queries, standard mode) returned written tutorials and a few
  video titles; channels and view counts of the videos could not be verified from snippets and are
  not used as evidence of demand.

## Observed wording

- "SGD vs Momentum vs Adam", "optimizers explained", "optimizers from scratch" (written tutorials,
  e.g. dev.to "Optimizers Explained: SGD vs Momentum vs Adam, Visualized", dadops "Optimizers from
  Scratch: How Neural Networks Actually Learn", a ZeroToAI "Optimization from Scratch: Gradient
  Descent & Adam" page).
- Video titles seen in snippets: "Optimizers Explained Visually | SGD, Momentum, AdaGrad, RMSProp &
  Adam", "MOMENTUM Gradient Descent (in 3 minutes)", "ADAM Optimization Algorithm Explained
  Visually". Verified only as titles, not as traffic.
- C++ specific: the search found a CodeSignal lesson on Adam in C++ and PyTorch's C++ docs for
  `torch::optim::SGD` with momentum. It did not find a from-scratch C++ neural-network build that
  covers both momentum and Adam. This is an observation about three searches, not a proof of a gap.
- Terminology check (original sources): Adam is Kingma and Ba, "Adam: A Method for Stochastic
  Optimization", ICLR 2015, arXiv 1412.6980. It keeps a running average of the gradient (first
  moment) and of its square (second moment), corrects both for starting at zero, and divides the
  step by the square root of the second. Momentum as a heavy-ball analogy goes back to Polyak (1964),
  as cited by the tutorials found; not independently checked.

## Candidate phrases

| Phrase | Fit | Decision |
| --- | --- | --- |
| momentum and Adam optimizer from scratch in C++ | exact scope; matches observed wording plus the series' C++ angle | PRIMARY |
| SGD vs momentum vs Adam | matches how tutorials phrase the comparison; the episode measures it | SUPPORTING |
| gradient descent with momentum | the concept introduced by the first edit | SUPPORTING |
| Adam optimizer | the second edit | SUPPORTING |
| velocity | Chapter 14's own word; the variable in the code | SUPPORTING (spoken once, tied to the code) |
| optimizers explained | broad, tutorial-style | REJECTED: overpromises explanation beyond measured behaviour |
| best optimizer / Adam vs SGD winner | invites a verdict the data does not give | REJECTED |
| faster training | blanket claim | REJECTED: we measure loss after a fixed number of epochs |
| AdamW, weight decay, learning rate scheduler, Nesterov | not built | REJECTED |

## Spoken-keyword map (intended natural uses, audited against the final `>` narration)

- Opening: names the subject and the check in one sentence: "gradient descent with momentum",
  and the comparison "against plain stochastic gradient descent". Pronounce "stochastic gradient
  descent" in full on first use, then "SGD".
- First code beat: "velocity" as the name of the stored running direction.
- Adam section: "the Adam optimizer", with the two running averages named by what they hold.
- Recap: "momentum and the Adam optimizer", "SGD, momentum and Adam" as the three compared methods.
- Title and thumbnail alignment stays pending until packaging exists (L02 check).

## Open items

Recheck the final captions after recording. Do not stuff terms; the map above is what the lesson
needs to say anyway.
