
---
language: 
- ind
pretty_name: Smsa
task_categories: 
- sentiment-analysis
tags: 
- sentiment-analysis
---

SmSA is a sentence-level sentiment analysis dataset (Purwarianti and Crisdayanti, 2019) is a collection of comments and reviews
in Indonesian obtained from multiple online platforms. The text was crawled and then annotated by several Indonesian linguists
to construct this dataset. There are three possible sentiments on the SmSA dataset: positive, negative, and neutral


## Languages

ind

## Supported Tasks

Sentiment Analysis

## Dataset Usage
### Using `datasets` library
```
from datasets import load_dataset
dset = datasets.load_dataset("SEACrowd/smsa", trust_remote_code=True)
```
### Using `seacrowd` library
```import seacrowd as sc
# Load the dataset using the default config
dset = sc.load_dataset("smsa", schema="seacrowd")
# Check all available subsets (config names) of the dataset
print(sc.available_config_names("smsa"))
# Load the dataset using a specific config
dset = sc.load_dataset_by_config_name(config_name="<config_name>")
```

More details on how to load the `seacrowd` library can be found [here](https://github.com/SEACrowd/seacrowd-datahub?tab=readme-ov-file#how-to-use).


## Dataset Homepage

[https://github.com/IndoNLP/indonlu](https://github.com/IndoNLP/indonlu)

## Dataset Version

Source: 1.0.0. SEACrowd: 2024.06.20.

## Dataset License

Creative Commons Attribution Share-Alike 4.0 International

## Citation

If you are using the **Smsa** dataloader in your work, please cite the following:
```
@INPROCEEDINGS{8904199,
    author={Purwarianti, Ayu and Crisdayanti, Ida Ayu Putu Ari},
    booktitle={2019 International Conference of Advanced Informatics: Concepts, Theory and Applications (ICAICTA)},
    title={Improving Bi-LSTM Performance for Indonesian Sentiment Analysis Using Paragraph Vector},
    year={2019},
    pages={1-5},
    doi={10.1109/ICAICTA.2019.8904199}
}

@inproceedings{wilie2020indonlu,
  title={IndoNLU: Benchmark and Resources for Evaluating Indonesian Natural Language Understanding},
  author={Wilie, Bryan and Vincentio, Karissa and Winata, Genta Indra and Cahyawijaya, Samuel and Li, Xiaohong and Lim, Zhi Yuan and Soleman, Sidik and Mahendra, Rahmad and Fung, Pascale and Bahar, Syafri and others},
  booktitle={Proceedings of the 1st Conference of the Asia-Pacific Chapter of the Association for Computational Linguistics and the 10th International Joint Conference on Natural Language Processing},
  pages={843--857},
  year={2020}
}


@article{lovenia2024seacrowd,
    title={SEACrowd: A Multilingual Multimodal Data Hub and Benchmark Suite for Southeast Asian Languages}, 
    author={Holy Lovenia and Rahmad Mahendra and Salsabil Maulana Akbar and Lester James V. Miranda and Jennifer Santoso and Elyanah Aco and Akhdan Fadhilah and Jonibek Mansurov and Joseph Marvin Imperial and Onno P. Kampman and Joel Ruben Antony Moniz and Muhammad Ravi Shulthan Habibi and Frederikus Hudi and Railey Montalan and Ryan Ignatius and Joanito Agili Lopo and William Nixon and Börje F. Karlsson and James Jaya and Ryandito Diandaru and Yuze Gao and Patrick Amadeus and Bin Wang and Jan Christian Blaise Cruz and Chenxi Whitehouse and Ivan Halim Parmonangan and Maria Khelli and Wenyu Zhang and Lucky Susanto and Reynard Adha Ryanda and Sonny Lazuardi Hermawan and Dan John Velasco and Muhammad Dehan Al Kautsar and Willy Fitra Hendria and Yasmin Moslem and Noah Flynn and Muhammad Farid Adilazuarda and Haochen Li and Johanes Lee and R. Damanhuri and Shuo Sun and Muhammad Reza Qorib and Amirbek Djanibekov and Wei Qi Leong and Quyet V. Do and Niklas Muennighoff and Tanrada Pansuwan and Ilham Firdausi Putra and Yan Xu and Ngee Chia Tai and Ayu Purwarianti and Sebastian Ruder and William Tjhi and Peerat Limkonchotiwat and Alham Fikri Aji and Sedrick Keh and Genta Indra Winata and Ruochen Zhang and Fajri Koto and Zheng-Xin Yong and Samuel Cahyawijaya},
    year={2024},
    eprint={2406.10118},
    journal={arXiv preprint arXiv: 2406.10118}
}

```