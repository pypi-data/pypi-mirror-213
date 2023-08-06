<!-- PROJECT NAME -->
<div align="center">
   <img src="https://ik.imagekit.io/m0ci8dgk4/nlpipes_logo_eSBhzDKCZ.png?updatedAt=1679840445991" alt="nlpipes_logo" title="nlpipes logo">
  <h2>Text Classification with Transformers</h2>
</div>

<div align="center">
    <a href="https://opensource.org/licenses/Apache-2.0">
       <img alt="Licence" src="https://img.shields.io/badge/License-Apache_2.0-blue.svg">
    </a>
     <a href="https://pypi.org/project/nlpipes/">
       <img alt="PyPi Version" src="https://img.shields.io/pypi/pyversions/nlpipes">
    </a> 
    <a href="https://pypi.org/project/nlpipes/">
        <img alt="PyPi Package Version" src="https://img.shields.io/pypi/v/nlpipes">
    </a>
    <!--
    <a href="https://pepy.tech/project/nlpipes/">
        <img alt="PyPi Downloads" src="https://static.pepy.tech/badge/nlpipes/month">
    </a>
    -->
</div>

<div align="center">
    <a href=""><strong>Documentation</strong></a>
    • <a href=""><strong>References</strong></a>
</div>


<div align="center">
  <img src="https://ik.imagekit.io/m0ci8dgk4/nlpipes_screenshot_q_FDeS4Js.png?updatedAt=1686231419316"
       alt="nlpipes_screenshot" 
       title="nlpipes screenshot"
       width="75%"
       height="75%"
  >
</div>


## Overview

`NLPipes` is for people unfamiliar with Transformers who want an end to end solution to solve practical text classification problems, including:

* **Single-label classification**: A typical use case is sentiment detection where one want to detect the overall sentiment polarity (e.g., positive, neutral, negative) in a review.
* **Multi-label classification**: A typical use case is aspect categories detection where one want to detect the multiple aspects mentionned in a review (e.g., product_quality, delivery_time, price, ...).
* **Aspect-based classification**: A typical use case is aspect based sentiment analysis where one want to detect sentiment polarity associated to each aspect categories mentionned in a review (e.g., product_quality: neutral, delivery_time: negative, price: positive, ...).

`NLPipes` expose a `Model` API that provide a unique and simple abstraction for all the tasks. 
The library maintain a common usage pattern across models (train, evaluate, predict, save) with
also a clear and consistent data structure (python lists as inputs/outputs data).

#### Built with
`NLPipes` is built with TensorFlow and HuggingFace Transformers:
* [TensorFlow](https://www.tensorflow.org/): An end-to-end open source deep learning framework
* [Transformers](https://huggingface.co/transformers/): An general-purpose open-sources library for transformers-based architectures

## Getting Started

#### Installation
1. Create a virtual environment

 ```console
 python3 -m venv nlpipesenv
 source nlpipesenv/bin/activate
 ```

2. Install the package

 ```console
 pip install nlpipes
 ```
 
 
#### Tasks

A model can be trained for a specific task by first loading a backbone model. The train command takes
at minimum two parameters (X and Y), where X is a list of texts to train on and Y is the 
training target.

The training target expect different formats, depending on what task you want to solve:


##### Single Label Classification:
Give one label name for each sequence of text in `X`:

 ```console
  model = Model("albert-base-v2",
                task='single-label-classification',
                all_labels=["NEG", "NEU", "POS"],
               )
  
  X = ["This was bad.", "This was great!"]
  Y = ["NEG", "POS"]
  
  model.train(X, Y)
 ```

##### Multiple Label Classification:
Give a list of class names for each sequence of text in `X`:

 ```console
  model = Model("albert-base-v2",
                task='multi-label-classification',
                all_labels=all_labels,
                )
  
  X = ["I want a refund!",
       "The bill I got is not correct and I also have technical issues",
       "All good"]
  Y = [
       ["billing"], 
       ["billing", "tech support"],
       []
      ]
      
  model.train(X, Y)
 ```
 
 ##### Aspect Based Classification:
Give a list of lists of label lists (pairs) for each given text in `X`:

 ```console
  model = Model("albert-base-v2",
                task='class-label-classification',
                all_labels=["NEG", "NEU", "POS"],
               )
  
  X = ["The room was nice.",
       "The food was great, but the staff was unfriendly.",
       "The room was horrible, but the waiters were welcoming"]
  Y = [
       [["room", "POS"],
       [["food", "POS"], ["staff", "NEG"]],
       [["room", "NEG"], ["staff", "POS"]],
      ]
      
  model.train(X, Y)
 ```


#### Examples

Here are some examples on open datasets that show how to use `NLPipes` on different tasks:

Name|Notebook|Description|Task|Size|Memory|Speed| 
----|-----------|-----|---------|---------|---------|---------|
GooglePlay Sentiment Detection|Available|Train a model to detect the sentiment polarity from the GooglePlay store |Single label classification|  |  |  
StackOverflow tags Detection|Available|Train a model to detect tags from the StackOverFlow questions |Multiple label classification|  |  |
Amazon Aspect Based Sentiment Detection|Available|Train a model to detect the aspect based sentiment polarity on Laptops Amazon reviews |Class label classification|  |  | 


## Notices
- `NLPipes` is still in its early stage. The library comes with no warranty and future releases could bring substantial API and behavior changes.

