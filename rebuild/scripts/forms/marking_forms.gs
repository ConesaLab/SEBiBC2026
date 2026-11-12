// Six marking forms for the SEBiBC 2026 practice, one per paper, linked to one spreadsheet.
// Run buildMarkingForms once. Uses the Forms service only. The statements below were copied from
// statement_marks.xlsx by a program (rebuild/scripts/forms/make_forms_script.py is not kept; see todo.md).

var DEST_ID = '1lWWhE69mVOg9wBy3s2t2Y1FyuasAMdQSHDXJCldjmk4';
var MARKS = ['Makes sense', 'Does not make sense', 'Especially good', "Can't judge"];
var PAPERS = [
 {
  "letter": "A",
  "name": "Hernandez 2017",
  "head": "A · Hernandez 2017, Mol Neurodegener. Does deleting the C5a receptor change microglia in an Alzheimer's model?",
  "doi": "https://doi.org/10.1186/s13024-017-0210-z",
  "job": "https://paintomics.org/?jobID=7NHQTK7rWz",
  "rows": [
   [
    "S1",
    "Ccl6 is induced by Arctic APP in microglia (Arctic_vs_WT +1.32 at 5mo, +1.19 at 7mo, +0.90 at 10mo) and this induction is not reversed by C5aR1 knockout (ArcticC5aR1KO_vs_Arctic +0.08 to +0.42)."
   ],
   [
    "S2",
    "Cxcl2 is induced by Arctic APP with age (Arctic_vs_WT +0.21 at 2mo to +1.20 at 7mo) and is strongly reversed by C5aR1 knockout at every age (ArcticC5aR1KO_vs_Arctic −0.96 to −0.66; C5aR1KO_vs_WT −0.95 at 2mo), identifying it as a C5aR1-dependent pro-inflammatory chemokine."
   ],
   [
    "S3",
    "Vegfa is induced late by Arctic APP (Arctic_vs_WT +0.57 at 10mo) and strongly suppressed by C5aR1 knockout at every age (ArcticC5aR1KO_vs_Arctic −1.43 to −0.83; C5aR1KO_vs_WT −2.06 at 2mo), a C5aR1-dependent angiogenic factor."
   ],
   [
    "S4",
    "Axl shows an early Arctic dip (Arctic_vs_WT −1.06 at 2mo) followed by strong induction at 5–7mo (+2.06, +1.96) that C5aR1 knockout does not block (ArcticC5aR1KO_vs_Arctic −0.14, −0.16 at 5–7mo), so C5aR1 loss normalises the early phase but not the mid-life DAM induction."
   ],
   [
    "S5",
    "Hck shows a late Arctic dip (Arctic_vs_WT −0.36 at 10mo) and mild C5aR1KO-up at 2mo (ArcticC5aR1KO_vs_Arctic +0.29), a mild modulation of a microglial Src-family kinase."
   ],
   [
    "S6",
    "Stat5a is suppressed by C5aR1 knockout (ArcticC5aR1KO_vs_Arctic −1.09 at 2mo, −0.96 at 7mo; C5aR1KO_vs_WT −1.50 at 2mo), a C5aR1-dependent STAT5 transcription factor."
   ],
   [
    "S7",
    "Cx3cr1 declines with age under Arctic APP (Arctic_vs_WT −0.06 at 2mo to −0.31 at 7mo) and is partially restored by C5aR1 knockout (C5aR1KO_vs_WT +0.31 at 2mo, +0.29 at 10mo)."
   ],
   [
    "S8",
    "Tlr2 and Cd14 are induced by the Arctic transgene in a mid-late pattern, and both encode components of the microglial fibrillar-Aβ receptor complex that initiates phagocytosis."
   ]
  ]
 },
 {
  "letter": "B",
  "name": "Wang 2019",
  "head": "B · Wang 2019, iScience. What does HNF4α need to make hepatocytes? Two edited mutants",
  "doi": "https://doi.org/10.1016/j.isci.2019.05.028",
  "job": "https://paintomics.org/?jobID=Y6n7275a0Z",
  "rows": [
   [
    "S1",
    "In DBDmut_vs_WT, the HNF1A target MTTP collapses at both transcript and protein level (Gene expression −6.46, Proteomics −8.50), while SUMOmut_vs_WT is near zero (+0.31/−0.43); HNF1A's own transcript is not relevant (unchanged, −0.39/−0.10)."
   ],
   [
    "S2",
    "In DBDmut_vs_WT, APOB falls at transcript and protein level (−5.28/−7.09) while SUMOmut is near zero (+0.67/−0.33); the core VLDL scaffold protein collapses on the DBD axis only."
   ],
   [
    "S3",
    "CDH1 is down in both axes at both mRNA and protein level, and HNF4A positively regulates E-cadherin expression."
   ],
   [
    "S4",
    "ITGB5 falls at the protein level only, and PRKCE (upstream of integrin signalling) drops specifically in the DBDmut axis."
   ],
   [
    "S5",
    "DAB2 is lost post-transcriptionally in the DBDmut axis, and DAB2 is a cargo-selective clathrin endocytic adaptor for LDL-receptor family members."
   ],
   [
    "S6",
    "The ER quality-control module (PRKCSH, GANAB, CALR) is coherently down at the protein level, and these proteins form the calnexin/calreticulin cycle for N-glycoprotein folding."
   ],
   [
    "S7",
    "MTTP is the rate-limiting lipid-transfer protein of apoB-containing lipoprotein assembly: it transfers neutral lipids to nascent apoB, and loss of MTTP activity abolishes apoB secretion and causes intracellular lipid accumulation in human iPSC-derived hepatocytes."
   ],
   [
    "S8",
    "HNF1A itself is not differentially expressed in either axis (Gene expression DBDmut_vs_WT −0.39, SUMOmut_vs_WT −0.10; not relevant), yet its direct transcriptional targets APOA4, APOA1, APOB and MTTP are all strongly down in DBDmut_vs_WT, indicating a DBD-specific loss of HNF1A transactivation rather than a change in HNF1A abundance."
   ]
  ]
 },
 {
  "letter": "C",
  "name": "Jiménez-Munguía 2021",
  "head": "C · Jiménez-Munguía 2021, Sci Rep. How do brain endothelial cells respond to pneumococcus and to its adhesin alone?",
  "doi": "https://doi.org/10.1038/s41598-021-87021-4",
  "job": "https://paintomics.org/?jobID=2Dh754YEIO",
  "rows": [
   [
    "S1",
    "IL6 is symmetrically induced by both stimuli, and the IL-17 signaling pathway edge (e1) places this induction in the shared inflammatory response of the two arms."
   ],
   [
    "S2",
    "TNFSF13B is induced only on the Lbp axis, and the NF-kappa B signaling pathway edges (e3, e4) place this Lbp-specific signal in the non-canonical NF-κB arm."
   ],
   [
    "S3",
    "GBP5 is the strongest GBP-family responder, induced on both axes with the Lbp axis higher, and the GBP-mediated host defense edges (e7, e8) ground this in the GBP module."
   ],
   [
    "S4",
    "The GBP2-to-CASP4 edge (e10) connects the GBP host-defence module to the non-canonical inflammasome, whose effector IL1B is induced only on the Spneumoniae axis (e11)."
   ],
   [
    "S5",
    "IL1B is induced only on the Spneumoniae axis, and this axis-specific induction sits inside a broadly NF-κB-driven cytokine response shared by both treatments."
   ],
   [
    "S6",
    "TNFSF13B (BAFF) is the Lbp-specific arm of the response: its mRNA is essentially flat under live pneumococcus (+0.05) but strongly induced by recombinant Lbp (+3.21), and it feeds the non-canonical NF-κB factors NFKB2 (+1.66 Lbp vs +1.32 Spn) and RELB (+2.21 Lbp vs +1.38 Spn), which are induced in both treatments but more strongly by Lbp."
   ],
   [
    "S7",
    "IL6 is the shared inflammatory hub of the perturbation: its mRNA rises identically in both treatments (+2.47 under both Spneumoniae_vs_control and Lbp_vs_control), consistent with IL6 being a canonical NF-κB target gene whose induction is common to both stimuli."
   ],
   [
    "S8",
    "IFNB1 is the pneumococcus-specific branch: its mRNA rises only under live S. pneumoniae (+1.60) and not under Lbp (+0.00), so the type I interferon response is specific to the live-bacteria stimulus."
   ],
   [
    "S9",
    "IL15RA is induced on both axes (+0.89 Spn, +1.18 Lbp), and its expression in cerebral microvascular endothelium is consistent with the established role of IL15Rα splice variants in mediating IL-15 neuroinflammatory signaling across the blood-brain barrier."
   ],
   [
    "S10",
    "The co-induction of SERPING1 (C1 inhibitor) with the C1 complex genes represents the pathway's own brake being turned on together with the classical complement cascade."
   ],
   [
    "S11",
    "NFKB2 is induced in both arms, and its induction together with the NF-kB-driven inflammatory genes is consistent with noncanonical NF-kB signalling amplifying the canonical RelA-driven response."
   ],
   [
    "S12",
    "The stronger induction of the complement and inflammatory genes under recombinant pneumococcal Lbp than under whole pneumococci suggests the Lbp stimulus is a sufficient trigger of the classical complement and NF-kB programmes in hBMEC."
   ],
   [
    "S13",
    "CEBPB is modestly induced in both arms (+0.47/+1.10) and sits upstream of the induced chemokines CXCL1, CXCL8 and CXCL6; C/EBPbeta is a transcription factor that drives the induction of inflammatory cytokines and chemokines in activated macrophages."
   ],
   [
    "S14",
    "IL6 is equally and strongly induced in both arms (+2.47/+2.47), while IL1B is induced only by live pneumococcus (+1.42 vs −0.20) and IL1A is induced in both (+2.60/+1.49); the pneumococcus-specific IL1B induction is consistent with the known activation of the NLRP3 inflammasome and IL-1β processing by the pneumococcal toxin pneumolysin."
   ],
   [
    "S15",
    "The Lbp-driven IFIT/CXCL10/CXCL11 response is mediated by the ISGF3 transcription factor complex containing IRF9, whose own transcript is not induced."
   ],
   [
    "S16",
    "The Lbp-induced CXCL10/CXCL11 chemokine pair recruits CXCR3-expressing lymphocytes, linking the pneumococcal Lbp stimulus to T-cell recruitment across the infected endothelium."
   ]
  ]
 },
 {
  "letter": "D",
  "name": "Balzano-Nogueira 2021",
  "head": "D · Balzano-Nogueira 2021, Genome Biol. What changes in blood in the year before islet autoimmunity?",
  "doi": "https://doi.org/10.1186/s13059-021-02262-w",
  "job": "https://paintomics.org/?jobID=560S3O473C",
  "rows": [
   [
    "S1",
    "Pluripotency transcription factors including OCT4, SOX2 and NANOG are expressed in human peripheral blood leukocytes, so the observed blood transcript changes of SALL1/SALL4/SOX2/NANOG can reflect a circulating cell population rather than an artifact."
   ],
   [
    "S2",
    "ACOT4 is the human peroxisomal acyl-CoA thioesterase that hydrolyzes medium- to long-chain acyl-CoAs, so its sustained downregulation is consistent with reduced thioester hydrolysis and a rise in free fatty acids."
   ],
   [
    "S3",
    "ACOT2 is a mitochondrial acyl-CoA thioesterase that hydrolyzes long-chain acyl-CoAs and accounts for about half of the mitochondrial thioesterase activity on C16:0-CoA, linking its 9mo expression bump to the fatty-acid rise."
   ],
   [
    "S4",
    "The relevant HIST1H2BI signal (mild positive, peak +0.05 at 9mo) sits on the KEGG Alcoholism histone H2B hub shared by HDAC10, HDAC11, HDAC8 and H2BC4, while HDAC11 and HDAC8 themselves are not relevant (baseline-positive +0.17 at 12mo and baseline-negative −0.13 at 12mo, respectively)."
   ],
   [
    "S5",
    "HDAC11 is not relevant (baseline-positive +0.17 at 12mo decaying to ~0), yet HDAC11 is a negative regulator of IL-10 in antigen-presenting cells, so its direction matters for immune tolerance."
   ],
   [
    "S6",
    "HDAC8 is not relevant (baseline-negative −0.13 at 12mo, ~0 at SC), and HDAC8 promotes innate antiviral immunity by deacetylating RIG-I, so its direction matters for the interferon axis."
   ],
   [
    "S7",
    "APOC3 is relevant and rises from −5.4e-03 at 12mo to +0.05 at 3mo before SC, peaking just before seroconversion; APOC3 is a regulator of triglyceride metabolism whose elevation is a risk factor in type 1 diabetes."
   ],
   [
    "S8",
    "APOA1 is relevant and persistently down (from −0.06 at 12mo to −0.02 at SC); LCAT is relevant with a transient 9mo trough (−0.15); phosphatidylcholine is relevant and troughs at 9mo (−0.08) and 3mo (−0.09); PLB1 is not relevant (baseline-negative −0.20 at 12mo)."
   ],
   [
    "S9",
    "BTD mRNA is flat through 12mo to 3mo before seroconversion and rises sharply at 0mo_at_SC (+0.14), an effect appearing at the time of seroconversion rather than at baseline, while HLCS (not relevant) stays flat/negative."
   ],
   [
    "S10",
    "KARS1 mRNA is positive at 12mo (+0.09), dips at 9mo (−0.03), then rises again at 3mo (+0.10) and stays up at 0mo (+0.06), a sustained late positive signal; L-Lysine itself returns to baseline at 0mo."
   ],
   [
    "S11",
    "C1QB and C1QC mRNA rise from negative early values toward positive endpoints at 0mo_at_SC (+0.11 and +0.06), a rising trajectory toward seroconversion, whereas C1QA is consistently positive from baseline and C1R (relevant) is flat/negative."
   ],
   [
    "S12",
    "GALR3 is constitutively up in cases across the whole window while its ligand GAL dips below baseline at 6 months before seroconversion; galanin signalling through GALR3 is pro-inflammatory in immune settings, so the sustained receptor upregulation with a transient ligand trough points to a tonic galanin/GALR3 tone in the pre-seroconversion period."
   ],
   [
    "S13",
    "CARD6 is a CARD-domain adaptor that binds RIPK2 (Cardiak/RICK) and NOD1 and selectively suppresses NF-κB activation by these proteins, so the early rise in CARD6 expression (12mo +0.11, 9mo +0.16) points to modulation of NOD/RIPK2-dependent innate immune signalling in the pre-SC window."
   ],
   [
    "S14",
    "APOC2 is the obligate cofactor that activates lipoprotein lipase for triglyceride hydrolysis, so the transient 6mo dip in APOC2 (APC2 row, −0.08) indicates a mid-window reduction in LPL-mediated triglyceride clearance in plasma, opposite in timing to the CREB3L3 peak."
   ]
  ]
 },
 {
  "letter": "E",
  "name": "Rubio 2021",
  "head": "E · Rubio 2021, Sci Rep. Minimal hepatic encephalopathy in cirrhosis: what changes in blood?",
  "doi": "https://doi.org/10.1038/s41598-020-80941-7",
  "job": "https://paintomics.org/?jobID=3oP1p37B25",
  "rows": [
   [
    "S1",
    "The IL4 transcript is induced in MHE while its serum cytokine stays flat, and IL4 is linked to CD36, whose up-regulation in IL-4-stimulated macrophages is a known PPARγ-dependent response."
   ],
   [
    "S2",
    "The IL6 serum cytokine is strongly up in MHE while the IL6 transcript is flat, and elevated serum IL-6 is a known marker of hepatic encephalopathy risk in cirrhosis."
   ],
   [
    "S3",
    "The IL4 transcript is up in MHE while its serum cytokine is flat, and AhR and IL-4 cooperate in human macrophages, linking the induced AHR arm to the IL4 signal."
   ],
   [
    "S4",
    "Serum IL6 is up in MHE while the IL6 transcript is flat, and this protein-dominant signal matches published data that serum IL-6 is elevated in MHE patients."
   ],
   [
    "S5",
    "The IL4 transcript is up in MHE while its serum protein is flat, and the TNF transcript is down while its serum protein trends up, showing transcript-protein discordance per cytokine."
   ],
   [
    "S6",
    "PSME1 is down in MHE while IFNG is up, and PSME1 encodes the PA28 proteasome activator subunit whose induction is classically IFN-γ-driven."
   ],
   [
    "S7",
    "The HOXA9–MEIS1–FLT3 chain (e39–e41) is a known transcriptional axis in which MEIS1 induces expression of FLT3; in the MHE-vs-noMHE comparison of blood cells from cirrhosis patients, HOXA9 is up (+0.53) while MEIS1 is down (−0.62), and FLT3 is not relevant (+0.34)."
   ],
   [
    "S8",
    "PDGFRB is up (noMHE +0.76, relevant) in the MHE-vs-noMHE comparison, the strongest of EREG's relevant receptor-tyrosine-kinase neighbours, in the same direction as the EGFR ligands EREG and AREG; PDGFRβ signalling is a well-established driver of hepatic stellate cell activation in liver fibrosis."
   ],
   [
    "S9",
    "The post-squalene cholesterol-synthesis enzymes around DHCR24 respond divergently in MHE: DHCR24 is down (−0.72, relevant) and SC5D is up (+0.60, relevant), while EBP, DHCR7 and LIPA are not relevant; DHCR24 catalyses the terminal desmosterol-to-cholesterol step of cholesterol biosynthesis."
   ],
   [
    "S10",
    "APOB, the core protein of VLDL and chylomicrons, is down (noMHE −0.97, relevant) in MHE, the strongest relevant neighbour of LIPA; reduced hepatic ApoB lowers VLDL secretion, and APOB loss-of-function predisposes to steatotic liver disease and cirrhosis."
   ]
  ]
 },
 {
  "letter": "F",
  "name": "Fàbregas 2018",
  "head": "F · Fàbregas 2018, Nat Commun. Why do plants that overexpress the BRL3 receptor survive drought?",
  "doi": "https://doi.org/10.1038/s41467-018-06861-3",
  "job": "https://paintomics.org/?jobID=044DBhQFC7",
  "rows": [
   [
    "S1",
    "BRL3ox rewires the monolignol branch of phenylpropanoid metabolism: CAD9 is induced by BRL3ox already at baseline and its drought induction is amplified, whereas FAH1/CYP84A4 and 4CL5 are repressed by BRL3ox under drought while WT drought induces them, and CCR2 is repressed at baseline but its drought induction is amplified."
   ],
   [
    "S2",
    "The trehalose-sucrose-glucose loop is a signature of the BRL3ox drought response: alpha,alpha-trehalose is up in BRL3ox at baseline but its drought induction is lost, TRE1 (trehalase) is the hub of the neighbourhood, TPS7 is repressed by BRL3ox at baseline, and the sucrose-cleaving enzymes A/N-InvC and ATBETAFRUCT4 are repressed by BRL3ox under drought while SUS3 is induced."
   ],
   [
    "S3",
    "Glucose is a drought-driven metabolite essentially unaffected by BRL3ox, and HKL1, a hexokinase-like sugar sensor, is repressed by BRL3ox at baseline and under drought while drought induces it in both genotypes."
   ],
   [
    "S4",
    "BGLU24 is flipped by BRL3ox from baseline repression to hyper-induction under drought, and AT1G30870 is turned drought-repressed by BRL3ox while its baseline is mildly induced."
   ],
   [
    "S5",
    "BRL3ox represses the PYL/RCAR ABA receptors PYL4 and PYL5 at the watered baseline while inducing the clade-A PP2C HAI3, an ABA-signalling configuration that is already present before drought."
   ],
   [
    "S6",
    "The SnRK2 kinases SNRK2.7 and SNRK2.9 are mildly induced by BRL3ox at baseline while drought represses them in both genotypes, and the downstream bZIP transcription factor ABF2 is induced by both BRL3ox and drought."
   ],
   [
    "S7",
    "MAPKKK18 is repressed by BRL3ox at baseline but strongly drought-induced, especially in the BRL3ox background, yet the MAP2K MKK3 downstream of it is not relevant and flat."
   ],
   [
    "S8",
    "LOX3 shows the strongest drought-dependent reversal of the BRL3ox effect in the lipoxygenase module: repressed by BRL3ox at baseline but nearly neutral under drought, with drought induction far stronger in BRL3ox than WT."
   ],
   [
    "S9",
    "In BRL3ox roots, the trehalose axis is shifted toward accumulation: alpha,alpha-trehalose is elevated at baseline (+1.60 watered) while TRE1 is mildly suppressed (−0.15/−0.42, not relevant), and drought still induces trehalose in WT (+1.85) but less in BRL3ox (+0.60); TPS7 is BRL3ox-suppressed at baseline (−0.98) yet drought-induced in BRL3ox (+1.18)."
   ],
   [
    "S10",
    "SUS3 is the strongest drought-induced gene on the sucrose loop (+3.23 WT, +3.73 BRL3ox) and is BRL3ox-amplified under drought (+0.79); sucrose is BRL3ox-up at baseline (+1.45) and drought-induced in WT (+1.35) but less in BRL3ox (+0.44)."
   ],
   [
    "S11",
    "The jasmonate/oxylipin chain LOX5→LOX4→AOS→AOC1→OPR3→OPCL1 is coherently BRL3ox-dependent drought-induced: watered BRL3ox represses (LOX4 −1.93, AOC1 −3.46, OPR3 −1.75) and drought flips it (BRL3ox drought +2.37/+2.79/+2.01); AOC2 responds to drought but is not BRL3ox-amplified."
   ],
   [
    "S12",
    "TPS1 is mildly BRL3ox-up under drought (+0.28) and drought-induced in BRL3ox (+0.50) but nearly flat in WT (+0.10), with a slight BRL3ox suppression at baseline (−0.11; not relevant)."
   ],
   [
    "S13",
    "A/N-InvC is BRL3ox-down at baseline (−0.74) but drought-induced in BRL3ox (+0.79), while sucrose accumulates in BRL3ox (+1.45); BRL3ox shifts sucrose handling from cleavage toward synthesis/accumulation."
   ]
  ]
 }
];

