from pprint import pprint
from sklearn import tree
from sklearn.tree import export_text
import re


class DecisionTreeBuilder():
    @staticmethod
    def random_training_data():
        raise NotImplementedError()

    @staticmethod
    def principal_components(m):
        return m

    @staticmethod
    def tree_to_python(clf, class_decode):
        exported_tree = export_text(clf)

        exported_tree = exported_tree.replace('|   ', '    ')
        exported_tree = exported_tree.replace('|--- class:', 'return')
        exported_tree = re.sub(r'\|--- feature_(\d+) ',
                               r'if args[\1] ', exported_tree)
        exported_tree = re.sub(r'if (.*)$', r'if \1:',
                               exported_tree, flags=re.MULTILINE)
        exported_tree = re.sub(r'^', '    ', exported_tree, flags=re.MULTILINE)
        exported_tree = "def decision_tree(*args):\n" + exported_tree

        for i in range(len(class_decode)):
            exported_tree = exported_tree.replace(
                'return {}'.format(i),
                'return "{}"'.format(class_decode[i])
            )

        return exported_tree

    @staticmethod
    def generate_tree(sample_size):
        training_data = []
        training_target = []

        known_targets = []

        while len(training_data) != sample_size:
            m = DecisionTreeBuilder.random_training_data()
            transformed_m = DecisionTreeBuilder.principal_components(m)

            if transformed_m in training_data:
                continue

            pprint(m)
            target = input()
            if target not in known_targets:
                known_targets.append(target)

            training_data.append(transformed_m)
            training_target.append(known_targets.index(target))

        clf = tree.DecisionTreeClassifier()
        clf = clf.fit(training_data, training_target)

        return clf, known_targets


def main():
    print('sample size: ')
    sample_size = int(input())
    clf, known_targets = DecisionTreeBuilder.generate_tree(sample_size)

    print("\n\ngenerated python code:\n""")
    print(DecisionTreeBuilder.tree_to_python(clf, known_targets))


if __name__ == '__main__':
    main()
