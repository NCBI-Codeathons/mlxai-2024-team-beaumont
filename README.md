# RAGVar MLXAI Codeathon Team

List of participants and affiliations:
- (Team Leader) David Beaumont, RTI International | SSES | Center for Data Modernization Solutions
- (Tech Lead) Corey Cox, University of Colorado | Anschutz Medical Campus | TISLab
- Nathaniel Braswell, RTI International | SSES | Center for Data Modernization Solutions
- Stephen Hwang, RTI International | SSES | Center for Data Modernization Solutions
- Oswaldo Alonso Lozoya, RTI International | SSES | Center for Data Modernization Solutions

## Project Goals
The goal of RAGVar is to build a system for harmonizing your data with the data that already exists within a data repository such as NCBI or NHLBI BDC. Harmonization is a major challenge for all research repositories as data sources do not have either the clear direction and/or the resources to align data before ingest. This results in retrospective data harmonization that must be done by the data users or through manual harmonization efforts by the repository teams. The RAGVar system evaluates the potential for retrieval augmented generation and AI reasoning to provide an evaluation mechanism for determining how new data, provided in a data dictionary, aligns with the data existing within a repository.

RAGVar focuses on the initial step of aligning user provided variables, in the form of a data dictionary with descriptive variable labels, with the existing variables in the corpus of data which a user may want to align with. After identifying prospective similar variables, RAGVar ranks which variable is most likely to be a match for each of the new variables and attempts to provide information to the user about how to harmonize their variables with the existing data sets.

