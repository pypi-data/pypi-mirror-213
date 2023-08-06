import os
import pathlib
import pickle
import shutil
import sys
from random import randint

import seaborn as sns

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from matplotlib import transforms

from keras.utils.np_utils import to_categorical
from keras.models import load_model

from matplotlib.collections import PathCollection
from matplotlib.legend_handler import HandlerPathCollection, HandlerLine2D
from matplotlib.patches import Ellipse
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from umap import UMAP

from fiiireflyyy import firefiles as ff


def k_fold_cross_validation_deprecated(k_fold, x, y, clf=None, loading=False, clf_path=''):
    """
    DEPRECATED - Compute a K-fold cross validation method.

    :param k_fold: Number of folds to split the dataset
    :param x: Features dataset
    :param y: target dataset
    :param clf: classifier object, if loading is False.
    :param clf_path: path of a classifier object, if loading is True.
    :param loading: Whether to load a classifier object from path or not.
    :return: k-fold scores, accuracy
    """
    if len(x) != len(y):
        raise ValueError("Features and Targets do not have the same length.")

    data_len = len(y)

    if loading:
        if clf_path == '':
            raise ValueError('No classifier path specified.')
        else:
            clf = pickle.load(open(clf_path, "rb"))
    elif clf is None:
        raise ValueError("no classifier object specified.")

    ori_x_train, ori_x_test, ori_y_train, ori_y_test = train_test_split(x, y, test_size=0.3)
    train_len = len(ori_y_train)
    test_len = len(ori_y_test)
    local_scores = []
    step = int(train_len / k_fold)
    clf.fit(ori_x_train, ori_y_train)
    for k in range(0, train_len - step, step):
        x_train_split = ori_x_train.iloc[k:k + step]
        y_train_split = ori_y_train.iloc[k:k + step]
        y_test_split = pd.concat([ori_y_test.iloc[0:k], ori_y_test.iloc[k + step:data_len]])
        x_test_split = pd.concat([ori_x_test.iloc[0:k], ori_x_test.iloc[k + step:data_len]])
        # clf.fit(x_train_split, y_train_split)
        local_scores.append(clf.score(x_test_split, y_test_split))

    return local_scores


def generate_classes(data_dir, destination, targets):
    """
    Generate a specific folder structure for Keras models by isolating classes as different folders.

    :param data_dir:
    :type data_dir: str
    :param destination: Where to generate the classes folders
    :type destination: str
    :param targets: the different classes to use
    :type targets: str
    :return:
    """
    ff.verify_dir(destination)
    files = ff.get_all_files(data_dir)

    # Creating directories architecture for keras model
    for target in targets:
        ff.verify_dir(os.path.join(destination, target))

        for file in files:
            if target in file:
                shutil.copy2(file, os.path.join(destination, target))





def train_RFC_from_dataset(dataset: pd.DataFrame, savepath=""):
    """
    Train a Random Forest Classifier model from an already formatted dataset.

        Parameters
        ----------
        dataset : pandas Dataframe
            a pandas Dataframe where each row is an entry for a machine
            learning model. Has a last column as 'target' containing
            the target value for each entry.

        savepath: str, optional, default:''
            name of the saved file. If empty, does not save the file.

            .. versionadded:: 1.0.0

        Returns
        -------
        out : tuple of size (1, 2).
            The first element is a trained random forest classifier.
            The second is its scores.
    """

    clf = RandomForestClassifier(n_estimators=1000)
    X = dataset[dataset.columns[:-1]]
    y = dataset["label"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.5)
    clf.fit(X_train, y_train)
    if savepath:
        pickle.dump(clf, open(savepath, "wb"))
    return clf, clf.score(X_test, y_test)


