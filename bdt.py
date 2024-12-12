import math
from collections import Counter
import csv

# Define the Node class
class Node:
    def __init__(self, feature=None, decision=None):
        self.feature = feature
        self.decision = decision
        self.children = {}  # Dictionary mapping feature values to child nodes

    def __repr__(self):
        if self.decision is not None:
            return f"Leaf(decision={self.decision})"
        return f"Node(feature={self.feature}, children={len(self.children)})"

# Calculate entropy
def calculate_entropy(data, target_column):
    """Calculate the entropy of a dataset."""
    total_count = len(data)
    label_counts = Counter(row[target_column] for row in data)
    entropy = 0.0
    for count in label_counts.values():
        p = count / total_count
        entropy -= p * math.log2(p)
    return entropy

# Split data by feature
def split_data_by_feature(data, feature_index):
    """Split data into subsets based on feature values."""
    subsets = {}
    for row in data:
        feature_value = row[feature_index]
        if feature_value not in subsets:
            subsets[feature_value] = []
        subsets[feature_value].append(row)
    return subsets

# Calculate information gain
def calculate_information_gain(feature_index, data, target_column):
    """Calculate the information gain for a feature."""
    total_entropy = calculate_entropy(data, target_column)
    total_count = len(data)
    subsets = split_data_by_feature(data, feature_index)

    weighted_entropy = 0.0
    for subset in subsets.values():
        subset_entropy = calculate_entropy(subset, target_column)
        weighted_entropy += (len(subset) / total_count) * subset_entropy

    info_gain = total_entropy - weighted_entropy
    return info_gain

# Determine the majority class
def majority_class(data, target_column):
    """Return the most common class in the target column."""
    counts = Counter(row[target_column] for row in data)
    return counts.most_common(1)[0][0]

# Build the decision tree
def build_decision_tree(data, features=None, target_column=-1):
    """Recursively builds a boolean decision tree."""
    # If the dataset is empty, return None
    if not data:
        return None

    # Check if all decisions are the same (leaf node)
    unique_decisions = set(row[target_column] for row in data)
    if len(unique_decisions) == 1:
        return Node(decision=unique_decisions.pop())

    # If no features are left, return a leaf with the majority class
    if not features:
        return Node(decision=majority_class(data, target_column))

    # Find the feature with the highest information gain
    best_feature = None
    max_ig = -float('inf')
    for feature_index in features:
        ig = calculate_information_gain(feature_index, data, target_column)
        if ig > max_ig:
            max_ig = ig
            best_feature = feature_index

    # If no feature provides information gain, return a majority class leaf
    if max_ig <= 0:
        return Node(decision=majority_class(data, target_column))

    # Create a root node for the best feature
    root = Node(feature=best_feature)

    # Split the data and recursively build child nodes
    subsets = split_data_by_feature(data, best_feature)
    remaining_features = [f for f in features if f != best_feature]

    for feature_value, subset in subsets.items():
        child_node = build_decision_tree(subset, remaining_features, target_column)
        root.children[feature_value] = child_node

    return root

# Load CSV data
def load_csv(filename):
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        data = list(reader)
    return data

# Example usage
def main():
    # Load data from CSV file
    data = load_csv('decision_tree_dataset.csv')  # Replace with your CSV file

    # Feature indices (assume all columns except the target column are features)
    features = list(range(len(data[0]) - 1))
    target_column = -1  # Last column is the target

    # Build the decision tree
    decision_tree = build_decision_tree(data, features, target_column)
    print(decision_tree)

if __name__ == "__main__":
    main()
