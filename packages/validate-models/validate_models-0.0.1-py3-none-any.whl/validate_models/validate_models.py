
def validation_inputs():
    import pandas
    import statsmodels.api
    from scipy.stats import probplot
    from sklearn.exceptions import NotFittedError
    from sklearn.inspection import permutation_importance
    from sklearn.model_selection import cross_val_score, cross_val_predict
    from sklearn.metrics import (r2_score, mean_squared_error, mean_absolute_error, 
                                 mean_absolute_percentage_error, mean_squared_log_error, 
                                 make_scorer, roc_curve, accuracy_score, balanced_accuracy_score, 
                                 precision_score, recall_score, f1_score, roc_auc_score, 
                                 average_precision_score, confusion_matrix, auc, 
                                 precision_recall_curve)
    from sklearn.calibration import calibration_curve
    import matplotlib.pyplot
    import plotly.express
    import plotly.graph_objects
    import seaborn
    from IPython.display import display, Markdown
    import ipywidgets
    import numpy

    descriptions = {
        'model': 'This is the already trained model, compatible with the Scikit-Learn framework. It can be a Scikit-Learn pipeline with a model as the last step. This model has already learned the patterns of the data and is ready to make predictions. For regression problems, the model must have the .predict method. In classification problems, in addition to .predict, the .predict_proba method is also needed.',
        'X_train': 'These are the data used to train the model. They are structured observations and variables that the model used to learn.',
        'y_train': 'These are the labels or target values associated with the training data. They served as an answer to the model during the training phase.',
        'X_test': 'These are new data, which the model has not yet seen. They will be used to evaluate the performance of the model, simulating a real situation.',
        'y_test': 'These are the labels or target values of the test data. They will serve as a reference to compare the predictions of the model and evaluate its performance.',
        'cv': 'This parameter is used as the number of divisions (folds) for cross-validation when using the Scikit-Learn cross_val_score function. It is essential to calculate the model\'s CV (Cross Validation Score). A higher value implies that the estimate of the model\'s generalization capacity is more robust, as it uses more divisions for validation. However, this can also increase computational time.',
        'nbinbs': 'The number of bins in the data histogram. This value can affect the interpretation of results, by determining the level of detail in the data visualization.',
        'n_repeats': 'This is the number of times we repeat the evaluation of the feature importance, by permutation. More repeats can give a more accurate view of which features are most relevant for the model predictions.'
    }

    def display_description(input):
        display(Markdown(f"<div style='background: #ffffff; color: #000000; padding: 0.5em; margin: 0.5em 0; font-family: Arial, sans-serif;'><h2 style='background: #c0c0c0; display: inline-block; padding: 0.2em 0.5em;'>{input}</h2><p>{descriptions[input]}</p></div>"))

    dropdown = ipywidgets.Dropdown(options=list(descriptions.keys()))
    ipywidgets.interact(display_description, input=dropdown)
    