def get_top_features_from_trained_RFC(clf, **kwargs):
    """
    select to top n% feature sorted by highest importance, of a trained Random Forest Classtifier model.

        Parameters
        ----------
        clf : RandomForestClassifier
            a trained model

        **kwargs: keyword arguments
            percentage: float, optional, default: 0.05
                proportion of the most important features to keep

            show: bool, optional, default: True
                Whether to show a plot of the model feature importance or not.

            save: bool, optional, default: False
                Whether to save a plot of the model feature importance or not.

            title: str, optional, default: ''
                the title to give the plot and name of the resulting file if save if True.

            savepath: str, optional, default: ""
                If not empty, path where le result will be saved.

        Returns
        -------
        out : tuple of lists
            first element: list of the indexes of the most important features
            second element: importance (values) corresponding to the indexes.
    """
    options = {"percentage": 0.05,
               "show": True,
               "save": False,
               "title": "",
               "savepath": ""}
    options.update(**kwargs)

    importances_over_iterations = []
    for i in range(10):
        mean = np.mean([tree.feature_importances_ for tree in clf.estimators_], axis=0)

        importances_over_iterations.append(mean)

    arrays = [np.array(x) for x in importances_over_iterations]
    mean_importances_over_iterations = [np.mean(k) for k in zip(*arrays)]
    std_arrays = [np.array(x) for x in importances_over_iterations]
    std_importances_over_iterations = [np.std(k) for k in zip(*std_arrays)]

    low_std = []
    for i in range(len(mean_importances_over_iterations)):
        low_std.append(mean_importances_over_iterations[i] - std_importances_over_iterations[i])
    high_std = []
    for i in range(len(mean_importances_over_iterations)):
        high_std.append(mean_importances_over_iterations[i] + std_importances_over_iterations[i])

    hertz = []
    factor = 5000 / 300
    for i in range(300):
        hertz.append(int(i * factor))
    n = int(options["percentage"] * len(mean_importances_over_iterations))
    idx_foi = sorted(range(len(mean_importances_over_iterations)),
                     key=lambda i: mean_importances_over_iterations[i], reverse=True)[:n]

    plt.bar([x for x in range(300)], mean_importances_over_iterations, color="blue", )

    xticks = [x for x in range(0, 300, 50)]
    new_ticks = [hertz[x] for x in xticks]
    xticks.append(300)
    new_ticks.append(5000)
    plt.xticks(xticks, new_ticks)
    plt.ylabel("Relative importance [AU]")
    plt.xlabel("Frequency-like features [Hz]")
    plt.title(options["title"])
    if options["save"]:
        plt.savefig(options["savepath"])
    # plt.fill_between(hertz, low_std, high_std, facecolor="blue", alpha=0.5)
    if options["save"]:
        plt.show()
    plt.close()
    return idx_foi, mean_importances_over_iterations


def fit_pca(dataframe: pd.DataFrame, n_components=3):
    """
    fit a Principal Component Analysis and return its instance and dataset.

        Parameters
        ----------
        dataframe: DataFrame
            The data on which the pca instance has to be fitted.
        n_components: int, optional, default: 3
            The number of components for the PCA instance.

        Returns
        -------
        out: tuple of shape (1, 3)
            The first element is the PCA instance. The second
            element is the resulting dataframe. The third is the
            explained variance ratios.
    """
    features = dataframe.columns[:-1]
    x = dataframe.loc[:, features].values
    x = StandardScaler().fit_transform(x)  # normalizing the features
    pca = PCA(n_components=n_components)
    principalComponent = pca.fit_transform(x)
    principal_component_columns = [f"principal component {i + 1}" for i in range(n_components)]

    principal_tahyna_Df = pd.DataFrame(data=principalComponent
                                       , columns=principal_component_columns)

    principal_tahyna_Df["label"] = dataframe["label"]

    return pca, principal_tahyna_Df, pca.explained_variance_ratio_


def apply_pca(pca, dataframe):
    """
    Transform data using an already fit PCA instance.

        Parameters
        ----------
        pca: PCA instance
            The fitted PCA instance from what the data will
            be transformed.
        dataframe: DataFrame
            The data to transform using an already fitted PCA.
            Must have a 'label' column.

        Returns
        -------
        out: DataFrame
            The transformed data.
    """
    features = dataframe.columns[:-1]
    x = dataframe.loc[:, features].values
    x = StandardScaler().fit_transform(x)  # normalizing the features
    transformed_ds = pca.transform(x)
    transformed_df = pd.DataFrame(data=transformed_ds,
                                  columns=[f"principal component {i + 1}" for i in range(transformed_ds.shape[1])])
    transformed_df['label'] = dataframe['label']
    return transformed_df


