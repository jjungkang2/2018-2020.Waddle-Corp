function displayNone(sel) {
    if ($(sel) != null) {
        $(sel).css('display', 'none');
    } else console.log('error');
};

function wildcardMatch(str1, str2) {
    var escapeRegex = (str1) => str1.replace(/([.*+?^=!:${}()|\[\]\/\\])/g, "\\$1");
    return new RegExp("^" + str2.split("*").map(escapeRegex).join(".*") + "$").test(str1);
};

function handler_DEBUG(handler) {
    return function () {
        console.log("Mutation");
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
        this.observer = new MutationObserver(handler_DEBUG(handler));
        this.connect();
    };
}

var mutationManager = new MutationManager();


function searchDisplay() {
    displayNone("strong.g_product_img");
}

function map_addMenuBar() {
    mutationManager.disconnect();

    var nodesel = "<div class=\"_1HoamrW2s3\" style=\"position: fixed; bottom: 0; z-index: 9000; display: table; padding: 6px 4px 7px 4px; width: 100%; box-sizing: border-box; table-layout: fixed; border-top: 1px solid #e5e5e5; background-color: #eee; font-size: 14px; line-height: 1.25em;\"><div class=\"DHpy4HCHrV\" style=\"display: table-cell; position: relative; padding: 0 2px; padding-bottom: env(safe-area-inset-bottom); text-align: center; vertical-align: top;\"><button type=\"button\" class=\"_3qTIMZDKm3 N=a:flo.buy\" style=\"border: none; color: #fff; background-color: #2bcb0f; font-size: 16px; width: 100%; height: 41px;\" onclick=\"window.location.href='https://m.pay.naver.com/o/main/cart';\">장바구니</button></div><div class=\"DHpy4HCHrV N=a:flo.basket\" style=\"display: table-cell; position: relative; padding: 0 2px; padding-bottom: env(safe-area-inset-bottom); text-align: center; vertical-align: top;\"><button type=\"button\" class=\"RJt2sajs2z\" style=\"border: none; color: #fff; background-color: #2bcb0f; font-size: 16px; width: 100%; height: 41px;\" onclick=\"window.location.href='https://m.pay.naver.com/o/home?tabMenu=SHOPPING&frm=s_order';\">주문배송</button></div></div>";

    const node = $(nodesel);
    $('body').append(node);

    mutationManager.connect();
}

function map_wrap(func) {
    if (func != null) {
        $("html").attr('lang', "ko");
        window.Android.saveFunction(func.name);
        console.log("wrap");

        mutationManager.newMutationObserver(func);
        func();
    } else {
        window.Android.saveFunction("");
    }
}

function map_init() {
    searchDisplay();

    displayNone("#common_header > div.g_header_area > h1 > a.g_logo_naver");
    displayNone("#header > div > div");

    displayNone("div.g_menu");
    displayNone("div.g_search_area");
    displayNone("#lnb");

    displayNone("#list_area1 > div:nth-child(1)");
    displayNone("#list_area1 > div:nth-child(2)");
    displayNone("#list_area1 > div:nth-child(3)");
    displayNone("#list_area1 > div:nth-child(4)");

    mutationManager.disconnect();
    if ($("span#user_nickname"))
        $("span#user_nickname").text("고객");
    $("h3.profile_none").text("고객님의 쇼핑정보");
    mutationManager.connect();

    $("#user_info_part").removeAttr('style');
    $("#user_info_part").children().css('display', 'none');
    $("#user_info_part > div.profile").removeAttr('style');

    displayNone("#list_area2");
    displayNone("#ranking_part");
    displayNone("#part_hotdeal_wrap > div");
    displayNone("#list_area2 > div:nth-child(3) > h4:nth-child(3)");
    displayNone("#list_area2 > div:nth-child(3) > div:nth-child(4)");

    $("#list_area2").removeAttr('style');

    $("#user_info_part > div > a").attr('href', "/my/keep-products");
    $("#part_hotdeal_wrap > h3 > a").attr('href', "/hotdeal/m/luckto/best.nhn");

    displayNone("div.footer");
    displayNone("#wrap > div.a");
}

