var rule = {
    title: '云盘资源网',
    host: 'https://res.yunpan.win',
    headers: {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36'},
    编码: 'utf-8',
    timeout: 5000,
    url: '/?PageIndex=1&PageSize=12&Keyword=&Type=fyclass&Tag=',
    searchUrl: '/?PageIndex=1&PageSize=12&Keyword=**&Type=&Tag=',
    searchable: 1,
    quickSearch: 1,
    filterable: 1,
    class_name: '电影&剧集&综艺&动漫',
    class_url: '电影&电视剧&综艺&动漫',
    filter_def: {},
    sniffer: 0,
    isVideo: '',
    play_parse: true,
    limit: 9,
    double: false,
    推荐: '*',
    一级: '.col;h5&&Text;img&&src;.card-text--span:eq(-2)&&Text;a:eq(-1)&&href',
    二级: {
        "title": "h5&&Text;.card-text--span:eq(-2)&&Text",
        "img": "img&&src",
        "desc": ".card-text:eq(2)&&Text;;;;",
        "content": ".card-text:eq(0)&&Text",
        "tabs": "js:TABS = ['云盘资源网']",
        lists: $js.toString(() => {
            LISTS = [];
            let lists1 = pdfa(html, '.card-footer&&.float-end').map(it => {
                let _tt = pdfh(it, 'a&&Text');
                let _uu = pdfh(it, 'a&&onclick').match(/open\('(.*?)'/)[1];
                return _tt + '$' + _uu;
            });
            LISTS.push(lists1);
        }),
    },
    搜索: '*',
    filter: {}
}