def confidence_ellipse(x, y, ax, n_std=3.0, color='none', **kwargs):
    """
    Create a plot of the covariance confidence ellipse of *x* and *y*.

        Parameters
        ----------
        x, y : array-like, shape (n, )
            Input data.

        ax : matplotlib.axes.Axes
            The axes object to draw the ellipse into.

        n_std : float
            The number of standard deviations to determine the ellipse's radiuses.

        color : str
            color of the ellipsis.

        **kwargs
            Forwarded to `~matplotlib.patches.Ellipse`

        Returns
        -------
        matplotlib.patches.Ellipse
    """
    if x.size != y.size:
        raise ValueError("x and y must be the same size")

    cov = np.cov(x, y)
    pearson = cov[0, 1] / np.sqrt(cov[0, 0] * cov[1, 1])
    # Using a special case to obtain the eigenvalues of this
    # two-dimensional dataset.
    ell_radius_x = np.sqrt(1 + pearson)
    ell_radius_y = np.sqrt(1 - pearson)
    ellipse = Ellipse((0, 0), width=ell_radius_x * 2, height=ell_radius_y * 2,
                      color=color, **kwargs)

    # Calculating the standard deviation of x from
    # the squareroot of the variance and multiplying
    # with the given number of standard deviations.
    scale_x = np.sqrt(cov[0, 0]) * n_std
    mean_x = np.mean(x)

    # calculating the standard deviation of y ...
    scale_y = np.sqrt(cov[1, 1]) * n_std
    mean_y = np.mean(y)

    transf = transforms.Affine2D() \
        .rotate_deg(45) \
        .scale(scale_x, scale_y) \
        .translate(mean_x, mean_y)

    ellipse.set_transform(transf + ax.transData)
    return ax.add_patch(ellipse)


def plot_pca(dataframe: pd.DataFrame, **kwargs):
    """
    plot the result of PCA.

        Parameters
        ----------
        dataframe: DataFrame
            The data to plot. Must contain a 'label' column.

        **kwargs: keyword arguments
            n_components: int, optional, default: 2
                Number of principal components. Also, teh dimension
                of the graph. Must be equal to 2 or 3.
            show: bool, optional, default: True
                Whether to show the plot or not.
            save: bool, optional, default: False
                Whether to save the plot or not.
            commentary: str, optional, default: "T=48H"
                Any specification to include in the file name while saving.
            points: bool, optional, default: True
                whether to plot the points or not.
            metrics: bool, optional, default: False
                Whether to plot the metrics or not
            savedir: str, optional, default: ""
                Directory where to save the resulting plot, if not empty.
            title: str, optional, defualt: ""
                The filename of the resulting plot. If empty,
                an automatic name will be generated.
            ratios: tuple of float, optional, default: ()
                the PCA explained variance ratio, to display on
                the plot axis.
    """

    options = {
        'n_components': 2,
        'show': True,
        'commentary': "",
        'points': True,
        'metrics': False,
        'savedir': "",
        'pc_ratios': [],
        'title': "",
        'ratios': ()

    }

    options.update(kwargs)
    targets = dataframe["label"].unique()
    colors = ['g', 'b', 'r', 'k', 'sandybrown', 'deeppink', 'gray']
    if len(targets) > len(colors):
        n = len(targets) - len(colors) + 1
        for i in range(n):
            colors.append('#%06X' % randint(0, 0xFFFFFF))

    if options['n_components'] == 2:
        label_params = {'fontsize': 30, "labelpad": 8}
        ticks_params = {'fontsize': 30, }
        fig, ax = plt.subplots(1, 1, figsize=(12, 10))

        plt.xticks(**ticks_params)
        plt.yticks(**ticks_params)
        xlabel = f'Principal Component-1 ({options["ratios"][0]}%)'
        ylabel = f'Principal Component-2 ({options["ratios"][1]}%)'
        if len(options['pc_ratios']):
            xlabel += f" ({round(options['pc_ratios'][0] * 100, 2)}%)"
            ylabel += f" ({round(options['pc_ratios'][1] * 100, 2)}%)"

        plt.xlabel(xlabel, **label_params)
        plt.ylabel(ylabel, **label_params)

        for target, color in zip(targets, colors):
            indicesToKeep = dataframe['label'] == target
            x = dataframe.loc[indicesToKeep, 'principal component 1']
            y = dataframe.loc[indicesToKeep, 'principal component 2']
            if options['points']:
                alpha = 1
                if options['metrics']:
                    alpha = .2
                plt.scatter(x, y, c=color, s=10, alpha=alpha, label=target)
            if options['metrics']:
                plt.scatter(np.mean(x), np.mean(y), marker="+", color=color, linewidth=2, s=160)
                confidence_ellipse(x, y, ax, n_std=1.0, color=color, fill=False, linewidth=2)

        def update(handle, orig):
            handle.update_from(orig)
            handle.set_alpha(1)

        plt.legend(prop={'size': 25}, handler_map={PathCollection: HandlerPathCollection(update_func=update),
                                                   plt.Line2D: HandlerLine2D(update_func=update)})
    elif options['n_components'] == 3:
        label_params = {'fontsize': 20, "labelpad": 8}
        ticks_params = {'fontsize': 20, }
        plt.figure(figsize=(10, 10))
        ax = plt.axes(projection='3d')

        xlabel = f'Principal Component-1 ({options["ratios"][0]}%)'
        ylabel = f'Principal Component-2 ({options["ratios"][1]}%)'
        zlabel = f'Principal Component-3 ({options["ratios"][2]}%)'
        if len(options['pc_ratios']):
            xlabel += f" ({round(options['pc_ratios'][0] * 100, 2)}%)"
            ylabel += f" ({round(options['pc_ratios'][1] * 100, 2)}%)"
            zlabel += f" ({round(options['pc_ratios'][2] * 100, 2)}%)"

        ax.set_xlabel(xlabel, **label_params)
        ax.set_ylabel(ylabel, **label_params)
        ax.set_zlabel(zlabel, **label_params)
        for target, color in zip(targets, colors):
            indicesToKeep = dataframe['label'] == target
            x = dataframe.loc[indicesToKeep, 'principal component 1']
            y = dataframe.loc[indicesToKeep, 'principal component 2']
            z = dataframe.loc[indicesToKeep, 'principal component 3']
            ax.scatter3D(x, y, z, c=color, s=10)
        plt.legend(targets, prop={'size': 18})

    if options['savedir']:
        if options["title"] == "":
            if options['commentary']:
                options["title"] += options["commentary"]

        plt.savefig(os.path.join(options['savedir'], options["title"] + ".png"), dpi=1200)

    if options['show']:
        plt.show()
    plt.close()