function map_product() {
    searchDisplay();


    displayNone("div._1wh159qWvr > h1 > a._3BfIe3ayn8");
    displayNone("div._1wh159qWvr > div");
    displayNone("div._13MDKIxtSc.nv-openmain");
    displayNone("div._14F-vCxnLa");
    displayNone("div._1tRucTDTOA");
    displayNone("div.JXzoJjkwDr");

    let children = $("#lnb > ul > li");
    for (let i = 0; i < children.length; i++) {
        if (!(i == 1 || i == 2))
            children[i].style.display = 'none';
    }
}

function map_searchResults() {
    searchDisplay();

    displayNone("#root > div > div._1RpitpZf-r.header_slimsrch.header_basic > div > h1");
    displayNone("#common_srch > div > div._1Evdr_XzkT");
    displayNone("#root > div > div._1RpitpZf-r.header_slimsrch.header_basic > div > div._13jVwiNI67");

    displayNone("#taglist");
    displayNone("#content > div._18q_Q69S6u > div._2mILB9DptZ");

    if ($("#content > div._1D9HVaXJhe > div._3hrWCKUnkA.active").attr('class').includes("active"))
        $("#content > div._1D9HVaXJhe > div._3hrWCKUnkA > h3 > a > span").trigger('click');

    let children = $("ul._2klRMnwJXJ").children();

    for (let i = 0; i < children.length; i++) {
        if (children.eq(i).text().includes("판매처") || !children.eq(i).text().includes("네이버페이"))
            children.eq(i).css('display', 'none');
    }

    let children2 = $("ul._2klRMnwJXJ > li");

    for (let i = 0; i < children2.length; i++) {
        let child = children2.eq(i);
        if (child.find('div').eq(0).find('a').eq(0).attr('href') != null) {
            child.find('div').eq(0).find('a').eq(0).css('display', 'none');
            child.find('div > div > div').eq(1).css('display', 'none');
            child.find('div > div > div').eq(2).css('display', 'none');
        } else if (child.find('a > span > img').attr('src') != null) {
            child.find('a > span').css('display', 'none');
            child.find('a > div > div').eq(1).css('display', 'none');
            child.find('a > div > div').eq(2).css('display', 'none');
        } else {
            child.find('a > div > span').css('display', 'none');
            child.find('a > div > div > div').eq(1).css('display', 'none');
            child.find('a > div > div > div').eq(2).css('display', 'none');
        }
    }
    displayNone("#content > div.Tmmg1SPFAk");
    displayNone("#content > div._5Xxa0muasn");
    displayNone("#content > div._3vBuLfqo2W");
    displayNone("#content > div._2v12zLtMjO");
    displayNone("#root > div > div._3npXF63qS1 > div > div:nth-child(3)");
    displayNone("#root > div > div._3npXF63qS1 > div > div._14F-vCxnLa");
}

function map_luckytoday() {
    displayNone("#common_header");
    displayNone("#category_area");

    let children = $("ul.tab_menu > li");
    children[0].style.display = 'none';
    children[1].style.display = 'none';

    let children2 = $("ul.luck_lst.hot_lst > li");
    for (let i = 0; i < children2.length; i++) {
        let child = children2.eq(i);
        /* delete image */
        child.find('div > a > div').eq(0).css('display', 'none');
        /* delete ranking */
        child.find('div > a > div').eq(1).find('div').eq(0).css('display', 'none');
        /* delete naverpay */
        child.find('div > a > div').eq(1).find('div').eq(2).find('span > span.txt.spr_bf.ico_npay').css('display', 'none');
        /* delete share button */
        child.find('div > div > span > a').eq(0).css('display', 'none');
    }

    displayNone("#content_list > a");
    displayNone("#content_list > div.tag_lst");
}

