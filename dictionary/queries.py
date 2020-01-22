from dictionary.models import DictionaryDisplayElement

query_base = """
SELECT
  %s AS entryOrder,
  DictionaryEntry.seq,
  DictionaryEntry.readingsPrio, 
  DictionaryEntry.readings, 
  DictionaryEntry.writingsPrio,
  DictionaryEntry.writings,
  DictionaryEntry.pos,
  DictionaryEntry.xref,
  DictionaryEntry.ant,
  DictionaryEntry.misc, 
  DictionaryEntry.lsource,
  DictionaryEntry.dial,
  DictionaryEntry.s_inf, 
  DictionaryEntry.field,
  DictionaryTranslation.lang,
  DictionaryTranslation.gloss
FROM
  jmdict.DictionaryEntry, 
  eng.DictionaryTranslation
WHERE
  DictionaryEntry.seq = DictionaryTranslation.seq AND
  DictionaryEntry.seq IN
  ({})"""

queries_select_writingsPrio = """SELECT DictionaryIndex.`rowid`
   FROM DictionaryIndex
   WHERE writingsPrio MATCH %s"""

class Query:
    def __init__(self, aOrder, aSelect):
        self.order = aOrder
        self.select = aSelect

    def execute(self, aTerm):
        return DictionaryDisplayElement.objects.raw(query_base.format(self.select), [self.order, aTerm])

queries = [Query(0, queries_select_writingsPrio)]

def execute(aTerm, aOrder):
    r = []
    for i in range(0, len(queries)):
        if i >= aOrder:
            r.append(queries[i].execute(aTerm))
    return r
