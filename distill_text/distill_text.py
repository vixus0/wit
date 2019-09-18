import sys
import spacy

def textify(token):
    if token is None:
        return ''
    return token.text


SUBJECTS = ["nsubj", "nsubjpass", "csubj", "csubjpass", "agent", "expl"]
OBJECTS = ["dobj", "dative", "attr", "oprd", "acomp"]
PREPOSITIONS = ["prep"]

nlp = spacy.load('en_core_web_sm')


def distill_text(input_text, debug=False):
    doc = nlp(input_text)

    distillation = []
    context_last_propnoun = None
    for sentence in doc.sents:

        if debug == True:
            print("\n")
            print(sentence)

#        for chunk in doc.noun_chunks:
#            print(chunk.text, chunk.label_, chunk.root.text, chunk.root.dep_)
#
#        print("\n")
#        for token in doc:
#            print(token.text, token.head.text, token.dep_, token.pos_)

        verbs = [token for token in sentence if token.pos_ == "VERB"]

        if debug == True:
            print("Verbs:", verbs)

        new_dist = []
        root_subj = None
        root_obj = None
        for verb in verbs:

            # Get subject
            subj = [token for token in verb.lefts if token.dep_ in SUBJECTS]
            if len(subj) == 0:
                continue
            subj = subj[0]


            # If subject is a pronoun, attempt to replace it with the proper noun it refers to
            if subj.pos_ == "PRON":
                current_verb = verb
                while current_verb.head != current_verb:
                    current_verb = current_verb.head
                    current_subj = [token for token in current_verb.lefts if token.dep_ in SUBJECTS]
                    if len(current_subj) == 0:
                        continue
                    current_subj = current_subj[0]
                    if current_subj.pos_ == "PROPN":
                        subj = current_subj

                        if debug == True:
                            print("Found true subject:", subj)

                        break
                else:
                    if debug == True:
                        print("Could not find true subject.")

                    if context_last_propnoun is not None:
                        if debug == True:
                            print("Using context_last_propnoun = ", context_last_propnoun)
                        subj = context_last_propnoun

            # Get direct object, if it exists
            obj = [token for token in verb.rights if token.dep_ in OBJECTS]
            if len(obj) > 0:
                obj = obj[0]
            else:
                obj = None

            if verb.dep_ == "ROOT":
                root_subj = subj
                root_obj = obj

            # Get the (one or more) indirect objects, via the prepositions
            preps = [token for token in verb.rights if token.dep_ in PREPOSITIONS]
            if len(preps) > 0:
                for prep in preps:
                    pobj = [token for token in prep.rights if len(token.text.split()) > 0]
                    if len(pobj) > 0:
                        pobj = pobj[0]
                        new_dist.append((subj.text, verb.lemma_, textify(obj), prep.text, pobj.text))
            else:
                new_dist.append((subj.text, verb.lemma_, textify(obj)))


        # Work out the context (prop noun that is the theme, may be referred to in subsequent sentences)
        if root_subj is not None and root_subj.pos_ == "PROPN":
            context_last_propnoun = root_subj
        elif root_obj is not None and root_obj.pos_ == "PROPN":
            context_last_propnoun = root_obj

        distillation.extend(new_dist)

        if debug == True:
            print("distillation:", new_dist)
            print("context_last_propnoun:", context_last_propnoun)
            input("next!")

    return distillation


if __name__ == "__main__":

    if len(sys.argv) != 2 and len(sys.argv) != 3:
        sys.exit("Usage: python3 distill_text.py STORY_TXT_FNAME [OPTIONAL 'DEBUG']")

    story_fname = sys.argv[1]

    debug = False
    if len(sys.argv) == 3:
        if sys.argv[2] == 'DEBUG':
            debug = True
        else:
            sys.exit("Unrecognised option " + sys.argv[2] + ". Did you mean DEBUG?")

    with open(story_fname, "r") as infile:
        input_text = infile.read()

    distilled = distill_text(input_text, debug=debug)

    for dist in distilled:
        print("_".join(dist))
