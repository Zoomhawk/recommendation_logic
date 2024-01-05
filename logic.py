import pandas as pd
import sys
import requests
import string
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from collections import Counter
from math import sqrt
import ast
model = pd.read_csv('model.csv')
dimensionArray = pd.read_csv('dimension.csv')
dimensionArray = dimensionArray['dimenstions']

movieIdList = []
for i in range(1,len(sys.argv)):
    movieIdList.append(sys.argv[i])

recommendationList = []

stopWords = '''i
me
my
myself
we
our
ours
ourselves
you
your
yours
yourself
yourselves
he
him
his
himself
she
her
hers
herself
it
its
itself
they
them
their
theirs
themselves
what
which
who
whom
this
that
these
those
am
is
are
was
were
be
been
being
have
has
had
having
do
does
did
doing
a
an
the
and
but
if
or
because
as
until
while
of
at
by
for
with
about
against
between
into
through
during
before
after
above
below
to
from
up
down
in
out
on
off
over
under
again
further
then
once
here
there
when
where
why
how
all
any
both
each
few
more
most
other
some
such
no
nor
not
only
own
same
so
than
too
very
s
t
can
will
just
don
should
now'''

stopWords = stopWords.split()

def vectorize(arr):
    freq = Counter(arr)
    vector = []
    for dimention in dimensionArray:
        if(dimention not in freq):
            vector.append(0)
        else:
            vector.append(freq[dimention])
    return vector

ps = PorterStemmer()

def getStemWordList(words):
    result = []
    for word in words :
        result.append(ps.stem(word))
    return result

def getGenresList(genreObj):
    ans = []
    for obj in genreObj:
        ans.append(obj['name'])
    return ans

def filterStopWords(words):
    result = []
    for word in words:
        if(word not in stopWords):
            result.append(word)
    return result



def validWord(word):
    ans = ""
    word = word.lower()
    for ch in word:
        if(ch in string.ascii_lowercase ):
            ans += ch
    return ans

def validWordList(words):
    ans = []
    for word in words:
        ans.append(validWord(word))
    return ans

def getMovieVector(movieID):
    url = f'https://api.themoviedb.org/3/movie/{movieID}?language=en-US&api_key=d2d5c04da9b8133f121a383dc3cb2d2a'
    response = requests.get(url).json()
    keyWordResp =  requests.get(f'https://api.themoviedb.org/3/movie/{movieID}/keywords?language=en-US&api_key=d2d5c04da9b8133f121a383dc3cb2d2a').json()
    castResp = requests.get(f'https://api.themoviedb.org/3/movie/{movieID}/credits?language=en-US&api_key=d2d5c04da9b8133f121a383dc3cb2d2a').json()
    genres = response['genres']
    keyWords = keyWordResp['keywords']
    title = response['title']
    cast =  castResp['cast']
    crew = castResp['crew']
    genres = validWordList(getGenresList(genres))
    keyWords = validWordList(getGenresList(keyWords))
    title = [validWord(title)]
    cast = validWordList(getGenresList(cast))[:5]
    crew = validWordList(getGenresList(crew))[:5]
    tagList = genres + keyWords + title + cast + crew
    tagList = filterStopWords(tagList)
    tagList = getStemWordList(tagList)
    tagVector = vectorize(tagList)
    return tagVector

    
def cosine_similarity(l1, l2):
    l2 = ast.literal_eval(l2) # this is bcz array was likely given like '['1,'2',3']' instead of ['1','2','3']
    dot_product = sum(int(i)*int(j) for i,j in zip(l1, l2))
    magnitude1 = sqrt(sum(int(i)**2 for i in l1))
    magnitude2 = sqrt(sum(int(j)**2 for j in l2))
    if(magnitude1 == 0):
        magnitude1 = 1
    if(magnitude2 == 0):
        magnitude2 = 1
    return dot_product / (magnitude1 * magnitude2)



def top3Movies(movieID):
    movieVector = getMovieVector(movieID)
    simmilarityArray = []
    simMovID = []
    for vec in model['vector']:
        simmilarityArray.append(cosine_similarity(movieVector,vec))
    for id in model['movieId']:
        simMovID.append(id)
    
    top1score = 0
    top2score = 0
    top3score = 0
    top1 = -1
    top2 = -1
    top3 = -1

    for i in range(model.shape[0]):   # look out might give error 
        if(simMovID[i] == movieID):
            continue

        if(simmilarityArray[i] > top1score):
            top3score = top2score
            top3 = top2
            top2score = top1score
            top2 = top1
            top1score = simmilarityArray[i]
            top1 = simMovID[i]
        elif(simmilarityArray[i] > top2score):
            top3score = top2score
            top3 = top2
            top2score = simmilarityArray[i]
            top2 = simMovID[i]
        elif(simmilarityArray[i] > top3score):
            top3score = simmilarityArray[i]
            top3 = simMovID[i]

    return [top1,top2,top3]


for id in movieIdList:
    recommendationList.extend(top3Movies(id))


print(recommendationList)