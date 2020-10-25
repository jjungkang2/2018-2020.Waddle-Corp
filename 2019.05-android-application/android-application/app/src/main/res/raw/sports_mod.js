function displayNone(sel) {
    if ($(sel) != null) {
        $(sel).css('display', 'none');

    }
    else console.log('error');
};

function displayNoneAll() {
    displayNone("body");
};

function displayShowParent(sel){
    if($(sel) != null && $(sel).parent() != null){
        $(sel).parent().removeAttr('style');
    }
    else console.log('error');
};

function displayShow(sel){
    if($(sel) != null){
        $(sel).removeAttr('style');
    }
    else console.log('error');
};

function insertBefore(sel1, sel2) {
    mutationManager.disconnect();

    if($(sel1)!=null && $(sel2)!=null && $(sel1).length && $(sel2).length) {
        $(sel2).before($(sel1));
    }
    mutationManager.connect();
};

function insertAfter(sel1, sel2) {
    mutationManager.disconnect();

    if($(sel1)!=null && $(sel2)!=null && $(sel1).length && $(sel2).length) {
        $(sel2).after($(sel1));
    }
    mutationManager.connect();
};

function match(sel, func) {
    if ($(sel)!=null && $(sel).length) {
        $(sel).click(func);
    }
};

function wildcardMatch(str1, str2) {
    var escapeRegex = (str1) => str1.replace(/([.*+?^=!:${}()|\[\]\/\\])/g, "\\$1");
    return new RegExp("^" + str2.split("*").map(escapeRegex).join(".*") + "$").test(str1);
}

function handlerWrapper(str, handler) {
    return function() {
        /*window.Android.checkInfiniteLoop();*/
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
        this.observer.observe(this.target, this.config);
    };

    newMutationObserver(handler) {
        this.disconnect();
        this.observer = new MutationObserver(handlerWrapper('Mutation', handler));
        this.connect();
    };
}

var mutationManager = new MutationManager();
/*var periodicHandler = new PeriodicHandler();*/

function defaultDisplay(){
    displayNone("footer");
    displayNone("div.lnb_home");
    displayNone("div.section_scroll_m");
    displayNone("a.page_fast2");
}

function headlinenewsDisplay(){
    displayNone("div.headline_bx");
}

function removeHeader(){
    displayNone("header#header");
}


function listNewsDisplay(){
    displayNone("div.home_group");
    displayNone("div.home_group2");
    displayNone("div.home_ad_group");
    displayNone("div.headline_news_guide");
    displayNone("div.home_option");
    displayNone("div.home_airs");
    displayShowParent("div.home_article_rank");
    displayShow("#_match_box_cms_tmp");
    displayNone("div.flick_pg");
    insertBefore("#_match_box_cms_tmp","div.headline_group");

    match("div.home_article_rank > div > a", function(){
          if($("div.home_article_rank > ol")[0].getAttribute('style'))
          $("div.home_article_rank > ol").removeAttr('style');
          else
          displayNone("div.home_article_rank > ol"); });

    if(!($("div.home_article_rank").attr('data-fixed'))){
        displayNone("div.home_article_rank > ol");
        $("div.home_article_rank").attr('data-fixed','fixed');
    }
    $("div.home_article_rank > div > a").removeAttr('href');
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
    defaultDisplay();
    displayNone("div#ct");
    displayNone("a.score");
    displayNone("div.page_fast");

}

function map_home() {
    defaultDisplay();
    removeHeader();
    listNewsDisplay();
    displayNone("div#myteam");
    displayNone("div.slide_lft");
}


function map_team(){
    displayNone("nav.top_nav");
    displayNone("a.myteam_count");
    displayNone("a.share");
    displayNone("ul#top_menu > li:nth-child(4)");
    displayNone("ul#top_menu > li:nth-child(5)");
    match("ul#top_menu > li:nth-child(1) > a",function(){map_wrap(map_team_schedule)});
    $("ul#top_menu > li:nth-child(1) > a").removeAttr('href');
}

function map_team_schedule(){
    displayNone("nav.top_nav");
    displayNone("div.team_cover");
    displayNone("section> time:nth-child(2)");
    displayNone("figure");
}

function map_team_vod(){
    displayNone("nav.top_nav");
    displayNone("div.team_cover");
    displayNone("footer");

}

function map_team_news(){
    displayNone("nav.top_nav");
    displayNone("div.team_cover");
    displayNone("ul.noti_tab");
    displayNone("div.img_area");
}

function map_events(){
    defaultDisplay();
    removeHeader();
    listNewsDisplay();
    displayNone("div.slide_lft");
}

