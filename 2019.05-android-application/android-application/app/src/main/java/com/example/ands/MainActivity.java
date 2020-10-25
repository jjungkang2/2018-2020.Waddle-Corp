package com.example.ands;

import androidx.appcompat.app.ActionBar;
import androidx.appcompat.app.AppCompatActivity;
import androidx.constraintlayout.widget.ConstraintLayout;
import androidx.constraintlayout.widget.ConstraintSet;

import android.app.Activity;
import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.content.res.Configuration;
import android.graphics.Bitmap;
import android.graphics.Rect;
import android.net.Uri;
import android.os.Build;
import android.os.Bundle;
import android.os.Handler;
import android.view.KeyEvent;
import android.view.MotionEvent;
import android.view.View;
import android.view.Window;
import android.view.accessibility.AccessibilityEvent;
import android.view.inputmethod.InputMethodManager;
import android.webkit.ConsoleMessage;
import android.webkit.CookieManager;
import android.webkit.CookieSyncManager;
import android.webkit.JavascriptInterface;
import android.webkit.JsResult;
import android.webkit.WebChromeClient;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageButton;
import android.widget.LinearLayout;
import android.widget.ProgressBar;
import android.widget.Toast;

import com.google.gson.Gson;
import com.google.gson.reflect.TypeToken;

import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Stack;

import static com.example.ands.R.id.webView;

public class MainActivity extends AppCompatActivity implements View.OnClickListener {
    private WebView mWebView; // WebView

    //history thing
    private Stack mBackStack;
    private Stack mNextStack;
    private ArrayList<String> mNow;
    private ArrayList<String> mPrevious = new ArrayList<>();

    //favorite thing
    private ArrayList < FavoriteList > myFavorites = new ArrayList < > ();
    private String myFavoritesToString;
    private Stack tempStack = new Stack();
    private Stack favoriteBackStack = new Stack();
    private Gson gson;
    private String titleName;

    //cookie thing
    private String isLogin;

    private String myUrl = "https://nid.naver.com/nidlogin.login";

    private String saveHTML;

    private String funcParam = null;

    private boolean clearNextStack;
    private Handler handler = new Handler();

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        getWindow().requestFeature(Window.FEATURE_PROGRESS);
        setContentView(R.layout.activity_main);

        // Hide action bar
        getSupportActionBar().hide(); // Hide action bar

