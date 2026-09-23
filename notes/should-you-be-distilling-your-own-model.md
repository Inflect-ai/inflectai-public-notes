---
title: "Should You Be Distilling Your Own Model?"
author: "Thomson Nguy"
entity: "InflectAI, Inc."
published: "2026-09-23"
canonical_url: "https://www.inflect-ai.com/notes/should-you-be-distilling-your-own-model"
status: "current public mirror"
---

> Canonical reading experience: https://www.inflect-ai.com/notes/should-you-be-distilling-your-own-model

Founder Note

# Should You Be Distilling Your Own Model?

- Author: Thomson Nguy
- Entity: InflectAI, Inc.
- Published: September 23, 2026

\$87,000 vs roughly \$1,000.<sup>[1](#cost-note)</sup> The decision seemed obvious to me. Those were our estimates for running an extraction workload of 6.5M semantic atoms on Sonnet or training and running our own distilled model.

It was kind of an exciting idea actually. We were extracting structured beliefs from financial text - who said what, what they actually claimed, and how certain the source was. Those extractions would become records the rest of the system relied on. Sonnet was our quality anchor. We would use Sonnet as the teacher, train a much smaller model on the narrow judgment we needed, and then run that model ourselves at a fraction of the cost. Every correction would improve a model we owned. The lower cost would solve the immediate problem. The accumulated learning could become a durable competitive advantage.

What's more - the idea of distilling your own model - something that seemed complicated and the realm of hard core data scientists only a few years ago was easy now. I had commissioned my own AI Data Scientist Agent - named Kepler, after the early German astronomer Johannes Kepler - running on Opus 4.8. In about 15 minutes, Kepler had written the developmental harness to train and distill a student model using Sonnet as the teacher model.

Good little Data Scientist that Kepler was, he built a gold standard test. 23 hard edge cases. Sonnet - the teacher model - itself scored 21/23. A student trained only on Sonnet's answers would have no correct teaching signal for the other 2 cases. But because we would own the model (Qwen2.5-7B-Instruct), our hope was that we could eventually improve on those 2 points with our own corrections. Over time, as we found more and more edge cases, each refinement would be built into our own Qwen model. We could tell the world we had built a specialized model for financial data as part of our durable competitive advantage.

Then Tycho, our FinOps/Science optimizer agent, asserted himself. Or more precisely, I inserted Tycho into the mix. You see, Tycho's charter was to get the most efficient science and production for the dollar. Optimization can come from the vendor or the algorithm. And we ran the test against open-weight models.

| Model              | Initial score | What it was                      |
|--------------------|---------------|----------------------------------|
| Claude Sonnet 5    | 21/23         | Teacher and quality ceiling      |
| DeepSeek V3.2      | 18/23         | Viable cheap pick                |
| Qwen3-Next-80B-A3B | 8/23          | Failed the hard cases; ruled out |

The initial results seemed to validate our decision to go with a distilled model with Sonnet as the teacher. The data indicated the open-weight models weren't good enough. DeepSeek was slightly worse than Sonnet and Qwen was a lot worse.

The pattern solidified. We would have a distilled model run against most of the corpus cheaply and the ones it could not catch (the residuals) would be escalated up to a higher model to solve. This seemed like a smart architectural pattern. So the residuals became the cost lever. The more we caught and trained into the rules, the more cost efficient our model would be.

This was the moment that the true nature of our true competitive advantage hit me - having a better model is a stock advantage. Learning how to do something better is a flow advantage. Stock advantages are static things - distribution, a cool technology, capital - you have them or you don't. Flow advantages are about process and rates of improvement. How quickly can you learn and metabolize it in your organization? How can you drive down your rate of defects? Flow eventually beats stock, every single time.

And the lever for improvement was driven by two things - (1) allowing the model to give Unknown as a legitimate option instead of pushing it to give a false answer when it was truly uncertain, (2) looking at the pool of Unknown as feedback to improve your own rubric.

This was when our distillation thesis died. We took the pool of Unknown atoms. Used it to refine our rubric. Reran it against three held-out sets. DeepSeek V4.1 Flash passed 46/46. The six control cases stayed clean every time. \$1,000 vs \$1,000 over our current corpus of 6.5M atoms.<sup>[1](#cost-note)</sup> The deciding factor wasn't the cost, it was the time. Every rubric improvement would require a new training distillation run if we ran our own model. If we just used DeepSeek (via the FireworksAI API), we could just improve the rubric.

<figure class="note-figure">
![Experiment sheet comparing the original 23-case bake-off, where Claude Sonnet 5 scored 21/23, DeepSeek V3.2 scored 18/23, and Qwen3-Next-80B-A3B scored 8/23, with separate later held-out tests where DeepSeek V4.1 Flash passed 46/46 across three new sets and six controls stayed clean.](https://www.inflect-ai.com/notes/distillation-experiment-sheet-v0.1.png)

*Original 23-case bake-off: Claude Sonnet 5, DeepSeek V3.2, and Qwen3-Next-80B-A3B. Separate later held-out tests: DeepSeek V4.1 Flash passed 46/46 across three new sets; six controls stayed clean.*
</figure>

The distilled model was a stock advantage, a perishable asset. The rate of learning and metabolizing it into the organization was the enduring asset. That was the flow advantage for us. And simply using an API model call against an iteratively improving rubric was faster. Flow beats stock.

<div class="section note-footnotes" aria-label="Footnotes">

<sup>1</sup> The \$87,000 came from our first estimate. Correcting the number of model calls lowered the all-Sonnet projection to about \$58,000. The roughly \$1,000 student figure models training and GPU time for the Predicator extraction pass, excluding engineering and operations; the student was never served over the corpus. The roughly \$1,000 DeepSeek figure is a cache-contingent projection for that same unbuilt Predicator instrument; the current uncached Fireworks batch projection for the same stage is about \$2,151. These are models, not invoices, and neither figure prices the whole pipeline.

</div>
