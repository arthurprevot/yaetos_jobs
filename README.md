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
This repository consists of data pipelines using yaetos data framework ([github.com/arthurprevot/yaetos](https://github.com/arthurprevot/yaetos)). These are generic use cases that can be leveraged.

## Generative AI:
 * Data pipelines to pull information out of ChatGPT programmatically, to feed into datasets.
 * Data pipelines to fine tune a "small" open source LLM (aka generative AI), called Albert, for classification, and to run inferences. The model is small enough to run from a laptop (no need for GPU).
 * Data pipelines to feed documents (pdf, text) to privateGPT vector database to add knowledge to local LLM.

## Scientific (Climate data, image processing):
 * Data pipelines to process carbon emissions data from climate-trace (https://climatetrace.org/).
 * Data pipelines to process images (could be satellite, medical, etc) to find contours (@ scale, using Spark).

## Sales/Marketing:
 * Data pipelines to pull employee contact information out of Apollo.io for a set of companies.
 * Data pipelines to pull information from Github contributors using Github API. 

## Other:
 * Data pipelines to showcase Yaetos core functionalities, using public wikipedia data.

Lots of room for improvements. Contributions welcome. Feel free to reach out at arthur@yaetos.com. 