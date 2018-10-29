class AttrDict(dict):
    ''' A cute trick to replace the instance dictionary with an inherited dictionary.
        Purpose is to gain the convenience of dotted access instead of square brackets
        But to retain all the interesting dictionary tools (keys, values, items, contains).

        Must use valid identifiers (variable names or attribute names):
              [A-Za-z_][A-Za-z0-9_]*

        Restriction.  If a key is an invalid identifier, the your have to use square brackets:

            d[10] = 'ten'
            print d.10                     # <--- This is not allowed
            print d[10]                    # <--- Brackets are required

            d['pyats-asa-5'] = Device()
            d.pyats-asa-5.connect()        # <--- This is not allowed
            d['pyats-asa-5'].connect()     # <--- Brackets are required
    '''

    def __init__(self):
        self.__dict__ = self
