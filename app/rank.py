import models

class Rank:
    def __init__(self,user,score,solve,tries):
        self.user = user
        self.score = score
        self.solve = solve
        self.tries = tries
        self.average = self.score / self.solve
        self.back_score = self.score + self.average

    def __repr__(self):
        return f"{ self.name } - {self.score}"

def get_ranking():
    ranks = []

    def get_group(list, point):
        group = []
        for i in list:
            if i.score == point:
                group.append(i)

        return group

    def sort(list):
        for i in range(len(list)):
            for j in range(len(list)):
                if list[i].score > list[j].score:
                    list[i] , list[j] = list[j], list[i]

        return list[0]

    def store_rank():
        def get_problem_solved_count(user):
            count = 0
            for i in models.ProblemSolved.objects.all():
                if i.user.username == user.username:
                    count += 1

            return count

        def get_problem_tried_count(user):
            count = 0
            for i in models.ProblemTried.objects.all():
                if i.user.username == user.username:
                    count += 1

            return count

        def get_profile(user):
            for i in models.Profile.objects.all():
                if i.user.username == user.username:
                    return i
        
        for i in models.InRank.objects.all():
            ranks.append(Rank(name=get_profile(i).user.username, score=get_profile(i).point, solve=get_problem_solved_count(i), tries=get_problem_tried_count(i)))

        sort(ranks)
    
    store_rank(ranks)

    def make_group():
        highest = ranks[0].score
        group_ranks = []

        while highest > 15:
            group = get_group(ranks, highest)
            for i in range(len(group)):
                for j in range(len(group)):
                    if group[i].backscore > group[j].backscore:
                        group[i] , group[j] = group[j], group[i]
            for g in group:
                group_ranks.append(g)
            highest -= 1

        return group_ranks

    ranks = make_group()

    return ranks


if __name__ == "__main__":
    ranks = get_ranking()

    for i in ranks:
        print("%s\t%d\t",i.name,i.score)


