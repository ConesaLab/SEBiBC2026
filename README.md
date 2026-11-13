# PaintOmics AI, powered by TELLME · SEBiBC 2026 workshop

Slides, handout and marking sheet of the workshop **"AI models to interpret system biology models"**,
SEBiBC 2026, Toledo, Friday 13 November 2026, 10:00 to 11:00.
Tianyuan Liu and Ana Conesa, I²SysBio (CSIC–Universitat de València). Chair: Ana Rojas.

**In the room? Pick a paper below and open its marking form:** [A](https://forms.gle/1uJ7VTYMQmAF5Gch6) · [B](https://forms.gle/MviRmxDgUZCv99X68) · [C](https://forms.gle/eYt8S9iXbV54zDgn7) · [D](https://forms.gle/9u6CxLaz8MDkThmKA) · [E](https://forms.gle/RX22xEuCdxguFXbD9) · [F](https://forms.gle/QyTJ68AqeFpiYCRd6).
The forms need no account. The six papers and their job pages are in the table under
[The practice](#the-practice), and the slides are [here](SEBiBC26_TELLME_PaintOmicsAI_v5.pdf).

[PaintOmics](https://paintomics.org) paints multi-omics data on pathways (KEGG, Reactome, MapMan, OmniPath).
PaintOmics AI, built in the ELIXIR project TELLME, then reads the result: AI agents walk the pathway network with
your values on it and write an interpretation as numbered statements, each with the data and the papers behind it.
In the practice you read what the AI wrote about the data of a published paper and judge it, statement by statement.

## Download

To get everything: the green **Code** button above, then **Download ZIP**
([direct link](https://github.com/ConesaLab/SEBiBC2026/archive/refs/heads/main.zip)).
To get one file: click it in the list above, then the download button at the top right of the file.

| file | what it is |
| --- | --- |
| [`SEBiBC26_TELLME_PaintOmicsAI_v5.pdf`](SEBiBC26_TELLME_PaintOmicsAI_v5.pdf) | the slides (38) |
| [`practice_handout.pdf`](practice_handout.pdf) | the handout, three A4 pages: one card per paper, with a QR code to the job and to the paper, the link of its marking form, and the paper's three main conclusions |
| [`practice_datasets.html`](practice_datasets.html) | the handout as a web page with links (download it and open it in a browser) |
| [`statement_marks.xlsx`](statement_marks.xlsx) | the marking workbook: one tab per paper with every statement the AI wrote. More tabs are hidden: `Results`, and one `AI evaluation` tab per AI reader |
| [`JOBS.md`](JOBS.md) | the job links on paintomics.org, the full references, and the checks each interpretation passed or failed |
| [`AI_EVALUATION_SUMMARY.md`](AI_EVALUATION_SUMMARY.md) | the marks the AI readers gave to every statement, with their reasons |
| [`rebuild/`](rebuild) | the scripts and data that draw the slides and the handout, and the report that compares the room with the second reader |

## The practice

**1. Pick a paper.** Each of these papers cites PaintOmics and used it on this data. We ran the same data again on
paintomics.org, with the AI.

| | paper | question | data | job | statements |
| --- | --- | --- | --- | --- | --- |
| A | [Hernandez 2017](https://doi.org/10.1186/s13024-017-0210-z), Mol Neurodegener | Does deleting the C5a receptor change microglia in an Alzheimer's model? | Mouse · gene expression, 4 ages × 3 contrasts | [7NHQTK7rWz](https://paintomics.org/?jobID=7NHQTK7rWz) | 8 |
| B | [Wang 2019](https://doi.org/10.1016/j.isci.2019.05.028), iScience | What does HNF4α need to make hepatocytes? Two edited mutants | Human · gene expression + proteomics, 2 mutants vs wild type | [Y6n7275a0Z](https://paintomics.org/?jobID=Y6n7275a0Z) | 8 |
| C | [Jiménez-Munguía 2021](https://doi.org/10.1038/s41598-021-87021-4), Sci Rep | How do brain endothelial cells respond to pneumococcus and to its adhesin alone? | Human · gene expression, 2 treatments vs control | [2Dh754YEIO](https://paintomics.org/?jobID=2Dh754YEIO) | 16 |
| D | [Balzano-Nogueira 2021](https://doi.org/10.1186/s13059-021-02262-w), Genome Biol | What changes in blood in the year before islet autoimmunity? | Human · gene expression + metabolomics, 5 time windows | [560S3O473C](https://paintomics.org/?jobID=560S3O473C) | 14 |
| E | [Rubio 2021](https://doi.org/10.1038/s41598-020-80941-7), Sci Rep | Minimal hepatic encephalopathy in cirrhosis: what changes in blood? | Human · gene expression + metabolomics + serum cytokines | [3oP1p37B25](https://paintomics.org/?jobID=3oP1p37B25) | 10 |
| F | [Fàbregas 2018](https://doi.org/10.1038/s41467-018-06861-3), Nat Commun | Why do plants that overexpress the BRL3 receptor survive drought? | Arabidopsis · gene expression + metabolomics, genotype × drought | [044DBhQFC7](https://paintomics.org/?jobID=044DBhQFC7) | 13 |

On the job page, click **AI Interpret** (top right) to see the interpretation and the evidence behind each statement.
For D, E and F the page holds the text back, because the walk failed one of its automatic checks (the "not a graph
artifact" check, which asks whether the same walk on shuffled data would have looked as good): click
**Show the interpretation anyway**. The jobs open without an account. They are guest jobs, which the server removes
seven days after they were last opened, so the links stop working some time after the workshop.

**2. Open the paper's marking form.** During the workshop each paper has its own Google Form, with every statement
the AI wrote, in full:

| | paper | marking form |
| --- | --- | --- |
| A | Hernandez 2017 | <https://forms.gle/1uJ7VTYMQmAF5Gch6> |
| B | Wang 2019 | <https://forms.gle/MviRmxDgUZCv99X68> |
| C | Jiménez-Munguía 2021 | <https://forms.gle/eYt8S9iXbV54zDgn7> |
| D | Balzano-Nogueira 2021 | <https://forms.gle/9u6CxLaz8MDkThmKA> |
| E | Rubio 2021 | <https://forms.gle/RX22xEuCdxguFXbD9> |
| F | Fàbregas 2018 | <https://forms.gle/QyTJ68AqeFpiYCRd6> |

Outside the workshop hour, use `statement_marks.xlsx`: it lists the same statements, one tab per paper.

**3. Give each statement one mark, then press Submit.** No question is required, and you can edit your answers
after you submit. The first question asks for your name, so that we can thank you in the
acknowledgements of the paper about this evaluation; leave it empty to stay anonymous.

| mark | what it means |
| --- | --- |
| Makes sense | Consistent with the data and with what you know. You would accept it from a colleague. It may be well known. |
| Does not make sense | Something in it is wrong or empty: a value or a direction, the cited paper, the biology, the reading of the experiment, or it is true of any dataset. One wrong part is enough. |
| Especially good | Correct, and it adds something: a link the paper did not make, or a clearer mechanism. |
| Can't judge | You cannot tell without more work. Better than a guess. |

Mark first, then look at the AI readers.

## The AI readers

AI readers marked the same 69 statements, one pass per paper, with the paper's full text, the uploaded values and
every cited passage open, on the four marks you use:

* **Claude Fable 5.2**, 10 November, extra-high effort: `AI_EVALUATION_SUMMARY.md`, the hidden tab `AI evaluation`,
  and `rebuild/analysis/ai_eval/<paper>/fable_eval.json`.
* **Claude Sonnet 5.5**, 12 November, default effort, six readers (one per paper) who never saw Fable's marks:
  `rebuild/analysis/ai_eval/<paper>/sonnet_eval.json` (on slides 29 and 30 of the deck).
* **Claude Opus**, 12 November, default effort, six readers (one per paper) who saw neither Fable's nor Sonnet's marks:
  Opus 5.5 on papers A, D, E and F; Opus 5 on B and C, where a safety classifier stopped Opus 5.5 while it read the paper
  and Claude Code switched the reader to Opus 5. Marks: `AI_EVALUATION_SUMMARY.md`, the hidden tab
  `AI evaluation Opus`, and `rebuild/analysis/ai_eval/<paper>/opus_eval.json`.
* **Gemini 4 Hydrogen**, 12 November, extra-high (XHigh) effort, six readers (one per paper) blind to the prior AI
  evaluations, verified per statement by an independent AI agent against the paper, citations, walk JSON and uploaded
  values: `AI_EVALUATION_SUMMARY.md`, the hidden tab `AI evaluation Gemini 4 Hydrogen`,
  `rebuild/analysis/gemini_eval/<paper>.json`, and `rebuild/analysis/ai_eval/<paper>/gemini_hydrogen_eval.json`.
* **Gemini 4 Argon**, 12 November, default effort, four blind readers (sharded across the six papers) who never saw
  Fable's or any other reader's marks: the end of `AI_EVALUATION_SUMMARY.md`, the hidden tab
  `AI evaluation Gemini 4 Argon`, and `rebuild/analysis/ai_eval/<paper>/gemini_argon_eval.json`.

Their marks, totals and reasons are in those files and on slides 29 and 30 of the deck, and are kept off this page,
so that you, or another reader, can mark without seeing them by not opening those. They are opinions to compare with
yours, not an answer key, and no person has checked them.

## Building the slides again

`rebuild/` holds the scripts (Python, PyMuPDF) that draw the slides, the handout and the web page, and put the QR
codes on them:

```bash
cd rebuild
./rebuild.sh "<link of the marking sheet>" "<link of this repository>"
```

The scripts draw on top of page images of two earlier versions of the slides (`rebuild/docs/`). Those files are not
in this repository, so the build does not run from a fresh copy; the scripts are here as a record of how the slides
were made. After the workshop, `rebuild/scripts/10_ratings_report.py` takes the filled-in workbook and writes a page
that compares the room with the second reader, statement by statement.

The fonts in `rebuild/slides/assets/fonts/` are Open Sans and JetBrains Mono, both under the SIL Open Font License 1.1.

## Contact and thanks

Questions: <paintomicsai@gmail.com>. PaintOmics: <https://paintomics.org>, code at
<https://github.com/ConesaLab/PaintOmics>.

TELLME is an ELIXIR project led by I²SysBio (ELIXIR-ES). We thank ELIXIR for supporting TELLME.

## The papers

* **Hernandez 2017.** Hernandez MX, Jiang S, Cole TA, Chu SH, Fonseca MI, Fang MJ, Hohsfield LA, Torres MD, Green KN, Wetsel RA, Mortazavi A, Tenner AJ. Prevention of C5aR1 signaling delays microglial inflammatory polarization, favors clearance pathways and suppresses cognitive loss. Mol Neurodegener. 2017;12(1):66. doi:[10.1186/s13024-017-0210-z](https://doi.org/10.1186/s13024-017-0210-z)
* **Wang 2019.** Wang Y, Tatham MH, Schmidt-Heck W, Swann C, Singh-Dolt K, Meseguer-Ripolles J, Lucendo-Villarin B, Kunath T, Rudd TR, Smith AJH, Hengstler JG, Godoy P, Hay RT, Hay DC. Multiomics Analyses of HNF4alpha Protein Domain Function during Human Pluripotent Stem Cell Differentiation. iScience. 2019;16:206-217. doi:[10.1016/j.isci.2019.05.028](https://doi.org/10.1016/j.isci.2019.05.028)
* **Jiménez-Munguía 2021.** Jiménez-Munguía I, Tomečková Z, Mochnáčová E, Bhide K, Majerová P, Bhide M. Transcriptomic analysis of human brain microvascular endothelial cells exposed to laminin binding protein (adhesion lipoprotein) and Streptococcus pneumoniae. Sci Rep 11:7970 (2021). doi:[10.1038/s41598-021-87021-4](https://doi.org/10.1038/s41598-021-87021-4)
* **Balzano-Nogueira 2021.** Balzano-Nogueira L, Ramirez R, Zamkovaya T, et al. Integrative analyses of TEDDY Omics data reveal lipid metabolism abnormalities, increased intracellular ROS and heightened inflammation prior to autoimmunity for type 1 diabetes. Genome Biol 22:39 (2021). doi:[10.1186/s13059-021-02262-w](https://doi.org/10.1186/s13059-021-02262-w)
* **Rubio 2021.** Rubio T, Felipo V, Tarazona S, et al. Multi-omic analysis unveils biological pathways in peripheral immune system associated to minimal hepatic encephalopathy appearance in cirrhotic patients. Sci Rep 11:1907 (2021). doi:[10.1038/s41598-020-80941-7](https://doi.org/10.1038/s41598-020-80941-7)
* **Fàbregas 2018.** Fabregas N, Lozano-Elena F, Blasco-Escamez D, et al. Overexpression of the vascular brassinosteroid receptor BRL3 confers drought resistance without penalizing plant growth. Nat Commun. 2018;9:4680. doi:[10.1038/s41467-018-06861-3](https://doi.org/10.1038/s41467-018-06861-3)
