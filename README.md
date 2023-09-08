# Retail GeoPlatform
## About
This repository was created as a part of the AI Talent Hackathon. During this hackathon, the problem of analyzing reviews of X5 retail stores was solving. As a solution, we have proposed the *GeoPlatform* - a tool for analyzing reviews both for one store and for a set of stores in a district/city.

## Data collection
The data was collected from open sources such as Yandex Maps and 2GIS. The result of parsing was more than 5,000 reviews of 55 stores of 5 different retail chains.
## Model selection and fitting
ML Task - hierarchical text classification by store parameter and it's sentiment.

The first-level model classifies the key storage parameter. The second level classifies sentiment of this parameter.
Due to the missing markup, the zero-shot text classification approach was chosen.

Two models from Hugging Face were considered:
- zero-shot-classify-SSTuning-XLMR, because it's fast and easy to integrate;
- multilingual-e5-large-xnli-english, because it's powerful.
##Frontend and deploy
- pydeck layers for build map and plot points
- streamlit for deploy app
## Results demonstration