        // WebView Setting
        mWebView = findViewById(webView);
        mWebView.getSettings().setJavaScriptEnabled(true);
        mWebView.addJavascriptInterface(new MyJavascriptInterface(), "Android");
        mWebView.setWebChromeClient(new WebChromeClient(){

            public boolean onConsoleMessage(ConsoleMessage cm) {
                //Log.d("MyApplication",
                if (cm.message().contains("Mutation")) return true;
                System.out.println(cm.message() + " -- From line "
                        + cm.lineNumber() + " of " + cm.sourceId() );
                return true;
            }
        });
        mWebView.setWebViewClient(new WebViewClientClass());
        mWebView.getSettings().setDomStorageEnabled(true);
        mWebView.getSettings().setRenderPriority(WebSettings.RenderPriority.HIGH);
        mWebView.getSettings().setCacheMode(WebSettings.LOAD_NO_CACHE);

        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.KITKAT) {
            mWebView.setLayerType(View.LAYER_TYPE_HARDWARE, null);
        } else mWebView.setLayerType(View.LAYER_TYPE_SOFTWARE, null);

        // History Setting
        mBackStack = new Stack();
        mNextStack = new Stack();

        // Cookie Setting
        if (Build.VERSION.SDK_INT < Build.VERSION_CODES.LOLLIPOP) {
            CookieSyncManager.createInstance(this);
        }

        SharedPreferences sf = getSharedPreferences("sFile",MODE_PRIVATE);
        isLogin = sf.getString("isLogin", "home");

        if(getIntent().hasExtra("isLogin")) {
            isLogin = getIntent().getStringExtra("isLogin");
        }

        if (isLogin.equals("logout")) toNotLogin();
        else if (isLogin.equals("home")) toHome();
        else if (isLogin.equals("login")){
            gson = new Gson();
            myFavoritesToString = getIntent().getStringExtra("favorite");
            myFavorites = gson.fromJson(myFavoritesToString, new TypeToken<ArrayList<FavoriteList>>(){}.getType());

            mPrevious = mNow;
            mNow = (ArrayList<String>)((ArrayList<String>)myFavorites.get(0).getBackStack().pop()).clone();
            mWebView.loadUrl(mNow.get(0));
            favoriteBackStack = (Stack) myFavorites.get(0).getBackStack().clone();
            mBackStack = (Stack) favoriteBackStack.clone();

        }
    }

    @Override
    protected void onResume() {
        super.onResume();

        if (Build.VERSION.SDK_INT < Build.VERSION_CODES.LOLLIPOP) {
            CookieSyncManager.getInstance().startSync();
        }
    }

    @Override
    protected void onPause() {
        super.onPause();

        if (Build.VERSION.SDK_INT < Build.VERSION_CODES.LOLLIPOP) {
            CookieSyncManager.getInstance().stopSync();
        }
    }

    @Override
    protected void onStop() {
        super.onStop();

        SharedPreferences sharedPreferences = getSharedPreferences("sFile",MODE_PRIVATE);
        SharedPreferences.Editor editor = sharedPreferences.edit();
        if (isLogin.equals("logout")) editor.putString("isLogin", isLogin);
        else if(isLogin.equals("logout") || isLogin.equals("home"))
            editor.putString("isLogin", "home");

        gson = new Gson();
        myFavoritesToString = gson.toJson(myFavorites);
        editor.putString("favorite", myFavoritesToString);

        editor.commit();
    }

    @Override
    public boolean onKeyDown(int keyCode, KeyEvent event) {
        ArrayList <String> str;
        System.out.println("hereeee: "+keyCode);
      if ((keyCode == KeyEvent.KEYCODE_BACK)) {
          System.out.println("haha");
          clearNextStack = false;
          if (mBackStack.isEmpty()) return true;

          str= (ArrayList) mBackStack.pop();
          mNextStack.push(str);

          if (mBackStack.isEmpty()) return true;
          mNow = (ArrayList) mBackStack.pop();
          funcParam = mNow.get(1);

          mWebView.loadUrl(mNow.get(0));
          return true;
      }
      return super.onKeyDown(keyCode, event);
    }

    @Override
    public void onConfigurationChanged(Configuration newConfig){
        super.onConfigurationChanged(newConfig);
    }

    private class WebViewClientClass extends WebViewClient {

        @Override
        public boolean shouldOverrideUrlLoading(WebView view, String url) {
            funcParam = null;
            if (url.startsWith("naverapp")) {
                return true;
            }
            view.loadUrl(url);

            return true;
        }

        @Override
        public void onPageStarted(WebView view, String url, Bitmap favicon) {
            view.setVisibility(View.INVISIBLE);
        }

        @Override
        public void onPageFinished(WebView view, String url) {
            super.onPageFinished(view, url);

            view.sendAccessibilityEvent(AccessibilityEvent.TYPE_VIEW_FOCUSED);
            if (url.equals("https://nid.naver.com/nidlogin.login")) {
                view.setVisibility(View.VISIBLE);
                return;
            }

            // Get Cookie
            if (Build.VERSION.SDK_INT < Build.VERSION_CODES.LOLLIPOP) {
                CookieSyncManager.getInstance().sync();
            } else {
                CookieManager.getInstance().flush();
            }
/*
            if (isLogin.equals("logout") && !mWebView.getUrl().contains("nidlogin.login")) {
                toHome();
            }
*/
            if (!view.getUrl().contains("entertain.naver.com") &&
                    !view.getUrl().contains("tv.naver.com") &&
                    !view.getUrl().contains("news.naver.com/entertain")) {
                view.loadUrl("javascript: " + readJsFile(R.raw.jquery_min));
            }

            view.loadUrl("javascript: " + news());

            view.sendAccessibilityEvent(AccessibilityEvent.TYPE_VIEW_FOCUSED);

            view.setVisibility(View.VISIBLE);
        }

        @Override
        public void onLoadResource(WebView view, String url) {
            if (funcParam != null) {
                view.loadUrl("javascript: run(" + funcParam + ");");
                funcParam = null;
            }
            else {
                view.loadUrl("javascript: run(null);");
            }
        }
    }

    private void setClipboard(Context context, String text) {
        if (android.os.Build.VERSION.SDK_INT < android.os.Build.VERSION_CODES.HONEYCOMB) {
            android.text.ClipboardManager clipboard = (android.text.ClipboardManager) context.getSystemService(Context.CLIPBOARD_SERVICE);
            clipboard.setText(text);
        } else {
            android.content.ClipboardManager clipboard = (android.content.ClipboardManager) context.getSystemService(Context.CLIPBOARD_SERVICE);
            android.content.ClipData clip = android.content.ClipData.newPlainText("Copied Text", text);
            clipboard.setPrimaryClip(clip);
        }
    }

    // unset focus on searchBox when we click other side
    @Override
    public boolean dispatchTouchEvent(MotionEvent event) {
        if (event.getAction() == MotionEvent.ACTION_DOWN) {
            View v = getCurrentFocus();
            if (v instanceof EditText) {
                Rect outRect = new Rect();
                v.getGlobalVisibleRect(outRect);
                if (!outRect.contains((int) event.getRawX(), (int) event.getRawY())) {
                    v.clearFocus();
                    InputMethodManager imm = (InputMethodManager) getSystemService(Context.INPUT_METHOD_SERVICE);
                    imm.hideSoftInputFromWindow(v.getWindowToken(), 0);
                }
            }
        }
        return super.dispatchTouchEvent(event);
    }

    public class MyJavascriptInterface {
        @JavascriptInterface
        public void getHTML(String html) {
            saveHTML = html;
        }

        @JavascriptInterface
        public void saveFunction(final String str) {
            handler.post(new Runnable() {
                @Override
                public void run() {
                    mWebView.setVisibility(View.VISIBLE);

                    System.out.println("save:" +str);

                    // handle를 통해서 화면에 접근하는 것임으로 가능함

                    mPrevious = mNow;
                    mNow = new ArrayList<> ();
                    mNow.add(mWebView.getUrl());
                    mNow.add(str);

                    if (!mBackStack.isEmpty() && ((ArrayList)mBackStack.peek()).get(1).equals(str)) {
                        return;
                    }
                    mBackStack.push(mNow);
                    System.out.println("mBackStack: "+mBackStack);

                    if (clearNextStack) mNextStack.clear();
                    clearNextStack = true;

                    gson = new Gson();
                    myFavoritesToString = gson.toJson(myFavorites);
                    System.out.println("fav: "+myFavoritesToString);
                    System.out.println("now: "+mNow.toString());

                    ImageButton button = findViewById(R.id.favorite2);
                    for (int i = 1; i < myFavorites.size(); i++) {
                        if (myFavorites.get(i).getBackStack().peek().equals(mNow)) {
                            System.out.println("here4"+i);
                            button.setImageResource(R.drawable.icon_favorite_selected);
                            button.setTag("Clicked");
                            button.setContentDescription("즐겨찾기 추가됨");
                            Toast.makeText(getApplication(), "즐겨찾기 추가됨", Toast.LENGTH_LONG);
                            return;
                        }
                    }
                    button.setImageResource(R.drawable.icon_favorite);
                    button.setTag("notClicked");
                    button.setContentDescription("즐겨찾기 추가하기");
                    Toast.makeText(getApplication(), "즐겨찾기 추가하기", Toast.LENGTH_LONG);
                }
            });
        }

        @JavascriptInterface
        public void saveTitle(final String _titleName) {
            titleName = _titleName;
        }

        @JavascriptInterface
        public void checkError(final String error) {
            System.out.println("MainActivity - checkError - " + error);
        }
    }

    public String readJsFile(int filename) {
        String result = "";
        InputStream txtResource = getResources().openRawResource(filename);
        ByteArrayOutputStream byteArrayOutputStream = new ByteArrayOutputStream();

        int i;
        try {
            i = txtResource.read();
            while (i != -1) {
                byteArrayOutputStream.write(i);
                i = txtResource.read();
            }
            result = new String(byteArrayOutputStream.toByteArray(), "UTF-8");
            txtResource.close();
        } catch (IOException e) {
            e.printStackTrace();
        }

        return result.trim();
    }

    public String news() {
        if (mWebView.getUrl().contains("entertain.naver.com")||
                mWebView.getUrl().contains("news.naver.com/entertain") ||
                mWebView.getUrl().contains("tv.naver.com")) {
            return readJsFile(R.raw.entertain_mod);
        } else if (mWebView.getUrl().contains("news.naver.com")) {
            return readJsFile(R.raw.news_mod);
        } else if (mWebView.getUrl().contains("sports.naver.com")) {
            return readJsFile(R.raw.sports_mod);
        } else if (mWebView.getUrl().contains("shopping.naver.com") ||
                mWebView.getUrl().contains("pay.naver.com") ||
                mWebView.getUrl().contains("smartstore.naver.com")) {
            return readJsFile(R.raw.shopping_mod);
        }

        return "console.log(\"error\");";
    }

    public String news_with_param(String func) {
        if (mWebView.getUrl().contains("entertain.naver.com")||
            mWebView.getUrl().contains("news.naver.com/entertain") ||
            mWebView.getUrl().contains("tv.naver.com")) {
            return readJsFile(R.raw.entertain_mod) + "run(" + func + ");";
        }
        if (mWebView.getUrl().contains("news.naver.com")) {
            return readJsFile(R.raw.news_mod) + "run(" + func + ");";
        } else if (mWebView.getUrl().contains("sports.naver.com")) {
            return readJsFile(R.raw.sports_mod) + "run(" + func + ");";
        } else if (mWebView.getUrl().contains("shopping.naver.com") ||
                mWebView.getUrl().contains("pay.naver.com") ||
                mWebView.getUrl().contains("smartstore.naver.com")) {
            return readJsFile(R.raw.shopping_mod) + "run(" + func + ");";
        }

        return "console.log(\"error\");";
    }

    public void toHome() {
        Intent intent = new Intent(this, HomeMenu.class);
        startActivity(intent);
        isLogin = "home";
    }

    public void toNotLogin() {
        mWebView.loadUrl(myUrl);
    }

    @Override
    public void onClick(View v) {
        int id = v.getId();
        ArrayList <String> str;

        //navigation-bar
        switch (id) {

            case R.id.goback2:
                clearNextStack = false;
                if (mBackStack.isEmpty()) break;

                str= (ArrayList) mBackStack.pop();
                mNextStack.push(str);

                if (mBackStack.isEmpty()) break;
                mNow = (ArrayList) mBackStack.pop();
                funcParam = mNow.get(1);

                System.out.println("MainActivity.java - goback2");
                System.out.println("mBackStack" + mBackStack);
                System.out.println("mNextStack" + mNextStack);
                System.out.println("mNow" + mNow);

                mWebView.loadUrl(mNow.get(0));
                break;

            case R.id.goforward2:
                clearNextStack = false;
                if (mNextStack.isEmpty()) break;

                str = (ArrayList) mNextStack.pop();
                funcParam = str.get(1);

                mWebView.loadUrl(str.get(0));
                break;

            case R.id.chatbot2:
                //mWebView.loadUrl("javascript:window.Android.getHTML('<html>'+document.getElementsByTagName('html')[0].innerHTML+'</html>');");
                setClipboard(this, mBackStack.peek().toString());
                startActivity(new Intent(Intent.ACTION_VIEW, Uri.parse("http://pf.kakao.com/_GgMFT/chat")));
                break;

            case R.id.favorite2:
                if (v.getTag().equals("notClicked")) {
                    ((ImageButton) v).setImageResource(R.drawable.icon_favorite_selected);
                    v.setTag("Clicked");
                    v.setContentDescription("즐겨찾기 추가됨");
                    Toast.makeText(getApplication(), "즐겨찾기가 추가되었습니다.", Toast.LENGTH_LONG);

                    boolean errorCheck = false;
                    for (int i = 1; i < myFavorites.size(); i++) {
                        if (myFavorites.get(i).getBackStack().peek().equals(mNow)) {
                            errorCheck = true;
                        }
                    }

                    if (!errorCheck) myFavorites.add(new FavoriteList((titleName), (Stack)mBackStack.clone()));
                    gson = new Gson();
                    myFavoritesToString = gson.toJson(myFavorites);
                    System.out.println(myFavoritesToString);
                } else {

                    System.out.println("fav: "+myFavorites);
                    ((ImageButton) v).setImageResource(R.drawable.icon_favorite);
                    v.setTag("notClicked");
                    v.setContentDescription("즐겨찾기 추가하기");
                    Toast.makeText(getApplication(), "즐겨찾기가 해제되었습니다.", Toast.LENGTH_LONG);

                    for (int i = 1; i < myFavorites.size(); i++) {
                        if (myFavorites.get(i).getBackStack().peek().equals(mNow)) {
                            myFavorites.remove(myFavorites.get(i));
                            break;
                        }
                    }

                    gson = new Gson();
                    myFavoritesToString = gson.toJson(myFavorites);
                    System.out.println(myFavoritesToString);
                }
                break;

            case R.id.viewMore2:
                //showMoreActionBar();

                SharedPreferences sharedPreferences = getSharedPreferences("sFile", MODE_PRIVATE);
                SharedPreferences.Editor editor = sharedPreferences.edit();
                editor.putString("isLogin", "home");

                myFavorites.get(0).setTitle("blank");
                tempStack.clear();
                tempStack.push(Arrays.asList("blank", "blank"));
                myFavorites.get(0).setBackStack(tempStack);

                gson = new Gson();
                myFavoritesToString = gson.toJson(myFavorites);
                editor.putString("favorite", myFavoritesToString);

                editor.commit();

                Intent intent2 = new Intent(this, HomeMenu.class);
                gson = new Gson();
                myFavoritesToString = gson.toJson(myFavorites);
                intent2.putExtra("favorite", myFavoritesToString);
                setResult(Activity.RESULT_OK, intent2);
                finish();

                break;

        }
    }
}