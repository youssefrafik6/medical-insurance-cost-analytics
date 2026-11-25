# Executive summary

This project analyzes 1,338 educational insurance records to show how analysts can investigate variation in billed charges, quantify uncertainty and explain conflicting statistical signals. It extends Youssef Rafik’s MAT 429 project with independent R and Python calculations, DuckDB queries and an interactive dashboard.

Recorded smoking status showed the clearest charge difference. Typical charges, measured by the median, were about $34,456 among smokers and $7,345 among nonsmokers. The estimated gap was $27,111, with a 95% interval of $22,048 to $28,866. Age showed the strongest association among the numeric characteristics examined. BMI and the number of covered children had weaker links.

Average charges for male records were about $1,387 higher than for female records, while their typical charges were within $44. The regional results also depended on whether the analysis emphasized averages or the ordering of charges. Upper-tail observations and differing group spreads helped explain why. The original and expanded analyses kept all valid records.

The workflow demonstrates how a healthcare analytics team could report charge distributions, compare segments and assess how high-charge observations affect operating metrics. The sample’s source population and time period are uncertain. Its results describe this educational file and cannot support causal, pricing or underwriting conclusions.
