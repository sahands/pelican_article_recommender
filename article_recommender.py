"""
Related posts plug-in that uses the content of the posts to determine post
similarity. Use scikit-learn, and nltk.
"""
from __future__ import unicode_literals
from __future__ import print_function

from codecs import open as codec_open
from docutils.frontend import OptionParser
from docutils.nodes import FixedTextElement
from docutils.nodes import Inline
from docutils.nodes import Text
from docutils.parsers.rst import Parser
from docutils.utils import new_document
from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer
from operator import itemgetter
from os import path
from pelican import signals
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from heapq import nlargest


ignored_node_types = (Inline, FixedTextElement)


class LemmaTokenizer(object):
    def __init__(self):
        self.wnl = WordNetLemmatizer()

    def __call__(self, doc):
        return [self.wnl.lemmatize(t) for t in word_tokenize(doc)]


def parse_rst_content(filename, source_content):
    settings = OptionParser(components=(Parser,)).get_default_values()
    parser = Parser()
    document = new_document(filename, settings)
    parser.parse(source_content, document)

    def _walk(node):
        if type(node) is Text:
            yield node
        if not isinstance(node, ignored_node_types):
            for child in node.children:
                for n in _walk(child):
                    yield n
    return ' '.join(n for n in _walk(document))


def get_content(article):
    source_content = None
    with codec_open(article.source_path, 'r', 'utf-8') as source_file:
        source_content = source_file.read()
    if path.splitext(article.source_path)[1] == '.rst':
        return parse_rst_content(article.source_path, source_content)
    return source_content


def add_recommended_articles(generator):
    options = generator.settings.get('ARTICLE_RECOMMENDER_OPTIONS', {})
    max_count = options.get('max_recommendations', 5)
    min_score = options.get('min_score', 0.05)
    documents = [get_content(article) for article in generator.articles]

    tfidf = TfidfVectorizer(max_df=0.9,
                            ngram_range=(1, 1),
                            stop_words='english',
                            strip_accents='unicode',
                            tokenizer=LemmaTokenizer()
                            ).fit_transform(documents)

    similarities = cosine_similarity(tfidf)

    for index, article in enumerate(generator.articles):
        recommended_indices = nlargest(max_count + 1,
                                       enumerate(similarities[index]),
                                       key=itemgetter(1))[1:]

        recommended_indices = [(i, s)
                               for i, s in recommended_indices
                               if s > min_score]

        article.recommended_articles = [generator.articles[i]
                                        for i, score
                                        in recommended_indices]

        print(recommended_indices)
        similar_articles = '\n'.join('- ' + r.title
                                     for r in article.recommended_articles)
        print('{} is similar to:\n{}\n'.format(article.title,
                                               similar_articles))


def register():
    signals.article_generator_finalized.connect(add_recommended_articles)