def fit_umap(dataframe, n_components=3):
    """
    fit a Uniform Manifold Approximated Projection and return its instance and dataset.

        Parameters
        ----------
        dataframe: DataFrame
            The data on which the umap instance has to be fitted.
            Contains a column 'label'.
        n_components: int, optional, default: 3
            The number of components for the UMAP instance.

        Returns
        -------
        out: tuple of shape (1, 2)
            The first element is the UMAP instance. The second
            element is the resulting dataframe.
    """
    # Configure UMAP hyperparameters
    features = dataframe.columns[:-1]
    x = dataframe.loc[:, features].values
    reducer = UMAP(n_neighbors=100,
                   n_components=n_components,  # default 2, The dimension of the space to embed into.
                   metric='euclidean',
                   n_epochs=1000,
                   learning_rate=1.0, )

    # Fit and transform the data
    X_trans = reducer.fit_transform(x)
    X_dimension = [f"dimension {i + 1}" for i in range(n_components)]
    transformed_df = pd.DataFrame(data=X_trans, columns=X_dimension)

    transformed_df["label"] = dataframe["label"]

    return reducer, transformed_df


def apply_umap(umap, dataframe):
    """
    Transform data using an already fit UMAP instance.

       Parameters
       ----------
       umap: UMAP instance
           The fitted PCA instance from what the data will
           be transformed.
       dataframe: DataFrame
           The data to transform using an already fitted PCA.
           Must have a 'label' column.

       Returns
       -------
       out: DataFrame
           The transformed data.
   """
    features = dataframe.columns[:-1]
    x = dataframe.loc[:, features].values
    x = StandardScaler().fit_transform(x)  # normalizing the features
    transformed_ds = umap.transform(x)
    transformed_df = pd.DataFrame(data=transformed_ds,
                                  columns=[f"dimension {i + 1}" for i in range(transformed_ds.shape[1])])
    transformed_df['label'] = dataframe['label']
    return transformed_df


