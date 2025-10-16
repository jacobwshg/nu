class Person:
    def __init__(self, name, title, salary, subords):
        self.name = name
        self.title = title
        self.salary = salary
        self.subords = subords

    # Return lowest salary and associated name 
    # within department directed by current person
    def dept_min_salary_and_name(self):
        min_sal = self.salary
        min_sal_name = self.name

        for sub in self.subords:
            ms, msn = sub.dept_min_salary_and_name()
            if ms < min_sal:
                min_sal = ms
                min_sal_name = msn

        return min_sal, min_sal_name

    def find_salary_inversion(self):
        if not self.subords:
            return None
        for sub in self.subords:
            ########
            print(f'Testing salary inversion between {self.name} and {sub.name}')
            if self.salary < sub.salary:
                return self.name, sub.name
            else:
                sub_sal_inv_pair = sub.find_salary_inversion()
                if sub_sal_inv_pair:
                    return sub_sal_inv_pair
        return None

class Org:
    def __init__(self, ceo):
        self.ceo = ceo

    def min_salary_name(self):
        _, min_sal_name = self.ceo.dept_min_salary_and_name()
        return min_sal_name

    def find_salary_inversion(self):
        return self.ceo.find_salary_inversion()

turner = Person('Theresa Turner', 'Backend Dev', 250000, [])
jacobs = Person('Joyce Jacobs', 'IT Staff', 90000, [])
jones = Person('Jane Jones', 'IT Staff', 80000, [])
jacobsen = Person('Juliet Jacobsen', 'Account Manager', 200000, [])
jensen = Person('Josie Jensen', 'Account Manager', 200000, [])
thompson = Person('Tina Thompson', 'CIO', 1300000, [turner])
jordan = Person('Jessica Jordan', 'CTO', 600000, [jacobs, jones])
jennings = Person('Julia Jennings', 'CFO', 500000, [jacobsen, jensen])
johnson = Person('Jasmine Johnson', 'CEO', 1400000, [thompson, jordan, jennings])

org = Org(johnson)

__all__ = [
    'Person',
    'Org',
    'org']

if __name__ == '__main__':
    print('Person with lowest salary: ' + org.min_salary_name())

    sal_inv_pair = org.find_salary_inversion()
    print(f'Original salary inversion: {sal_inv_pair}')

    turner.salary *= 10
    sal_inv_pair = org.find_salary_inversion()
    print(f'Salary inversion after adjustment: {sal_inv_pair}')

