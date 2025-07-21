# AntisemitismSelfTest
based on ADL pyramid of Hate, this survey aims to be a reliable tool to measure exposure to antisemitic risk

## Concept of survey

This extensive survey is based on the ADL Pyramid of Hate framework and its  intended use if for individuals affected by antisemitism to have a sound tool with which to methodically reflect on and measure exposure to antisemitism. The timeframe of reference could be the past twelve months or (alternatively) since Oct 7th, 2023.

## Structure

Following the Pyramid framework, there are five successive levels increasing in severity of aggression. Each of these five levels is subdivided in 2 parts (except the third level, which has three) comprising about 20 items each, totalling over 200 items.

## The scoring system

The scoring is done with a python script which calculates the scores and produces a visual representation of the result. The key indicator, exposure to risk, is shown by the surface of the polygons, which are given as percentage of respective maximal extent.

There are three layers:
1. layer 1 is orange/red, reflecting the detailed score for each of the ten sections.
2. Layer 2 is blue, reflecting the pattern of exposure of the five levels.
3. Layer 3 only appears if and only if the raw score of levels 3C+4A OR any section of levels 4 and 5 surpasses the combined raw scores of levels 1A-3C. This last layer indicates significant, concerning exposure.

## scoring concept

'''bash

  '1A': (2, 30, 0.35),  # (weight, num_questions, bonus_fraction)
    '1B': (3, 12, 0.30),
    '2A': (5, 21, 0.25),
    '2B': (8, 23, 0.20),
    '3A': (13, 22, 0.15),
    '3B': (21, 10, 0.10),
    '3C': (34, 14, 0.02),    
    '4A': (55, 22, 0),
    '4B': (89, 19, 0),
    '5A': (144, 20, 0),
    '5B': (233, 17, 0)
'''
    As seen here, the weighting of each section follows the fibonacci series, which is exponential. Each successive section scoring comprises the the weights of the preceding two (hence 2A items are weighted 5, which is 2+3). Furthermore, if the respondent answers positively to at least 2/3 of questions in each section, a "cumulation bonus" is added to the score of that section. This reflects the suplemental psychological stress that is incured by the subject.

The idea is that up to the last tier of level 3, the cumulative psychological andvemotional toll of the aggressions prevail over the individual incidents taken separately. After that, singular physical aggressions are important in themselves and deepen the risk exposure to a much stronger degree than previous types. Also, the gradually decreasing bonus additions of the first three levels reflect a tendency to "getting used to" psychological aggression as it becomes part of routine daily life.

  A this stage, the answers are binary (yes/no) but it is intended in further development to switch to a scaled response scheme such as: never/sometimes/often/constantly which would be itself weighted 0.3/0.5/0.7/1