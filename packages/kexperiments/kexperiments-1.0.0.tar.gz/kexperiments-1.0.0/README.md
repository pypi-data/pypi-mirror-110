# kexperiments

## A Python package for utilizing experimentation methods in tests, sample size calculations, inference, and sampling.

This package implements helper functions primarily to aid in experimentation. A few of the different areas are:

1. Statistical Tests (1/2 tailed t-tests, one-way anova, two-way anova, etc.)
2. Sample Size Calculations (for the above tests)
3. Inference Methods (CausalImpact package)


## Installation

You will need to add this line to your requirements.txt file or inside your DockerFile in the analytics repo. You could also install this package locally as long as you have configured your KOHO github access to your local computer. 

```bash
pip install write_line_here 
```

## Requirements

- python{>=3.4}
- numpy
- scipy
- statsmodels
- pandas
- pycausalimpact

## Content

- [**1.0 Causal Inference**](https://github.com/kohofinancial/kexperiments/wiki/Causal-Inference)

   - [1.1 Causal Impact Summary/Plot](https://github.com/kohofinancial/kexperiments/wiki/Causal-Inference#kexperimentscausalcausal_impact)


- [**2.0 Sample Size Calculations**](https://github.com/kohofinancial/kexperiments/wiki/Sample-Size-Calculations)
   
   - [2.1 T-Test Sample Size (A/B Tests)](https://github.com/kohofinancial/kexperiments/wiki/Sample-Size-Calculations#kexperimentssample_sizesamplesize_ttest)
   - [2.2 One-Way ANOVA Sample Size (A/B/n Tests)](https://github.com/kohofinancial/kexperiments/wiki/Sample-Size-Calculations#kexperimentssample_sizesamplesize_oneway_anova)

- [**3.0 Statistical Tests**](https://github.com/kohofinancial/kexperiments/wiki/Statistical-Tests)
   - [3.1 T-Tests (A/B Tests)](https://github.com/kohofinancial/kexperiments/wiki/Statistical-Tests#kexperimentscalc_ttest)
   - [3.2 One-Way ANOVA (A/B/n Tests)](https://github.com/kohofinancial/kexperiments/wiki/Statistical-Tests#kexperimentscalc_one_way_anova)
   - [3.3 Two-Way ANOVA (2x2 Factorial)](https://github.com/kohofinancial/kexperiments/wiki/Statistical-Tests#kexperimentscalc_two_way_anova)

