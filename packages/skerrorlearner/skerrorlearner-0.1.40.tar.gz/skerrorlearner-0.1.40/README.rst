==============
skerrorlearner
==============

``skerrorlearner`` is a Python library which learns error to produce another model that can be used to predict the error that may occur. It uses ``numpy``, ``pandas``, ``scikit-learn``, ``xgboost``, ``ligtgbm`` and ``catboost`` for the same.

Installation
------------

**Using pip**

Use the package manager ``pip`` to install skerrorlearner.

   ``pip install skerrorlearner``

Initialization
--------------

   
   ``from skerrorlearner.learn_error import LearnRegressionError``
   
   ``from skerrorlearner.learn_error import LearnClassificationError``
   
   ``from skerrorlearner.learn_error import ProductionPredictionGeneration``


   ``#initialise a skerrorlearner instance``

   ``lre = LearnRegressionError(rdf_train.copy(), rdf_val.copy(), rdf_test.copy(), feat.copy(), 'cnt', lgbm, 'rmse', True)``
   
   ``lce = LearnClassificationError(cdf_train.copy(), cdf_val.copy(), cdf_test.copy(), feat.copy(), 'income', cat,'accuracy', 'binary', 'macro', True, True)``
   
   ``cdf_ppg = ProductionPredictionGeneration()``
