# -*- coding: utf-8 -*-
"""Week 4 Lab_TanayKapoor.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1F5y-LSG6tsEiu9fiTr-Kvpt3VPV5yjBE

# Week 4 Lab - due by 11:59pm CDT on July 30th

## Objective: to implement machine learning methods and models on classification problems

### Setup and Loading Packages
"""

# Commented out IPython magic to ensure Python compatibility.
# %matplotlib inline

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns

import scipy.stats as stats

from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import scale
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay, mean_squared_error, f1_score, classification_report, roc_curve, auc, roc_auc_score
from sklearn.multiclass import OneVsRestClassifier

from sklearn.preprocessing import StandardScaler
from sklearn.datasets import make_multilabel_classification

"""## Problem 1: Russell 2000 Directional Move

Recall that in the last two lectures, we attempted to use the BMED and IVEG log returns to predict IWM daily directions.

The first model we implemented was logistic regression. Let's examine other models and compare their performances.

a) Write a code piece to load in the 'IWM_BMED_IVEG.csv'. Then convert the IWM log returns into binary values, 0 represents a day with negative return (downward direction) and 1 represents a day with positive return (upward direction), then replace the original 'IWM' column with this.
"""

################ EDIT CODE LINES HERE #################
# Load in IWM, BMED, IVEG dataset
from google.colab import drive
drive.mount('/content/drive')

IWM_BMED_IVEG = pd.read_csv('/content/drive/MyDrive/DSQFRM/Week 4/IWM_BMED_IVEG.csv'); IWM_BMED_IVEG = IWM_BMED_IVEG.set_index('Date')
IWM_BMED_IVEG.info()



# convert IWM log returns into binary values 1's and 0's

IWM_BMED_IVEG['IWM Direction'] = (IWM_BMED_IVEG.IWM > 0).astype(int)
IWM_BMED_IVEG.head()
######################################################

"""b) Please write a code piece to split data into 80% training set and 20% testing set."""

################ EDIT CODE LINES HERE #################
# Splitting data into 80% training set and 20% testing set

FEATURES = ['']
X_train, X_test, y_train, y_test = train_test_split(IWM_BMED_IVEG.iloc[:, 0:3], IWM_BMED_IVEG.iloc[:, 3], test_size=0.2, random_state=0)




######################################################

"""c) Please select ONE classification model to fit the training data. Why did you chose this model?

The data set is a pre-processed, meaning that features are standardized, missing values & potential outliers are removed, and unimportant & highly correlated features are dropped. You DO NOT have to pre-process the data again before fitting your model.
"""

################ EDIT CODE LINES HERE #################
# Visualization of features and response to help select model


# Visualize IWM Direction by BMED and IVEG Log Returns
plt.scatter(IWM_BMED_IVEG.BMED[IWM_BMED_IVEG['IWM Direction'] == 1],
            IWM_BMED_IVEG.IVEG[IWM_BMED_IVEG['IWM Direction'] == 1],
           color='green',
           label='Up')
plt.scatter(IWM_BMED_IVEG.BMED[IWM_BMED_IVEG['IWM Direction'] == 0],
            IWM_BMED_IVEG.IVEG[IWM_BMED_IVEG['IWM Direction'] == 0],
           color='red',
           label='Down')
plt.title('IWM Directions by BMED and IVEG Log Returns')
plt.xlabel('BMED')
plt.ylabel('IVEG')
plt.legend()
plt.show()


######################################################

################ EDIT CODE LINES HERE #################
# (Optional) Using GridSearchCV to search for optimal parameters

from sklearn.tree import DecisionTreeClassifier
from sklearn import tree

parameters = {'max_depth':range(3,20)}
dt = GridSearchCV(tree.DecisionTreeClassifier(), parameters, n_jobs=4)
dt.fit(X_train, y_train)
tree_model = dt.best_estimator_
print (dt.best_score_, dt.best_params_)



######################################################

# Evaluate the best Decision Tree model on the test data
test_accuracy = tree_model.score(X_test, y_test)
print('Test Accuracy: {:.2f}'.format(test_accuracy))

################ EDIT CODE LINES HERE #################
# Fitting your chosen model


