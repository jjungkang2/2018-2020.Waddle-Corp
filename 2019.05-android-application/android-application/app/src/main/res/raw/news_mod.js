function displayNone(sel) {
   let el = document.querySelectorAll(sel);

   if (el.length == 0) return;
   for (let i = 0; i < el.length; i++) {
       el[i].style.display = 'none';
   }
};

function displayNoneAll() {
    displayNone("body");
};

function removeAttribute(sel, tag) {
   let el = document.querySelectorAll(sel);

   if (el.length == 0) return;
   for (let i = 0; i < el.length; i++) {
       el[i].removeAttribute(tag);
   }
}

function insertBefore(sel1, sel2) {
   let el1 = document.querySelector(sel1), el2 = document.querySelector(sel2);

   if (el1 == null || el2 == null) return;
   mutationManager.disconnect();
   el2.insertAdjacentElement('beforebegin', el1);
   mutationManager.connect();
};

function match(sel, func) {
   let el = document.querySelector(sel);

   if (el == null) return;
   el.addEventListener('click', func);
};

function wildcardMatch(str1, str2) {
    var escapeRegex = (str1) => str1.replace(/([.*+?^=!:${}()|\[\]\/\\])/g, "\\$1");
    return new RegExp("^" + str2.split("*").map(escapeRegex).join(".*") + "$").test(str1);
}

function handlerWrapper(str, handler) {
    return function() {
        handler();
    }
}

class MutationManager {
    constructor() {
        this.target = document.body;
        this.config = {
            characterData: true,
            characterDataOldValue: true,
            childList: true,
            subtree: true
        };
        this.observer = null;
    };

    disconnect() {
        if (this.observer) this.observer.disconnect();
    };

    connect() {
        if (this.observer) this.observer.observe(this.target, this.config);
    };

    newMutationObserver(handler) {
        this.disconnect();
        this.observer = new MutationObserver(handlerWrapper('Mutation', handler));
        this.connect();
    };
}

var mutationManager = new MutationManager();

function defaultDisplay() {
    displayNone("div.Nlnb");
    displayNone("div.Ngnb");
    displayNone("div.Nlnb._lnb_scroll");
    displayNone("div.section_headline");
    displayNone("#ct > div.shortcutlnb");
    displayNone("div.r_group_comp.r_group_footer");
    displayNone("div.sh_thumb");
    displayNone("div.sh_body > ul > li:nth-child(2)");
    displayNone("div.sh_body > ul > li:nth-child(3)");
    displayNone("div.sh_body > ul > li:nth-child(4)");
    displayNone("div.r_news_im");
    displayNone("div.ad_area");
    displayNone("div.r_group_comp.section_list_box");
    displayNone("div.section_list_box_inner");
    displayNone("div.r_group_comp.topic.newstopic");
    displayNone("div.u_ft");
    displayNone("div.section_airs");
    displayNone("div.like_channel");
}

function headNewsDisplay() {
    displayNone("div.sh_thumb");
    displayNone("div.sh_body > ul > li:nth-child(2)");
    displayNone("div.sh_body > ul > li:nth-child(3)");
    displayNone("div.sh_body > ul > li:nth-child(4)");
    displayNone("div.sh_nav");
}

function listNewsDisplay() {
    insertBefore("div.r_group_comp", "div._bottom_item");
    $("div.h2_area_inner > a").removeAttr('href');
    displayNone("ul.commonlist");
    let list = $("ul.commonlist");

    if ($("div.h2_area_inner > a")!=null) {
        for (let i = 0; i < $("div.h2_area_inner > a").length; i++) {
            $("div.h2_area_inner > a")[i].onclick = function() {
                if (list[i].getAttribute('style'))
                    list[i].removeAttribute('style');
                else
                    list[i].style.display = 'none';
            }
        }
    }
    displayNone("div.commonlist_img");
}

function minimumDisplay() {
    displayNone("div.Nlnb");
    displayNone("div.Nlnb._lnb_scroll");
    displayNone("div.r_group_comp.r_group_footer");
    displayNone("img");
}


function contentDisplay() {
    displayNone("div.Ngnb");
    displayNone("div.Nlnb");
    displayNone("div.Nlnb._lnb_scroll");
    displayNone("div#channelBanner");
    displayNone("div.u_ft");
}

function map_wrap(func) {
    window.Android.saveTitle(document.title);
    if(func != null){
        window.Android.saveFunction(func.name);
        mutationManager.newMutationObserver(func);
        func();
    }
    else
    {
        window.Android.saveFunction("");
        mutationManager.disconnect();
    }
}

function map_init() {
    displayNone("body > div.u_skip");
    displayNone("body > header > div > span");
    displayNone("span.Nservice_subitem");
    displayNone("div.Ngnb_tool");
    displayNone("div.shortcutlnb");

    removeAttribute("#ct > div.Nlnb._lnb_scroll > div > div > ul", 'role');

    displayNone("#ct > div.r_home_wrp._moreViewLinkArea");
    displayNone("#ct > div.Nlnb._lnb_scroll > button");

    for (let i = 8; i < 14; i++)
        displayNone(`#ct > div.Nlnb._lnb_scroll > div > div > ul > li:nth-child(${i})`);

    displayNone("#goTop");
}

