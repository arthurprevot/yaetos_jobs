<p align="center">
	<img src="./docs/images/logo_full_2_transp.png" alt="Yaetos Project" width="300" height="auto"/>
</p>

<div align="center">

[![Continuous Integration](https://github.com/arthurprevot/yaetos_jobs/actions/workflows/pythonapp.yml/badge.svg)](https://github.com/arthurprevot/yaetos_jobs/actions/workflows/pythonapp.yml)
[![Pypi](https://img.shields.io/pypi/v/yaetos.svg)](https://pypi.python.org/pypi/yaetos)
[![Users Documentation](https://img.shields.io/badge/-Users_Docs-blue?style=plastic&logo=readthedocs)](https://yaetos.readthedocs.io/en/latest/)
[![Medium](https://img.shields.io/badge/_-Medium-orange?style=plastic&logo=medium)](https://medium.com/@arthurprevot/yaetos-data-framework-description-ddc71caf6ce)

</div>

# yaetos_jobs
This repository consists of data pipelines using yaetos data framework ([github.com/arthurprevot/yaetos](https://github.com/arthurprevot/yaetos)). The code for these data pipelines is found in the ["jobs"](/jobs/) folder. Most pipelines are setup with small sample inputs so they should work out of the box.

## Generative AI:
 * Data pipeline to pull information out of ChatGPT programmatically, to feed into datasets.
 * Data pipeline to fine-tune a "small" open source LLM called Albert, for classification, and to run inferences. The model is small enough to run from a laptop in minutes for the test case (no need for GPU).
 * Data pipeline to feed documents (pdf, text) to privateGPT vector database to add knowledge to local LLM.

## Scientific (Climate data, image processing):
 * Data pipeline to process carbon emissions data from climate-trace (https://climatetrace.org/), with a sample dashboard available [here](https://arthurprevot.github.io/yaetos_jobs/dashboard_climate.html) 
 * Data pipeline to process images (could be satellite, medical, etc) to find contours (@ scale, using Spark).

## Sales/Marketing:
 * Data pipeline to pull employee contact information out of Apollo.io for a set of companies.
 * Data pipeline to pull information from Github contributors using Github API. 

## Other:
 * Data pipeline to showcase Yaetos core functionalities, using public wikipedia data.

Lots of room for improvements. Contributions welcome. Feel free to reach out at arthur@yaetos.com. 

#----- TODO: to add later ------
 * Data pipeline to process banking information, grouping data from various accounts, re-labeling transactions differently from the bank, and organising it in a way not available from the bank.
 * Data pipeline to pull all contacts from various sources and put it in one dataset.