from sklearn import svm
# build SVC model and choose the Radial Basis Function (RBF) kernel function
rbf = svm.SVC(kernel='rbf', gamma=0.5, C=0.1, probability=True).fit(X_train, y_train)
# choose the Polynomial kernel function
poly = svm.SVC(kernel='poly', degree=3, C=1, probability=True).fit(X_train, y_train)

# predicted liquidity strengths
y_train_pred_rbf = rbf.predict(X_train)
y_test_pred_rbf = rbf.predict(X_test)
y_train_pred_poly = poly.predict(X_train)
y_test_pred_poly = poly.predict(X_test)




######################################################

"""[Write your answer here]

I choose to use Support Vector Machines (SVM) classification. At first, I was going to use logistic regression as it does well with linear data and small datasets. However, we must compare a different classification to logistic regression in the next question. I choose SVM as after visualizing the data in the above scatterplot, I wanted to account for any non-linearities. SVM can handle non-linear data pretty well since it transforms it into multiple dimensions to find the optimal decision boundary to separate both of our classes. The dataset is also relatively small, so we need fewer training samples than more complex models. Since SVM can handle small datasets, we reduce the risk of overfitting and can generalize better. Also, our problem is binary classification, so SVM is suitable for this.

c) Compare the performance of the model you chose above with that of the logistic regression applied in Week 3 lecture. Which model performs better and why? (Remark: please output proper metrics to support your claim)
"""

################ EDIT CODE LINES HERE #################

# Fitting to logistic regression

from sklearn.linear_model import LogisticRegression
logistic_model = LogisticRegression()
logistic_model = logistic_model.fit(X_train, y_train)
lr_probs = logistic_model.predict_proba(X_test) # calculate the probabilities of the class for the test dataset using ‘predict_proba’
y_test_pred_logistic = logistic_model.predict(X_test) # predict the class labels using predict function for the test dataset


# Calculate training and testing error for logistic regression
train_error_logistic = 1 - logistic_model.score(X_train, y_train)
test_error_logistic = 1 - logistic_model.score(X_test, y_test)

print('Logistic Regression Training Error = %.3f' % train_error_logistic)
print('Logistic Regression Testing Error = %.3f' % test_error_logistic)




# Calculating training and testing errors for SVM
train_error_rbf= 1-rbf.score(X_train,y_train)
test_error_rbf= 1-rbf.score(X_test,y_test)
print('SVC (RBF Kernel) Training Error = %.3f' % train_error_rbf)
print('SVC (RBF Kernel) Testing Error = %.3f' % test_error_rbf)
train_error_poly= 1-poly.score(X_train,y_train)
test_error_poly= 1-poly.score(X_test,y_test)
print('SVC (3rd-Degree Polynomial Kernel) Training Error = %.3f' % train_error_poly)
print('SVC (3rd-Degree Polynomial Kernel) Testing Error = %.3f' % test_error_poly)



######################################################

################ EDIT CODE LINES HERE #################
# Calculating training and testing accuracy scores


# Calculating training and testing accuracy scores for logistic regression

print('training accuracy score for logistic regression:', logistic_model.score(X_train,y_train))
print('testing accuracy score for logistic regression:', logistic_model.score(X_test,y_test))

# Calculating training and testing accuracy for SVM

train_accuracy_rbf= rbf.score(X_train,y_train)
test_accuracy_rbf= rbf.score(X_test,y_test)
print('SVC (RBF Kernel) Training Accuracy Score = %.3f' % train_accuracy_rbf)
print('SVC (RBF Kernel) Testing Accuracy Score = %.3f' % test_accuracy_rbf)
train_accuracy_poly= poly.score(X_train,y_train)
test_accuracy_poly= poly.score(X_test,y_test)
print('SVC (3rd-Degree Polynomial Kernel) Training Accuracy Score = %.3f' % train_accuracy_poly)
print('SVC (3rd-Degree Polynomial Kernel) Testing Accuracy Score = %.3f' % test_accuracy_poly)

######################################################

################ EDIT CODE LINES HERE #################
# Visulaize confusion matrix

