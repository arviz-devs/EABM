---
title: 'Exploratory Analysis of Bayesian Models'
tags:
  - Python
  - Bayesian statistics
  - Bayesian modeling
authors:
  - name: Osvaldo A Martin
    orcid: 0000-0001-7419-8978
    corresponding: true
    affiliation: 1
  - name: Oriol Abril-Pla 
    orcid: 0000-0002-1847-9481
    affiliation: 2
affiliations:
 - name: Aalto University. Espoo, Finland
   index: 1
 - name: Independent Researcher, Spain
   index: 2
date: 30 May 2025
bibliography: paper.bib
---

# Summary

This paper introduces an educational resource designed to teach Exploratory Analysis of Bayesian Models. The material has been developed around the ArviZ library [@Kumar:2019] and grounded in probabilistic programming-agnostic principles. It covers key topics such as MCMC diagnostics, model criticism, and model comparison. The resource aims to make Bayesian methods more accessible. It is intended to complement typical courses in Bayesian modeling, support self-directed learning, and serve as a reference for practitioners. The material is hosted online using Quarto [@Quarto:2022].


# Statement of need

Bayesian statistics has emerged as a highly flexible and powerful technique, witnessing increased adoption in recent years, yet it remains a challenging topic to teach and learn. It demands a fundamental shift in mindset: students must move beyond frequentist habits and embrace probabilistic thinking, where uncertainty is expressed through distributions rather than point estimates. While methods like MCMC offer great flexibility, they introduce additional complexity through the need for careful convergence diagnostics and model checking. Moreover, the Bayesian modeling workflow emphasizes generative models and iterative refinement, which stands in contrast to the more rigid, procedural approaches common in traditional statistics. To help learners navigate these challenges, we propose an open educational resource that focuses on conceptual explanations with examples. By working with pre-fitted models or intentionally simple examples, learners can concentrate on other aspects of the Bayesian workflow without being distracted by the model-building aspects. Hence, this material is designed to complement more theory-heavy or inference-focused resources by filling a gap in accessible, practice-oriented learning. The examples leverage the open-source library ArviZ for visualization and analysis, demonstrating principles that transcend any single probabilistic programming language. 


# Target Audience

This resource is designed for learners and educators in statistics, data science, and applied fields that use statistics who seek a practical understanding of Bayesian data analysis. Examples use tools written in Python, so readers should be familiar with this programming language to fully take advantage of the material, but readers with a knowledge of high-level languages like R or Julia may also follow the material with little extra guidance. 

# Content

The main objective of the material is to provide students with a practical understanding of aspects of Bayesian modeling that are usually given little attention in many courses. The resource uses the ArviZ library [@Kumar:2019] and other open source tools, including Preliz [@Icazatti:2023],  PyMC [@pymc:2023], Bambi [@Capretto:2022], and cmdstanpy [@cmdstanpy], among others. However, the focus is on practical statistical ideas, and hence the material could be easily adapted to use a different set of tools, even from other programming languages like R or Julia. Additionally, the content encompasses basic concepts useful for effective Bayesian data analysis and state-of-the-art methods grounded in well-established statistical principles, providing robust, interpretable diagnostics and visualizations [@Vehtari:2017; @Gelman:2019; @Paananen:2020; @Vehtari:2021; @Dimitriadis:2021; @Sailynoja:2022; @Kallioinen:2023; @Sailynoja:2025].  In summary, this educational resource is designed to equip students with the skills and knowledge necessary to effectively and critically apply Bayesian statistics. While this resource has not been used for teaching in its present form. It is based on notes, slides, and material used for teaching Bayesian statistics. The feedback received from students has been taken into account to make it clearer and accessible.

# Conclusions

By focusing on often neglected topics, this resource equips learners with practical skills for Bayesian analysis. It offers an accessible, adaptable resource that can be used on its own or as a complement to more traditional Bayesian courses. We hope this material will be of use for both classrooms and self-guided study, fostering deeper statistical literacy.

# Acknowledgments

We thank the many contributors to the open-source software packages used in this material. This work for financially supported by:

* Essential Open Source Software Round 4 grant by the Chan Zuckerberg Initiative (CZI)
* The Research Council of Finland Flagship Programme "Finnish Center for Artificial Intelligence" (FCAI)


# References

