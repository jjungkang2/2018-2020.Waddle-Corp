function displayNone(sel) {
   let el = document.querySelectorAll(sel);
   console.log(el.length);
   if (el.length == 0) return;
   for (let i = 0; i < el.length; i++) {
       el[i].style.display = 'none';
   }
};

function setAttribute(sel, tag, value) {
   let el = document.querySelectorAll(sel);

   if (el.length == 0) return;
   for (let i = 0; i < el.length; i++) {
       el[i].setAttribute(tag, value);
   }
}

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
};

function handler_DEBUG(handler) {
   return function() {
       console.log("Mutation");
       handler();
   }
};

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
       this.observer = new MutationObserver(handler_DEBUG(handler));
       this.connect();
   };
}

var mutationManager = new MutationManager();

function defaultDisplay() {
    displayNone("body > header");
    displayNone("div.sh_title._user_info");
    displayNone("div.thumb");
    displayNone("div.u_ft");
    displayNone("#goTop");
    displayNone("div.ad_area");
    document.querySelectorAll("[role = 'tab']").forEach(function(el){el.removeAttribute('role');});
}

function headNewsDisplay() {
    displayNone("div.sh_more.is_unfolded");
    displayNone("div.sh_thumb");
    displayNone("div.sh_body > ul > li:nth-child(2)");
    displayNone("div.sh_body > ul > li:nth-child(3)");
    displayNone("div.sh_body > ul > li:nth-child(4)");
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
   if (func != null) {
      window.Android.saveFunction(func.name);
      mutationManager.newMutationObserver(func);
      func();
   } else
      window.Android.saveFunction("");
      mutationManager.disconnect();
};

function map_init() {
    displayNone("span.Ngnb_logo");
    displayNone("div.Ngnb_service > span");
    displayNone("div.Ngnb_tool");
    displayNone("#LNB_SCROLLER > ul > li:nth-child(3)");
    displayNone("#LNB_SCROLLER > ul > li:nth-child(5)");
    document.querySelectorAll("[role = 'tab']").forEach(function(el){el.removeAttribute('role');});


    setAttribute("#LNB_SCROLLER > ul > li.Nlist_item.is_active > a", 'href', "/home.nhn");

    displayNone("body > div");
    displayNone("div.u_ft");

    document.querySelectorAll("[role = 'tab']").forEach(function(el){el.removeAttribute('role');});
}

function map_home() {
    defaultDisplay();
    headNewsDisplay();

    displayNone("div.Nlnb_submenu.Ntype_scroll");
    insertBefore("div.com_ranking.basic", "div#clusterHeadline");


    displayNone("div.com_ct_wrp");
    displayNone("#ct > div > div.com_ct_scr.star_cast");


    displayNone("#enterRankingContainer > div.ra_area > div.ra_tab._RANKING_WRAP > ul > li:nth-child(3)");

    displayNone("div.rl_img");
}

function map_tv() {
    defaultDisplay();
    displayNone("div.tv_brand_menu");
    displayNone("div.util_wrp");
}

function map_tvbrand() {
    defaultDisplay();
    displayNone("div.util_wrp");
    displayNone("div.tvcast_area");
    displayNone("#tvBandNews > div:nth-child(2)");
    displayNone("#tvBandNews > div.com_date_scr.tv_episode.tv_episode2");
}

function map_tvv() {
    displayNone("#header > div.gnbnew");
    displayNone("#clipInfo > div > div.info_tags");
    displayNone("#clipInfo > div > div.info_sub._info_btn");
    displayNone("#cate_lst > div.ch_more");

    displayNone("#list_scroll > ul > li.on > div > dl > dd");

    displayNone("#wrap_end");
    displayNone("#divFooter");
}

function map_ranking() {
    defaultDisplay();

    setAttribute("#sub_scroller > ul > li.Nsublist_item.is_active > a", 'href', "/ranking.nhn");
    displayNone("div.com_ranking.index");
}

function map_rankingOther() {
    defaultDisplay();
    displayNone("div.Nlnb_submenu.Ntype_scroll");
}

function map_movie() {
   defaultDisplay();
};

function map_now() {
    defaultDisplay();
    setAttribute("#sub_scroller > ul > li.Nsublist_item.is_active > a", 'href', "/now.nhn");
    setAttribute("div.Nlnb_submenu.Ntype_scroll", 'style', 'block');
    displayNone("ul.news_lst");
}

function map_nowOther() {
    defaultDisplay();
    displayNone("#ct > div > div.loading");
    displayNone("div.Nlnb_submenu.Ntype_scroll");
}