cm_logistic = confusion_matrix(y_test, y_test_pred_logistic, labels=logistic_model.classes_)
disp = ConfusionMatrixDisplay(confusion_matrix=cm_logistic, display_labels=logistic_model.classes_)
disp.plot()
plt.title("Logistic Regression Confusion Matrix")

# Visualizing SVC-RBF Confusion Matrix

cm_rbf = confusion_matrix(y_test, y_test_pred_rbf, labels=rbf.classes_)
disp = ConfusionMatrixDisplay(confusion_matrix=cm_rbf, display_labels=rbf.classes_)
disp.plot()
plt.title("SVC (RBF Kernel) Confusion Matrix")

# Visualizing SVC-Polynomial Confusion Matrix

cm_poly = confusion_matrix(y_test, y_test_pred_poly, labels=poly.classes_)
disp = ConfusionMatrixDisplay(confusion_matrix=cm_poly, display_labels=poly.classes_)
disp.plot()
plt.title("SVC (3rd-Degree Polynomial Kernel) Confusion Matrix")

######################################################

################ EDIT CODE LINES HERE #################
# Calculating f1 score

print("\033[1m" + "\033[4m" + "Classification Report for Logistic Regression")
print("\033[0m")
print(classification_report(y_test, y_test_pred_logistic))

# storing f1 score for SVC-RBF
print("\033[1m" + "\033[4m" + "Classification Report for SVC-RBF")
print("\033[0m")
f1_score_rbf= f1_score(y_test, y_test_pred_rbf, average='weighted')
print(classification_report(y_test, y_test_pred_rbf))

# storing f1 score for SVC-Polynomial
print("\033[1m" + "\033[4m" + "Classification Report for SVC-Polynomial")
print("\033[0m")
f1_score_poly= f1_score(y_test, y_test_pred_poly, average='weighted')
print(classification_report(y_test, y_test_pred_poly))

######################################################

################ EDIT CODE LINES HERE #################
# Calculating ROC AUC score




# Extract the probabilities for class 1
lr_probs_class1 = lr_probs[:, 1]

# Calculate ROC-AUC scores for logistic regression
ns_probs = [1 for _ in range(len(y_test))]
ns_auc = roc_auc_score(y_test, ns_probs)
lr_auc = roc_auc_score(y_test, lr_probs_class1)

# Print the results
print("\033[1m" + "\033[4m" + "ROC-AUC scores for Logistic Regression")
print("\033[0m")
print("No Skill ROC-AUC:", ns_auc)
print("Logistic Regression ROC-AUC:", lr_auc)


# summarize scores
print('No Skill Classifier: ROC AUC=%.3f' % (ns_auc))
print('Logistic Classifier: ROC AUC=%.3f' % (lr_auc))

print("\033[1m" + "\033[4m" + "ROC-AUC scores for SVC_RBF and SVC-Polynomial")
print("\033[0m")
# Calculate ROC AUC for the RBF kernel SVM model
y_test_pred_rbf_proba = rbf.predict_proba(X_test)[:, 1]
auc_score_rbf = roc_auc_score(y_test, y_test_pred_rbf_proba)


# Calculate ROC AUC for the Polynomial kernel SVM model
y_test_pred_poly_proba = poly.predict_proba(X_test)[:, 1]
auc_score_poly = roc_auc_score(y_test, y_test_pred_poly_proba)

print('SVC (RBF Kernel) Classifier: ROC AUC=%.3f' % auc_score_rbf)
print('SVC (3rd-Degree Polynomial Kernel) Classifier: ROC AUC=%.3f' % auc_score_poly)


######################################################

