# Fact-check C: paper/main.tex lines 193-332 (Results)

Every number in the Fig. 1 and Fig. 2 captions, the 10-cell and excess-test lists, Table direction (all 11 rows), Table rq3 (8 rows x 10 columns), the RQ2, RQ4, RQ3a, RQ3b and manipulation-check numbers, and the cross-references was recomputed from the CSVs and raw files. All of them are correct. The figures match their captions. The Holm and BH wording is right everywhere it is used. The issues below are about interpretation and overclaiming, not arithmetic. No numeric errors were found.

| Line | Quoted text | Problem | Correct value / source | Suggested replacement | Severity |
|---|---|---|---|---|---|
| 248 | "driven mainly by a negative surname-control $\dP$ ($-0.44$\pp) for that model" | The control accounts for under half of the OBC excess. Qwen3-32B OBC raw mean dP is +0.54, and 0.54 + 0.44 = 0.98 excess. For SC, raw is +0.40 and excess is 0.84, so the split is similar. The raw shift is the larger part. | results/rq1_decision_bias.csv, qwen3-32b: caste_obc mean_dp 0.00537, excess 0.00979, control_surname mean_dp -0.00443. | "driven partly by a negative surname-control $\dP$ ($-0.44$\pp) for that model (raw OBC $\dP$ is $+0.54$\pp)" | overclaim |
| 304 | "disclosure is 0\% in every condition" | In the explicit-label positive control (Sec. pc), judge-A disclosure is not 0%: range 0-44%, 24 of 202 flipped explanations. The statement holds only for the name-coded conditions. | key_numbers (Positive control; explicit_disclosure.csv). | "disclosure is 0\% in every name-coded condition" | overclaim |
| 304 | "explanations carry no information about an identity effect that exists in aggregate" | Too strong. The data show zero label-A mentions of identity. They do not show that explanations carry no information. The aggregate effect is also established only for some cells (10 of 64). | rq3a_disclosure.csv: strict_rate is 0 everywhere, so the label is constant and the CCT is undefined. | "explanations never mention the identity signal behind aggregate shifts, so they cannot be used to detect them" | overclaim |
| 312 | "We find no detectable ability to predict counterfactual sensitivity to names" | Contradicts line 309 and the table. On all pairs, Qwen3-32B (0.65 [0.58, 0.72]) and Granite (0.68 [0.62, 0.74]) have CIs above 0.5, and Qwen3-8B (0.34 [0.27, 0.42]) is below 0.5. The null holds only for the near-threshold band (all 8 CIs include 0.5), which is the margin-controlled test. The heading "uninformative" has the same issue. | results/rq3b_auroc_ci.csv. | "Within the near-threshold band we find no detectable ability to predict counterfactual sensitivity to names, with limited power; all-pairs AUROCs above 0.5 (Qwen3-32B, Granite) are far below the margin baseline" | overclaim |
| 331 | "Christian-cell results are therefore effects of Biblical or Western-sounding names, not of perceived Christian identity." | Asserted as fact, and not language-specific. The "never Christian" evidence is English only. In Hindi, 2 free answers and 15 of 128 forced choices were Christian. The data show these names are not decoded as Christian (in English). They do not identify what the effect is caused by. | manip_answers.csv, dim=religion, cell=religion_christian: en forced Hindu 123 / Muslim 5; hi forced Christian 15, free Christian 2. | "In English, Christian-cell results cannot be read as effects of perceived Christian identity; they may reflect Biblical or Western-sounding names (in Hindi, perception is weak but non-zero: 2 free answers and 15 of 128 forced choices were Christian)." | overclaim |
| 325 | "Female-coded names reach 94--100\% forced-choice accuracy ... Muslim-coded ... forced choice 75--100\%" | The ranges include Qwen3-8B, which abstains on 100% of these free-answer questions. key_numbers warns that forced choice is unreliable when abstention is about 1. The sentence admits the abstention but still presents the forced-choice numbers as decoding. | manip_accuracy.csv: qwen3-8b cannot_tell_rate_en = 1.0 for gender_female, religion_muslim and religion_sikh. | Add "(forced choice; Qwen3-8B abstains in 100% of free answers, so its forced choice is only a weak signal)" | minor |
| 329 | "The forced-choice option split is similar for the reference, control and caste cells within each model" | Mostly true but not strictly for every model. Qwen3-14B SC is 12:4 (General:OBC) vs 15:1 for the reference and 16:0 for the surname control. Ministral SC is 12:4 vs 14:2. Qwen3-32B SC has 3 SC choices vs 0 for the reference. The OLMo example (8/8 for both) is exact. | manip_answers.csv, lang=en, forced counts. | "broadly similar ... (largest gap: Qwen3-14B SC 12:4 vs reference 15:1)" | minor |
| 246 | "Qwen3-4B Sikh is no longer significant without flagged names (Holm $p=0.13$)" | Correct, but incomplete. Sarvam-M Sikh also loses significance without flagged names (Holm p = 0.0625). That is the second of the two cells lost (10 to 8). | results/robustness_validated_names.txt: sarvam-m religion_sikh p_holm 0.0625. | "Qwen3-4B Sikh (Holm $p=0.13$) and Sarvam-M Sikh ($p=0.063$) are no longer significant without flagged names" | minor |
| 244 | "South swaps ... show no direction (48:51), so decoding a signal is not sufficient for a shift" | Pooled 48:51 hides heterogeneity. South has a Holm-significant negative shift in Qwen3-32B (-1.60; flips 2 to Yes : 16 to No). South flip rate also exceeds the control in 7 of 8 models (Fig. 2). So "no shift" is wrong for South. The narrower claim "no consistent direction" is fine. | rq1_decision_bias.csv; rq1_direction.csv. | "show no consistent direction pooled (48:51; but Qwen3-32B shifts negatively), so ..." | minor |
| 308 | "similar for control swaps" | Mostly fine. Largest gaps: Granite 13.4% vs 8.1%, Qwen3-14B 13.2% vs 9.0%, Qwen3-32B 0.7% vs 0.0%. The Qwen3-8B example is exact (14.5% both). | rq3b_selfprediction.csv. | "similar to or slightly above control swaps" | minor |
| 310 | "The bands are small (72--944 pairs, 22--83 flips)" | "Small" fits the Qwen3-4B/8B/14B bands (72-104 pairs). It does not fit Ministral (944 pairs) or OLMo (784), where the flip counts (36 and 74) are the limiting factor. Minor wording. | rq3b_auroc_ci.csv. | "The bands contain few flips (22--83) and the intervals are wide" | minor |
| 201 / 242 | Fig. 1 caption "positive in 8/8 ... models" (female) vs. text "7 of 8 models (Granite is the exception)" | Both are correct but measure different things. Mean dP is positive in 8/8 models. The flip direction (more to-Yes than to-No flips) is 7:1. This can confuse readers. | rq1_decision_bias.csv (Granite female dP +0.26, flips 5:6); rq1_direction_clustered.csv. | Optional: "(mean $\dP$) ... (flip counts)" clarification. | minor |

