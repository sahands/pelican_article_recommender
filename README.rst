Pelican Article Recommender
===========================

Article recommendation system for Pelican_ based on post similarity calculated
using NLTK and scikit-learn's TFIDF vectorizer.

Requirements
============
You will need to have ``numpy``, ``scikit-learn`` and ``nltk`` installed. You
also need to have the necessary ``nltk`` corpus installed. Run ``>>>
nltk.download()`` to download if necessary.

Usage
=====
When the plug-in is activated, you can use ``article.recommended_articles``
list to get a list of recommended articles. You can then use this inside your
templates. For example:

.. code:: 
    :lexer: jinja2

    {% if article.recommended_articles %}
        <div class="related-posts">
            <h1>Recommended Articles</h1>
            <ul>
                {% for post in article.recommended_articles %}
                    <li>
                        <a href="{{ SITEURL }}/{{ post.url }}" 
                           rel="bookmark"
                           title="Permalink to {{ post.title|striptags }}">
                           <span itemprop="name">
                               {{ post.title }}
                           </span>
                        </a>
                    </li>
                {% endfor %}
            </ul>
        </div>
    {% endif %}


Options
=======
A dictionary ``ARTICLE_RECOMMENDER_OPTIONS`` can be defined in Pelican's
settings file. Currently the following two keys from this dictionary are used:

- ``max_recommendations`` (default = 5): the maximum number of articles recommended.
- ``min_score`` (default = 0.05): minimum score to be included as a recommendation. Value must be between 0 and 1.

Example:


.. code::
    :lexer: python

    ARTICLE_RECOMMENDER_OPTIONS = {'max_recommendations':  5,
                                   'min_score':            0.1}


.. _Pelican: https://github.com/getpelican/pelican
