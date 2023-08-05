====================================
GROGU
====================================
GROGU (GRanular Opinion GaUge) is a Python package that enhances sentiment analysis by providing domain-specific dictionaries. Built upon the VADER sentiment analysis tool, GROGU offers improved results for sentiment analysis in specific contexts.
The package is fully open-source and released under the `[MIT License] <http://choosealicense.com/>`_ (we appreciate attributions and accept most contributions but cannot be held liable).

* `GROGU: Tool for Enhancing Sentiment Lexicon with Machine Learning`_
* Introduction_
* Installation_
* `Package explanation`_
* `Example`_

GROGU: Tool for Enhancing Sentiment Lexicon with Machine Learning
------------------------------------
The GROGU project aims to overcome the limitations of lexicon-based sentiment analysis tools, such as VADER, which are too general and not suitable for specific contexts. It addresses issues like word ambiguity, where a term may have different meanings based on the domain.
For example, "bull" can refer to an animal or indicate positive growth in the financial domain. 
The project consists of two main parts that lay the foundation for a comprehensive system capable of recognizing and analyzing specific discussion topics.

The GROGU package provides specialized dictionaries for sentiment analysis in the following domains:
#. Food: food review on amazon
#. Electronics: review of electronic products on amazon
#. Hotel: review of amusement parks on tripadvisor
#. Finance: reviews and tweets of financial topics

In addition to the GROGU sentiment analysis module, options 3 or 4 during installation will download additional resources and datasets (described below).

The complete procedure and research findings are explained in detail in the **Project_explanation** PDF file. The key takeaway is that using specialized dictionaries trained on specific lexicons consistently improves the performance of VADER for sentiment analysis.

We encourage you to explore the insights and input provided by this project, which involves developing a system capable of identifying the topic of discussion in text and performing accurate analysis using specialized dictionaries. Furthermore, if you have specialized dictionaries that you would like to contribute, we welcome your collaboration to expand the range of options provided by GROGU.
====================================
Introduction
====================================

This README file briefly describes the proposed package:

	|  **GROGU: Tool for Enhancing Sentiment Lexicon with Machine Learning**
	|  (-)  
 
 

Starting from Vader
------------------------------------

The project was developed starting from Vader, who was born thanks to cjhotto. For the operation of this fantastic tool we refer directly to the github page of the creator `[Vader] <https://github.com/cjhutto/vaderSentiment>` _. The original article is shown below:

  **Hutto, C.J. & Gilbert, E.E. (2014). VADER: A Parsimonious Rule-based Model for Sentiment Analysis of Social Media Text. Eighth International Conference on Weblogs and Social Media (ICWSM-14). Ann Arbor, MI, June 2014.** 

====================================
Installation
====================================

To install and use GROGU you can proceed in the following way:  

Use the command line to do an installation from `[PyPI] <https://pypi.org/project/GROGU/>`_ using pip, e.g., 
    ``> pip install GROGU``


====================================
Package explanation
====================================
IT start by installing the "GROGU" package via pip install.

The package contains the dictionaries and functions relating to the 4 topics separately, which can be imported individually.
------------------------------------
:: 
   from GROGU import GROGU_food

   from GROGU import GROGU_electronic

   from GROGU import GROGU_hotel

   from GROGU import GROGU_finance

The package contains the dictionaries and functions relating to the 4 topics separately, which can be imported individually.
That is, two replacement functions, respectively of SentiText() which identifies the string-level properties relevant to the sentiment of the input text, and SentimentIntensityAnalyzer() which instead assigns a sentiment intensity score to the phrases. The two functions are renamed for each argument.
------------------------------------
:: 
   from GROGU.GROGU_food import Food_ST, Food_SIA

   from GROGU.GROGU_electronic import Electronic_ST, Electronic_SIA 

   from GROGU.GROGU_hotel import Hotel_ST, Hotel_SIA

   from GROGU.GROGU_finance import Finance_ST, Finance_SIA

STfunctions identify sentiment-relevant string-level properties of input text.
Now let’s see how the SIA functions work and how with one of its sub-functions we find the compound values. The resulting values are more accurate, as they refer to specific dictionaries. 

For all callable sub-functions, reference is always made to the VaderSentiment guide, remember that the operation of the GROGU package is in all respects the same as that of VaderSentiment, the only change is the specific domain of the dictionaries used.

Inclusion we invite you to try and experiment the potential of the package, which, we remind you once again,
only acts as a showcase of how a specialization of VaderSentiment leads to more accurate analyzes.

====================================
Example
====================================

We now show how the package works with an example.

Code Examples
------------------------------------
::

	from GROGU.GROGU_finance import Finance_ST, Finance_SIA

    # --- example -------
    sentence = "GROGU is a very cool project."
    
    analyzer = vader_finance.Finance_SIA()
    vs = analyzer.polarity_scores(sentence) print("{:<13} {}".format(sentence, str(vs))




Output for the above example
------------------------------------
::

	Just an example {’neg’: 0.0, ’neu’: 0.286, ’pos’: 0.714, ’compound’: 0.7184}