"""[Write your answer here]

Lets analyze the training/testing errors/accuracy for logistic regression and both the kernels for Support Vector Classifier. Logically, the greater the accuracy score, the lower the error score. SVC with RBF Kernel had the lowest training error at 7.4%, and in other words the highest testing accuracy at 92.6%. Logistic Regression came in second, with a training error of 8.4% and a training accuracy of 91.6%, just 1% less than that of SVC-RBF. SVC with a 3rd-Degree Polynomial Kernel performed the worst on the training dataset, with a training error of 11.1% and a training accuracy of 88.9%. Based on these metrics we should analyze the testing accuracy compared to the training accuracy. For SVC-RBF, the testing accuracy was  87.5%, which is not a substantial difference compared to the training accuracy (92.6%), but suggests some overfitting. The model still generalizes well and is less prone to overfitting. The logistic regression model has a testing accuracy equal to that of SVC-RBF (87.5%), suggesting that both are less prone to overfitting and can generalize well. The SVC-Polynomial's testing accuracy was lower at 85.4%, suggesting that the model may be underfitting the data compared to the SVC-RBF and logistic regression models. However, the difference between its training accuracy is not substantial, so there is still a slight chance of overfitting.

Now, let's analyze the confusion matrices. The SVC-RBF Kernel and logistic regression had the same exact confusion matrices. They both have 24 instances of true negative (so when the models predicted 0, the true outcome was 0), 18 true positives (so when the models predicted 1, the true outcome was 1), and just 4 instances of false negatives and 2 isntances of false positives. On the other hand, the SVC-Polynomial performed slightly worse, with 5 instances of false positives, and fewer true negatives (21). It did have more true positives (20), suggesting that this model is slightly more flexible in fitting complex patterns and that handled the decision boundary slightly better (only if we consider true positive outcomes)

The F1 scores for both logistic regression and SVC-RBF were very high at 0.89 for class 0 and 0.86 for class 1. These high scores indicate that both models perform well and have a good balance between precision and recall, basically indicating that the models are accurate and predict the correct outcome the majority of the time. The F1 scores for SVC-Polynomial were not as high, at 0.86 and 0.85 for class 0 and 1 respectively. These scores still demonstrate well-performing models, and as of now the logistic regression and SVC-RBF are equally as good.

Lastly, the ROC-AUC scores were really good. For both the logistic regression and SVC-RBF, the score was 0.946, indicating that these are well-performing models, much better than the no-skill classifier. This means that they do not just randomly guess. The SVC-Polynomial model had a score of 0.932, slightly lower than the other two, but still indicating strong models that do not randomly guess.

Overall, the logistic regression and SVC-RBF were equally as good, and the SVC-Polynomial model was slightly worse. However, all 3 models performed very well on this dataset.

## Problem 2: Corporate Bond Ratings Prediction

Companies issue bonds, which are debt securities, to raise funds that can be used to invest in the long-term future of the company. A corporate bond is a debt instrument from a company that investors can buy and, in doing so, pay the company the value of the bond upfront, which is called the principal amount. In return, the company pays the investor interest (called a coupon rate) on the bond's principal amount via periodic interest payments. At the bond's maturity date, which is typically in one to five years, the principal is paid back to the investor. Before investors buy a corporate bond, they need to know how financially stable the company that issued the bond is because this implies the ability of the company to pay back the bond obligations. Investors know this by looking at the bond ratings.

According to Fitch Ratings,  bond rating of triple-A (AAA) signifies the highest investment grade and means that there is a very low credit risk. "AA" represents very high credit quality; "A" means high credit quality, and "BBB" is a satisfactory credit quality. These ratings are considered to be investment grade, which means that the security or entity being rated carries a high-enough quality level for most financial institutions to make investments in those securities. "BBB" is the lowest rating of investment-grade securities, while ratings below "BBB", like "C" or "D" is the lowest or junk quality.  

You are the head of Investment Analytics in a hedge fund company. Your subordinates gathered some financial metrics (e.g., current ratio, asset turnover) of 593 companies for you from 1/10/2014 to 9/9/2016. This data set is in the "corporate_rating.csv" file. Your goal is to predcit the bond ratings of companies that exhibit different financial properties based on these metric values.

<p style="color:red;"> Please add as many new code chunks as you need for this problem. </p>

a) Please load in the financial metrics data that your subordinate collects. Please drop any columns thaat are irrelevant in predicting the bond ratings, namely 'Name', 'Symbol', and 'Rating Agency Name'.

Set the 'Date' column to be your index column.
"""

################ EDIT CODE LINES HERE #################

# loading corporate bond .csv file

bond_rating = pd.read_csv('/content/drive/MyDrive/DSQFRM/Week 4/bond_rating.csv'); bond_rating = bond_rating.set_index('Date')
bond_rating.info()

