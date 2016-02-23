from mrjob.job import MRJob
from mrjob.step import MRStep

class MRMoneySpentByCustomerSorted(MRJob):

    def steps(self):
            return [
                MRStep(mapper=self.mapper_get_users,
                       reducer=self.reducer_count_money),
                MRStep(mapper=self.mapper_make_counts_key,
                       reducer = self.reducer_output_sorted)
        ]
    
    def mapper_get_users(self, _, line):
        (UserID, ItemID, Cost) = line.split(',')
        yield UserID, float(Cost)

    def reducer_count_money(self, UserID, Cost):
        yield UserID,sum(Cost)

    def mapper_make_counts_key(self, UserID, Cost):
        yield '%04.02f'%float(Cost),UserID
        
    def reducer_output_sorted(self, Cost, UserIDs):
    	for UserID in UserIDs:
            yield UserID, Cost	

if __name__ == '__main__':
    MRMoneySpentByCustomerSorted.run()