Pelican Article Recommender
===========================

Article recommendation system for pelican based on post similarity calculated
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




