# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['minicons', 'minicons.bin']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.3.5,<2.0.0',
 'torch>=1.8.0,<2.0.0',
 'transformers>=4.4.1,<5.0.0',
 'urllib3>=1.26.7,<2.0.0']

entry_points = \
{'console_scripts': ['minicons = minicons.bin.score_cli:process']}

setup_kwargs = {
    'name': 'minicons',
    'version': '0.2.17',
    'description': 'A package of useful functions to analyze transformer based language models.',
    'long_description': '# minicons: Enabling Flexible Behavioral and Representational Analyses of Transformer Language Models\n\n[![Downloads](https://static.pepy.tech/personalized-badge/minicons?period=total&units=international_system&left_color=black&right_color=brightgreen&left_text=Downloads)](https://pepy.tech/project/minicons)\n\nThis repo is a wrapper around the `transformers` [library](https://huggingface.co/transformers) from Hugging Face :hugs:\n\n<!-- TODO: Description-->\n\n\n\n## Installation\n\nInstall from Pypi using:\n\n```pip install minicons```\n\n## Supported Functionality\n\n- Extract word representations from Contextualized Word Embeddings\n- Score sequences using language model scoring techniques, including masked language models following [Salazar et al. (2020)](https://www.aclweb.org/anthology/2020.acl-main.240.pdf).\n\n\n## Examples\n\n1. Extract word representations from contextualized word embeddings:\n\n```py\nfrom minicons import cwe\n\nmodel = cwe.CWE(\'bert-base-uncased\')\n\ncontext_words = [("I went to the bank to withdraw money.", "bank"), \n                 ("i was at the bank of the river ganga!", "bank")]\n\nprint(model.extract_representation(context_words, layer = 12))\n\n\'\'\' \ntensor([[ 0.5399, -0.2461, -0.0968,  ..., -0.4670, -0.5312, -0.0549],\n        [-0.8258, -0.4308,  0.2744,  ..., -0.5987, -0.6984,  0.2087]],\n       grad_fn=<MeanBackward1>)\n\'\'\'\n\n# if model is seq2seq:\nmodel = cwe.EncDecCWE(\'t5-small\')\n\nprint(model.extract_representation(context_words))\n\n\'\'\'(last layer, by default)\ntensor([[-0.0895,  0.0758,  0.0753,  ...,  0.0130, -0.1093, -0.2354],\n        [-0.0695,  0.1142,  0.0803,  ...,  0.0807, -0.1139, -0.2888]])\n\'\'\'\n```\n\n2. Compute sentence acceptability measures (surprisals) using Word Prediction Models:\n\n```py\nfrom minicons import scorer\n\nmlm_model = scorer.MaskedLMScorer(\'bert-base-uncased\', \'cpu\')\nilm_model = scorer.IncrementalLMScorer(\'distilgpt2\', \'cpu\')\ns2s_model = scorer.Seq2SeqScorer(\'t5-base\', \'cpu\')\n\nstimuli = ["The keys to the cabinet are on the table.",\n           "The keys to the cabinet is on the table."]\n\n# use sequence_score with different reduction options: \n# Sequence Surprisal - lambda x: -x.sum(0).item()\n# Sequence Log-probability - lambda x: x.sum(0).item()\n# Sequence Surprisal, normalized by number of tokens - lambda x: -x.mean(0).item()\n# Sequence Log-probability, normalized by number of tokens - lambda x: x.mean(0).item()\n# and so on...\n\nprint(ilm_model.sequence_score(stimuli, reduction = lambda x: -x.sum(0).item()))\n\n\'\'\'\n[39.879737854003906, 42.75846481323242]\n\'\'\'\n\n# MLM scoring, inspired by Salazar et al., 2020\nprint(mlm_model.sequence_score(stimuli, reduction = lambda x: -x.sum(0).item()))\n\'\'\'\n[13.962685585021973, 23.415111541748047]\n\'\'\'\n\n# Seq2seq scoring\n## Blank source sequence, target sequence specified in `stimuli`\nprint(s2s_model.sequence_score(stimuli, source_format = \'blank\'))\n## Source sequence is the same as the target sequence in `stimuli`\nprint(s2s_model.sequence_score(stimuli, source_format = \'copy\'))\n\'\'\'\n[-7.910910129547119, -7.835635185241699]\n[-10.555519104003906, -9.532546997070312]\n\'\'\'\n```\n\n## A better version of MLM Scoring by Kauf and Ivanova\n\nThis version leverages a locally-autoregressive scoring strategy to avoid the overestimation of probabilities of tokens in multi-token words (e.g., "ostrich" -> "ostr" + "#ich"). In particular, tokens probabilities are estimated using the bidirectional context, excluding any future tokens that belong to the same word as the current target token.\n\nFor more details, refer to [Kauf and Ivanova, 2023](https://arxiv.org/abs/2305.10588)\n\n```py\nfrom scorer import MaskedLMScorer\nmlm_model = MaskedLMScorer(\'bert-base-uncased\', \'cpu\')\n\nstimuli = [\'The traveler lost the souvenir.\']\n\n# un-normalized sequence score\nprint(mlm_model.sequence_score(stimuli, reduction = lambda x: -x.sum(0).item(), PLL_metric=\'within_word_l2r\'))\n\'\'\'\n[32.77983617782593]\n\'\'\'\n\nprint(mlm_model.token_score(stimuli, PLL_metric=\'within_word_l2r\'))\n\'\'\'\n[[(\'the\', -0.07324600219726562), (\'traveler\', -9.668401718139648), (\'lost\', -6.955361366271973),\n(\'the\', -1.1923179626464844), (\'so\', -7.776356220245361), (\'##uven\', -6.989711761474609),\n(\'##ir\', -0.037807464599609375), (\'.\', -0.08663368225097656)]]\n\'\'\'\n```\n\n## Tutorials\n\n- [Introduction to using LM-scoring methods using minicons](https://kanishka.xyz/post/minicons-running-large-scale-behavioral-analyses-on-transformer-lms/)\n- [Computing sentence and token surprisals using minicons](examples/surprisals.md)\n- [Extracting word/phrase representations using minicons](examples/word_representations.md)\n\n## Recent Updates\n- **November 6, 2021:** MLM scoring has been fixed! You can now use `model.token_score()` and `model.sequence_score()` with `MaskedLMScorers` as well!\n- **June 4, 2022:** Added support for Seq2seq models. Thanks to [Aaron Mueller](https://github.com/aaronmueller) 🥳\n\n## Citation\n\nIf you use `minicons`, please cite the following paper:\n\n```tex\n@article{misra2022minicons,\n    title={minicons: Enabling Flexible Behavioral and Representational Analyses of Transformer Language Models},\n    author={Kanishka Misra},\n    journal={arXiv preprint arXiv:2203.13112},\n    year={2022}\n}\n```\n\nIf you use Kauf and Ivanova\'s PLL scoring technique, please additionally also cite the following paper:\n\n```tex\n@inproceedings{kauf2023better,\n  title={A Better Way to Do Masked Language Model Scoring},\n  author={Kauf, Carina and Ivanova, Anna},\n  booktitle={Proceedings of the 61st Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)},\n  year={2023}\n}\n```\n',
    'author': 'Kanishka Misra',
    'author_email': 'kmisra@purdue.edu',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/kanishkamisra/minicons',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.1,<4',
}


setup(**setup_kwargs)