function map_hpnews() {
    displayNone("#common_header");

    let children = $("ul.tab_menu > li");
    children[0].style.display = 'none';
    children[1].style.display = 'none';

    displayNone("#bannerArea");
    displayNone("#content > div.sort_box_inline > div > ul > li:nth-child(4)");
    displayNone("#content > div.sort_box_inline > div > ul > li:nth-child(5)");

    let children2 = $("ul.list > li");
    children2.eq(3).css('display', 'none');
    children2.eq(4).css('display', 'none');

    let children3 = $("ul#eventList > li");
    for (let i = 0; i < children3.length; i++) {
        let child = children3.eq(i);
        child.find('div > a > div').eq(0).css('display', 'none');
    }
}

function map_hpnews_detail() {
    displayNone("#MAIN_CONTENT_ROOT_ID > div > div.lp6_4DcgX6 > div._1RpitpZf-r.header_basic");
    displayNone("#content > div.JkoeNDsDqc");
    displayNone("#content > div._24HL5AhpfG");
    displayNone("#content > div.u0Kz0YS6I9");

    let children = $("div#content > div").eq(2).find('div').eq(1).find('ul > li');
    for (let i = 0; i < children.length; i++) {
        child = children.eq(i);
        child.find('a > div').eq(0).css('display', 'none');
        child.find('button').css('display', 'none');
        child.find('a > div > div').eq(2).css('display', 'none');
        if (child.find('h3').text() == "인기 태그") {
            child.css('display', 'none');
        }
    }

    displayNone("img");
}

function map_smartstore() {
    $('html').attr('lang', 'ko');

    displayNone("#wrap > header");
    /* 제품 이미지 */
    displayNone("#content > div._2Lqek8czMS");
    /* 배송정보 */
    displayNone("#content > ul._36zPYPEn2D");
    /* 상품정보 */
    displayNone("#content > div._13zS-8ytsi");
    /* 광고 */
    displayNone("#content > div.NuIHCUj0xw");

    /* 탭에서 상세정보 삭제 */
    $("#_productTabContainer > ul > li:nth-child(1)").css('display', 'none');

    $('img').css('display', 'none');

    mutationManager.disconnect();
    if ($("#REVIEW").attr('class') != "_3bCe-Qsh3J _-9S54Gohnj" && $("#QNA").attr('class') != "_3bCe-Qsh3J _-9S54Gohnj")
        $("#REVIEW > a > div > span").trigger('click');

    displayNone("#content > div._18JPsCkcVe > div.hd0pgui6pR");
    displayNone("#content > div._18JPsCkcVe > div.hd0pgui6pR > div.dUUTbau5Q2._2vu3CUrLjO");
    displayNone("#content > div._18JPsCkcVe > div._2xyJEsJ96x > div._1QgpbPEYUA");
    displayNone("#content > div.s0vn2iP7ko");

    let list1 = $("#content > div#content").children();
    for (let i = 0; i < list1.length - 3; i++) {
        if (i > 6)
            list1.eq(i).css('display', 'none');
    }

    let list = $("#content > div._1Hgglz8odI > ul").children();

    for (let i = 0; i < list.length; i++) {
        if (list.eq(i).text().includes("비밀글입니다."))
            list.eq(i).css('display', 'none');
    }


    list1.eq(list1.length - 3).find('div > div').eq(0).find('button').text("지금 구매하기");
    list1.eq(list1.length - 3).find('div > div').eq(1).find('button').text("장바구니 담기");
    mutationManager.connect();

    list1.eq(list1.length - 3).find('div > div').eq(2).css('display', 'none');

    if (list1.eq(list1.length - 2).attr('style') == 'display:none') {
        mutationManager.disconnect();

        buttons = list1.eq(list1.length - 2).find('div > div > button');
        gift = list1.eq(list1.length - 2).find('div > div');

        buttons.eq(buttons.length - 3).text("지금 구매하기");
        gift.eq(gift.length - 2).css('display', 'none');
        buttons.eq(buttons.length - 1).text("장바구니 담기");

        mutationManager.connect();
    }

    let list2 = $("#content > ul.E2QDRW5f2k").children();
    for (let i = 0; i < list2.length; i++) {
        if (!(i == 2 || i == 3))
            list2.eq(i).css('display', 'none');
    }

    insertBefore("#content > ul.E2QDRW5f2k", "div._2ZS3TDbYf8");

    displayNone("#footer > div._3sv30komac");
}