function map_article() {
    contentDisplay();
    console.log("11");

    insertBefore("div.media_end_head_info_variety_cmtcount", "div.ends_btn");
    displayNone("div.media_end_head_top");
    displayNone("div.media_end_head_fontsize._font_size_config_wrapper");
    displayNone("div.media_end_head_share");
    displayNone("div.media_end_head_tts");

    console.log("12");
    displayNone("div#channelRecommend");
    displayNone("div.media_end_linked");
    displayNone("div.r_group_comp.ad_box._da_banner");
    displayNone("div.ends_addition");
    displayNone("div#cbox_module");
    displayNone("div.nbd_a");

    console.log("13");
    displayNone("div.responsive_col2");
    displayNone("div#channelRecommendLayer");
    displayNone("div.media_journalistcard._JOURNALIST_CARD");
    displayNone("div.media_journalistcard._my_feed_extension_wrapper");
    displayNone("div.ad_area");
    displayNone("div#commentFontGroup");
    displayNone("div.more_news2");
    displayNone("div#likeItCountViewDiv");
    displayNone("div.media_end_head_lang._TRANSLATOR_WRAP");
    $("#dic_area").find('a').css('display', 'none');
    displayNone("div.more_news2");
    displayNone("div#likeItCountViewDiv");
    $("#dic_area").find('a').css('display', 'none');
    displayNone("div.relatedvideo");
    displayNone("div.rankingnews._FLICKING_WRAP._OFFICE_RANKING_ALL._PERSIST_META");

    if ($("html").attr('class') === "autosummary_active") {
        displayNone("a.media_end_head_autosummary_layer_close._close_button");
        displayNone("span.media_end_head_autosummary_layer_head_txt");
        displayNone("div.media_end_head_autosummary_layer_btn");
    }
}

function map_comment() {
    contentDisplay();
console.log("14");
    displayNone("div.media_end_head");
    displayNone("div#changecmt_text");
    displayNone("div.r_group_comp.section_list_box");
    displayNone("div.u_cbox_chart_wrap.u_cbox_chart_open");
    displayNone("div.u_cbox_comment_count_wrap");
    displayNone("div.u_cbox_slider");
    displayNone("div.u_cbox_head_tools");
    displayNone("div.u_cbox_notice");
    displayNone("div.u_cbox_translate_set_info");
    displayNone("div.u_cbox_info");
    displayNone("div.u_cbox_info_base");
console.log("15");
    displayNone("button.u_cbox_btn_refresh");
    displayNone("span.u_cbox_name");
    displayNone("span.u_cbox_ico_arrow");
    displayNone("div.media_end_channel_banner");
    displayNone("div.u_cbox_layer_comment_type");
    displayNone("button.u_cbox_btn_totalcomment");
}

function map_remainEntertain() {
   defaultDisplay();
}

let entertainURL = "https://m.entertain.naver.com";
let entertainNewsURL = "https://n.news.naver.com";
let tvURL = "https://m.tv.naver.com";

let entertainURLlist = [
                        ["/home", map_init],
                        ["/home.nhn", map_home],
                        ["/tv", map_tv],
                        ["/ranking", map_ranking],
                        ["/ranking.nhn", map_rankingOther],
                        ["/ranking/*", map_rankingOther],
                        ["/movie", map_movie],
                        ["/now", map_now],
                        ["/now.nhn", map_nowOther],
                        ["/now?*", map_nowOther],
                        ];

let entertainNewsURLlist = [
                            ["/entertain/article/comment/*", map_comment],
                            ["/entertain/ranking/article/comment/*", map_comment],
                            ["/entertain/movie/article/comment/*", map_comment],
                            ["/entertain/now/article/comment/*", map_comment],
                            ["/entertain/article/*", map_article],
                            ["/entertain/ranking/article/*", map_article],
                            ["/entertain/movie/article/*", map_article],
                            ["/entertain/now/article/*", map_article]
                            ];
let tvURLlist = [
                 ["/tvBrand/*", map_tvbrand],
                 ["/v/*", map_tvv]
                 ];

let prefixes = [ entertainURL, entertainNewsURL, tvURL ];
let URLlist = [ entertainURLlist, entertainNewsURLlist, tvURLlist ];


function run (func) {
   let isOperated = false, handlerIndex = 0;

   if (func) {
       map_wrap(func);
       return;
   }

   for (var i = 0; i < URLlist.length; i++) {
       for (var j = 0; j < URLlist[i].length; j++){
           if (wildcardMatch(window.location.href, prefixes[i] + URLlist[i][j][0]) && !isOperated) {
               handler = URLlist[i][j][1];
               handlerIndex = i;
               isOperated = true;
               break;
           }
       }
   }

   if (isOperated) {
       window.Android.saveTitle(document.title);
       map_wrap(handler);
   }
   else {
       window.Android.saveFunction("");
       window.Android.saveTitle(document.title);
       console.log("No Template");
   }
};