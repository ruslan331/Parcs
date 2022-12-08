from Pyro4 import expose

class Solver:
    def __init__(self, workers=None, input_file_name=None, output_file_name=None):
        self.input_file_name = input_file_name
        self.output_file_name = output_file_name
        self.workers = workers
        print("Inited")

    def solve(self):
        print("Job Started")
        workers_cnt = len(self.workers)
        print("Workers %d" % workers_cnt)
        N, matrix = self.read_input()

        reduced = int(-1e9)
        mapped = []
        sum_pref = [0] * N

        for i in range(N):
            sum_pref[i] = [0] * N
            sum_pref[i][0] = matrix[i][0]
            for j in range(1, N):
                sum_pref[i][j] = sum_pref[i][j - 1] + matrix[i][j]

        for len_ in range(1, N + 1):
            mapped.append(self.workers[len_ % workers_cnt].mymap(N, len_, sum_pref)) # TODO: change workers
        reduced = max(reduced, self.myreduce(mapped))

        # output
        print(reduced)
        self.write_output(reduced)
        print("Job Finished")

    @staticmethod
    @expose
    def mymap(N, len_, sum_pref):
        res = int(-1e9)

        a = [0] * N
        for l in range(0, N - len_+ 1):
            r = l + len_ - 1
            cur_sum = 0
            min_pref_sum = 0
            for i in range(0, N):
                a[i] = sum_pref[i][r]
                if l - 1 >= 0:
                    a[i] -= sum_pref[i][l - 1]
                cur_sum += a[i]
                res = max(res, cur_sum - min_pref_sum)
                min_pref_sum = min(min_pref_sum, cur_sum)

        return res

    @staticmethod
    @expose
    def myreduce(mapped):
        output = int(-1e9)
        for x in mapped:
            # output = max(output, x) # TODO: x.value
            output = max(output, x.value)
        return output

    def read_input(self):
        f = open(self.input_file_name, 'r')
        N = int(f.readline())
        matrix = [[int(num) for num in line.split()] for line in f]
        f.close()
        return N, matrix

    def write_output(self, output):
        f = open(self.output_file_name, 'w')
        f.write(str(output))
        f.write('\n')
        f.close()

# workers = [Solver]
# solver = Solver(workers=workers, input_file_name="in.txt", output_file_name="out.txt")
# solver.solve()
#

