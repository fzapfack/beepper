import nltk
import re
import string
from unidecode import unidecode
from sklearn.feature_extraction.text import CountVectorizer
from hello.models import Question, Answer


class Matcher:
    def __init__(self, num_match_returned=5):
        self.num_match_returned = num_match_returned
        self.stpwds = nltk.corpus.stopwords.words("french")
        self.vectorizer = None
        self.dtm = None
        self.questions_id = None
        # rajouter des mots commes les, docteur, ...

    def tokenize(self, content):
        if content is None:
            return None
        else:
            #remove http links
            content = re.sub(r'http\S+', '', content)
            # remove formatting
            content = re.sub("\s+", " ", content)
            # convert to lower case
            content = content.lower()
            # Remove accent
            content = unidecode(content)
            # remove punctuation (preserving intra-word dashes)
            # content = "".join(letter for letter in content if letter not in punct)
            punct = string.punctuation.replace("-", "")
            regex = re.compile('[%s]' % re.escape(punct))
            content = regex.sub(' ', content)
            content = re.sub("[^a-zA-Z]", " ", content)
            # remove dashes attached to words but that are not intra-word
            content = re.sub("[^[:alnum:]['-]", " ", content)
            content = re.sub("[^[:alnum:][-']", " ", content)

            # remove extra white space
            content = re.sub(" +", " ", content)
            # remove leading and trailing white space
            content = content.strip()
            # tokenize
            tokens = content.split(" ")
            # remove stopwords
            tokens = [token for token in tokens if token not in self.stpwds and len(token) > 2]
            return tokens

    def tokenize_questions(self):
        questions = Question.objects.all()
        tokens = [self.tokenize(q.txt_clean) for q in questions]
        self.questions_id = [q.pk for q in questions]
        return tokens

    def train(self):
        tokens = self.tokenize_questions()
        voc = list(set([i for sublist in tokens if sublist is not None for i in sublist]))
        join_tokens = [" ".join(i) for i in tokens]
        self.vectorizer = CountVectorizer(vocabulary=voc)
        self.dtm = self.vectorizer.fit_transform(join_tokens)
        return True

    def transform(self, query):
        if self.vectorizer is None:
            self.train()
        query_tokens = self.tokenize(query)
        join_tokens = " ".join(query_tokens)
        transf = self.vectorizer.transform([join_tokens])
        return transf

    def match_question(self, query):
        transf = self.transform(query)
        res = self.dtm.dot(transf.transpose())
        res = res.toarray().flatten()
        top = res.argsort()[-1:-10:-1]
        match_questions = []
        for i in top:
            id = self.questions_id[i]
            q = Question.objects.get(pk=id)
            out = {'id': id,
                   'txt': q.txt_clean,
                   }
            ans = Answer.objects.filter(question_id=id)
            if len(ans) == 0:
                out['answers'] = None
            else:
                out['answers'] = [{'id':a.pk, 'txt':a.txt_clean} for a in ans]
            match_questions.append(out)
        return match_questions


