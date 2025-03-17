/*
 * Filters state can be one of:
 * - undefined => disabled
 * - true => select ONLY articles with this tag
 * - false => do NOT select articles with this tag
 * */
(function iife() {
  'strict';

  globalThis.tagFilters = {};

  function parseQuery(queryString) {
    const query = {};
    for (let pair of (queryString[0] === '?' ? queryString.slice(1) : queryString).split('&')) {
      pair = pair.split('=');
      const name = decodeURIComponent(pair[0]);
      const values = decodeURIComponent(pair[1] || '').split(',');
      if (!query[name]) {
        query[name] = [];
      }
      Array.prototype.push.apply(query[name], values);
    }
    return query;
  }

  function includes(anArray, value) {
    return anArray.includes(value);
  }

  function updateArticlesVisibility() {
    const includeFilters = Object.keys(globalThis.tagFilters).filter((tagFilter) => globalThis.tagFilters[tagFilter] === true);
    const excludeFilters = Object.keys(globalThis.tagFilters).filter((tagFilter) => globalThis.tagFilters[tagFilter] === false);
    for (const article of Array.prototype.slice.call(document.getElementsByTagName('article'))) {
      // article-excerpt: we ignore it
      if (!article.dataset.tags) {
        continue;
      }
      const articleTags = JSON.parse(article.dataset.tags);
      const allIncludeTags = includeFilters.every((tag) => includes(articleTags, tag));
      const anyExcludeTag = excludeFilters.some((tag) => includes(articleTags, tag));

      // Now implementing the core logic
      let shouldDisplay = !anyExcludeTag;
      if (shouldDisplay && includeFilters.length > 0) {
        shouldDisplay = allIncludeTags;
      }

      if (shouldDisplay) {
        article.classList.remove('mg-faded');
      } else {
        article.classList.add('mg-faded');
      }
    }
  }

  globalThis.toggleTagFilter = function toggleTagFilter(tag) {
    let filterState = globalThis.tagFilters[tag];
    if (filterState === true) {
      this.classList.remove('mg-tag-filter-include');
      filterState = false;
      this.classList.add('mg-tag-filter-exclude');
      this.title = 'Tag filter (exclude matching articles)';
    } else if (filterState === false) {
      this.classList.remove('mg-tag-filter-exclude');
      filterState = undefined;
      this.title = 'Tag filter (disabled)';
    } else {
      filterState = true;
      this.classList.add('mg-tag-filter-include');
      this.title = 'Tag filter (include matching articles)';
    }
    globalThis.tagFilters[tag] = filterState;
    updateArticlesVisibility();
  };

  globalThis.toggleLangTagFilter = function toggleLangTagFilter(newLang) {
    let lang = this.textContent;
    globalThis.tagFilters[`lang:${ lang }`] = undefined;
    lang = newLang || globalThis.langs[langs.indexOf(lang) + 1];
    if (lang === undefined) {
      lang = 'lang';
      this.title = 'Language filter (disabled)';
    } else {
      globalThis.tagFilters[`lang:${ lang }`] = true;
      this.title = `Language filter (include only "${ lang }" articles)`;
    }
    this.textContent = lang;
    updateArticlesVisibility();
  };

  // This is a bit redundant with /tag/$tag.html pages,
  // but is slightly more powerful as it allow to combine multiple filters
  const queryParameters = parseQuery(globalThis.location.search);
  for (const [ qpName, qpValue ] of Object.entries(queryParameters)) {
    if (!qpValue) {
      continue;
    }
    if (qpName === 'lang') {
      const buttonElement = document.getElementById('lang-tag-filter');
      globalThis.toggleLangTagFilter.bind(buttonElement)(qpValue[0]);
    } else if (qpName === 'tags') {
      for (const tag of qpValue) {
        const buttonElement = document.getElementById(`${ tag }-tag-filter`);
        globalThis.toggleTagFilter.bind(buttonElement)(tag);
      }
    }
  }
}());