function map_gamecenter_kbaseball(){

   displayNone("div.score_stat");
   displayNone("div.score_etc");
 if ($("div#_scoreboard").attr('display') != 'none' && $("div#summary").length == 0) {
      mutationManager.disconnect();
      away_selector = $("div.score_etc > table > tbody > tr:nth-child(1)");
      home_selector = $("div.score_etc > table > tbody > tr:nth-child(2)");
      $("<div id='summary' class='score_tit'><table><caption>스코어보드 요약</caption><thead><tr><th scope='col'><span class='blind'>요약</span></th></tr></thead><tbody><tr><td id= 'target1'></td></tr><tr><td id = 'target2'></td></tr></tbody></table></div>").insertAfter("div.score_tit");
      $("td#target1").append("<span class= 'tit'>총" + away_selector.children("td:nth-child(1)").text() + "점 안타" + away_selector.children("td:nth-child(2)").text() + "개 에러" + away_selector.children("td:nth-child(3)").text() + "개</span>");
      $("td#target2").append("<span class= 'tit'>총" + home_selector.children("td:nth-child(1)").text() + "점 안타" + home_selector.children("td:nth-child(2)").text() + "개 에러" + home_selector.children("td:nth-child(3)").text() + "개</span>");
      mutationManager.connect();
   }

    displayNone("footer#footer");
    displayNone("header.end_head");
    displayNone("div#_today_games_scroll");
    displayNone("div.ad_box");
    displayNone("a.logo");
    if($("span:contains('기록')") != null) $("span:contains('기록')").parent().parent().remove();
    if($("span:contains('응원')") != null) $("span:contains('응원')").parent().parent().remove();
    displayNone("div#wrap > div:nth-child(3)");
    if($("span:contains('전력')") != null) $("span:contains('전력')").parent().click(function(){map_wrap(map_preview_kbaseball)});
    if($("span:contains('중계')") != null) $("span:contains('중계')").parent().click(function(){map_wrap(map_relay_kbaseball)});
    if($("span:contains('영상')") != null) $("span:contains('영상')").parent().click(function(){map_wrap(map_vod_kbaseball)});

}

function map_preview_kbaseball(){

    $(document).ready(function(){
                      $("div.record_bx_wrap").each(function(){

                                                   mutationManager.disconnect();
                                                   lose = $(this).children(".stat_lose").length;


                                                   win = $(this).children(".stat_win").length;

                                                   if($(this).find("em").length == 0){
                                                   $(this).append("<em class ='score' >"+win+"승"+lose+"패</em>");
                                                   mutationManager.connect();
                                                   }
                                                   });
                      $("div.record_by_wrap").attr('data-fixed','fixed');
                      });
    displayNone("div.ad_box");
    displayShow("div#wrap > div:nth-child(3)");
    displayNone("footer#footer");
    displayNone("div.record_bx_wrap > span");
    displayNone("div#_gamecenter_top");
    insertAfter("div#_live_player_wrap","div#_gamecenter_top");
    displayNone("span.thmb");
    displayNone("div.team_vs_info");
    displayNone("div.thmb_image");
    displayNone("div.end_chart_box");
    displayNone("div#_top_player_section");
    displayNone("div.score_graph_wrap");
    $("ul.lineup_list > li > a").removeAttr('href');

    /* make table */
    $('tbody > tr > th').each(function() {
                              $(this).insertBefore($(this).prev('tbody > tr > td:nth-child(1)'));
                              });
}

function map_relay_kbaseball(){
    displayShow("div#wrap > div:nth-child(3)");
    displayNone("footer#footer");
    displayNone("div#_gamecenter_top");
    insertAfter("div#_live_player_wrap","div#_gamecenter_top");

    displayNone("a.logo");
    displayNone("div#_pitch_select_area");
    displayNone("div#_pts_area");
    displayNone("div#_view_option_box");
    displayNone("span.img");
}
function map_vod_kbaseball(){
    displayShow("div#wrap > div:nth-child(3)");
    displayNone("footer#footer");
    displayNone("div#_gamecenter_top");
    insertAfter("div#_live_player_wrap","div#_gamecenter_top");

    displayNone("a.logo");
    displayNone("span.video_thmb");
}