function buildMarkingForms() {
  var out = PAPERS.map(function (p) {
    var f = FormApp.create('Paper ' + p.letter + ' · ' + p.name + ' · mark the AI\'s statements');
    f.setTitle('Paper ' + p.letter + ' · ' + p.name);
    f.setDescription(
      p.head + '\n\n' +
      'PaintOmics AI read the data of this paper and wrote ' + p.rows.length + ' numbered statements. Give each one a mark. ' +
      'No question is required: mark the ones you get to, then press Submit at the bottom, even if you did not finish.\n\n' +
      'Makes sense: consistent with the data and with what you know. You would accept it from a colleague.\n' +
      'Does not make sense: something in it is wrong or empty. One wrong part is enough.\n' +
      'Especially good: correct, and it adds something.\n' +
      'Can\'t judge: you cannot tell without more work. Better than a guess.\n\n' +
      'The evidence behind each statement is on the job page (AI Interpret, top right): ' + p.job + '\n' +
      'The paper: ' + p.doi);
    f.setCollectEmail(false);
    f.setAllowResponseEdits(true);
    f.setProgressBar(false);
    f.setShowLinkToRespondAgain(false);
    try { f.setRequireLogin(false); } catch (e) {}
    f.setConfirmationMessage('Thank you, your marks are in. If you want to change or add one, use "Edit your response" below.');
    p.rows.forEach(function (r) {
      f.addMultipleChoiceItem().setTitle(r[0] + ' · ' + r[1]).setChoiceValues(MARKS).setRequired(false);
    });
    f.setDestination(FormApp.DestinationType.SPREADSHEET, DEST_ID);
    f.setAcceptingResponses(true);
    try { f.setPublished(true); } catch (e) { Logger.log('setPublished not available: ' + e); }
    var url = f.getPublishedUrl(), short = url;
    try { short = f.shortenFormUrl(url); } catch (e) { Logger.log('shorten failed: ' + e); }
    Utilities.sleep(1500);
    return { letter: p.letter, n: p.rows.length, url: url, short: short, edit: f.getEditUrl() };
  });
  Logger.log('LINKS ' + JSON.stringify(out));
  return out;
}
