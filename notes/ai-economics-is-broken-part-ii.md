---
title: "AI Economics Is Broken, Part II"
author: "InflectAI, Inc."
entity: "InflectAI, Inc."
published: "2026-06-15"
canonical_url: "https://www.inflect-ai.com/notes/ai-economics-is-broken-part-ii"
status: "current public mirror"
---

> Canonical reading experience: https://www.inflect-ai.com/notes/ai-economics-is-broken-part-ii

Field Note

# AI Economics Is Broken, Part II

Falling token prices help customers. They can hurt the balance sheets holding the GPUs.

- Entity: InflectAI, Inc.
- Published: June 15, 2026
- Status: current

## Listen

Audio version read with Thomson Nguy's licensed voice clone.

[Download the audio version.](https://www.inflect-ai.com/audio/ai-economics-is-broken-part-ii-thomson-nguy.mp3)

OpenAI CFO Sarah Friar has been making the optimistic case for AI economics. On the All-In podcast circuit, she framed falling token costs as progress. The reported headline number is dramatic: she said compute cost per token fell roughly 97% from GPT-4 to GPT-5.4 in about two years. She also said OpenAI raised prices on GPT-5.5 by 2x, while customers still received roughly a 20% to 30% reduction in cost per token because the newer model was more efficient per token. That is the customer story. Cheaper tokens make more workflows economical. A coding agent can run longer. A support system can answer more tickets. An internal automation project can clear the finance department's ROI test. Enterprises get more AI for the same dollar, and the lab gets to argue that AI is moving down the cost curve like every serious computing platform before it.

The infrastructure story moves on a different clock. A token is produced by GPU capacity, power, memory, networking, scheduling software, data-center infrastructure, and capital. When the token gets cheaper, the customer sees savings and the lab sees more usage. The balance sheet holding the GPUs sees the earning power of the machine reset. The token price can fall this month. The GPU was bought before the price cut. The data center was built before the price cut. The power contract, lease, and debt obligation do not automatically fall with the token.

Token prices are falling for three reasons at once. Some of it is real engineering: inference systems are improving, caching is improving, routing is improving, and smaller models are getting more capable. Some of it is competition: OpenAI, Anthropic, Google, xAI, Meta, and Chinese open-model competitors are fighting for developer usage and enterprise workflow capture. A model priced too high for production gets routed around. Some of it is utilization pressure: AI infrastructure has to stay full. A GPU-second that goes unused cannot be sold tomorrow. Cheap tokens help customers, and they help keep expensive machines occupied while the clock is running.

The delayed reckoning comes from the split between the lab's mirror and the cloud provider's mirror. The lab sees the first mirror: lower cost per token, rising usage, better models, and more enterprise workloads becoming possible. The cloud provider sees the second mirror: committed contracts, backlog, utilization plans, and multi-year depreciation schedules. Both mirrors can look good at the same time. The lab says efficiency improved. The cloud provider says capacity is contracted. The customer gets cheaper AI. The bill arrives later.

CoreWeave is the clean public example of the second mirror. At the end of 2025, it reported \$66.8 billion of revenue backlog, up from \$15 billion, with weighted-average contract length extending from four years to five. The comforting version says the capacity is spoken for. The same filings show the cost side arriving quickly. CoreWeave's depreciation and amortization rose from \$843 million in 2024 to \$2.3 billion in 2025, an increase of roughly \$1.5 billion. Interest expense rose from \$361 million to \$1.229 billion. The mirror says backlog. The machine says depreciation and financing cost.

Amazon gives the broader cloud-era comparison. Effective January 1, 2025, Amazon changed the useful life of a subset of servers and networking equipment from six years to five years, citing the increased pace of technology development, especially AI and machine learning. Amazon expected that change to reduce 2025 operating income by about \$0.7 billion. A one-year useful-life adjustment can move hyperscaler operating income by hundreds of millions of dollars. Five years still spreads the cost evenly. AI token prices are not moving evenly.

Claude Opus is the clean price example. Opus output pricing fell from \$75 per million tokens to \$25 per million tokens. The same million output tokens now earns one-third as much. If that six-month reset is annualized, one-third becomes one-ninth. Roughly 11% of the original premium token earning power remains after a year. Roughly 89% is gone before any throughput offset. The physical GPU can still serve smaller models, batch inference, embeddings, internal workloads, lower-priority jobs, and older-model traffic. That residual work has value. The premium value is the issue.

The operator's defense is obvious: throughput can improve, utilization can rise, and demand can grow. If the same chip can serve three times as many billable tokens, the two-thirds price cut can be offset. If utilization rises enough, lower price can still produce more revenue. If demand explodes, the fleet can stay full. That is the bet under the entire AI infrastructure buildout. Efficiency exists. The question is whether throughput, utilization, and demand can outrun token deflation fast enough to protect the earning power of the asset.

Straight-line depreciation assumes a smoother world. Amazon, Microsoft, Alphabet, and CoreWeave all depreciate data-center or computing equipment over multi-year useful lives using straight-line depreciation. CoreWeave uses six years for technology equipment. Amazon uses roughly five to six years for servers and networking equipment. Alphabet generally uses six years for servers and network equipment. Microsoft discloses two to six years for computer equipment. Straight-line depreciation treats the asset cost as a steady annual expense. AI GPUs may have a short premium life and a longer residual life. The first part can fall quickly. The second part can linger for years.

The cash was spent early. The debt was raised early. The data center was built early. The income statement recognizes the asset cost slowly. If premium earning power falls quickly, the accounting catches up late. The lab can point to lower token costs and higher usage. The cloud provider can point to backlog and useful life. Investors can point to growth. Customers can point to cheaper AI. Each number is real. None answers the asset question by itself: can the GPU fleet earn back its cost after the price of its output falls?

Agentic workloads make the question harder. A normal chat completion is bounded. A coding agent can read repository context, write code, call tools, run tests, inspect failures, retry, summarize, and open a pull request. GitHub Copilot's coding agent can work from an issue, create a branch, operate in a GitHub Actions-powered environment, write code, push commits, and open a pull request. One visible assignment can become many model calls. Agentic traffic uses more context, more output, more retries, more tool calls, and more latency-sensitive model time. It is the workload everyone wants to sell, and it is also the workload that raises the volume required to pay for the machines behind it.

The depreciation bag sits behind falling token prices. Token deflation is good for customers. It may work for labs if usage rises fast enough and infrastructure partners keep carrying the buildout. It is dangerous for the companies holding the GPUs. The price cut happens now. The compute commitment comes due later. The asset markdown comes later. The delay lets the economics look better than they are.

Cheaper tokens are the point of the platform. The problem starts when falling token prices are treated as proof that AI economics are improving while the machines producing those tokens lose earning power faster than the books recognize. A 97% decline in cost per token may be a triumph for customers and a sales argument for labs. For the balance sheets holding the GPUs, it is also a warning label.

## Sources

- All-In transcript with OpenAI CFO Sarah Friar: [Happy Scribe transcript](https://podcasts.happyscribe.com/all-in-with-chamath-jason-sacks-friedberg/openai-cfo-sarah-friar-ipo-ai-rivalries-new-device-and-spending-100b-on-compute).
- All-In episode video: [YouTube episode](https://www.youtube.com/watch?v=TjrShuj_Zsg).
- CoreWeave fiscal 2025 results: [CoreWeave investor release](https://investors.coreweave.com/news/news-details/2026/CoreWeave-Reports-Strong-Fourth-Quarter-and-Fiscal-Year-2025-Results/).
- CoreWeave 2025 Form 10-K: [SEC filing](https://www.sec.gov/Archives/edgar/data/1769628/000176962826000104/crwv-20251231.htm).
- Amazon 2024 Form 10-K language on 2025 useful-life change: [SEC filing](https://www.sec.gov/Archives/edgar/data/1018724/000101872425000004/amzn-20241231.htm).
- Anthropic pricing page: [Claude pricing](https://platform.claude.com/docs/en/about-claude/pricing).
- GitHub Copilot coding agent documentation: [GitHub Docs](https://docs.github.com/en/copilot/using-github-copilot/coding-agent/about-assigning-tasks-to-copilot).
