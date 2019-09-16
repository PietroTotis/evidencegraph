
from evidencegraph.argtree import SIMPLE_RELATION_SET,FULL_RELATION_SET_ADU

class Config: 
    def __init__(self):
        self.features = [
            'default', 'bow', 'bow_2gram', 'first_three',
            'tags', 'deps_lemma', 'deps_tag',
            'punct', 'verb_main', 'verb_all', 'discourse_marker',
            'context', 'clusters', 'clusters_2gram', 'discourse_relation',
            'vector_left_right', 'vector_source_target',
            'verb_segment', 'same_sentence', 'matrix_clause'
        ]

class Complete(Config):
    def __init__(self, corpus_name):
        super().__init__()

        self.N_FOLDS = 50
        self.conditions = {
            '{}-test-complete-adu-full-op|equal'.format(corpus_name): {
                'feature_set': self.features,
                'relation_set': FULL_RELATION_SET_ADU,
                'segmentation': 'adu',
                'optimize': True,
                'optimize_weighting': True
            }
        }

class Minimal(Config):
    def __init__(self, corpus_name):
        super().__init__()
        
        self.N_FOLDS = 5
        self.conditions = {
            '{}-test-adu-simple-noop|equal'.format(corpus_name): {
                'feature_set': self.features,
                'relation_set': SIMPLE_RELATION_SET,
                'segmentation': 'adu',
                'optimize':  False,
                'optimize_weighting': False
            }
        }