def plot_umap(dataframe, **kwargs):
    """
    plot the result of UMAP.

        Parameters
        ----------
        dataframe: DataFrame
            The data to plot. Must contain a 'label' column.

        **kwargs: keyword arguments
            n_components: int, optional, default: 3
                Number of principal components. Also, teh dimension
                of the graph. Must be equal to 2 or 3.
            show: bool, optional, default: True
                Whether to show the plot or not.
            save: bool, optional, default: False
                Whether to save the plot or not.
            commentary: str, optional, default: ""
                Any specification to include in the file name while saving.
            points: bool, optional, default: True
                whether to plot the points or not.
            metrics: bool, optional, default: False
                Whether to plot the metrics or not
            savedir: str, optional, default: ""
                Directory where to save the resulting plot, if not empty.
    """
    options = {"n_components": 3, "show": True, "save": False, "commentary": "", "points": True,
               "metrics": False, "savedir": ""}
    options.update(**kwargs)
    targets = dataframe["label"].unique()
    colors = ['r', 'g', 'b', 'k', 'sandybrown', 'deeppink', 'gray']
    if len(targets) > len(colors):
        n = len(targets) - len(colors) + 1
        for i in range(n):
            colors.append('#%06X' % randint(0, 0xFFFFFF))
    if options["n_components"] == 2:
        fig, ax = plt.subplots(1, 1, figsize=(10, 10))
        plt.xticks(fontsize=12)
        plt.yticks(fontsize=14)
        plt.xlabel(f'PC-1', fontsize=20)
        plt.ylabel(f'PC-2', fontsize=20)
        plt.title(f"Uniform Manifold Approximated Projection", fontsize=20)
        for target, color in zip(targets, colors):
            indicesToKeep = dataframe['label'] == target
            x = dataframe.loc[indicesToKeep, 'dimension 1']
            y = dataframe.loc[indicesToKeep, 'dimension 2']
            if options["points"]:
                alpha = 1
                if options["metrics"]:
                    alpha = .2
                plt.scatter(x, y, c=color, s=10, alpha=alpha, label=target)
            if options["metrics"]:
                plt.scatter(np.mean(x), np.mean(y), marker="+", color=color, linewidth=2, s=160)
                confidence_ellipse(x, y, ax, n_std=1.0, color=color, fill=False, linewidth=2)

        def update(handle, orig):
            handle.update_from(orig)
            handle.set_alpha(1)

        plt.legend(prop={'size': 15}, handler_map={PathCollection: HandlerPathCollection(update_func=update),
                                                   plt.Line2D: HandlerLine2D(update_func=update)})
    if options["n_components"] == 3:
        plt.figure(figsize=(10, 10))
        ax = plt.axes(projection='3d')
        ax.set_xlabel(f'dimension-1', fontsize=20)
        ax.set_ylabel(f'dimension-2', fontsize=20)
        ax.set_zlabel(f'dimension-3', fontsize=20)
        for target, color in zip(targets, colors):
            indicesToKeep = dataframe['label'] == target
            x = dataframe.loc[indicesToKeep, dataframe.columns[0]]
            y = dataframe.loc[indicesToKeep, dataframe.columns[1]]
            z = dataframe.loc[indicesToKeep, dataframe.columns[2]]
            ax.scatter3D(x, y, z, c=color, s=10, label='bla')
        plt.legend(targets, prop={'size': 15})
        plt.title(f"Uniform Manifold Approximated Projection", fontsize=20)

    if options["savedir"]:
        if options["commentary"]:
            plt.savefig(os.path.join(options["savedir"],
                                     f"UMAP n={options['n_components']} t={targets} {options['commentary']}.png"))
        else:
            plt.savefig(os.path.join(options["savedir"], f"UMAP n={options['n_']} t={targets}.png"))

    if options["show"]:
        plt.show()
    plt.close()


