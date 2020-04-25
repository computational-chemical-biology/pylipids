from sklearn import tree
from sklearn.externals.six import StringIO
import pydot
import pandas as pd

def decision_tree(feat, meta, meta_field, dout):
    meta_order = pd.merge(meta, feat, left_index=True,
                     right_index=True)
    feat = feat.loc[meta_order.index]
    clf = tree.DecisionTreeClassifier()
    clf = clf.fit(feat, meta_order[meta_field])

    dot_data = StringIO()
    dot_data = tree.export_graphviz(clf, out_file=None,
                      feature_names=feat.columns,
                      class_names=meta_order[meta_field],
                      filled=True, rounded=True,
                      special_characters=True)
    graph = pydot.graph_from_dot_data(dot_data)

    graph[0].write_pdf(dout)