## Approach
The following outlines our approach and methods for project name
### Workflow
![image](https://github.com/NCBI-Codeathons/mlxai-2024-team-beaumont/assets/153935407/37b62e40-3978-49f4-90f3-3472dd2a6223)

### Methods
Publically available data from BioLINCC studies were scraped to collect machine readable data dictionaries for the studies. The raw data was given a unique identifier (UID) to preserve attributes, such as source study and variable name, in a lookup table.

Descriptive variable labels were cleaned using regex expressions to strip out artifacts, i.e. ‘1.‘ or ‘Q1’, that often precede the label and duplicative fields were collapsed preserving the UID in a vector.  A vector database was constructed using these variable descriptive labels for embedding in retrieval augmented generation (RAG).

User provided data dictionaries were parsed into single variable labels, with varying levels of descriptiveness. Single variables were then provided to RAG to identify the top 5 best matches based on our embeddings. Identified best matches were then re-ranked using Cohere to produce relevance scores for all matches with the best three selected by relevance score.

After Cohere reranking, variables names were re-extracted from the lookup table for the top 3 matches. Using a constructed prompt, top 3 variable name matches and the original variable label were provided to an LLM to suggest the best match for the original variable with an emphasis on using the suggested options. The LLM was also asked to provide the user instructions to align their variable with the variable selected.

### Evaluation
Results from the Cohere re-ranking, each of top three selected, and LLM final output were evaluated by a human experienced in data alignment and harmonization. For each result, our judge rated the result into the following three categories.

 - ‘Success’ - Helpful for a data analyst in aligning a variable.
 - ‘Neutral’ - Ambiguous but may help to identify appropriate variables.
 - ‘Failure’ - No value or adverse in aligning with existing data.

## Results

### Model Performance
| llm_rank | count | percentages
| -------- | ------- |  ------- |
| Success | 61 | 59.22% |
| Neutral | 25 | 24.27% |
| Failure | 17 | 16.5% |

| cohere_rank | count | percentages
| -------- | ------- |  ------- |
| Success | 59 | 57.28% |
| Neutral | 27 | 26.21% |
| Failure | 17 | 16.5% |

| cohere_llm_match | count | percentages
| -------- | ------- |  ------- |
| Match | 92 | 89.32% |
| Mismatch | 11 | 10.68% |


Lots of successes, generally the frequency of success is considered good for LLM at the proof-of-concept stage.

### Model Comparison

| | |
|:-------------------------:|:-------------------------:|
|![](https://github.com/NCBI-Codeathons/mlxai-2024-team-beaumont/blob/gen-ai-dev/jupyter/notebooks/complete_workflow/evaluation/plots/r_llmVcohere_boxplot.png?raw=true)  |  ![](https://github.com/NCBI-Codeathons/mlxai-2024-team-beaumont/blob/gen-ai-dev/jupyter/notebooks/complete_workflow/evaluation/plots/s_llmVcohere_count.png?raw=true)|

Successful matches had a high confidence score, with little difference in performance between models. 
When confidence score was moderate, then both llms often gave potential options that would need additional effort by the user.
Match failures also had a high confidence score, this indicates an area for improvement in either the data for training or in pre-processing the input. Cohere had high-confidence in certain low-value matches that are likely due to model fixation on certain input words.

![](https://github.com/NCBI-Codeathons/mlxai-2024-team-beaumont/blob/gen-ai-dev/jupyter/notebooks/complete_workflow/evaluation/plots/_boneyard/heatmap.png?raw=true)

-In most cases LLM and Cohere agreed but there were cases when the LLM reasoned into  a higher success category although there was one case of the reverse.

| | |
|:-------------------------:|:-------------------------:|
|![](https://github.com/NCBI-Codeathons/mlxai-2024-team-beaumont/blob/gen-ai-dev/jupyter/notebooks/complete_workflow/evaluation/plots/goldilocks_h3_llmVmatch_collapsed.png?raw=true)  |  ![](https://github.com/NCBI-Codeathons/mlxai-2024-team-beaumont/blob/gen-ai-dev/jupyter/notebooks/complete_workflow/evaluation/plots/goldilocks_k3_cohereVmatch_collapsed.png?raw=true)|

Goldilocks-Zones: This figure is a scatterplot of model results with the Y-Axis representing the Cohere Relevance Score and the X-Axis based on the user designation of model response with the attributes of Neutral, Failure, and Success. The three colored circles in each grouping represent the “Goldilocks Zones”. 

### The Goldilocks Zones 
In the chart above are a depiction of the 3 areas of highest import. 
Areas encircled in Red represent points of failure in our application: the model had high confidence in its relevance to a user variable but the result was classified as a failure. These data points should be examined on each failure case for a deeper understanding on if there are pre-processing steps that must take place on user input or if fine tuning the model is needed.
Areas encircled in Green are true successes: the user was satisfied with the model’s output and the model returned a high confidence in its relevance.
Areas encircled in Yellow is where future research is required: These points represent an area where the model was not confident in the accuracy of the returned RAG value but the user considered the results useful. If upon further investigation these areas continue to be found in the results then this application could be shown to be beneficial to users. Because the results returned to the user in this grouping would not be found by “traditional” semantic search applications and would require LLMs to find adjacent relevant contexts with a low relevance score as shown.

## Future Work

### Study Descriptions embeddings
Future work could create embeddings for a separate RAG based on study descriptions to align study-by-study and help to inform the LLM in the output prompt of the study space these variables should be aligned within.

### Prompt versioning and engineering
We initiated work towards prompt-versioning with the goal to run prompts head-to-head and develop better prompts for the final output.  One area we have identified for prompt improvement is for the LLM to identify when the Cohere results do not provide useful information to the user. As our results show above, when the cohere relevance scores are high but Cohere fails the LLM has a very high likelihood of failure providing output of no value or adverse to researcher alignment. An engineered prompt may allow the LLM to reject the results from Cohere and tell the user there is no good match.

### Data Ops
The greatest challenge in using AI in data harmonization is a term commonly known as concept drift. This is when the users of a model adjust their perception of a concept association over time rendering model training data incorrect. We believe the biggest threat to the success of this application is concept drift in research terminology, this could be due to concept drift in association to changing perspectives of the researchers or more likely our vector database would not contain the domains of a novel datatype submission. For example after the outbreak of the global COVID-19 pandemic there would not have any existing reference for many of the research terminologies in a database created pre 2019.

We can identify potential concept drift  by evaluating data output where there is a  high-relevance score from Cohere but were considered failures via user response. Annectodatally, we noticed the model appeared on certain words, especially age and unit. This particular example could be solved by adding a data cleaning pre-processing step before running user input. Alternatively, DataOps strategies could be leveraged to store user curation output for variables where the model struggles, allowing us to determine whether the database is missing some data or if our model requires fine-tuning for complex data harmonization tasks.

### MLOps
As the data corpus evolves with users adding more variables there will be two outcomes, either the submitted variables are aligned to the existing corpus of data or our dataset will have no identifiable matches. By capturing the user response of successful or unsuccessful matches we will be able to create mapped associations of new variables to user curated variable descriptions in the relevant areas. Over time this additional data will allow us to finetune the embeddings with a larger spread of descriptions allowing the model to have better identification as more data is added.

### Better Test Data Set
Our initial test data was based on a set of alignment variables identified for a different use-case. These variables were in some ways a synthetic set of variables with lower resemblance to the real-world use-case. Due to time constraints, we were unable to use other test data sets to evaluate the model. Using variables more similar to the training data (variables from real studies) may give better information about how the model is performing.

## NCBI Codeathon Disclaimer
This software was created as part of an NCBI codeathon, a hackathon-style event focused on rapid innovation. While we encourage you to explore and adapt this code, please be aware that NCBI does not provide ongoing support for it.

For general questions about NCBI software and tools, please visit: [NCBI Contact Page](https://www.ncbi.nlm.nih.gov/home/about/contact/)


