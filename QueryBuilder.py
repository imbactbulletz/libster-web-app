class QueryBuilder:

    def reverse_sentence(self, sentence=[]):
        new_sentence = []

        for i in range(len(sentence)-1, -1, -1):
            new_sentence.append(sentence[i])


        return new_sentence

    # pravi OR query za prefikse
    def orify(self, parameters=[]):
        orified_list = []

        prefix_list = parameters[0]
        prefix_value = parameters[1]

        for prefix in prefix_list:
            orified_list.append({prefix: prefix_value})

        return dict({"$or": orified_list})

    def r_builder(self, sentence, index):

        #  zaustavni slucaj, ako je predzadnji element u listi operator
        if len(sentence) < (index + 2):
            return self.orify(sentence[index - 1])

        #  ukoliko je recenica neispravna
        if sentence[index] != "AND" and sentence[index] != "OR":
            raise Exception("Bad sentence format.")

        return {"$" + sentence[index]: [self.orify(sentence[index - 1]), self.r_builder(sentence, index + 2)]}

    def build_from(self, sentence):
        # revertuje listu kako bismo mogli da isparsiramo od kraja
        reversed_sentence = self.reverse_sentence(sentence)

        #  ukoliko je recenica neispravna
        if sentence[1] != "AND" and sentence[1] != "OR":
            raise Exception("Bad sentence format.")

        return {"$" + reversed_sentence[1]: [self.orify(reversed_sentence[0]), self.r_builder(reversed_sentence, 3)]}
