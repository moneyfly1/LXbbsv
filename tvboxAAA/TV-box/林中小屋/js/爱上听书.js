var rule = {
    title: '爱上你听书网',
    host: 'https://www.230ts.net',
    url: '/sort/fyclass/fypage.html',
    searchUrl: '/search.html?searchtype=name&searchword=**&page=fypage',
    searchable: 2,
    quickSearch: 0,
    headers: {
        'User-Agent': 'PC_UA'
    },
    timeout: 5000,
    class_parse: '.nav-ol&&li:gt(0):lt(6);a&&Text;a&&href;.*/(\\w+).html',
    play_parse: true,
    lazy: `js:
        let url = input.replace("www","m");
        let html = request(url, {headers: rule.headers});
        let match = html.match(/<audio.*?src="(.*?)"/i);
        if (match) {
            input = match[1];
        } else {
            let m3u8 = html.match(/"(https?:\/\/[^"]*m3u8[^"]*)"/i);
            input = m3u8 ? m3u8[1] : input;
        }
    `,
    limit: 6,
    推荐: '#myTab_Content1&&li;.tab-book-title&&Text;*;.tab-book-author&&Text;*',
    一级: 'ul.list-works&&li;.list-book-dt--span&&Text;.lazy&&data-original;.book-author:eq(2)&&a&&Text;a&&href',
    二级: {
        title: '.book-cover&&alt;.book-info&&dd--span:eq(1)&&Text',
        img: '.book-cover&&src',
        desc: '.book-info&&dd:eq(4)&&Text;;;.book-info&&dd--span:eq(3)&&Text;.book-info&&dd--span:eq(2)&&Text',
        content: '.book-des&&Text',
        tabs: '.playlist-top&&h2',
        lists: `js:
            let tabs = [];
            let lists = [];
            pdfa(html, '.playlist-top&&h2').forEach((tab, index) => {
                tabs.push(pd(tab, '&&Text'));
                let list = pdfa(html, '#playlist:eq(' + index + ')&&li');
                lists.push(list.map(item => {
                    let title = pd(item, 'a&&Text');
                    let url = pd(item, 'a&&href');
                    return title + '$' + url;
                }).join('#');
            });
            setResult(tabs, lists);
        `,
    },
    搜索: '*',
}