# dropping irrelevant columns
# Drop the columns 'Name', 'Symbol', and 'Rating Agency Name'
bond_rating.drop(['Name', 'Symbol', 'Rating Agency Name'], axis=1, inplace=True)
bond_rating.info()

######################################################

"""b) Please identify your explanatory and response variables.

[Write your answer here]

The response variable is the bond rating (Rating). The explanatory variables are currentRatio, quickRatio, cashRatio, daysOfSalesOutstanding, netProfitMargin, pretaxProfitMargin, grossProfitMargin, operatingProfitMargin, returnOnAssets, returnOnCapitalEmployed, returnOnEquity, assetTurnover, fixedAssetTurnover, debtEquityRatio, debtRatio, effectiveTaxRate, freeCashFlowOperatingCashFlowRatio, freeCashFlowPerShare, cashPerShare, companyEquityMultiplier, ebitPerRevenue, enterpriseValueMultiple, operatingCashFlowPerShare, operatingCashFlowSalesRatio, payablesTurnover

c) Please use Exploratory Data Analysis (EDA) techniques that you've learned to Visualize and pre-process the data set.
For every techniques used, you must give the reason as to why you used them.

(Hint 1: You must encode the rating classes into numerical values for the model to interpret)<br>
(Hint 2: If you use feature importance, please drop feature with scores < 0.04)<br>
(Hint 3: When balancing labels, you can remove observations with labels that exists < 5% of the time)
"""

################ EDIT CODE LINES HERE #################
# Please create as many code chunks as you'd like to help with your EDA & data pre-processing

# BOX PLOTS

# Filter out non-numeric columns if any
numerical_features = bond_rating.select_dtypes(include='float64')

# Setting up the figure and axis for subplots
fig, axes = plt.subplots(nrows=5, ncols=6, figsize=(20, 15))

# Flatten the axes array to iterate through features
axes = axes.ravel()

# Loop through each numerical feature and create box plots
for i, feature in enumerate(numerical_features.columns):
    axes[i].boxplot(numerical_features[feature], vert=False)
    axes[i].set_title(f"Boxplot of {feature}")
    axes[i].set_xlabel(feature)

# Remove any empty subplots, if there are fewer than 26 features
for j in range(len(numerical_features.columns), len(axes)):
    fig.delaxes(axes[j])

# Adjust layout and display the plots
plt.tight_layout()
plt.show()







######################################################

# HISTOGRAMS

# Excluding the 'Rating' column (response variable) from the numerical features
numerical_features = bond_rating.drop(columns=['Rating']).select_dtypes(include='float64')

# Setting up the figure and axis for subplots
fig, axes = plt.subplots(nrows=5, ncols=5, figsize=(20, 15))

# Flatten the axes array to iterate through features
axes = axes.ravel()

# Loop through each numerical feature and create histograms
for i, feature in enumerate(numerical_features.columns):
    _, bins, _ = axes[i].hist(numerical_features[feature], bins=50, density=1, alpha=0.5)
    axes[i].set_title(f"Histogram of {feature}")
    axes[i].set_xlabel(feature)
    axes[i].set_ylabel("Density")

# Remove any empty subplots, if there are fewer than 25 features (excluding 'Rating')
for j in range(len(numerical_features.columns), len(axes)):
    fig.delaxes(axes[j])

# Adjust layout and display the plots
plt.tight_layout()
plt.show()

# QQ PLOTS

# Excluding the 'Rating' column (response variable) from the numerical features
numerical_features = bond_rating.drop(columns=['Rating']).select_dtypes(include='float64')

# Setting up the figure and axis for subplots
fig, axes = plt.subplots(nrows=5, ncols=5, figsize=(20, 15))

# Flatten the axes array to iterate through features
axes = axes.ravel()

# Loop through each numerical feature and create Normal QQ plots
for i, feature in enumerate(numerical_features.columns):
    stats.probplot(numerical_features[feature], dist='norm', plot=axes[i], fit=True)
    axes[i].set_title(f"Normal QQ Plot of {feature}")
    axes[i].set_ylabel('Sample quantiles')

# Remove any empty subplots, if there are fewer than 25 features (excluding 'Rating')
for j in range(len(numerical_features.columns), len(axes)):
    fig.delaxes(axes[j])

