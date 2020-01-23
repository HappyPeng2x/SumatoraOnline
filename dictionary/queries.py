import romkan

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

queries_select_readingsPrio = """SELECT DictionaryIndex.`rowid`
   FROM DictionaryIndex
   WHERE readingsPrio MATCH %s"""

queries_select_writings = """SELECT DictionaryIndex.`rowid`
   FROM DictionaryIndex
   WHERE writings MATCH %s"""

queries_select_readings = """SELECT DictionaryIndex.`rowid`
   FROM DictionaryIndex
   WHERE readings MATCH %s"""

queries_select_writingsPrio_begin = """SELECT DictionaryIndex.`rowid`
   FROM DictionaryIndex
   WHERE writingsPrio MATCH %s || '*'"""

queries_select_readingsPrio_begin = """SELECT DictionaryIndex.`rowid`
   FROM DictionaryIndex
   WHERE readingsPrio MATCH %s || '*'"""

queries_select_writings_begin = """SELECT DictionaryIndex.`rowid`
   FROM DictionaryIndex
   WHERE writings MATCH %s || '*'"""

queries_select_readings_begin = """SELECT DictionaryIndex.`rowid`
   FROM DictionaryIndex
   WHERE readings MATCH %s || '*'"""

class Query:
    def __init__(self, aOrder, aSelect,
                 aConvertKana = False):
        self.order = aOrder
        self.select = aSelect
        self.convertKana = aConvertKana

    def execute(self, aTerm):
        if self.convertKana:
            return DictionaryDisplayElement.objects.raw(query_base.format(self.select), [self.order, romkan.to_katakana(romkan.to_hepburn(aTerm))])
        else:
            return DictionaryDisplayElement.objects.raw(query_base.format(self.select), [self.order, aTerm])

queries = [Query(0,
                 queries_select_writingsPrio),
           Query(1,
                 queries_select_readingsPrio,
                 True),
           Query(2,
                 queries_select_writings),
           Query(3,
                 queries_select_readings,
                 True),
           Query(4,
                 queries_select_writingsPrio_begin),
           Query(5,
                 queries_select_readingsPrio_begin,
                 True),
           Query(6,
                 queries_select_writings_begin),
           Query(7,
                 queries_select_readings_begin,
                 True)]

def execute(aTerm, aMin, aCount):
    r = []
    seqs = set()
    
    for i in range(0, len(queries)):
        if len(r) == aCount:
            break

        for e in queries[i].execute(aTerm):
            if len(r) == aCount:
                break
            
            if not e.seq in seqs:
                seqs.add(e.seq)
                
                if len(r) >= aMin:
                    r.append(e)
    
    return r