function map_seller() {
    let list = $("#content > div").children();
    for (let i = 2; i < list.length; i++)
        list.eq(i).css('display', 'none');

    displayNone("#content > div._1vnhtDKWjF");
    displayNone("#MAIN_CONTENT_ROOT_ID > div > div.lp6_4DcgX6.product_detail > div._3npXF63qS1 > div > div._13MDKIxtSc.nv-openmain");
    displayNone("#MAIN_CONTENT_ROOT_ID > div > div.lp6_4DcgX6.product_detail > div._3npXF63qS1 > div > div._14F-vCxnLa");

}

function map_cart() {
    displayNone("#header > div > div");
    displayNone("#header > div > h2 > a");
    displayNone("div.banner_pointplus");
    displayNone("div.box_cart.shop_link_item");
    displayNone("div.spot_event");
    displayNone("div.footer");
    displayNone("div.ck_allbx.topbx");
}

function map_order() {
    displayNone("body > div._body > div.header._header > div > a");
    displayNone("div._deliveryInfos > div > table > tbody > tr:nth-child(1)");
    displayNone("div._deliveryInfos > div > table > tbody > tr:nth-child(4)");


    displayNone("div.banner_pointplus");
    displayNone("div.gift_send_banner");

    document.querySelector("h3.ord_tit_v1 > a").click();

    displayNone("div._paymentAmountInfoArea > h3:nth-child(1)");
    displayNone("div._paymentAmountInfoArea > div._discountForm");

    displayNone("div.error_info.guide_layer.paymentMethodStatementArea");
    $("#orderSheetForm > div.ord_cont._productDetail._productInfos._coupon_area > div._paymentInfoArea > span > div > div > div.simplepay_cont > div > div.pay_tab_area > ul > li.pay_tab_menu._GENERAL_TAB.on > a > strong").click();
    $("#orderSheetForm > div.ord_cont._productDetail._productInfos._coupon_area > div._paymentInfoArea > span > div > div > div.simplepay_cont > div > div.payreg_area._generalPaymentTab > table > tbody > tr > td:nth-child(3) > a > span").click();
    displayNone("div.pay_tab_area");

    displayNone("div._creditCardTab");

    $("#bankname").val('020').trigger('change');
    $("#refund2").trigger('click');
    $("#rdo3_r2").trigger('click');


    displayNone("div._npayBenefit.on");
    displayNone("div.spot_event");

    displayNone("#orderSheetForm > div.ord_cont._productDetail._productInfos._coupon_area > h3.ord_tit_v1._paymentInfoTitle");
    displayNone("#orderSheetForm > div.ord_cont._productDetail._productInfos._coupon_area > div._paymentInfoArea");
    displayNone("#orderSheetForm > div.ord_cont._productDetail._productInfos._coupon_area > div.order_box.receipt_sc._cashReceiptTemplate");
}

function map_status_home() {
    displayNone("#header");
    displayNone("#container > div.ptitle_sc > a");
    displayNone("#content > div.detail_section.ordernum_sc");
    displayNone("#content > div.spot_event");
    displayNone("div.footer");
}

function map_status_delivery() {
    displayNone("body > div > div.header");
    displayNone("#ct > h2 > a");
    displayNone("#ct > div:nth-child(4)");
    displayNone("#ct > div:nth-child(5)");
    displayNone("#ct > div:nth-child(6)");
    displayNone("#ct > div:nth-child(7)");

    let info = $("#ct > div.wrap_buy_box.delivery_check > table > tbody > tr > td");
    for (let i = 0; i < info.length; i++) {
        if (i % 3 === 0)
            info.eq(i).text(alt_str(info.eq(i).text()));
    }
}

