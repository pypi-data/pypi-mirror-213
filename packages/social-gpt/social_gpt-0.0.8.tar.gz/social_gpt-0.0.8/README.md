# Social GPT
This package helps you to build embeddings based on someone social profile. It will scrape the data from the social media and build the embeddings based on the data. The embeddings can be used for further analysis.
Once scraped, you can query it with the use of openai.

## Installation
Install using following command:
`pipenv install social-gpt==0.0.6`

## Setup
Update the `example.env` and change it's name to `.env`. Add relevant information in the `.env` file.

## Creating embeddings

As of now, only youtube is supported. We will be bringing more social media platforms soon. To create embeddings, run the following command:

```
from social_gpt.ingestion.indexer import Indexer
indexer = Indexer()
```