def test_rfc_by_confusion(clf, dataset: pd.DataFrame, training_targets: tuple, **kwargs):
    """
    Test an already trained Random forest classifier model,
    resulting in a confusion matrix. The test can be done
    on targets_labels different from the targets_labels used for training
    the model.
        Parameters
        ----------
        clf: RandomForestClassifier
            the trained model.
        dataset:  pandas Dataframe.
            Dataframe containing the data used for testing the
            model. The rows are the entries, and the columns are
            the features on which the model has been trained.
            The last column is 'status' containing the labels
            of the targets_labels for each entry.
        training_targets: tuple of str
            the targets on which the model has been trained.
        **kwargs: keyword arguments
            savepath: str, optional, default: ""
                If not empty, path where le result will be saved.
            verbose: Bool, optional. Default: False
                Whether to display more information when computing
                or not.
            show: Bool, optional. Default: True
                Whether to show the resulting confusion matrix or not.
            iterations: int, optional. Default: 10
                Number of iterations the test will be computed.
            commentary: str, optional. Default: ""
                If any specification to add to the file name.
            testing_targets: tuple of str
                the targets on which the model will be tested.
                Can be different from the training targets.
    """
    options = {"verbose": False, "show": True,
               "testing_targets": (),
               "iterations": 10,
               "commentary": "", "savepath": "", "title": ""}
    options.update(**kwargs)
    if not options["testing_targets"]:
        options["testing_targets"] = training_targets
    CORRESPONDANCE = {}
    target_id = 0
    for t in training_targets:
        if t not in CORRESPONDANCE:
            CORRESPONDANCE[t] = target_id
            target_id += 1
    for t in options["testing_targets"]:
        if t not in CORRESPONDANCE:
            CORRESPONDANCE[t] = target_id
            target_id += 1
    X = dataset[dataset.columns[:-1]]
    y = dataset["label"]

    if options["verbose"]:
        progress = 0
        sys.stdout.write(f"\rTesting model: {progress}%")
        sys.stdout.flush()

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)

    # get predictions and probabilities
    all_matrixes = []
    all_probability_matrixes = []
    for iters in range(options["iterations"]):
        matrix = np.zeros((len(training_targets), len(options['testing_targets'])))
        probabilities_matrix = np.empty((len(training_targets), len(options['testing_targets'])), dtype=object)

        # Initializing the matrix containing the probabilities
        for i in range(len(probabilities_matrix)):
            for j in range(len(probabilities_matrix[i])):
                probabilities_matrix[i][j] = []

        # Making predictions and storing the results in predictions[]
        predictions = []
        for i in X_test.index:
            row = X_test.loc[i, :]
            y_pred = clf.predict([row])[0]
            proba_class = clf.predict_proba([row])[0]
            predictions.append((y_pred, proba_class))

        #
        targets = []
        for i in y_test.index:
            targets.append(y_test.loc[i])
        # Building the confusion matrix
        for i in range(len(targets)):
            y_true = targets[i]
            y_pred = predictions[i][0]
            y_proba = max(predictions[i][1])
            matrix[CORRESPONDANCE[y_pred]][CORRESPONDANCE[y_true]] += 1

            probabilities_matrix[CORRESPONDANCE[y_pred]][CORRESPONDANCE[y_true]].append(y_proba)
        mean_probabilities = np.zeros((len(training_targets), len(options['testing_targets'])))
        for i in range(len(probabilities_matrix)):
            for j in range(len(probabilities_matrix[i])):
                mean_probabilities[i][j] = np.mean(probabilities_matrix[i][j])
        all_matrixes.append(matrix)
        all_probability_matrixes.append(mean_probabilities)

    mixed_labels_matrix = np.empty((len(training_targets), len(options['testing_targets']))).tolist()
    mean_probabilities_matrix = np.empty((len(training_targets), len(options['testing_targets'])))
    overall_matrix = np.mean(np.array([i for i in all_matrixes]), axis=0)
    overall_probabilities = np.mean(np.array([i for i in all_probability_matrixes]), axis=0)

    # averaging the probabilities
    for i in range(len(overall_probabilities)):
        for j in range(len(overall_probabilities[i])):
            mean_probabilities_matrix[i][j] = np.mean(overall_probabilities[i][j])

    # mixing count and probabilities for displaying
    for i in range(len(overall_probabilities)):
        for j in range(len(overall_probabilities[i])):
            np.nan_to_num(overall_matrix[i][j])
            np.nan_to_num(mean_probabilities_matrix[i][j])
            mixed_labels_matrix[i][j] = str(int(overall_matrix[i][j])) + "\nCUP=" + str(
                round(mean_probabilities_matrix[i][j], 3))

    # plotting
    fig, ax = plt.subplots(1, 1, figsize=(7 / 4 * len(options['testing_targets']), 6 / 4 * len(training_targets)))

    fig.suptitle("")
    sns.heatmap(ax=ax, data=overall_matrix, annot=mixed_labels_matrix, fmt='', cmap="Blues")
    ax.xaxis.tick_top()
    ax.xaxis.set_label_position('top')
    ax.set_ylabel("The input is classified as")
    ax.set_xlabel("The input is")
    ax.set_xticks([CORRESPONDANCE[x] + 0.5 for x in options['testing_targets']], options['testing_targets'])
    ax.set_yticks([CORRESPONDANCE[x] + 0.5 for x in training_targets], training_targets)
    plt.tight_layout()

    if options['savepath']:
        plt.savefig(os.path.join(options['savepath'], options["title"] + ".png"))
    if options['show']:
        plt.show()
    plt.close()


