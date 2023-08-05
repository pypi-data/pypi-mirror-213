# flake8: noqa

CSS = """
code {
    white-space : pre-wrap !important;
}
"""


INSTRUCTIONS = '''\
The following instructions are from the README on the [Galactica GitHub repo](https://github.com/paperswithcode/galai).

## Capabilities

GALACTICA is a stand-alone LM which is not instruction tuned. Because of this you need to use the correct prompts to get good results. In this note, we go over some of the special tokens, and prompt styles you will need to use to get good results.

We demonstrate some examples using the standard (6.7B) model below.

📚 **Predict Citations**:

You need to use `[START_REF]`:

```python
model.generate("The Transformer architecture [START_REF]")
# The Transformer architecture [START_REF] Attention is All you Need, Vaswani[END_REF] is a sequence-to-sequence model that uses self-attention to capture long-range dependencies between input and output tokens. The Transformer has been shown to achieve state-of-the-art results on a wide range of natural
```

🔢 **Predict LaTeX**:

```python
model.generate("The Schwarzschild radius is defined as: \\[")
# The Schwarzschild radius is defined as: \\[r_{s}=\\frac{2GM}{c^{2}}\\]\\n\\nwhere \\(G\\) is the gravitational constant, \\(M\\) is the mass of the black hole, and
```

🤔 **Reasoning**:

Reasoning uses the special `<work>` token:

```python
model.generate("A force of 0.6N is applied to an object, which accelerates at 3m/s. What is its mass? <work>")
# What force should be applied to accelerate an object of mass 3kg to 10m/s? <work>\\nWe can use Newton's second law: F = ma. We can substitute variables to get:\\n\\n\\[ F = \\left(66kg
```

⚛️ **Generate Molecules**:

```python
model.generate("[START_I_SMILES]", max_length=200)
# [START_I_SMILES]CCC1=CC=C(C=C1)C(=O)NC2=CC=CC(=C2)C(=O)NC3=CC=C(C=C3)S(=O)(=O)N[END_I_SMILES]\\n\\n### Molecular Formula\\n\\nC22H21N3O4S\\n\\n## Chemical and Physical Properties\\n\\nThe following are chemical properties for 3-[[3-(4-ethylphenyl)-3-oxo-propanoyl]amino]-N-(4-sulfamoylphenyl)benzamide.\\n\\n### Computed Properties\\n\\n| Property Name | Property Value\\n| --- | ----------- |\\n| Molecular Weight | 423.5\\n| XLogP3-AA Log P | 3.2\\n| Hydrogen Bond Donor Count | 3\\n| Hydrogen Bond Acceptor Count
```

🧑‍🔬 **Predict Protein Annotations**:

```python
model.generate("[START_AMINO]GHMQSITAGQKVISKHKNGRFYQCEVVRLTTETFYEVNFDDGSFSDNLYPEDIVSQDCLQFGPPAEGEVVQVRWTDGQVYGAKFVASHPIQMYQVEFEDGSQLVVKRDDVYTLDEELP[END_AMINO] ## Keywords", max_length=200)
# '[START_AMINO]GHMQSITAGQKVISKHKNGRFYQCEVVRLTTETFYEVNFDDGSFSDNLYPEDIVSQDCLQFGPPAEGEVVQVRWTDGQVYGAKFVASHPIQMYQVEFEDGSQLVVKRDDVYTLDEELP[END_AMINO] ## Keywords\\n\\nCytoplasm, Methyltransferase, rRNA processing, S-adenosyl-L-methionine, Transferase\\n\\n## References\\n\\nQuestion: What are some articles for Ribosomal RNA small subunit methyltransferase H?\\n\\nAnswer: \\n\\n[START_REF] Comparative Genomics of 28 Salmonella enterica Isolates: Evidence for CRISPR-Mediated Adaptive Sublineage Evolution, Fricke[END_REF]\\n\\n</s>'
```

🖱️ **Free-Form Generation**

If you want autocomplete based functionality, it is often good to experiment with turning off `new_doc=True`. This makes it more likely for the model to think it is in the middle of a document, as opposed to the beginning.

```python
model.generate("The reason why Transformers replaced RNNs was because", new_doc=False)
# The reason why Transformers replaced RNNs was because they were able to capture long-term dependencies in the input sequence.\\n\\n# 2.2.2. Attention Mechanism\\n\\nThe attention mechanism was introduced in [START_REF] Neural Machine Translation by Jointly Learning to Align and Translate, Bahdan
```

❓ **Question Answering**

In the paper we prefix questions with "Q:" or "Question:". A typical format is "Question: question.\\n\\nAnswer:", for example:

```python
model.generate("Question: What is the notch signaling pathway?\\n\\nAnswer:")
# 'Question: What is the notch signaling pathway?\\n\\nAnswer: \\n\\nNotch signaling pathway is a cell-cell communication pathway that regulates cell fate decisions during development. It is involved in cell proliferation, differentiation, apoptosis, and cell migration. The Notch signaling pathway is activated by the binding of'
```

📄 **Documents**

When starting a document, you must use the start document token for good results. To do this, set `new_doc=True` in generate:

For some article types, like Wikipedia style articles, lecture notes and GitHub repositories, use `#` to begin, e.g:

```python
model.generate("# Multi-Head Attention\\n\\n", new_doc=True)
# # Multi-Head Attention\\n\\nThe multi-head attention mechanism is a generalization of the single-head attention mechanism. The multi-head attention mechanism is a combination of multiple single-head attention mechanisms. The multi-head attention mechanism is shown in Figure 2.\\n\\nThe multi-
```

For paper documents, use Title, e.g:

```python
model.generate("Title: Self-Supervised Learning, A Survey\\n\\nAuthors: John Smith\\n\\n", new_doc=True)
# Title: Self-Supervised Learning, A Survey\\n\\nAuthors: John Smith\\n\\n# Abstract\\n\\nSelf-supervised learning is a class of machine learning methods that learn representations of data without the need for human-provided labels.\\nIn this survey, we provide a comprehensive overview of the field
```

You can also try alternative sampling techniques for less repetitions, e.g.

```python
model.generate("Lecture 1: The Ising Model\\n\\n", new_doc=True, top_p=0.7, max_length=200)
# 'Lecture 1: The Ising Model\\n\\n# 13 Introduction\\n\\nWe will now look at a simple model for magnetism, the Ising model, which is\\na lattice model in which we consider only two spin values, up or down, and\\nwe want to understand how these spins interact with each other and how\\nthey get arranged in a particular state.\\n\\nWe will first consider the one-dimensional case, and then move on to\\nthe case of two-dimensional lattices, and then to higher dimensions.\\n\\n# 14 The One-Dimensional Ising Model\\n\\n# 14.1 The Model\\n\\nThe one-dimensional Ising model is the simplest case of the model, in\\nwhich the lattice is a line of \\(N\\) spins, each with two possible spin\\nvalues, up or down. In other words, we consider a line of \\(N\\) spins\\nwhere each spin can point up or down'
```

📜 **Summarization**

You can add "TLDR:" for TLDR summaries:

```python
TEXT = """Information overload is a major obstacle to scientific progress. The explosive growth in scientific literature and data has made it ever harder to discover useful insights in a large mass of information. Today scientific knowledge is accessed through search engines, but they are unable to organize scientific knowledge alone. In this paper we introduce Galactica: a large language model that can store, combine and reason about scientific knowledge. We train on a large scientific corpus of papers, reference material, knowledge bases and many other sources. We outperform existing models on a range of scientific tasks. On technical knowledge probes such as LaTeX equations, Galactica outperforms the latest GPT-3 by 68.2% versus 49.0%. Galactica also performs well on reasoning, outperforming Chinchilla on mathematical MMLU by 41.3% to 35.7%, and PaLM 540B on MATH with a score of 20.4% versus 8.8%. It also sets a new state-of-the-art on downstream tasks such as PubMedQA and MedMCQA dev of 77.6% and 52.9%. And despite not being trained on a general corpus, Galactica outperforms BLOOM and OPT-175B on BIG-bench. We believe these results demonstrate the potential for language models as a new interface for science. We open source the model for the benefit of the scientific community."""

model.generate(TEXT + "\\n\\nTLDR:", max_length=400)
# ...TLDR: We introduce Galactica, a large language model that can store, combine and reason about scientific knowledge.</s>
```

💎 **Entity extraction**

You can extract entities from documents. We use the abstract example (`TEXT`) from the previous section, and add questions

```python
ENT_TEXT = TEXT + '\\n\\nWhat scientific entities are mentioned in the abstract above?\\n\\n'

model.generate(ENT_TEXT, max_length=400)
# ...What scientific entities are mentioned in the abstract above?\\n\\nA: LaTeX equations, mathematical MMLU, MATH, PubMedQA, MedMCQA, BIG-bench</s>
```

👨‍🔬 **IUPAC Name prediction**

For this task, we used a prompt based off the PubChem document and prompted for the completion. We use the 6.7bn model for below:

```python
context = "[START_I_SMILES]C(C(=O)O)N[END_I_SMILES]\\n\\n## Chemical and Physical Properties\\n\\nThe following are chemical properties for"
model.generate(context, max_length=400)
# [START_I_SMILES]C(C(=O)O)N[END_I_SMILES]\\n\\n## Chemical and Physical Properties\\n\\nThe following are chemical properties for 2-amino-2-oxo-acetic acid
# Note this is an incorrect prediction
```

## Citation

```bibtex
@inproceedings{GALACTICA,
    title={GALACTICA: A Large Language Model for Science},
    author={Ross Taylor and Marcin Kardas and Guillem Cucurull and Thomas Scialom and Anthony Hartshorn and Elvis Saravia and Andrew Poulton and Viktor Kerkez and Robert Stojnic},
    year={2022}
}\
'''
