import json

from django.db import models

class DictionaryEntity(models.Model):
    name = models.TextField(primary_key=True)
    content = models.TextField()

    class Meta:
        managed = False
        db_table = 'unspecified'

class DictionaryDisplayElement(models.Model):
    entryOrder = models.IntegerField()
    seq = models.IntegerField(primary_key=True)
    readingsPrio = models.TextField()
    readings = models.TextField()
    writingsPrio = models.TextField()
    writings = models.TextField()
    pos = models.TextField()
    xref = models.TextField()
    ant = models.TextField()
    misc = models.TextField()
    lsource = models.TextField()
    dial = models.TextField()
    s_inf = models.TextField()
    field = models.TextField()
    lang = models.TextField()
    gloss = models.TextField()

    class Meta:
        managed = False
        db_table = 'unspecified'

    def convert_pos(self):
        pos = json.loads(self.pos)
        r = []

        for p in pos:
            s = []
            
            for e in p:
                s.append(DictionaryEntity.objects.raw('SELECT * FROM jmdict.DictionaryEntity WHERE name=%s', [e])[0].content)

            r.append(s)

        return r

    def get_gloss(self):
        gloss = json.loads(self.gloss)
        pos = self.convert_pos()
        r = []

        for i in range(0, len(gloss)):
            r.append({'pos':pos[i],
                      'gloss':gloss[i]})

        return r

    def get_writings(self):
        r = []
        
        for w in self.writingsPrio.split(' '):
            if len(w) > 0:
                d = {'prio':True, 'writing':w}
                r = r + [d]
                
        for w in self.writings.split(' '):
            if len(w) > 0:
               d = {'prio':False, 'writing':w}
               r = r + [d]
               
        return r

    def get_readings(self):
        r = []
        
        for w in self.readingsPrio.split(' '):
            if len(w) > 0:
                d = {'prio':True, 'reading':w}
                r = r + [d]
                
        for w in self.readings.split(' '):
            if len(w) > 0:
               d = {'prio':False, 'reading':w}
               r = r + [d]
               
        return r