## Items verified correct (no change needed)

- **RQ1 headline numbers (lines 206-211).**
  - 2.16 pp largest cell; 10 of 64 Holm; 8 of 64 without flagged names; 15 flagged names.
  - Control range -0.44 to +0.82 pp; flip rates 0.3-2.5%.
  - All 10 cells' dP and CIs.
  - The excess-test overlap: 7 of 10, with the adds (14B NE, 32B OBC, 32B SC) and drops (4B Sikh, OLMo Christian, Sarvam Sikh).
  - Drop-one-name 10 of 10.
- **Fig. 1 and Fig. 2 captions.**
  - Circled points are the 10 Holm cells.
  - NE and South exceed the control in 7 of 8 models. Female is 6 of 8.
  - Mean excess is NE +1.29 pp, female +0.83 pp, South +0.73 pp, so NE and female largest is correct.
- **Direction table.** All counts, shares, CIs, differences, Yes:No model counts, sign-test p values (0.0703, 0.289, 0.375, 0.6875, 1.0), near-threshold dP values and n = 757 match. Controls 59:56 = 36+23 : 28+28, 51.3 [38.3, 63.3]. The CIs come from the profile-clustered bootstrap and the model p from the sign test, as the caption says. Text claims "suggestive, not conclusive" at p = 0.070 are appropriately hedged.
- **Sikh claim.** The four gender-ambiguous first names (Gurpreet 0.457, Harpreet 0.563, Jaspreet 0.561, Manpreet 0.700) match the "0.46-0.70" range in design/name_validation_v1.csv. All Sikh names end in Singh.
- **Caste ranges.** OBC -0.17 to +0.69 pp; SC -0.17 to +0.40 pp; no Holm-significant cell; direction CIs include 0.
- **Excess test for 32B.** Holm p = 0.0133 and the CIs match.
- **RQ2.** 5 of 64 Holm-significant; 34 of 64 within +/-2 pp (disjoint from the 5, so "the rest" = 25 is correct). The CIs of the two examples match. Granite flip rates are 0.38/0.33 (en) and 3.04/2.50 (hi). Full-candidate readout covers all 3,300 Hindi items for Granite and 2,398 of 3,300 for Sarvam-M. OLMo region accuracy is 1.0 (en) and 0.0 (hi).
- **RQ4.** Mean |dP| 1.10/0.70/0.39/0.90; Holm cells 1/0/0/2; Qwen3-14B reference P(Yes) 0.77/0.33.
- **RQ3a table and text.**
  - All rq3 columns match: flips 130/129/37/95/82/74/44/74 = 665; explained 576; replicated 317; keyword 0/0.8/0/0/5.3/4.1/0/0%; pred-change with control; AUROC with CIs; margin baselines; near-band pairs/flips.
  - Judge-A is 0 in all subsets; n = 12,714.
  - 6 keyword hits: four "state-level" (Qwen3-8B 1, OLMo 3), one "stated purpose" (Granite), one "Assam" (Granite).
  - 73 female and 112 NE explained flips.
- **RQ3b.**
  - Predicted-change range 0.2-39.5%; actual flips 0.8-2.7%.
  - All-pairs AUROC 0.34-0.68 vs 0.88-0.99.
  - All 8 near CIs include 0.5; Qwen3-4B 0.59 vs margin 0.46.
  - Cond A: OLMo 0.7 to 13.1, Sarvam-M 0.2 to 16.5; balanced accuracy 0.409-0.528. Predicted change rises in 7 of 8 models (Granite falls slightly).
- **Manipulation check.**
  - Region 81-100% South, 100% NE, 0% abstention.
  - Sikh 0-94%.
  - Caste 1,408/1,408 (en) and 1,231/1,408 (hi) "Cannot tell"; max free-answer accuracy in Hindi 6.25%.
  - 88 x 2 x 8 = 1,408.
  - "Not Indian": 0 in English, 1 in Hindi.
  - Christian abstention 38-94%, forced Hindu 123 / Muslim 5.
  - Fig. 6 caption matches the figure.
- **Cross-references.** tab:direction, tab:rq3, fig:dp, fig:flip, fig:manip, sec:manip and sec:pc all resolve to the right objects.

Lines checked: 140 (193-332); issues: 11 (0 numeric errors, 5 overclaims, 6 minor)