def test_sequential_by_confusion(model_path, dataset, training_targets, **kwargs):
    """
    Test an already trained keras Sequential model,
    resulting in a confusion matrix. The test can be done
    on targets_labels different from the targets_labels used for training
    the model.
        Parameters
        ----------
        model_path: str
            the absolute path to the trained model, with extension (to open).
        dataset:  list of lists, shape (n, (2, (ndarray(m,m)))
            list of n pictures of size m*m, coupled with its
            int-like label.
        training_targets: list of int
            the targets on which the model has been trained.
        **kwargs: keyword arguments
            savepath: str, optional, default: ""
                If not empty, path where le result will be saved.
            verbose: Bool, optional. Default: False
                Whether to display more information when computing
                or not.
            show: Bool, optional. Default: True
                Whether to show the resulting confusion matrix or not.
            iterations: int, optional. Default: 10
                Number of iterations the test will be computed.
            commentary: str, optional. Default: ""
                If any specification to add to the file name.
            testing_targets: list of int
                the targets on which the model will be tested.
                Can be different from the training targets.
            target_rename: dict, optional, default: {}
                the keys are the actual targets, the values are
                how you want to rename them on the confusion matrix.
    """
    model = load_model(model_path)
    options = {"verbose": False, "show": True,
               "testing_targets": (),
               "iterations": 10,
               "commentary": "",
               "savepath": "",
               "title": "",
               "target_rename": ""}
    options.update(**kwargs)
    if not options["testing_targets"]:
        options["testing_targets"] = training_targets
    CORRESPONDANCE = {}
    target_id = 0
    for t in training_targets:
        if t not in CORRESPONDANCE:
            CORRESPONDANCE[t] = target_id
            target_id += 1
    for t in options["testing_targets"]:
        if t not in CORRESPONDANCE:
            CORRESPONDANCE[t] = target_id
            target_id += 1
    x_train, x_val, y_train, y_val = split_train_test(dataset, train_size=0.1)

    x_val = np.array(x_val)
    y_val = np.array(y_val)

    # get predictions and probabilities
    all_matrixes = []
    all_probability_matrixes = []
    for iters in range(options["iterations"]):
        matrix = np.zeros((len(training_targets), len(options['testing_targets'])))
        probabilities_matrix = np.empty((len(training_targets), len(options['testing_targets'])), dtype=object)

        # Initializing the matrix containing the probabilities
        for i in range(len(probabilities_matrix)):
            for j in range(len(probabilities_matrix[i])):
                probabilities_matrix[i][j] = []

        # Making predictions and storing the results in predictions[]
        predictions = []
        for x in x_val:
            y_pred = model.predict(x[None, ...])[0]
            predictions.append((np.where(y_pred == max(y_pred))[0][0], list(y_pred)))

        targets = []
        for i in y_val:
            targets.append(np.where(i == max(i))[0][0])
        # Building the confusion matrix

        for i in range(len(targets)):
            y_true = targets[i]
            y_pred = predictions[i][0]
            y_proba = max(predictions[i][1])

            matrix[CORRESPONDANCE[y_pred]][CORRESPONDANCE[y_true]] += 1

            probabilities_matrix[CORRESPONDANCE[y_pred]][CORRESPONDANCE[y_true]].append(y_proba)
        mean_probabilities = np.zeros((len(training_targets), len(options['testing_targets'])))
        for i in range(len(probabilities_matrix)):
            for j in range(len(probabilities_matrix[i])):
                mean_probabilities[i][j] = np.mean(probabilities_matrix[i][j])
        all_matrixes.append(matrix)
        all_probability_matrixes.append(mean_probabilities)

    mixed_labels_matrix = np.empty((len(training_targets), len(options['testing_targets']))).tolist()
    mean_probabilities_matrix = np.empty((len(training_targets), len(options['testing_targets'])))
    overall_matrix = np.mean(np.array([i for i in all_matrixes]), axis=0)
    overall_probabilities = np.mean(np.array([i for i in all_probability_matrixes]), axis=0)

    # averaging the probabilities
    for i in range(len(overall_probabilities)):
        for j in range(len(overall_probabilities[i])):
            mean_probabilities_matrix[i][j] = np.mean(overall_probabilities[i][j])

    # mixing count and probabilities for displaying
    for i in range(len(overall_probabilities)):
        for j in range(len(overall_probabilities[i])):
            np.nan_to_num(overall_matrix[i][j])
            np.nan_to_num(mean_probabilities_matrix[i][j])
            mixed_labels_matrix[i][j] = str(int(overall_matrix[i][j])) + "\nCUP=" + str(
                round(mean_probabilities_matrix[i][j], 3))

    # plotting
    fig, ax = plt.subplots(1, 1, figsize=(7 / 4 * len(options['testing_targets']), 6 / 4 * len(training_targets)))

    fig.suptitle("")
    sns.heatmap(ax=ax, data=overall_matrix, annot=mixed_labels_matrix, fmt='', cmap="Blues")
    ax.xaxis.tick_top()
    ax.xaxis.set_label_position('top')
    ax.set_ylabel("The input is classified as")
    ax.set_xlabel("The input is")

    ax.set_xticks([CORRESPONDANCE[x] + 0.5 for x in options['testing_targets']],
                  [options["target_rename"][x] for x in options['testing_targets']])
    ax.set_yticks([CORRESPONDANCE[x] + 0.5 for x in training_targets],
                  [options["target_rename"][x] for x in training_targets])
    plt.tight_layout()

    if options['savepath']:
        plt.savefig(os.path.join(options['savepath'], options["title"] + ".png"))
    if options['show']:
        plt.show()
    plt.close()