function map_home(){
    displayNone("body > div.u_skip");
    displayNone(".r_more.r_more_stop");
    displayNone(".r_ico_b.r_cmt._template");
    displayNone("#ct > div.r_home_wrp._moreViewLinkArea.no_tap_highlight1569163639211 > div.r_more.r_more_stop");

    defaultDisplay();
    headNewsDisplay();
    displayNone("div.r_group_comp");
}

function map_pol() {
    defaultDisplay();
    headNewsDisplay();
    listNewsDisplay();
}

function map_eco(){
    insertBefore("div.r_stock", "body > header");
    displayNone("div.r_stock_inner > img");
    defaultDisplay();
    headNewsDisplay();
    listNewsDisplay();
    }

function map_soc() {
    defaultDisplay();
    headNewsDisplay();
    listNewsDisplay();
}

function map_it() {
    defaultDisplay();
    headNewsDisplay();
    listNewsDisplay();
}

function map_lif() {
    defaultDisplay();
    headNewsDisplay();
    listNewsDisplay();
}

function map_wor() {
    defaultDisplay();
    headNewsDisplay();
    listNewsDisplay();
}

function map_ran() {
    defaultDisplay();
    headNewsDisplay();
    listNewsDisplay();

    displayNone("div.tab_sec");
}

function map_opi() {
    defaultDisplay();
    headNewsDisplay();
    listNewsDisplay();
}

function map_pho() {
    minimumDisplay();
}

function map_tv() {
    headNewsDisplay();
    listNewsDisplay();
    displayNone("div.r_news_im");
}

function map_article() {
    contentDisplay();

    insertBefore("div.media_end_head_info_variety_cmtcount", "div.ends_btn");
    displayNone("div.media_end_head_top");
    displayNone("div.media_end_head_fontsize._font_size_config_wrapper");
    displayNone("div.media_end_head_share");
    displayNone("div.media_end_head_tts");
    displayNone("div.media_end_head_info_datestamp");
    displayNone("div#channelRecommend");
    displayNone("div.media_end_linked");
    displayNone("div.r_group_comp.ad_box._da_banner");
    displayNone("div.ends_addition");
    displayNone("div#cbox_module");
    displayNone("div.nbd_a");
    displayNone("div.responsive_col2");
    displayNone("div#channelRecommendLayer");
    displayNone("div.media_journalistcard._my_feed_extension_wrapper");
    displayNone("div.ad_area");
    displayNone("div#commentFontGroup");
    displayNone("div.more_news2");
    displayNone("div#likeItCountViewDiv");

    if ($("html").attr('class') === "autosummary_active") {
        displayNone("span.media_end_head_autosummary_layer_head_txt");
        displayNone("div.media_end_head_autosummary_layer_btn");
        displayNone("a.media_end_head_autosummary_help");
        window.Android.saveFunction("");
    }
}

function map_comment() {
    contentDisplay();

    displayNone("div.media_end_head");
    displayNone("div#changecmt_text");
    displayNone("div.r_group_comp.section_list_box");
    displayNone("div.u_cbox_chart_wrap.u_cbox_chart_open");
    displayNone("div.u_cbox_comment_count_wrap");
    displayNone("div.u_cbox_slider");
    displayNone("div.u_cbox_head_tools");
    displayNone("button.u_cbox_btn_refresh");
    displayNone("span.u_cbox_name");
    displayNone("span.u_cbox_ico_arrow");
    displayNone("div.media_end_channel_banner");
    displayNone("div.u_cbox_layer_comment_type");
    displayNone("button.u_cbox_btn_totalcomment");
}

function map_test() {
    console.log('test');
}

var URLprefix = "https://m.news.naver.com";

var URLlist = [
    ["/", map_init, "map_init"],
    ["/home.nhn*", map_home, "map_home"],
    ["/main.nhn?mode=LSD&sid1=100*",map_pol,"map_pol"],
    ["/main.nhn?mode=LSD&sid1=101*", map_eco, "map_eco"],
    ["/main.nhn?mode=LSD&sid1=102*", map_soc, "map_soc"],
    ["/main.nhn?mode=LSD&sid1=105*", map_it, "map_it"],
    ["/main.nhn?mode=LSD&sid1=103*", map_lif, "map_lif"],
    ["/main.nhn?mode=LSD&sid1=104*", map_wor, "map_wor"],
    ["/rankingList.nhn*", map_ran, "map_ran"],
    ["/opinion/home.nhn*", map_opi, "map_opi"],
    ["/photoHome.nhn*", map_pho, "map_pho"],
    ["/tvHome.nhn*", map_tv, "map_tv"],
    ["/read.nhn?*", map_article, "map_article"],
    ["*Read.nhn?*",map_article, "map_article"],
    ["/comment/list.nhn?*", map_comment, "map_comment"]
];

function run (func) {
    let isOperated = false,
        handlerIndex = 0;
    if (func) {
        window.Android.saveTitle(document.title);
        map_wrap(func);
        return;
    }
    if (URLlist!=null) {
        for (var i = 0; i < URLlist.length; i++) {
            if (wildcardMatch(window.location.href, URLprefix + URLlist[i][0]) && !isOperated) {
                handler = URLlist[i][1];
                handlerIndex = i;
                isOperated = true;
            }
        }
    }
    if (isOperated) {
        console.log(URLlist[handlerIndex][2]);
        map_wrap(handler);
    } else {
        window.Android.saveFunction("");
        window.Android.saveTitle(document.title);
        console.log("No Template");
    }
}