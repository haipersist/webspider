#-*-coding:utf-8 -*-


import multiprocessing
import collections



class MapReduce(object):

    def __init__(self,mapper,reducer):
        self.mapper = mapper
        self.reducer = reducer
        self.pool = multiprocessing.Pool()

    def partition(self,mapped_value):
        result = []
        for item in mapped_value:
            result.extend(item)
        partition_data = collections.defaultdict(list)
        for key, value in result:
            partition_data[key].append(value)
        return partition_data.items()


    def __call__(self,inputs):
        mapped_result = self.pool.map(self.mapper,inputs,chunksize=1)
        mapped_value = self.partition(mapped_result)
        reduced_value = self.pool.map(self.reducer,mapped_value)
        return reduced_value





def mapper(logfile):
    mapped_value = []
    with file(logfile,'r') as f:
        for line in f.readlines():
            #print line
            line = line.split()
            #print line
            item = ()
            try:
                item = (line[0],1)
            except Exception,e:
                print str(e)
            mapped_value.append(item)
    return mapped_value



def reducer(item):
    cookie,occurances = item
    return (cookie,sum(occurances))




if __name__ == "__main__":
    mapreduce = MapReduce(mapper,reducer)
    import os
    logfile1 = os.environ.get("SPIDERPATH") + '/logs/spiderInfo-2017-03-08.log'
    logfile2 = os.environ.get("SPIDERPATH") + '/logs/spiderInfo-2017-03-09.log'
    logfile3 = os.environ.get("SPIDERPATH") + '/logs/spiderInfo-2017-03-10.log'
    result = mapreduce([logfile1,logfile2,logfile3])
    print result