def model_history_plot(history_path, savepath=""):
    """
    Save in a fancy way the history logs of a
    trained keras model, saved in the form of a
    csv file.

        Parameters
        ----------
        history_path: str
            the absolute path to the .log file,
            containing the history in csv format.
        savepath: str, optional, default: ""
            If not empty, the directory where the plot will be saved.
            If empty, the plot is shown.
    """
    data = pd.read_csv(history_path, index_col=False)
    plt.figure(figsize=(6, 5))
    plt.plot(data["accuracy"], linestyle="dashed", color="blue", label="training accuracy")
    plt.plot(data["val_accuracy"], linestyle="solid", color="blue", label="validation accuracy")
    plt.plot(data["loss"], linestyle="dashed", color="red", label="training loss")
    plt.plot(data["val_loss"], linestyle="solid", color="red", label="training loss")

    plt.xlabel("epochs", fontsize=15)
    plt.ylabel("score", fontsize=15)
    plt.xticks(fontsize=13)
    plt.yticks(fontsize=13)
    plt.legend(fontsize=13)
    title = "history " + os.path.basename(history_path).replace("history", "").split(".")[0] + ".png"
    if savepath:
        plt.savefig(os.path.join(savepath, title))
    else:
        plt.show()
    plt.close()



def split_train_test(data, train_size: float = 0.7):
    """
    Split a dataset into train and validation sets for features and labels.

        Parameters
        ----------
        data: ndarray, shape((n, 2), m)
            The numpy array containing the data.
            Each entry is coupled within a tuple with its
            corresponding label
        train_size: float, optional, default: 0.7
            The proportion, between 0 and 1, that the train
            set will take on the whole dataset.

        Returns
        -------
        out: tuple of length 4
            The first element is the train set for features.
            The second is the validation set for features.
            The third is the train set for the labels.
            The fourth is the validation set for labels.
    """
    img_size = 224
    train = data[:int(len(data) * train_size)]
    val = data[int(len(data) * train_size):]

    x_train = []
    y_train = []
    x_val = []
    y_val = []

    for feature, label in train:
        x_train.append(feature)
        y_train.append(label)

    for feature, label in val:
        x_val.append(feature)
        y_val.append(label)

    x_train = np.array(x_train) / 255
    x_val = np.array(x_val) / 255

    x_train.reshape(-1, img_size, img_size, 1)
    y_train = np.array(y_train)

    x_val.reshape(-1, img_size, img_size, 1)
    y_val = np.array(y_val)

    y_train = to_categorical(y_train, 2)
    y_val = to_categorical(y_val, 2)
    return x_train, x_val, y_train, y_val