# Adjust layout and display the plots
plt.tight_layout()
plt.show()

bond_rating.iloc[:, 1:] = scale(bond_rating.iloc[:, 1:]) # standardizing indicators
bond_rating.head()

# REMOVING OUTLIERS

# Function to remove outlying values that lie > 3 standard deviations away from the mean
def remove_outliers(df, n_std):
    numerical_columns = df.select_dtypes(include='float64').columns
    for col in numerical_columns:
        print('Working on column: {}'.format(col))

        mean = df[col].mean() # mean
        sd = df[col].std() # standard deviation

        df = df[(df[col] <= mean + (n_std * sd))] # criteria

    return df


bond_rating1 = remove_outliers(bond_rating, 3)
bond_rating1.info()

# ENCODING RATING

# Declare an encoder that helps convert outcome strings to labels
le = LabelEncoder()
le.fit(bond_rating1.iloc[:, 0])
bond_rating1.Rating = le.fit_transform(bond_rating1.iloc[:, 0])
le_name_mapping = dict(zip(le.classes_, le.transform(le.classes_)))
le_name_mapping

# FEATURE IMPORTANCE WITH RANDOM FOREST CLASSIFIER

X_train, X_test, y_train, y_test = train_test_split(bond_rating1.iloc[:, 1:], bond_rating1.iloc[:, 0], test_size=0.2, random_state=0)

from sklearn.ensemble import RandomForestClassifier # importing the random forest module

rf_model = RandomForestClassifier(random_state=0)
rf_model.fit(X_train, y_train)

importances = rf_model.feature_importances_
indices = np.argsort(importances)

# Use the column names of X_train as y-axis labels
plt.title('Feature Importances in the Random Forest Model')
plt.barh(range(len(indices)), importances[indices], align='center')
plt.yticks(range(len(indices)), X_train.columns[indices])
plt.xlabel('Importance Score')
plt.show()

indices = np.argsort(importances)[::-1]  # Sort the indices in descending order

# Print feature names and importance scores in descending order
for idx in indices:
    print(f"Feature: {X_train.columns[idx]}, Importance Score: {importances[idx]:.4f}")

# Create a list of features to drop
features_to_drop = [feature for feature, importance in zip(bond_rating1.iloc[:, 1:], importances) if importance < 0.04]

# Drop the features from your DataFrame
bond_rating1.drop(features_to_drop, axis=1, inplace=True)

# Print the remaining features after dropping
print(bond_rating1.columns)

RESPONSE = 'Rating'
FEATURES = bond_rating1.columns.to_list(); FEATURES.remove(RESPONSE)# explanatory variables

from statsmodels.stats.outliers_influence import variance_inflation_factor

# Compute VIF to identify high correlations b/w features
VIF = [variance_inflation_factor(bond_rating1.loc[:, FEATURES].values, i) for i in range(len(FEATURES))]
VIF_table = pd.DataFrame({'Numerical Features': FEATURES, 'VIF': VIF})
VIF_table

# Features to drop based on high VIF values
features_to_drop = ['returnOnAssets', 'returnOnCapitalEmployed', 'cashPerShare',
                    'operatingCashFlowPerShare', 'operatingCashFlowSalesRatio',
                    'payablesTurnover']

# Drop the features from the DataFrame
bond_rating1 = bond_rating1.drop(columns=features_to_drop)

# Verify that the features have been dropped
print(bond_rating1.info())

# LABEL BALANCING

# Visualize the distribution of ratings in the bond_rating1 DataFrame
ax = sns.countplot(x="Rating", data=bond_rating1)
plt.title('Distribution of Bond Ratings')
plt.xlabel('Ratings')

# Calculate the total number of samples
total = len(bond_rating1["Rating"])

# Annotate each bar with the percentage of samples in that category
for p in ax.patches:
    percentage = '{:.2f}%'.format(100 * p.get_height() / total)
    x_coord = p.get_x()
    y_coord = p.get_height() + 0.02
    ax.annotate(percentage, (x_coord, y_coord))

# Show the plot
plt.show()

