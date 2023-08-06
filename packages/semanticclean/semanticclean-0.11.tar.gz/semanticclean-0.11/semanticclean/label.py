import numpy as np
import pandas as pd
from tqdm import tqdm
from typing import List, Dict

class LabelIssues:
    def __init__(self, labels, pred_probs):
        self.labels = np.array(labels)
        self.pred_probs = pred_probs
        self.epsilon = 1e-6
        self.num_examples = len(labels)
        self.num_classes = pred_probs.shape[1]
        self.idx_issues = []
        self.guessed_labels = []
        self.score_list = []
        self.confident_joint_mat = None
        
        
    def _get_class_thresholds(self, labels, pred_probs, epsilon, verbose):
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
        class_thresholds = np.sum(self.pred_probs * y_eq_k, axis=0) / (nk + epsilon)

        return class_thresholds


    def _get_confident_joint_mat(self, labels, pred_probs, class_thresholds, rank_by, verbose):
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

            if cnt > 1: # if cnt > 1, this means we need to break the tie
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
                    rank_score_list.append(self._rank_score(pred_probs[i][noisy_label], max_prob, by=rank_by))
        return conf_mat, np.array(idx_list), np.array(guessed_labels_list), np.array(rank_score_list)


    def detect_issues(self, rank_by='normalized_margin', verbose=False):
        
        class_thresholds = self._get_class_thresholds(self.labels, self.pred_probs, self.epsilon, verbose)
        conf_mat, idx_arr, guessed_labels_arr, rank_score_arr = self._get_confident_joint_mat(self.labels, self.pred_probs, class_thresholds, rank_by, verbose)
        
        if len(idx_arr) > 0:
            sort_indices = np.argsort(rank_score_arr)
            self.idx_issues = idx_arr[sort_indices]
            self.guessed_labels = guessed_labels_arr[sort_indices]
            self.score_list = np.sort(rank_score_arr)
            
        self.confident_joint_mat = conf_mat
    
    def _rank_score(self, noisy_label_prob, max_prob, by='normalized_margin'):
        if by=='normalized_margin':
            return noisy_label_prob - max_prob
    
    def prune(self, *args, frac: float=0.4, n: int=0, axis: int=0) -> List[np.ndarray]:
        """_summary_

        Args:
            frac (float, optional): _description_. Defaults to 0.4.
            n (int, optional): _description_. Defaults to 0.
            axis (int, optional): _description_. Defaults to 0.

        Returns:
            _type_: _description_
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
        
    def suggest(self, frac: float=0.4, n: int=0):
        # provide a new version of data with suggested labels
        if n > 0:
            num_to_return = n
        num_to_return = int(frac * len(self.guessed_labels))
        return self.guessed_labels[:num_to_return]
    
    def report(self, include_cols: Dict[str, np.ndarray]={}):
        data_cols = {'example': self.idx_issues, 'given_label': self.labels[self.idx_issues], \
             'score': self.score_list, 'guessed_label': self.guessed_labels}
        
        if len(include_cols) > 0:
            include_cols = {'_'+k: v[:len(self)] for k, v in include_cols.items()}
            data_cols = {**include_cols,**data_cols}
        
        df = pd.DataFrame(data_cols)
        return df
    
    def summary(self):
        print('-'*79)
        for i in range(self.num_classes):
            for j in range(self.num_classes):
                if i==j:
                    continue
                num_wrong_examples = int(self.confident_joint_mat[i][j])
                if num_wrong_examples > 0:
                    text = f'--> {num_wrong_examples} example(s) is(are) labeled {i} but should be labeled {j} <--'
                    print(text)
        print('-'*79)
    def __len__(self):
        return len(self.idx_issues)
