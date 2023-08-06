"""Simple implementation of the paper: Confident Learning: Estimating Uncertainty in Dataset Labels."""


import numpy as np
import pandas as pd
from tqdm import tqdm
from typing import List, Dict, Tuple


class LabelIssues:
    """Class that finds issues in data labels."""

    def __init__(self, labels: np.ndarray, pred_probs: np.ndarray):
        """Initialize the class with labels and prediction probabilities.

        Args:
            labels (np.ndarray): the noisy (given) labels of shape (n,),
            n is the number of examples.
            pred_probs (np.ndarray): prediction probabilities of shape (n, m), 
            n is the number of examples, and m is the number of classes.
        """
        self.labels = np.array(labels)
        self.pred_probs = pred_probs
        self.epsilon = 1e-6
        self.num_examples = len(labels)
        self.num_classes = pred_probs.shape[1]
        self.idx_issues = []
        self.guessed_labels = []
        self.score_list = []
        self.confident_joint_mat = None

    def _get_class_thresholds(self, labels: np.ndarray, pred_probs: np.ndarray, epsilon: float, verbose: bool) -> np.ndarray:
        """Calculate the threshold of every class.

        Args:
            labels (np.ndarray): given (noisy) labels of shape (n,), n is the number of examples
            pred_probs (np.ndarray): the prediction probabilities of shape (n, m),
            n is the number of examples, and m is the number of classes
            epsilon (float): small positive number to avoid division by zero
            verbose (bool): if to print some info or not

        Returns:
            np.ndarray: the calculated thresholds of each class, of shape (m,), m is the number of classes
        """
        if verbose:
            print('--> Calculating class thresholds...\n')
        # initialize empty 2D matrix with shape (num_examples, num_classes)
        y_eq_k = np.zeros_like(pred_probs)
        # for each example put 1 at the position of its label(column)
        y_eq_k[np.arange(len(labels)), labels] = 1
        # nk as an 1D array with shape (num_classes, )
        # each value is the number of examples with the label at this index
        nk = y_eq_k.sum(axis=0)

        # now, we get class_thresholds with shape (num_classes, )
        # add epsilon to avoid dividing by zero
        class_thresholds = np.sum(
            self.pred_probs * y_eq_k, axis=0) / (nk + epsilon)

        return class_thresholds

    def _get_confident_joint_mat(self, labels: np.ndarray, pred_probs: np.ndarray, class_thresholds: np.ndarray,
                                 rank_by: str, verbose: bool) -> Tuple[np.ndarray]:
        """Calculate the confident joint matrix.

        Args:
            labels (np.ndarray): given (noisy) labels of shape (n,)
            pred_probs (np.ndarray): prediction probabilities of shape (n, m), n: number of examples, 
            and m: number of classes.
            class_thresholds (np.ndarray): the calculated class thresholds of shape (m,), m: number of classes
            rank_by (str): how to calculate the score of each suspicious label
            verbose (bool): if to print some info or not

        Returns:
            Tuple[np.ndarray]: conf_mat, the confident joint matrix of shape (m, m), m: number of classes,
            idx_list, a numpy array of indices of all labels that may have issue,
            guessed_labels_list, a numpy array fo guessed true labels, 
            rank_score_list, a numpy array that stores a score for each example that might has a label issue.
        """
        if verbose:
            print('--> Detecting label issues...\n')
        # class_thresholds = self._get_class_thresholds(labels, pred_probs, epsilon)
        conf_mat = np.zeros((self.num_classes, self.num_classes))
        # indices of examples that may have label issues
        idx_list = []
        # list of guessed true labels
        guessed_labels_list = []
        # list that store a score for each example that has a label issue
        # this score is calculated using a method from [normalized_margin, ...]
        # currently only support normalized margin
        rank_score_list = []

        disable_tqdm = False if verbose else True
        for i in tqdm(range(self.num_examples), disable=disable_tqdm):
            # how many classes may this example belongs to in other than its given class
            cnt = 0
            # the noisy label is the given label
            noisy_label = labels[i]
            for j in range(self.num_classes):
                # if this the probability of this j class >= its threshold
                # increase cnt variable
                if pred_probs[i][j] >= class_thresholds[j]:
                    cnt += 1
                    # so this class(j) may be the true label for this example(i)
                    guessed_true_label = j

            if cnt > 1:  # if cnt > 1, this means we need to break the tie
                guessed_true_label = np.argmax(pred_probs[i])

            # now, we increase the corresponding cell in the confident joint matrix

            if cnt > 0:
                conf_mat[noisy_label][guessed_true_label] += 1

                # any noisy_label != guessed_true_label, this means that this example has label issue
                if noisy_label != guessed_true_label:
                    # get max probability of this example neglecting the probability of the given label
                    max_prob = np.max(np.delete(pred_probs[i], noisy_label))

                    # append the index of this example to the the list of indices that may have label issues
                    idx_list.append(i)
                    guessed_labels_list.append(guessed_true_label)
                    rank_score_list.append(self._rank_score(
                        pred_probs[i][noisy_label], max_prob, by=rank_by))
        return conf_mat, np.array(idx_list), np.array(guessed_labels_list), np.array(rank_score_list)

    def detect_issues(self, rank_by: str = 'normalized_margin', verbose: bool = False):
        """Detect label issues and rank them.

        Args:
            rank_by (str, optional): how to calculate the score of each example. Defaults to 'normalized_margin'.
            CURRENTLY, only supports 'normalized_margin'.
            verbose (bool, optional): if to print some info or not. Defaults to False.
        """
        class_thresholds = self._get_class_thresholds(
            self.labels, self.pred_probs, self.epsilon, verbose)
        conf_mat, idx_arr, guessed_labels_arr, rank_score_arr = self._get_confident_joint_mat(
            self.labels, self.pred_probs, class_thresholds, rank_by, verbose)

        if len(idx_arr) > 0:
            sort_indices = np.argsort(rank_score_arr)
            self.idx_issues = idx_arr[sort_indices]
            self.guessed_labels = guessed_labels_arr[sort_indices]
            self.score_list = np.sort(rank_score_arr)

        self.confident_joint_mat = conf_mat

    def _rank_score(self, noisy_label_prob: float, max_prob: float, by: str = 'normalized_margin') -> float:
        """Calculate the score of each example.

        Args:
            noisy_label_prob (float): the prediction probability fo given label (noisy label)
            max_prob (float): max probability of this example neglecting the probability of the given label
            by (str, optional): how to calculate this score. Defaults to 'normalized_margin'.
            CURRENTLY, only supports 'normalized_margin'

        Returns:
            float: the score of this example
        """
        if by == 'normalized_margin':
            return noisy_label_prob - max_prob

    def prune(self, *args, frac: float = 0.4, n: int = 0, axis: int = 0) -> List[np.ndarray]:
        """Prune the examples with issues.

        Args:
            frac (float, optional): the percentage you want to drop. Defaults to 0.4.
            n (int, optional): number of examples you want to drop. Defaults to 0.
            axis (int, optional): axis you want to drop along,
            for example if the data shape is (n, m), then axis=0, if data shape is (m, n), then axis=1. Defaults to 0.

            NOTE: this method works on ranked data, so it will prune the most sever ones
            NOTE: if n > 0, then the frac arg will be neglected.

        Returns:
            List[np.ndarray]: list of supplied arrays without noisy data
            NOTE: the labels array will be added automatically, so don't provide it as an argument
            NOTE: labels will always be the last element in this list
        """
        if n > 0:
            num_to_remove = n
        else:
            num_to_remove = int(frac * len(self.idx_issues))

        to_remove = self.idx_issues[:num_to_remove]
        new_data = []
        if len(args) > 0:
            for arr in args:
                arr = np.delete(arr, to_remove, axis=axis)
                new_data.append(arr)
        new_data.append(np.delete(self.labels, to_remove, axis=axis))
        return new_data

    def suggest(self, frac: float = 0.4, n: int = 0) -> np.ndarray:
        """Suggest new labels to replace the given labels.

        Args:
            frac (float, optional): the percentage of corrupted labels you want 
            to replace with suggested labels. Defaults to 0.4.
            n (int, optional): the percentage of corrupted labels you want 
            to replace with suggested labels. Defaults to 0.

            NOTE: if n>0, then frac will be neglected

        Returns:
            np.ndarray: array of suggested labels
        """
        # provide a new version of data with suggested labels
        if n > 0:
            num_to_return = n
        num_to_return = int(frac * len(self.guessed_labels))
        return self.guessed_labels[:num_to_return]

    def report(self, include_cols: Dict[str, np.ndarray] = {}) -> pd.DataFrame:
        """Return a dataframe with some info about the data.

        Args:
            include_cols (Dict[str, np.ndarray], optional): if you want to add any column to the report dataframe. Defaults to {}.
            NOTE: any column you provide, will be preceded with '_'

        Returns:
            pd.DataFrame: pandas dataframe
        """
        data_cols = {'example': self.idx_issues, 'given_label': self.labels[self.idx_issues],
                     'score': self.score_list, 'guessed_label': self.guessed_labels}

        if len(include_cols) > 0:
            include_cols = {'_'+k: v[self.idx_issues]
                            for k, v in include_cols.items()}
            data_cols = {**include_cols, **data_cols}

        df = pd.DataFrame(data_cols)
        return df

    def summary(self):
        """Print the contents of confident joint matrix in human readable format."""
        print('-'*79)
        for i in range(self.num_classes):
            for j in range(self.num_classes):
                if i == j:
                    continue
                num_wrong_examples = int(self.confident_joint_mat[i][j])
                if num_wrong_examples > 0:
                    text = f'--> {num_wrong_examples} example(s) is(are) labeled {i} but should be labeled {j} <--'
                    print(text)
        print('-'*79)

    def __len__(self):
        """Return the number of detected issues."""
        return len(self.idx_issues)
