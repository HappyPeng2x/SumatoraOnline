from django.db import models

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
                d = {'prio':True, 'writing':w}
                r = r + [d]
                
        for w in self.readings.split(' '):
            if len(w) > 0:
               d = {'prio':False, 'writing':w}
               r = r + [d]
               
        return r
