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

.. code-block:: jinja

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


.. code-block:: python

    ARTICLE_RECOMMENDER_OPTIONS = {'max_recommendations':  5,
                                   'min_score':            0.1}


Notes
=====
The recommender will parse the content of all articles, pass the plain text
(ignoring code and math blocks, for example) to an NLTK tokenizer, and then
vectorizes all the articles using scikit-learn's TFIDF vectorizer. Finally, a
similarity score is calculated based on cosine similarity.


Because of all the above, the plug-in will make the generation process
*significantly* slower. Please keep this in mind. You might want to only enable
this plug-in in ``publishconf.py``.


Credits
=======
This plug-in started off as modifications to the ``related_posts`` plug-in
available on `Pelican's Plugin Repository`_, and diverged enough for me to
release it as an independent plug-in.

.. _Pelican: https://github.com/getpelican/pelican
.. _`Pelican's Plugin Repository`: https://github.com/getpelican/pelican-plugins