# Calculate the frequency distribution of each label in the "Rating" column
rating_counts = bond_rating1["Rating"].value_counts(normalize=True)

# Identify the labels that occur less than 5% of the time
labels_to_drop = rating_counts[rating_counts < 0.05].index
print(labels_to_drop)

# Drop the rows corresponding to these labels from the DataFrame
bond_rating2 = bond_rating1[~bond_rating1["Rating"].isin(labels_to_drop)]

bond_rating2.info()

X_train, X_test, y_train, y_test = train_test_split(bond_rating2.loc[:, FEATURES], bond_rating2.loc[:, RESPONSE], test_size=0.2, random_state=0)

"""[Description of EDA techniques]

After plotting box plots, histograms, and QQ plots for all my features, I realized that none of them are normally distributed and are all over the place, so now I know I need to pre-process. Specifically, I see outliers need to be removed, and I need to standardize and eliminate unimportant features.

[Description of data pre-processing techniques]

After my EDA, I realized I had to do a few things. First, I standarized all my features to fit a normal distribution features. Then, I removed all outliers that lie 3 standard deviations away from the mean. I then encoded the ratings into numbers, and I found feature importance. I dropped features with importance less than 0.04. I did label balancing and dropped the rating labels that appeared less than 5% of times. I also dropped features with a VIF score of greater than 10.

At the end, I re-split my data into 80-20 train-test split.

d) Implement AT LEAST TWO classification models to predict the bond ratings based on their financial metrics features, then output their performance results. Why did you choose these methods?
"""

################ EDIT CODE LINES HERE #################
# Implementation - Model 1
# Please create as many code chunks as you'd like to implement your model


from sklearn.neighbors import KNeighborsClassifier
# Specifying the K of K-Fold CV
k_cv = 5
# choose k between 1 to 30
k_range = range(1, 50)
k_accuracy = []
# use iteration to caclulator different k in the KNN model, then return the average accuracy based on the cross validation
for k in k_range:
    knn = KNeighborsClassifier(n_neighbors=k)
    accuracy = cross_val_score(knn, bond_rating2.loc[:, FEATURES], bond_rating2.loc[:, RESPONSE], cv=k_cv, scoring='accuracy')
    k_accuracy.append(accuracy.mean())

plt.plot(k_range, k_accuracy)
plt.title('KNN Accuracy Score with '+str(k_cv)+'-Fold Cross Validation')
plt.xlabel('Value of K for KNN')
plt.ylabel('Cross-Validated Accuracy Score')
plt.show()







######################################################

# # build KNN model and choose n_neighbors
knn = KNeighborsClassifier(n_neighbors=40)
# train the model
knn.fit(X_train, y_train)
# predicted liquidity strengths
y_train_pred_knn = knn.predict(X_train)
y_test_pred_knn = knn.predict(X_test)

train_error_knn= 1-knn.score(X_train,y_train)
test_error_knn= 1-knn.score(X_test,y_test)
print('KNN Training Error = %.3f' % train_error_knn)
print('KNN Testing Error = %.3f' % test_error_knn)

train_accuracy_knn= knn.score(X_train,y_train)
test_accuracy_knn= knn.score(X_test,y_test)
print('KNN Training Accuracy Score = %.3f' % train_accuracy_knn)
print('KNN Testing Accuracy Score = %.3f' % test_accuracy_knn)

cm_knn = confusion_matrix(y_test, y_test_pred_knn, labels=knn.classes_)
disp = ConfusionMatrixDisplay(confusion_matrix=cm_knn, display_labels=knn.classes_)
disp.plot()
plt.title("KNN Confusion Matrix")

# printing full report
f1_score_knn= f1_score(y_test, y_test_pred_knn, average='weighted')
print(classification_report(y_test, y_test_pred_knn))

# calculating probabilites
y_test_pred_knn_proba = knn.predict_proba(X_test)
auc_score_knn = roc_auc_score(y_test, y_test_pred_knn_proba, multi_class='ovr') #'ovr' b/c multi-class problem
print('KNN Classifier: ROC AUC=%.3f' % auc_score_knn)

"""[Description of Model 1]

I choose KNN because it is non-parametric model, meaning it does not assume anything about the data, especially that it is normally distributed. My data is not normally distributed, so this model should work well.
"""