def validate_regression(model, X_train, y_train, X_test, y_test, cv, nbins, n_repeats):
    import pandas
    import statsmodels.api
    from scipy.stats import probplot
    from sklearn.exceptions import NotFittedError
    from sklearn.inspection import permutation_importance
    from sklearn.model_selection import cross_val_score, cross_val_predict
    from sklearn.metrics import (r2_score, mean_squared_error, mean_absolute_error, 
                                 mean_absolute_percentage_error, mean_squared_log_error, 
                                 make_scorer, roc_curve, accuracy_score, balanced_accuracy_score, 
                                 precision_score, recall_score, f1_score, roc_auc_score, 
                                 average_precision_score, confusion_matrix, auc, 
                                 precision_recall_curve)
    from sklearn.calibration import calibration_curve
    import matplotlib.pyplot
    import plotly.express
    import plotly.graph_objects
    import seaborn
    from IPython.display import display, Markdown
    import ipywidgets
    import numpy
    from plotly.subplots import make_subplots


    ### Transforming y_test and y_train into numpy.array if they are not already in that format.

    if not isinstance(y_test, numpy.ndarray):
         y_test = numpy.array(y_test)

    if not isinstance(y_train, numpy.ndarray):
         y_train = numpy.array(y_train)


    ### Testing if the model is already trained, otherwise the model or pipeline is trained with the default parameters.

    try:


        y_pred = model.predict(X_test)
        y_train_pred = model.predict(X_train)


    except NotFittedError:


        print("Pipeline aka Model Not Trained Yet..... Training......... model with Default Pipeline Have you set_params yet?")

        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        y_train_pred = model.predict(X_train)
    
    def mean_absolute_percentage_error(y_true, y_pred): 
        
        
        
        return numpy.mean(numpy.abs((y_true - y_pred) / y_true)) * 100   
    
        ###### Veio olhar o código né?? :D     
    def evaluation_metrics():

        y_train_pred = model.predict(X_train)
        y_pred = model.predict(X_test)

        r2_train = r2_score(y_train, y_train_pred)
        r2_test = r2_score(y_test, y_pred)

        rmse_train = numpy.sqrt(mean_squared_error(y_train, y_train_pred))
        rmse_test = numpy.sqrt(mean_squared_error(y_test, y_pred))

        mae_train = mean_absolute_error(y_train, y_train_pred)
        mae_test = mean_absolute_error(y_test, y_pred)

        mape_train = mean_absolute_percentage_error(y_train, y_train_pred) * 100
        mape_test = mean_absolute_percentage_error(y_test, y_pred) * 100

        scoring_dict = {
            'r2': 'r2',
            'rmse': make_scorer(mean_squared_error, greater_is_better=False, squared=False),
            'mae': 'neg_mean_absolute_error',
            'mape': make_scorer(mean_absolute_percentage_error, greater_is_better=False),
        }
        ##### BRAZILIAN BEAST &&&&&&&&&&&&&&&&& UNTOUCHABLE PRESENTS 
        cv_scores = {}
        for metric_name, scorer in scoring_dict.items():
            cv_score = cross_val_score(model, X_train, y_train, cv=cv, scoring=scorer)
            cv_scores[metric_name] = cv_score.mean()

        metrics = pandas.DataFrame({
            'Metric': ['R2', 'RMSE', 'MAE', 'MAPE'],
            'Train Value': [r2_train, rmse_train, mae_train, mape_train],
            'Test Value': [r2_test, rmse_test, mae_test, mape_test],
            'CV Score': [cv_scores['r2'], -cv_scores['rmse'], -cv_scores['mae'], -cv_scores['mape']]
        })

        fig = plotly.graph_objects.Figure(data=[plotly.graph_objects.Table(header=dict(values=['Metric', 'Train Data Value', 'Test Data Value', 'Cross Validation Score']),
                                       cells=dict(values=[metrics['Metric'], metrics['Train Value'], metrics['Test Value'], metrics['CV Score']]))])
        fig.show()  

    ### Function for Real Value Versus Predicted 


    def predicted_vs_real_graph():
        
        fig = make_subplots(rows=1, cols=2, subplot_titles=("Predicted vs Real - Train", "Predicted vs Real - Test"))

        fig.add_trace(
            plotly.graph_objects.Scatter(x=y_train, y=y_train_pred, mode='markers'),
            row=1, col=1
        )

        fig.add_trace(
            plotly.graph_objects.Scatter(x=[y_train.min(), y_train.max()], y=[y_train.min(), y_train.max()], mode='lines'),
            row=1, col=1
        )

        fig.add_trace(
            plotly.graph_objects.Scatter(x=y_test, y=y_pred, mode='markers'),
            row=1, col=2
        )

        fig.add_trace(
            plotly.graph_objects.Scatter(x=[y_test.min(), y_test.max()], y=[y_test.min(), y_test.max()], mode='lines'),
            row=1, col=2
        )

        fig.update_layout(height=600, width=1200, title_text="Predicted vs Real")
        fig.show()

    def residual_graph():
        
        fig = make_subplots(rows=1, cols=2, subplot_titles=("Residual Plot - Train", "Residual Plot - Test"))

        train_residuals = y_train - y_train_pred
        fig.add_trace(
            plotly.graph_objects.Scatter(x=y_train_pred, y=train_residuals, mode='markers'),
            row=1, col=1
        )

        fig.add_trace(
            plotly.graph_objects.Scatter(x=[y_train_pred.min(), y_train_pred.max()], y=[0, 0], mode='lines'),
            row=1, col=1
        )

        test_residuals = y_test - y_pred
        fig.add_trace(
            plotly.graph_objects.Scatter(x=y_pred, y=test_residuals, mode='markers'),
            row=1, col=2
        )

        fig.add_trace(
            plotly.graph_objects.Scatter(x=[y_pred.min(), y_pred.max()], y=[0, 0], mode='lines'),
            row=1, col=2
        )

        fig.update_layout(height=600, width=1200, title_text="Residual Plot")
        fig.show()


    def residual_histogram():
        
        fig = make_subplots(rows=1, cols=2, subplot_titles=("Residual Histogram - Train", "Residual Histogram - Test"))

        train_residuals = y_train - y_train_pred
        fig.add_trace(
            plotly.graph_objects.Histogram(x=train_residuals, nbinsx=nbins),
            row=1, col=1
        )

        test_residuals = y_test - y_pred
        fig.add_trace(
            plotly.graph_objects.Histogram(x=test_residuals, nbinsx=nbins),
            row=1, col=2
        )

        fig.update_layout(height=600, width=1200, title_text="Residual Histogram")
        fig.show()

    def qq_plot():
        
        fig, ax = matplotlib.pyplot.subplots(1, 2, figsize=(15, 5))

        train_residuals = y_train - y_train_pred
        statsmodels.api.qqplot(train_residuals, line ='45', ax=ax[0])
        ax[0].set_title('QQ Plot Residuals - Train')

        test_residuals = y_test - y_pred
        statsmodels.api.qqplot(test_residuals, line ='45', ax=ax[1])
        ax[1].set_title('QQ Plot Residuals - Test')

        matplotlib.pyplot.show()


    def permutation_feature_importance():

        scoring_dict = {
            'r2': 'r2',
            'rmse': make_scorer(mean_squared_error, greater_is_better=False, squared=False),
            'mae': 'neg_mean_absolute_error',
            'mape': make_scorer(mean_absolute_percentage_error, greater_is_better=False),
        }

        results_train = {}
        results_test = {}
        for metric_name, scorer in scoring_dict.items():
            result_train = permutation_importance(model, X_train, y_train_pred, scoring=scorer, n_repeats=10, random_state=42)
            result_test = permutation_importance(model, X_test, y_test, scoring=scorer, n_repeats=10, random_state=42)

            importance_df_train = pandas.DataFrame({'Variable': X_train.columns,
                                           'Importance Train': result_train.importances_mean,
                                           'Importance Standard Deviation Train': result_train.importances_std})

            importance_df_test = pandas.DataFrame({'Variable': X_test.columns,
                                           'Importance Test': result_test.importances_mean,
                                           'Importance Standard Deviation Test': result_test.importances_std})

            importance_df_train.sort_values(by='Importance Train', ascending=False, inplace=True)
            importance_df_test.sort_values(by='Importance Test', ascending=False, inplace=True)

            results_train[metric_name] = importance_df_train
            results_test[metric_name] = importance_df_test

            importance_difference = pandas.merge(importance_df_train, importance_df_test, on="Variable", suffixes=('_train', '_test'))
            importance_difference["Difference"] = abs(importance_difference['Importance Train'] - importance_difference['Importance Test'])

            fig = plotly.graph_objects.Figure()
            fig.add_trace(plotly.graph_objects.Bar(name='Train', 
                                 x=importance_df_train['Variable'], 
                                 y=importance_df_train['Importance Train'], 
                                 error_y=dict(array=importance_df_train['Importance Standard Deviation Train'])))

            fig.add_trace(plotly.graph_objects.Bar(name='Test', 
                                 x=importance_df_test['Variable'], 
                                 y=importance_df_test['Importance Test'], 
                                 error_y=dict(array=importance_df_test['Importance Standard Deviation Test'])))
            fig.update_layout(barmode='group', title=f'Permutation Feature Importance ({metric_name.upper()})')
            fig.show()


            fig_diff = plotly.graph_objects.Figure(data=[plotly.graph_objects.Table(header=dict(values=['Variable', 'Difference']),
                                                cells=dict(values=[importance_difference['Variable'], importance_difference['Difference']]))])
            fig_diff.show()

    

    def plot_explanation(plot_type):

        explanations = {
            'Evaluation Metrics': 
            '''
            Evaluation metrics are like a "report card" for our prediction model. Four important metrics to highlight are R2, RMSE, MAE, and MAPE.

            1- R2 (R-squared): Imagine you have a magnifying glass that allows you to see how well our "prediction line" fits the data points. That's R2. It tells us the proportion of variance in the data that is explained by the model. Its value ranges from 0 to 1, where 1 is the maximum score, indicating that our model perfectly predicts the data.

            2- RMSE (Root Mean Square Error): Here we measure the difference between what the model predicted and what actually happened. The lower the RMSE, the better. It's like measuring the distance between the points and our "prediction line".

            3- MAE (Mean Absolute Error): Similar to RMSE, MAE also measures the difference between predictions and reality. However, it doesn't give as much weight to large errors. It's like measuring the distance between the points and our "prediction line" without considering the very distant points as much.

            4- MAPE (Mean Absolute Percentage Error): MAPE gives us the average error in percentage terms. It's like calculating, on average, how much percent the model deviates from the predictions.

            5- CV Score (Cross-Validation Score): Imagine that we want to test how good our model is in different situations. For that, we divide the data into several parts and train the model several times, each time using different parts of the data. The average of these tests is the CV Score. It helps us have a more robust view of the model's performance.

            6- TRAIN_SCORE and TEST_SCORE: These are like final tests we give to our model. TRAIN_SCORE is like a test done with the material that the student studied, and TEST_SCORE is a surprise test with questions that the student has never seen before. If the grade on the surprise test is much lower, it may indicate that the student (or our model) memorized the material instead of actually learning it.
            ''',
            'Plot of Real Value vs Predicted Value':
            '''
            This plot is like a competition between what our model predicted and what actually happened. If our model were perfect, all points would align on the diagonal line.
            ''',

            'Residual Plot':
            '''
            Imagine if we could see the "face" of our model's errors. That's what the residual plot shows. If the errors appear "messy" and randomly distributed around zero, it's a good sign. If they appear "organized" or forming a pattern, the model may be making systematic errors.
            ''',

            'Residual Histogram':
            '''
            Imagine if our model's errors were students in a school, and we wanted to know how their grades are distributed. This histogram shows us that. If the grades (i.e., errors) follow a bell curve (normal distribution) centered around zero, it's a good sign. It means that the errors are balanced, and our model is not consistently biased towards one side or the other.
            ''',

            'Q-Q Plot':
            '''
            The Q-Q Plot is another way to check if our model's errors are well distributed. It's like checking if the students' grades are balanced. If the grades are well distributed, the points will lie on the diagonal line.
            ''',

            'Permutation Feature Importance':
            '''
            Imagine if we want to know which "subject" (or feature) weighs the most in our model's final grade. And we also want to know if the model is "cheating" (overfitting) on that subject. For that, we permute the features and see how it affects the result. If a subject has a high weight on the final grade and the model performs poorly when that subject is changed, it may indicate that the model is "cheating" on that subject. It's like trying to better understand the model's "learning process" to ensure that it will perform well on new questions.
            '''
        }

        text_widget = ipywidgets.Textarea(
            value=explanations[plot_type],
            layout=ipywidgets.Layout(width="100%", height="200px")
        )

        display(text_widget)

        plot_selected(plot_type)

    def plot_selected(plot_type):

        if plot_type == 'Evaluation Metrics':
            evaluation_metrics()
        elif plot_type == 'Plot of Real Value vs Predicted Value':
            predicted_vs_real_graph()
        elif plot_type == 'Residual Plot':
            residual_graph()
        elif plot_type == 'Residual Histogram':
            residual_histogram()
        elif plot_type == 'Q-Q Plot':
            qq_plot()
        elif plot_type == 'Permutation Feature Importance':
            permutation_feature_importance()

    dropdown = ipywidgets.Dropdown(options=['Evaluation Metrics', 'Plot of Real Value vs Predicted Value', 'Residual Plot', 'Residual Histogram', 'Q-Q Plot', 'Permutation Feature Importance'])
    ipywidgets.interact(plot_explanation, plot_type=dropdown)
    
    

