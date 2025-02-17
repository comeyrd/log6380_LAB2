from poly_fuzzer.fuzzers.abstract_fuzzer import AbstractFuzzer
import random
import numpy as np
from poly_fuzzer.common.abstract_seed import AbstractSeed
from poly_fuzzer.power_schedules.abstract_power_schedule import AbstractPowerSchedule



class CGIFuzzer(AbstractFuzzer):
    def __init__(
        self,
        executor,
        seeds: list[AbstractSeed],
        power_schedule: AbstractPowerSchedule = None,
        min_mutations: int = 1,
        max_mutations: int = 10,
    ):
        super().__init__(executor)
        self.seeds = seeds
        self.seed_index = 0
        self.base_seeds = len(seeds)
        self.executor = executor
        self.power_schedule = power_schedule
        self.min_mutations = min_mutations
        self.max_mutations = max_mutations
        self.mutators = [self._delete_random_character, self._replace_random_character,self._insert_random_character,self._insert_random_percent,self._insert_random_percent]

    def generate_input(self):

        """Mutate the seed to generate input for fuzzing.
        With this function we first use the gien seeds to generate inputs 
        and then we mutate the seeds to generate new inputs."""

        if self.seed_index < self.base_seeds:
            # Still seeding
            inp = self.seeds[self.seed_index].data
            self.seed_index += 1
        else:
            # Mutating
            inp = self._create_candidate()

        return inp

    def find_seed_index(self,input):
        for index, seed in enumerate(self.seeds):
            if seed.data == input:
                return index
        return None
    def _update(self, input,coverage,execution_time,exceptions):
        """Update the fuzzer with the input and its coverage."""
        s_ix = self.find_seed_index(input)
        if exceptions !=0:
            if s_ix is not None:
                self.seeds.pop(s_ix)
            return 
            
        new_seed = AbstractSeed(input,coverage=coverage,execution_time=execution_time)
        if s_ix is not None:
            self.seeds[s_ix] = new_seed
        else:
            self.seeds.append(new_seed)
        return
    
    def _create_candidate(self):
        # Stacking: Apply multiple mutations to generate the candidate
        if self.power_schedule:
            candidate = self.power_schedule.choose(self.seeds).data
        else:
            candidate = np.random.choice(self.seeds).data

        # Apply power schedule to generate the candidate
        #
        trials = random.randint(self.min_mutations, self.max_mutations)
        for i in range(trials):
            candidate = self.mutate(candidate)
        return candidate

    def mutate(self, s):
        """Return s with a random mutation applied"""
        mutator = random.choice(self.mutators)
        return mutator(s)

    def _delete_random_character(self, s):
        """Returns s with a random character deleted"""
        if len(s) > 5:
            pos = random.randint(0, len(s) - 1)
            return s[:pos] + s[pos + 1 :]
        else:
            return s

    def _insert_random_character(self, s):
        """Returns s with a random character inserted"""
        pos = random.randint(0, len(s))
        random_character = chr(random.randrange(32, 127))
        return s[:pos] + random_character + s[pos:]

    def _replace_random_character(self, s):
        """Returns s with a random character replaced"""
        if s == "":
            return ""
        pos = random.randint(0, len(s) - 1)
        random_character = chr(random.randrange(32, 127))
        return s[:pos] + random_character + s[pos + 1 :]

    def _insert_random_plus(self, s):
            """Returns s with a random percent with two char inserted"""
            pos = random.randint(0, len(s))
            return s[:pos] + "+" + s[pos:]
    
    def _insert_random_percent(self,s):
            pos = random.randint(0, len(s))
            return s[:pos] + "%" +random.choice('0123456789abcdefABCDEF')+random.choice('0123456789abcdefABCDEF')+ s[pos:]