################ EDIT CODE LINES HERE #################
#Implementation - Model 2
# Please create as many code chunks as you'd like to implement your model


# Create the parameter grid based on the results of random search
from sklearn.ensemble import BaggingClassifier
param_grid = {
    'n_estimators': [10, 25, 50, 100, 200, 300, 1000],
    'max_samples':[1, 5, 10],
    'max_features': [1, 2 , 3 , 4]
}
# Create a based model
bagging = BaggingClassifier()
# Instantiate the grid search model
grid_search = GridSearchCV(estimator = bagging, param_grid = param_grid, cv = 5, n_jobs = -1, verbose = 2)
# fit the grid search to the training data
grid_search.fit(X_train, y_train)
grid_search.best_params_







######################################################

# Creating a Bagging classifier
bagging = BaggingClassifier(max_features= 4, max_samples= 10, n_estimators= 25)
# fit the bagging on the training data
bagging.fit(X_train, y_train)

# predicted liquidity strengths
y_train_pred_bagging = bagging.predict(X_train)
y_test_pred_bagging = bagging.predict(X_test)

train_error_bagging= 1-bagging.score(X_train,y_train)
test_error_bagging= 1-bagging.score(X_test,y_test)
print('Bagging Training Error = %.3f' % train_error_bagging)
print('Bagging Testing Error = %.3f' % test_error_bagging)

train_accuracy_bagging= bagging.score(X_train,y_train)
test_accuracy_bagging= bagging.score(X_test,y_test)
print('Bagging Training Accuracy Score = %.3f' % train_accuracy_bagging)
print('Bagging Testing Accuracy Score = %.3f' % test_accuracy_bagging)

cm_bagging = confusion_matrix(y_test, y_test_pred_bagging, labels=bagging.classes_)
disp = ConfusionMatrixDisplay(confusion_matrix=cm_bagging, display_labels=bagging.classes_)
disp.plot()
plt.title("Bagging Confusion Matrix")

# storing f1 score
f1_score_bagging= f1_score(y_test, y_test_pred_bagging, average='weighted')
print(classification_report(y_test, y_test_pred_bagging))

y_test_pred_bagging_proba = bagging.predict_proba(X_test)
auc_score_bagging = roc_auc_score(y_test, y_test_pred_bagging_proba, multi_class='ovr')
print('Bagging Method: ROC AUC=%.3f' % auc_score_bagging)

"""[Description of Model 2]

I choose bagging ensemble next, for similar reasons. It is non-parametric so it does not assume normal distribution. Also, bagging is supposedly a better ensemble method

e) Compare your models' performance results from above. What can you conclude from this? Which model performs the best?
"""

################ EDIT CODE LINES HERE #################
# Model performances



df = pd.DataFrame(data={
    'Model': ['KNN', 'Bagging'],
    'Train Error': [train_error_knn, train_error_bagging],
    'Test Error': [test_error_knn, test_error_bagging],
    'Train Accuracy': [train_accuracy_knn, train_accuracy_bagging],
    'Test Accuracy': [test_accuracy_knn, test_accuracy_bagging],
    'F1 Score': [f1_score_knn, f1_score_bagging],
    'AUC Score': [auc_score_knn, auc_score_bagging]
})

df

######################################################

"""[Write your answer here]


Both models performed relatively poorly. I think this is because of the amount of ratings (not features) that were dropped. We dropped a number of ratings and had few features so the model is only able to predict a few ratings (instead of all of them). We see that both have low accuracy scores (KNN = 36% and Bagging = 41%), and they have low F1 scores as well. This means there is not a good balance between precision and recall, so the models both perform poorly on testing data. The AUC scores were also very low (both around 60%), meaning they are hardly better than a no-skill classifier (50% AUC).

f) How do you think bond ratings can affect stock prices?

[Write your answer here]

I think that since bond ratings measure a company's reliability/financial strength as well as credit risk, the bond ratings can be used for an investor to decide if a company is doing well and is not risky. This can boost confidence in the company, causing investors to buy more stock, hence driving stock prices up. So a higher bond rating could increase stock prices if investor perception is a factor.
"""