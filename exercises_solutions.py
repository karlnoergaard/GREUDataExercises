'''------------Exercises-----------------'''
import gamspy as gp
import pandas as pd

# 1. initialize a container and write a gdx containing a single set called "my_first_set" with elements "one", "two", "three" (populate manually)
m=gp.Container()
my_first_set=gp.Set(container=m,name='my_first_set',records=['one','two','three'])
m.write('my_first_gdx_solution.gdx')

# 2. read the excel file data/some_parameter_ex1.xlsx and create sets and a parameter in a new container
some_parameter_ex1_raw=pd.read_excel(r'mock_data\some_parameter_ex1.xlsx')
letters=gp.Set(m,name='letters',records=some_parameter_ex1_raw['letters'])
nouns=gp.Set(m,name='nouns',records=some_parameter_ex1_raw['nouns'])
adjectives=gp.Set(m,name='adjectives',records=some_parameter_ex1_raw['adjectives'])
some_parameter_ex1=gp.Parameter(m,name='some_parameter_ex1',domain=[letters,nouns,adjectives],records=some_parameter_ex1_raw)

# 3. read the excel file data/some_parameter_ex2.xlsx and create a parameter in the same container as in exercise 2 adding missing elements to sets as needed
some_parameter_ex2_raw=pd.read_excel(r'mock_data\some_parameter_ex2.xlsx')
#combine records
all_letters=some_parameter_ex1_raw['letters'].tolist()
all_letters.extend(some_parameter_ex2_raw['letters'].tolist())
all_nouns=some_parameter_ex1_raw['nouns'].tolist()
all_nouns.extend(some_parameter_ex2_raw['nouns'].tolist())
all_adjectives=some_parameter_ex1_raw['adjectives'].tolist()
all_adjectives.extend(some_parameter_ex2_raw['adjectives'].tolist())
all_my_first_set=['one','two','three']
all_my_first_set.extend(some_parameter_ex2_raw['my_first_set'].tolist())
#ensure uniqueness
all_letters=list(dict.fromkeys(all_letters))
all_nouns=list(dict.fromkeys(all_nouns))
all_adjectives=list(dict.fromkeys(all_adjectives))
all_my_first_set=list(dict.fromkeys(all_my_first_set))
#rebuild sets - updating set records makes them "dynamic" and dynamic sets cannot be domains causing the ensuing parameter to be ill-defined
letters=gp.Set(m,name='letters',records=all_letters)
nouns=gp.Set(m,name='nouns',records=all_nouns)
adjectives=gp.Set(m,name='adjectives',records=all_adjectives)
my_first_set=gp.Set(container=m,name='my_first_set',records=all_my_first_set)

#add parameter
some_parameter_ex2=gp.Parameter(m,name='some_parameter_ex2',domain=[letters,nouns,adjectives,my_first_set],records=some_parameter_ex2_raw)

# 4. Create the set "colors" as a subset of adjectives containing only the color-adjectives and add it to the container
actual_colors=['pink','red','purple','blue','green','yellow','orange']
colors_set=[i for i in all_adjectives if i in actual_colors]
colors=gp.Set(m,name='colors',domain=[adjectives],records=colors_set)

# 5. Read some_parameter_ex3.xlsx and create a parameter in the same container as in exercise 1-4 dropping entries containing NaN as needed
some_parameter_ex3_raw=pd.read_excel(r'mock_data\some_parameter_ex3.xlsx')
some_parameter_ex3=some_parameter_ex3_raw.dropna()
some_parameter_ex3=gp.Parameter(m,name='some_parameter_ex3',domain=[nouns],records=some_parameter_ex3)

# 6. Read some_parameter_ex4.xlsx and create a parameter in the same container as in exercise 1-5 renaming elements according to mock_metadata.xlsx as needed
some_parameter_ex4_raw=pd.read_excel(r'mock_data\some_parameter_ex4.xlsx')
metadata_translation=pd.read_excel(r'mock_data\mock_metadata.xlsx',sheet_name='translations')
metadata_synonyms=pd.read_excel(r'mock_data\mock_metadata.xlsx',sheet_name='synonyms')
#build renaming-dicts
translation_dict=dict(zip(metadata_translation['Danish'], metadata_translation['English']))
synonyms_dict=dict(zip(metadata_synonyms['synonym'], metadata_synonyms['word']))
some_parameter_ex4_raw['nouns']=some_parameter_ex4_raw['nouns'].replace(translation_dict)
some_parameter_ex4_raw['adjectives']=some_parameter_ex4_raw['adjectives'].replace(synonyms_dict)
some_parameter_ex4=gp.Parameter(m,name='some_parameter_ex4',domain=[nouns,adjectives],records=some_parameter_ex4_raw)
# 7. export gdx and compare to "solutions.gdx"
m.write('solutions.gdx')