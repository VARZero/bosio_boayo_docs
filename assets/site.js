(() => {
  const menu = document.querySelector('.menu-button');
  const sidebar = document.querySelector('.sidebar');
  menu?.addEventListener('click', () => {
    const open = sidebar.classList.toggle('open');
    menu.setAttribute('aria-expanded', String(open));
    menu.setAttribute('aria-label', open ? '메뉴 닫기' : '메뉴 열기');
  });
  sidebar?.querySelectorAll('a').forEach(link => link.addEventListener('click', () => {
    sidebar.classList.remove('open');
    menu?.setAttribute('aria-expanded', 'false');
  }));

  const headings = [...document.querySelectorAll('.article h2, .article h3')];
  const toc = document.querySelector('#toc-links');
  headings.forEach((heading, i) => {
    if (!heading.id) heading.id = `section-${i + 1}`;
    const link = document.createElement('a');
    link.href = `#${heading.id}`;
    link.textContent = heading.textContent;
    if (heading.tagName === 'H3') link.style.paddingLeft = '18px';
    toc?.append(link);
  });
  if (!headings.length) document.querySelector('.toc')?.remove();

  document.querySelectorAll('.article pre').forEach(pre => {
    const button = document.createElement('button');
    button.type = 'button';
    button.className = 'copy-button';
    button.textContent = '복사';
    button.setAttribute('aria-label', '코드 복사');
    pre.append(button);
    button.addEventListener('click', async () => {
      const value = pre.querySelector('code')?.textContent || '';
      try {
        await navigator.clipboard.writeText(value);
        button.textContent = '복사됨';
      } catch {
        button.textContent = '복사 불가';
      }
      setTimeout(() => button.textContent = '복사', 1600);
    });
  });

  const input = document.querySelector('#site-search');
  const results = document.querySelector('#search-results');
  let index = [];
  fetch('assets/search-index.json').then(r => r.json()).then(data => index = data).catch(() => {});
  function updateSearch() {
    const query = input.value.trim().toLocaleLowerCase();
    results.replaceChildren();
    if (!query) { results.hidden = true; return; }
    const matches = index.filter(item =>
      `${item.label} ${item.title} ${item.summary} ${item.keywords}`.toLocaleLowerCase().includes(query)).slice(0, 8);
    if (!matches.length) {
      const empty = document.createElement('p');
      empty.textContent = '일치하는 문서가 없습니다.';
      results.append(empty);
    } else matches.forEach(item => {
      const link = document.createElement('a');
      link.href = item.url;
      const title = document.createElement('strong');
      title.textContent = item.label;
      const summary = document.createElement('small');
      summary.textContent = item.summary;
      link.append(title, summary);
      results.append(link);
    });
    results.hidden = false;
  }
  input?.addEventListener('input', updateSearch);
  input?.addEventListener('keydown', e => {
    if (e.key === 'Escape') { input.value = ''; updateSearch(); input.blur(); }
    if (e.key === 'Enter') results.querySelector('a')?.click();
  });
  document.addEventListener('click', e => {
    if (!e.target.closest('.search-wrap')) results.hidden = true;
  });
})();