def validate_binary_classification(model, X_train, y_train, X_test, y_test, cv, nbins, n_repeats):
    import pandas
    import statsmodels.api
    from scipy.stats import probplot
    from sklearn.exceptions import NotFittedError
    from sklearn.inspection import permutation_importance
    from sklearn.model_selection import cross_val_score, cross_val_predict
    from sklearn.metrics import (r2_score, mean_squared_error, mean_absolute_error, 
                                 mean_absolute_percentage_error, mean_squared_log_error, 
                                 make_scorer, roc_curve, accuracy_score, balanced_accuracy_score, 
                                 precision_score, recall_score, f1_score, roc_auc_score, 
                                 average_precision_score, confusion_matrix, auc, 
                                 precision_recall_curve)
    from sklearn.calibration import calibration_curve
    import matplotlib.pyplot
    import plotly.express
    import plotly.graph_objects
    import seaborn
    from IPython.display import display, Markdown
    import ipywidgets
    import numpy
    from plotly.subplots import make_subplots
    
    if not isinstance(y_test, numpy.ndarray):
        y_test = numpy.array(y_test)

    if not isinstance(y_train, numpy.ndarray):
        y_train = numpy.array(y_train)

    try:
        y_pred = model.predict(X_test)
        y_train_pred = model.predict(X_train)
        y_train_prob = model.predict_proba(X_train)[:, 1]
        y_test_prob = model.predict_proba(X_test)[:, 1]      

    except NotFittedError:
        print("Pipeline aka Model Not Yet Trained.....    training......... model with Default Pipeline Have you Set_PARAMS?")
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        y_train_pred = model.predict(X_train)
        y_train_prob = model.predict_proba(X_train)[:, 1]
        y_test_prob = model.predict_proba(X_test)[:, 1]
    
    
    def evaluation_metrics():
        y_train_pred = model.predict(X_train)
        y_pred = model.predict(X_test)

        y_train_prob = model.predict_proba(X_train)[:, 1]
        y_test_prob = model.predict_proba(X_test)[:, 1]

        acc_train = accuracy_score(y_train, y_train_pred)
        acc_test = accuracy_score(y_test, y_pred)

        b_acc_train=balanced_accuracy_score(y_train, y_train_pred)
        b_acc_test=accuracy_score(y_test, y_pred)

        prec_train = precision_score(y_train, y_train_pred)
        prec_test = precision_score(y_test, y_pred)

        rec_train = recall_score(y_train, y_train_pred)
        rec_test = recall_score(y_test, y_pred)

        f1_train = f1_score(y_train, y_train_pred)
        f1_test = f1_score(y_test, y_pred)

        auc_train = roc_auc_score(y_train, y_train_prob)
        auc_test = roc_auc_score(y_test, y_test_prob)

        pr_auc_train = average_precision_score(y_train, y_train_prob)
        pr_auc_test = average_precision_score(y_test, y_test_prob)

        scoring_dict = {
            'Accuracy': make_scorer(accuracy_score),
            'Balanced Accuracy': make_scorer(balanced_accuracy_score),
            'Precision': make_scorer(precision_score),
            'Recall': make_scorer(recall_score),
            'F1-Score': make_scorer(f1_score),
            'AUC-ROC': make_scorer(roc_auc_score, needs_proba=True),
            'PR AUC Score': make_scorer(average_precision_score, needs_proba=True),
        }

        cv_scores = {}
        for metric_name, scorer in scoring_dict.items():
            cv_score = cross_val_score(model, X_train, y_train, cv=cv, scoring=scorer,n_jobs=-1)
            cv_scores[metric_name] = cv_score.mean()

        metrics = pandas.DataFrame({
            'Metric': ['Accuracy', 'Balanced Accuracy', 'Precision', 'Recall', 'F1-Score', 'AUC-ROC', 'PR AUC Score'],
            'Train Value': [acc_train, b_acc_train, prec_train, rec_train, f1_train, auc_train, pr_auc_train],
            'Test Value': [acc_test, b_acc_test, prec_test, rec_test, f1_test, auc_test, pr_auc_test],
            'Cross-Validation Score': [cv_scores['Accuracy'], cv_scores['Balanced Accuracy'], cv_scores['Precision'], cv_scores['Recall'], cv_scores['F1-Score'], cv_scores['AUC-ROC'], cv_scores['PR AUC Score']]
        })

        fig = plotly.graph_objects.Figure(data=[plotly.graph_objects.Table(header=dict(values=['Metric', 'Train Value', 'Test Value', 'Cross-Validation Score']),
                                       cells=dict(values=[metrics['Metric'], metrics['Train Value'], metrics['Test Value'], metrics['Cross-Validation Score']]))])
        fig.show() 

    def confusion_matrix_plot():
        fig, ax = matplotlib.pyplot.subplots(1, 2, figsize=(15, 5))

        cm_train = confusion_matrix(y_train, y_train_pred)
        acc_train = accuracy_score(y_train, y_train_pred)
        b_acc_train = balanced_accuracy_score(y_train, y_train_pred)
        prec_train = precision_score(y_train, y_train_pred)
        rec_train = recall_score(y_train, y_train_pred)

        seaborn.heatmap(cm_train, annot=True, fmt="d", ax=ax[0], cmap='Blues', cbar=False, xticklabels=[0, 1], yticklabels=[0, 1])
        ax[0].set_title(f'Train\nAccuracy: {acc_train:.2f}\nBalanced Accuracy: {b_acc_train:.2f}\nPrecision: {prec_train:.2f}\nRecall: {rec_train:.2f}')
        ax[0].set_xlabel('Predicted')
        ax[0].set_ylabel('Actual')

        cm_test = confusion_matrix(y_test, y_pred)
        acc_test = accuracy_score(y_test, y_pred)
        b_acc_test = balanced_accuracy_score(y_test, y_pred)
        prec_test = precision_score(y_test, y_pred)
        rec_test = recall_score(y_test, y_pred)

        seaborn.heatmap(cm_test, annot=True, fmt="d", ax=ax[1], cmap='Blues', cbar=False, xticklabels=[0, 1], yticklabels=[0, 1])
        ax[1].set_title(f'Test\nAccuracy: {acc_test:.2f}\nBalanced Accuracy: {b_acc_test:.2f}\nPrecision: {prec_test:.2f}\nRecall: {rec_test:.2f}')
        ax[1].set_xlabel('Predicted')
        ax[1].set_ylabel('Actual')

        matplotlib.pyplot.show()

    def roc_auc_curve():
        fig, ax = matplotlib.pyplot.subplots(1, 2, figsize=(15, 5))

        fpr_train, tpr_train, _ = roc_curve(y_train, y_train_prob)
        roc_auc_train = auc(fpr_train, tpr_train)

        ax[0].plot(fpr_train, tpr_train, color='darkorange', lw=2, label=f'ROC curve (area = {roc_auc_train:.2f})')
        ax[0].plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
        ax[0].set_xlim([0.0, 1.0])
        ax[0].set_ylim([0.0, 1.05])
        ax[0].set_xlabel('False Positive Rate')
        ax[0].set_ylabel('True Positive Rate')
        ax[0].set_title('ROC Curve - Train')
        ax[0].legend(loc="lower right")

        fpr_test, tpr_test, _ = roc_curve(y_test, y_test_prob)
        roc_auc_test = auc(fpr_test, tpr_test)

        ax[1].plot(fpr_test, tpr_test, color='darkorange', lw=2, label=f'ROC curve (area = {roc_auc_test:.2f})')
        ax[1].plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
        ax[1].set_xlim([0.0, 1.0])
        ax[1].set_ylim([0.0, 1.05])
        ax[1].set_xlabel('False Positive Rate')
        ax[1].set_ylabel('True Positive Rate')
        ax[1].set_title('ROC Curve - Test')
        ax[1].legend(loc="lower right")

        matplotlib.pyplot.show()

    def precision_recall_curve_plot():
        fig, ax = matplotlib.pyplot.subplots(1, 2, figsize=(15, 5))

        precision_train, recall_train, _ = precision_recall_curve(y_train, y_train_prob)
        average_precision_train = average_precision_score(y_train, y_train_prob)

        ax[0].step(recall_train, precision_train, color='b', alpha=0.2, where='post')
        ax[0].fill_between(recall_train, precision_train, step='post', alpha=0.2, color='b')
        ax[0].set_xlabel('Recall')
        ax[0].set_ylabel('Precision')
        ax[0].set_ylim([0.0, 1.05])
        ax[0].set_xlim([0.0, 1.0])
        ax[0].set_title('Precision-Recall Curve: AP={0:0.2f}'.format(average_precision_train))

        precision_test, recall_test, _ = precision_recall_curve(y_test, y_test_prob)
        average_precision_test = average_precision_score(y_test, y_test_prob)

        ax[1].step(recall_test, precision_test, color='b', alpha=0.2, where='post')
        ax[1].fill_between(recall_test, precision_test, step='post', alpha=0.2, color='b')
        ax[1].set_xlabel('Recall')
        ax[1].set_ylabel('Precision')
        ax[1].set_ylim([0.0, 1.05])
        ax[1].set_xlim([0.0, 1.0])
        ax[1].set_title('Precision-Recall Curve: AP={0:0.2f}'.format(average_precision_test))
        matplotlib.pyplot.show()
        
    def probability_histogram():
        df_train = pandas.DataFrame({'Predicted Probability': y_train_prob, 'True Label': y_train, 'Data': 'Train'})
        df_test = pandas.DataFrame({'Predicted Probability': y_test_prob, 'True Label': y_test, 'Data': 'Test'})

        df = pandas.concat([df_train, df_test])

        fig = plotly.express.histogram(df, x='Predicted Probability', color='True Label', facet_col='Data', nbins=50, opacity=0.7,
                                       labels={'Predicted Probability': 'Predicted Probability', 'True Label': 'True Label'},
                                       title='Histogram of Predicted Probability')
        fig.show()

    def probability_density_plot():
        df_train = pandas.DataFrame({'Predicted Probability': y_train_prob, 'True Label': y_train, 'Data': 'Train'})
        df_test = pandas.DataFrame({'Predicted Probability': y_test_prob, 'True Label': y_test, 'Data': 'Test'})

        df = pandas.concat([df_train, df_test])

        fig = plotly.express.histogram(df, x='Predicted Probability', color='True Label', facet_col='Data', nbins=50, opacity=0.7,
                                       marginal='box', histnorm='density', barmode='overlay',
                                       labels={'Predicted Probability': 'Predicted Probability', 'True Label': 'True Label'},
                                       title='Probability Density Plot')
        fig.show()

    def probability_calibration_plot():
        prob_true_train, prob_predicted_train = calibration_curve(y_train, y_train_prob, n_bins=10)
        prob_true_test, prob_predicted_test = calibration_curve(y_test, y_test_prob, n_bins=10)

        fig = plotly.graph_objects.Figure()

        fig.add_trace(plotly.graph_objects.Scatter(x=prob_predicted_train, y=prob_true_train, mode='lines+markers', name='Train'))
        fig.add_trace(plotly.graph_objects.Scatter(x=prob_predicted_test, y=prob_true_test, mode='lines+markers', name='Test'))
        fig.add_shape(type='line', x0=0, x1=1, y0=0, y1=1, yref='y', xref='x', line=dict(color='Black', dash='dash'))

        fig.update_layout(title='Probability Calibration Plot', xaxis_title='Predicted Probability', yaxis_title='True Probability')

        fig.show()

    def permutation_feature_importance():
        scoring_dict = {
            'Accuracy': make_scorer(accuracy_score),
            'Balanced Accuracy': make_scorer(balanced_accuracy_score),
            'Precision': make_scorer(precision_score),
            'Recall': make_scorer(recall_score),
            'F1-Score': make_scorer(f1_score),
            'AUC-ROC': make_scorer(roc_auc_score, needs_proba=True),
            'PR AUC Score': make_scorer(average_precision_score, needs_proba=True),
        }

        results_train = {}
        results_test = {}
        for metric_name, scorer in scoring_dict.items():
            result_train = permutation_importance(model, X_train, y_train, scoring=scorer, n_repeats=10, random_state=42)
            result_test = permutation_importance(model, X_test, y_test, scoring=scorer, n_repeats=10, random_state=42)

            importance_df_train = pandas.DataFrame({'Feature': X_train.columns,
                                                   'Importance (Train)': result_train.importances_mean,
                                                   'Standard Deviation (Train)': result_train.importances_std})

            importance_df_test = pandas.DataFrame({'Feature':

     X_test.columns,
                                                   'Importance (Test)': result_test.importances_mean,
                                                   'Standard Deviation (Test)': result_test.importances_std})

            importance_df_train.sort_values(by='Importance (Train)', ascending=False, inplace=True)
            importance_df_test.sort_values(by='Importance (Test)', ascending=False, inplace=True)

            results_train[metric_name] = importance_df_train
            results_test[metric_name] = importance_df_test

            importance_difference = pandas.merge(importance_df_train, importance_df_test, on="Feature", suffixes=('_train', '_test'))
            importance_difference["Difference"] = abs(importance_difference['Importance (Train)'] - importance_difference['Importance (Test)'])

            fig = plotly.graph_objects.Figure()
            fig.add_trace(plotly.graph_objects.Bar(name='Train', 
                                 x=importance_df_train['Feature'], 
                                 y=importance_df_train['Importance (Train)'], 
                                 error_y=dict(array=importance_df_train['Standard Deviation (Train)'])))

            fig.add_trace(plotly.graph_objects.Bar(name='Test', 
                                 x=importance_df_test['Feature'], 
                                 y=importance_df_test['Importance (Test)'], 
                                 error_y=dict(array=importance_df_test['Standard Deviation (Test)'])))
            fig.update_layout(barmode='group', title=f'Permutation Feature Importance ({metric_name.upper()})')
            fig.show()

            fig_diff = plotly.graph_objects.Figure(data=[plotly.graph_objects.Table(header=dict(values=['Feature', 'Difference']),
                                                cells=dict(values=[importance_difference['Feature'], importance_difference['Difference']]))])
            fig_diff.show()

    
    
    def plot_explanation(plot_type):

        explanations = {
            'Evaluation Metrics':
            '''
            The evaluation metrics table is a crucial tool that aggregates various essential metrics for determining the efficiency of a binary classification model. It includes measures such as Accuracy, Balanced Accuracy, Precision, Recall (Sensitivity), F1-Score, Area Under the ROC Curve (AUC-ROC), and Area Under the Precision-Recall Curve (AUC-PR).

            Accuracy: This is the proportion of correct predictions made by the model out of all the predictions made.

            Balanced Accuracy: This is the average of accuracies obtained for each individual class. It is useful for dealing with situations where classes are imbalanced. This metric ranges from 0 to 1, where 1 indicates perfect performance.

            Precision: This is the proportion of true positive (TP) predictions made out of the total positive predictions, i.e., the sum of true positives (TP) and false positives (FP).

            Recall: This is the proportion of true positive (TP) predictions made out of the total samples that were actually positive, i.e., the sum of true positives (TP) and false negatives (FN).

            F1-Score: This is a harmonic mean of precision and recall and seeks a balance between the two.

            AUC-ROC: This is the area under the Receiver Operating Characteristic (ROC) curve. An ROC curve is a probability curve for different classes. AUC is a measure of the model's ability to distinguish between classes.

            AUC-PR: This is the area under the Precision-Recall curve. This curve plots precision against recall. AUC provides an aggregated evaluation of performance across all possible classification thresholds.

            CV Score (Cross-Validation Score):

            Cross-validation score is a technique for assessing the model's ability to generalize to new data. In cross-validation, the dataset is divided into multiple parts, and the model is trained and tested multiple times, each time on different parts of the data. This provides a robust estimate of the model's performance on unseen data.

            TRAIN_SCORE: This is the score obtained when evaluating the model on the same dataset used for training. If this score is much higher than the other two, it may indicate an overfitting problem, where the model has memorized the training data but is not able to generalize well to new data.

            TEST_SCORE: This is the score obtained when evaluating the model on a separate test dataset that was not used during training. If this score is significantly lower than TRAIN_SCORE, it again may indicate an overfitting problem.

            By analyzing the difference between TRAIN_SCORE, TEST_SCORE, and CV_SCORE, we can get an idea of how our model is performing on different datasets.
            ''',
            'Confusion Matrix':
            '''
            The confusion matrix is a table that facilitates the evaluation of the performance of a supervised learning algorithm. Each row represents instances of a predicted class by the algorithm, while each column represents instances of a true class. This clear presentation of true positives, true negatives, false positives, and false negatives allows us to understand how the model is classifying the information.
            ''',
            'AUC-ROC Curve':
            '''
            The AUC-ROC curve is a visual representation that shows how well the binary classification model is differentiating the classes. The graph plots the true positive rate against the false positive rate for different classification thresholds (Above which predicted probability value is considered as class 1). The more the model approaches the top-left corner of the graph (high true positive rate and low false positive rate), the more efficient it is.
            ''',
            'Precision-Recall Curve':
            '''
            The precision-recall

     curve is a graph that shows the balance between precision (the proportion of true positives among all positive predictions) and recall (the proportion of true positives among all positive instances). A model whose precision-recall curve approaches the top-right corner of the graph demonstrates a high level of precision and recall.
            ''',
            'Probability Histogram':
            '''
            The probability histogram is a chart that shows the distribution of predictions from a classification model in terms of probability. It allows for a more detailed analysis of the model's predictions by providing a visual representation of the probability associated with each prediction, which can help better understand the model's classification ability.
            ''',
            'Probability Density Plot':
            '''
            The probability density plot is a chart that shows the distribution of predictions from a classification model in a smoother way compared to the probability histogram. This visualization facilitates the identification of patterns and trends in the distribution of the model's predictions.
            ''',
            'Probability Calibration Plot':
            '''
            The probability calibration plot compares the probabilities predicted by the model with the observed frequencies. This visualization is useful for assessing whether the model's predicted probabilities are well-calibrated, meaning that the predicted probability matches the observed frequency of events.
            ''',
            'Permutation Feature Importance':
            '''
            In addition to identifying the most relevant features for the model's predictions, permutation feature importance also allows for analyzing the possibility of variable overfitting. The resulting graph from this analysis not only highlights the importance of features but also compares this importance in the training and testing data.

            This comparison plays a crucial role in evaluating model overfitting, also known as overfitting. If a feature has high importance in the training data but does not show the same relevance in the testing data, it can be an indicator of overfitting. In such a case, the model may be overly tuned to the training data, making it unable to generalize well to the testing data. This can lead to inaccurate predictions or failures when the model is exposed to new data.

            Therefore, permutation feature importance and its subsequent visual analysis in a graph provide crucial insights into the robustness and generalizability of the model, as well as the model's ability to make reliable predictions when confronted with new data.
            '''
        }

        text_widget = ipywidgets.Textarea(
            value=explanations[plot_type],
            layout=ipywidgets.Layout(width="100%", height="200px")
        )
        display(text_widget)

        plot_selected(plot_type)

    def plot_selected(plot_type):

        if plot_type == 'Evaluation Metrics':
            evaluation_metrics()

        elif plot_type == 'Confusion Matrix':
            confusion_matrix_plot()

        elif plot_type == 'AUC-ROC Curve':
            roc_auc_curve()

        elif plot_type == 'Precision-Recall Curve':
            precision_recall_curve_plot()

        elif plot_type == 'Probability Histogram':
            probability_histogram()

        elif plot_type == 'Probability Density Plot':
            probability_density_plot()

        elif plot_type == 'Probability Calibration Plot':
            probability_calibration_plot()

        elif plot_type == 'Permutation Feature Importance':
            permutation_feature_importance()

    dropdown = ipywidgets.Dropdown(options=['Evaluation Metrics', 'Confusion Matrix', 'AUC-ROC Curve', 'Precision-Recall Curve', 'Probability Histogram', 'Probability Density Plot', 'Probability Calibration Plot', 'Permutation Feature Importance'])

    ipywidgets.interact(plot_explanation, plot_type=dropdown)
