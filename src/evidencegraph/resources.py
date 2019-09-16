import pickle
from collections import defaultdict
from lxml import etree


def loadDimlex(filename):
    discourse_markers = {}
    print( "Loading German DimLex ..." )
    dimlex_tree = etree.parse(filename)
    # iterate over all lexicon entries
    for entry in dimlex_tree.iter("eintrag"):
        dm_id = int(entry.get('id'))
        # get all continous orthographies (get single or phrasal typed parts)
        dm_orths = []
        for orth in entry.iter('orth'):
            if orth.get('type') == 'cont':
                for part in orth.iter('part'):
                    # dm_orth = part.text.replace(',', ' ,').lower()
                    dm_orth = str(part.text.lower())
                    dm_orths.append(dm_orth)
        # for each syntactic variant, extract their semantic relation
        dm_rels = []
        for syn in entry.iter('syn'):
            found = syn.find(".//relation")
            if found is not None:
                dm_rels.append(found.text)
        # store all
        for dm_orth in dm_orths:
            discourse_markers[dm_orth] = dm_rels
    print( " found {} discourse markers.".format(len(discourse_markers)) )
    return discourse_markers


def loadConanolex(filename, lang):
    discourse_markers = {}
    print( "Loading {} Conano Lexicon ...".format(lang) )
    dimlex_tree = etree.parse(filename)
    # iterate over all lexicon entries
    for entry in dimlex_tree.iter("entry"):
        dm_id = int(entry.get('id'))
        # get all continous orthographies (get single or phrasal typed parts)
        dm_orths = []
        for orth in entry.iter('orth'):
            if orth.get('type') == 'cont':
                for part in orth.iter('part'):
                    # dm_orth = part.text.replace(',', ' ,').lower()
                    dm_orth = str(part.text.lower())
                    dm_orths.append(dm_orth)
        # for each syntactic variant, extract their semantic relation
        dm_rels = []
        # TODO: At the moment the relations list in the lexicon are incorrect.
        # for syn in entry.iter('syn'):
        #     found = syn.find(".//coh-relation")
        #     if found is not None:
        #         dm_rels.append(found.text)
        # store all
        for dm_orth in dm_orths:
            discourse_markers[dm_orth] = dm_rels
    print( " found {} discourse markers.".format(len(discourse_markers)) )
    return discourse_markers


def load_educe_markers(filename):
    discourse_markers = {}
    print( "Loading English EDUCE Lexicon ..." )
    lines = open(filename).readlines()
    for line in lines:
        if line.startswith('#') or line.strip() == '':
            continue
        left, right = line.split(';')
        marker = left.strip()
        right_parts = [r.strip() for r in right.strip().split(' ')]
        relations = [r for r in right_parts if r != '']
        discourse_markers[marker] = relations
    print( " found {} discourse markers.".format(len(discourse_markers)) )
    return discourse_markers


def join_lexica(lexica):
    discourse_markers = defaultdict(set)
    for lexicon in lexica:
        for marker, relations in lexicon.items():
            discourse_markers[marker] |= set(relations)
    return discourse_markers

##################################################
# LOAD PRE-PROCESSED SEGMENTS -> SE TYPES LOOKUP
##################################################

def load_seg_setypes_lookup(file_path):

  print( "Loading micro-text ADUs annotated with Situation Entity types ..." )

  item = pickle.load(open(str(file_path), mode = "rb"), encoding='latin1')

  print( " found {} micro-text ADUs annotated with Situation Entity types.".format(len(item)) )

  return item

###########################################################



connectives_de = loadDimlex('resources/newDimLex.xml')
connectives_it = loadConanolex('resources/Lico_Connectives_Ita.xml', "Italian")

conano_en = loadConanolex('resources/ConnectorLexiconEnglish.xml', "English")
educe_en = load_educe_markers('resources/educe_pdtb_markers_cleaned.txt')

connectives_en = join_lexica([conano_en, educe_en])

se_types_de = load_seg_setypes_lookup('resources/adu2setypes.pkl')
