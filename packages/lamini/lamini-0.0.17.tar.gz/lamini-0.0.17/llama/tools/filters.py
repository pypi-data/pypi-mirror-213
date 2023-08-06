from random import Random
from llama.program.util.run_ai import query_run_embedding
from llama.program.util.run_ai import fuzzy_is_duplicate
from collections import defaultdict
from random import sample
from copy import deepcopy


def get_attributes(value):
    return [
        attribute
        for attribute, _ in value.__fields__.items()
    ]


def type_to_string(type):
    attributes = get_attributes(type)
    return ' '.join([type[attribute] for attribute in attributes])


class DatasetDeduper:
    """Dedupe your dataset with embeddings"""

    def __init__(self, dataset):
        self.dataset = dataset
        self.kept_dataset = []
        self.kept_indices = []
        self.removed_dataset = []
        self.removed_indices = []
        self.index = []
        self.deduped_index = []

    def get_inputs(self):
        if type(self.dataset[0]) is list:
            return [datum[0] for datum in self.dataset]
        return self.dataset

    def get_all_embeddings(self):
        dataset = [type_to_string(datum) for datum in self.get_inputs()]
        self.index = []
        for i in range(0, len(dataset), 32):
            # Get embeddings
            print("Processing Embeddings: " + str(i) + " of " + str(len(dataset)))
            embeddings = query_run_embedding(dataset[i : i + 32])
            self.index.extend(embeddings)

        return self.index

    def stochastic_dedupe_dataset(self, sample_size=1, threshold=0.99):
        self.deduped_index = []
        self.kept_indices = []
        self.kept_dataset = []
        index = self.get_all_embeddings()
        rand = Random()
        for i in range(len(self.dataset)):
            print("Comparing: " + str(i) + " of " + str(len(self.dataset)))
            # print("Deduped Index: " + str(len(deduped_index)))
            # Get embeddings
            embedding = index[i]
            random_sample = rand.sample(
                self.deduped_index, min(sample_size, len(self.deduped_index))
            )
            if not fuzzy_is_duplicate(embedding, random_sample, threshold):
                print("Adding: " + str(i) + " of " + str(len(self.dataset)))
                self.deduped_index.append(embedding)
                self.kept_indices.append(i)
                self.kept_dataset.append(self.dataset[i])
            else:
                self.removed_indices.append(i)
                self.removed_dataset.append(self.dataset[i])

        return self.kept_dataset

    def full_dedupe_dataset(self, threshold=0.99):
        self.deduped_index = []
        self.kept_indices = []
        self.kept_dataset = []
        index = self.get_all_embeddings()
        for i in range(len(self.dataset)):
            print("Processing: " + str(i) + " of " + str(len(self.dataset)))
            # print("Deduped Index: " + str(len(deduped_index)))
            # Get embeddings
            embedding = index[i]
            if not fuzzy_is_duplicate(embedding, self.deduped_index, threshold):
                print("Adding: " + str(i) + " of " + str(len(self.dataset)))
                self.deduped_index.append(embedding)
                self.kept_indices.append(i)
                self.kept_dataset.append(self.dataset[i])
            else:
                self.removed_indices.append(i)
                self.removed_dataset.append(self.dataset[i])

        return self.kept_dataset

class DatasetBalancer:
    """Balance your dataset"""
    

    def __init__(self, dataset):
        self.dataset = dataset
        self.kept_dataset = []
        self.kept_indices = []
        self.removed_dataset = []
        self.removed_indices = []

    def get_outputs(self):
        if type(self.dataset[0]) is list:
            return [datum[1] for datum in self.dataset]
        return self.dataset
    
    def list_classes(self, data, attribute):
        classes = defaultdict(list)
        for i, datum in enumerate(data):
            classes[datum[attribute]].append(i)
        return classes
    
    def augment_data(self, data_indices, num_copies=20):
        augmented_indices = data_indices
        while len(augmented_indices) < num_copies:
            augmented_indices.extend([deepcopy(datum) for datum in sample(data_indices, min(len(data_indices), num_copies - len(augmented_indices)))])
        return augmented_indices
    
    def balance_dataset(self, max_num_samples=5000):
        attributes = get_attributes(self.get_outputs()[0])
        list_attribute_classes = {attribute: self.list_classes(self.get_outputs(), attribute) for attribute in attributes}
        # TODO: figure out better heuristic to determine attribute to balance on
        # TODO: allow for balancing on multiple attributes
        attribute = min(list_attribute_classes, key=lambda x: len(list_attribute_classes[x]))
        classes = list_attribute_classes[attribute]
        num_classes = len(classes)
        num_samples_per_class = max_num_samples // num_classes
        for class_name in classes:
            sampled_indices = sample(self.augment_data(classes[class_name], num_samples_per_class), len(classes[class_name]))
            self.kept_dataset.extend([self.dataset[i] for i in sampled_indices[:num_samples_per_class]])
            self.kept_indices.extend(sampled_indices[:num_samples_per_class])
            self.removed_dataset.extend([self.dataset[i] for i in sampled_indices[num_samples_per_class:]])
            self.removed_indices.extend(sampled_indices[num_samples_per_class:])
        return self.kept_dataset