function map_video(){
    displayNone("header#end_header");
    displayNone("footer#footer");
    displayNone("div#changecmt_text");
    displayNone("div.ad_box");
    displayNone("span.video_thmb_wrap");
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
    displayNone("div.to_article");
    displayNone("div.u_cbox_cleanbot");
    displayNone("div.u_cbox_notice");
    displayNone("div.btn_fixed");
    match("h4.video_section_title", function(){
          if($("div#_rec_video_list").attr('style'))
          $("div#_rec_video_list").removeAttr('style');
          else
          displayNone("div#_rec_video_list"); });

    if(!($("h4.video_section_title").attr('data-fixed'))){
        displayNone("div#_rec_video_list");
        $("h4.video_section_title").attr('data-fixed','fixed');
    }

}
function map_article(){
    defaultDisplay();
    contentDisplay();
    removeHeader();
    displayNone("div.slide_lft");

    $(document).ready(
        function() {
            insertBefore("div.media_end_head_info_variety_left", "div.ends_btn");
        }
    );

    $("div.media_end_head_info_variety_cmtcount").css('width', 'fit-content');
    $("div.media_end_head_info_variety_cmtcount").css('float', 'none');

    displayNone("div.media_end_head_top");
    displayNone("div.media_end_head_fontsize");
    displayNone("div.media_end_head_share");
    displayNone("div.media_end_head_tts");
    displayNone("div#channelRecommend");
    displayNone("div.media_end_linked");
    displayNone("div.media_end_linked_more");
    displayNone("div.r_group_comp.ad_box._da_banner");
    displayNone("div.ends_addition");
    displayNone("div#cbox_module");
    displayNone("div.responsive_col2");
    displayNone("div#channelRecommendLayer");
    displayNone("div.media_journalistcard._my_feed_extension_wrapper");
    displayNone("div.ad_area");
    displayNone("div.more_news2");
    displayNone("div.ends_btn");
    displayNone("div.end_ad_bottom");
    displayNone("div.end_comp");
    displayNone("div.section_scroll_m");
    displayNone("div#_scoreboard_table");
    displayNone("div.scroll_area");
    displayNone("div.sns_share_wrap");
    displayNone("div.news_cmt_option2");
    displayNone("div.nw_im_n");
    displayNone("div.ad_box_wrap");
    displayNone("article.main_article > a");
    displayNone("div.media_end_categorize");
    displayNone("div.media_journalistcard");
    displayNone("a.page_fast2");

}
function map_comment(){
    contentDisplay();
    removeHeader();

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
    displayNone("div.to_article");
    displayNone("div.u_cbox_cleanbot");
    displayNone("header.end_head");
    displayNone("div.u_cbox_notice");
}

function map_sports_schedule() {
    defaultDisplay();
    removeHeader();
    displayNone("img");
    displayNone("div.schedule_floating_box");
    displayNone("a.veta_native_at_link");
    displayNone("div.ad_box");
    displayNone("div.gamedata_info");
    displayNone("a#_team_schedule_btn");
    match("ul.schedule_tab_list > li > a", map_sports_schedule);
}



var URLprefix= "https://m.sports.naver.com";

var URLlist = [
               ["/", map_init, "map_init"],
               ["/index.nhn*", map_home, "map_home"],
               ["/kbaseball/index.nhn*", map_events],
               ["/wbaseball/index.nhn*", map_events],
               ["/kfootball/index.nhn*", map_events],
               ["/wfootball/index.nhn*", map_events],
               ["/basketball/index.nhn*", map_events],
               ["/volleyball/index.nhn*", map_events],
               ["/golf/index.nhn*", map_events],
               ["/general/index.nhn*", map_events],
               ["/esports/index.nhn*", map_events],
               ["/*/vod/index.nhn*", map_video, "map_video"],
               ["/*video.nhn?*", map_video, "map_video"], /* video */
               ["/*/news/read.nhn?*", map_article, "map_article"], /* article */
               ["/comment/list.nhn?*", map_comment, "map_comment"], /* comment */
               ["/*/schedule/index.nhn*", map_sports_schedule,"map_gamecenter_kbaseball"],
               ["*/baseball/gamecenter/*", map_gamecenter_kbaseball, "map_gamecenter_kbaseball"],
               ["/team/schedule.nhn?*date=*",map_team_schedule,"map_team_schedule"],
               ["/team/schedule.nhn?*",map_team, "map_team"],
               ["/team/vod.nhn?*",map_team_vod,"map_team_vod"],
               ["/team/news.nhn?*",map_team_news,"map_team_news"]

               ];


function run (func) {

    let isOperated = false,
    handlerIndex = 0;
    if (func) {
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
        map_wrap(handler); /* Mystery: Why codes after this line does not execute? */
    } else {
        map_wrap(null);
        console.log("No Template");
    }
};