function map_order_delivery() {
    if ($("div.layer_pointplus > button > span") != null)
        $("div.layer_pointplus > button > span").trigger('click');

    displayNone("body > div.wrap > div.header");
    displayNone("body > div.wrap > div.container > div.spot_event");
    displayNone("body > div.wrap > div.container > div.pointplus_section.benefit_section");
    displayNone("div.thmb");
    displayNone("body > div.wrap > div.footer > div.f_box");
    displayNone("body > div.wrap > div.footer > p");
    displayNone("body > div.wrap > div.footer > div.f_corp_area");
}

function map_done() {
    $("#ct > div.dimlayer._pointChargeLayer > div.layer_bottom > div > button").trigger('click');

    displayNone("body > div._body > div.header._header > div > a");
    displayNone("#ct > div.ord_cont > div.ordf_sc > dl");
    displayNone("#ct > div.ord_cont > div.ordf_sc > div.ordf_inr > div.ord_sc.fst");
    displayNone("#ct > div.ord_cont > ul > li:nth-child(2)");
    displayNone("#ct > div.ord_cont > div:nth-child(3)");
    displayNone("#ct > div.ord_cont > div:nth-child(4)");
    displayNone("#ct > div.ord_cont > div.spot_event");
}

function altstr(str) {
    let newstr = str.substring(0, 4) + '년' + str.substring(5, 7) + '월' + str.substring(8, 10) + '일' + str.substring(10, 12) + '시' + str.substring(13, 15) + '분' + str.substring(16, 18) + '초';
    return newstr;
}

const prefixes = [
    "https://m.shopping.naver.com",
    "https://msearch.shopping.naver.com",
    "https://m.smartstore.naver.com",
    "https://m.pay.naver.com"
];

let shoppingURLlist = [
    ["/", map_init],
    ["/home/m/index.nhn", map_init],
    ["/my/keep-products", map_product],
    ["/my/keep-stores", map_product],
    ["/my/recently-viewed-products", map_product],
    ["/hotdeal/m/luckto/*", map_luckytoday],
    ["/hotdeal/m/plan/*", map_hpnews],
    ["/plan/details/*", map_hpnews_detail],
    ["*/seller", map_seller],
    ["/*/stores/*/products/*", map_smartstore]
];

let msearchURLlist = [
    ["*search/*", map_searchResults],
    ["/search/all?*", map_searchResults],
    ["/bridge/recentGate.nhn?*", map_smartstore]
];

let smartstoreURLlist = [
    ["*/seller", map_seller],
    ["*/products/*", map_smartstore]
];

let payURLlist = [
    ["/o/main/cart*", map_cart],
    ["/o/orderSheet/*", map_order],
    ["/o/orderDone/*", map_done],
    ["/o/orderStatus/*", map_status_home],
    ["*deliveryTracking*", map_status_delivery],
    ["/o/orderStatus/deliveryTracking/*", map_status_delivery],
    ["/o/home?tabMenu=SHOPPING*", map_order_delivery]
];

const URLlist = [
    shoppingURLlist,
    msearchURLlist,
    smartstoreURLlist,
    payURLlist
];

function run(func) {
    let isOperated = false,
        handlerIndex = 0;
    if (func) {
        map_wrap(func);
        return;
    }

    for (var i = 0; i < URLlist.length; i++) {
        for (var j = 0; j < URLlist[i].length; j++) {
            if (wildcardMatch(window.location.href, prefixes[i] + URLlist[i][j][0]) && !isOperated) {
                handler = URLlist[i][j][1];
                handlerIndex = i;
                isOperated = true;
                if (i === 0 || i === 1) map_addMenuBar();
                break;
            }
        }
    }

    if (isOperated) {
        window.Android.saveTitle(document.title);
        if (i < 9) map_addMenuBar();
        map_wrap(handler);
    } else {
        window.Android.saveFunction("");
        window.Android.saveTitle(document.title);
    }
};