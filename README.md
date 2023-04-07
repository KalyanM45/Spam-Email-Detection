# Spam Email Detection using Machine Learning Algorithms

This repository contains a Python script that uses various machine learning models to classify spam messages from ham messages.  The model is trained on a Popular dataset of Spam emails and we use multiple machine learning models for classification.

# Dataset

We use the publicly available Email-Spam dataset, which is collected from the Kaggle. The dataset includes a total of 5,572 emails having 2 features i.e. Category - Spam/Ham,
and Message.

# Data Pre-processing

We use a supervised learning approach to train our model, using a combination of natural language processing (NLP) techniques and traditional machine learning algorithms. Specifically, we use the following steps:

The Unnamed: 2, Unnamed: 3, and Unnamed: 4 columns are dropped.

The Category column is converted to binary values.

The dataset is split into training and testing sets using train_test_split() function from sklearn.model_selection.

The emails are transformed into numerical features using the TfidfVectorizer() function from sklearn.feature_extraction.text.

# Model Training and Evaluation

We split the dataset into training and testing sets and trained on multiple models such as Logistic Regression, Decision Trees, K Nearest Neighbors, Random Forest and also a Stacking model on the training set. We evaluate the performance of the models on the testing set using metrics such as accuracy, precision, recall, and F1-score.

# Usage

The code is written in Python and can be run using any Python environment such as Jupyter Notebook, Spyder, etc.

The code imports the necessary libraries, reads the dataset, preprocesses it, and trains the classifiers.

To use the code, simply run the cells in the order they appear.

# Dependencies

The code requires the following Python libraries to be installed:

Numpy 

Pandas

Matplotlib

Seaborn

Sklearn

# Contributing

We welcome contributions from the community! If you have any ideas or suggestions for improving the project, please feel free to create an issue or submit a pull request.

# Acknowledgements

This project was inspired by the Kaggle dataset on Spam Email Detection and the corresponding competition. We also acknowledge the open-source Python libraries used in this project and their contributors.
