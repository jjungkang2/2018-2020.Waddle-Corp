package com.example.ands;

import androidx.appcompat.app.ActionBar;
import androidx.appcompat.app.AppCompatActivity;

import android.app.Activity;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Build;
import android.os.Bundle;
import android.view.Gravity;
import android.view.View;
import android.view.inputmethod.InputMethodManager;
import android.webkit.CookieSyncManager;
import android.widget.Button;
import android.widget.EditText;

import com.google.gson.Gson;
import com.google.gson.reflect.TypeToken;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Stack;

public class HomeMenu extends AppCompatActivity implements View.OnClickListener {

    //favorite thing
    private ArrayList<FavoriteList> myFavorites= new ArrayList<>();
    private String myFavoritesToString;
    private Stack tempStack = new Stack();
    private Gson gson;
    private Button button00;
    private Button button01;
    private Button button02;
    private Button button03;
    private Button button04;
    private Button button05;
    private Button button06;
    private Button button07;
    private Button button08;
    private Button button09;

    //searchBox thing
    private EditText searchBox;
    private Button cancleBox;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        setContentView(R.layout.activity_home);

        //ActionBar thing
        ActionBar actionbar = getSupportActionBar();
        actionbar.hide();

        //searchBox thing
        searchBox = findViewById(R.id.searchbox);
        cancleBox = findViewById(R.id.canclebox);
        initSearchBox();

        //favorite thing
        button00 = findViewById(R.id.button00);
        button01 = findViewById(R.id.button01);
        button02 = findViewById(R.id.button02);
        button03 = findViewById(R.id.button03);
        button04 = findViewById(R.id.button04);
        button05 = findViewById(R.id.button05);
        button06 = findViewById(R.id.button06);
        button07 = findViewById(R.id.button07);
        button08 = findViewById(R.id.button08);
        button09 = findViewById(R.id.button09);

        //cookie thing
        if (Build.VERSION.SDK_INT < Build.VERSION_CODES.LOLLIPOP) {
            CookieSyncManager.createInstance(this);
        }
        //저장된 값을 불러오기 위해 같은 네임파일을 찾음.
        SharedPreferences sf = getSharedPreferences("sFile",MODE_PRIVATE);

        gson = new Gson();
        myFavoritesToString = sf.getString("favorite", "null");
        myFavorites = gson.fromJson( myFavoritesToString, new TypeToken<ArrayList<FavoriteList>>(){}.getType());

        if (myFavorites==null || myFavorites.size()==0){
            myFavorites = new ArrayList<>();

            tempStack.clear();
            tempStack.push(new ArrayList<>(Arrays.asList("blank", "blank")));
            myFavorites.add(new FavoriteList("blank", tempStack));

            tempStack.clear();
            tempStack.push(new ArrayList<>(Arrays.asList("https://m.news.naver.com/", "mainFunc.init")));
            myFavorites.add(new FavoriteList("네이버 뉴스", tempStack));
        }
        updateMyFavorites();
    }


    @Override
    protected void onStop() {
        super.onStop();

        SharedPreferences sharedPreferences = getSharedPreferences("sFile",MODE_PRIVATE);
        SharedPreferences.Editor editor = sharedPreferences.edit();
        editor.putString("isLogin", "home");

        gson = new Gson();
        myFavoritesToString = gson.toJson(myFavorites);
        editor.putString("favorite", myFavoritesToString);

        editor.commit();
    }


    public void initSearchBox(){
        cancleBox.setVisibility(View.GONE);

        searchBox.setOnFocusChangeListener(new View.OnFocusChangeListener() {

            public void onFocusChange(View v, boolean gainFocus) {
                if (gainFocus) {
                    v.setBackgroundResource(R.drawable.search_clicked);
                    ((EditText) v).setGravity(Gravity.LEFT);
                    ((EditText) v).setGravity(Gravity.CENTER_VERTICAL);
                    v.setPadding(30, 0, 30, 0);

                    cancleBox.setVisibility(View.VISIBLE);
                }
                else {
                    InputMethodManager immhide = (InputMethodManager) getSystemService(Activity.INPUT_METHOD_SERVICE);
                    immhide.toggleSoftInput(InputMethodManager.HIDE_IMPLICIT_ONLY, 0);
                    v.setBackgroundResource(R.drawable.search_notclicked);
                    ((EditText) v).setGravity(Gravity.CENTER);
                    v.setPadding(0, 0, 0, 0);

                    cancleBox.setVisibility(View.GONE);
                }
            }
        });
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        myFavorites.clear();

        if (data!=null && data.hasExtra("favorite")){
            gson = new Gson();
            myFavoritesToString = data.getStringExtra("favorite");
            myFavorites = gson.fromJson(myFavoritesToString, new TypeToken<ArrayList<FavoriteList>>(){}.getType());
        }

        System.out.println(myFavoritesToString);
        updateMyFavorites();
    }

    public void updateMyFavorites(){
        System.out.println("size: "+myFavorites.size() );
        if (myFavorites.size()>2){
            button01.setVisibility(View.VISIBLE);
            button01.setText(myFavorites.get(2).getTitle());
        }
        else button01.setVisibility(View.GONE);
        if (myFavorites.size()>3){
            button02.setVisibility(View.VISIBLE);
            button02.setText(myFavorites.get(3).getTitle());
        }
        else button02.setVisibility(View.GONE);
        if (myFavorites.size()>4){
            button03.setVisibility(View.VISIBLE);
            button03.setText(myFavorites.get(4).getTitle());
        }
        else button03.setVisibility(View.GONE);
        if (myFavorites.size()>5){
            button04.setVisibility(View.VISIBLE);
            button04.setText(myFavorites.get(5).getTitle());
        }
        else button04.setVisibility(View.GONE);
        if (myFavorites.size()>6){
            button05.setVisibility(View.VISIBLE);
            button05.setText(myFavorites.get(6).getTitle());
        }
        else button05.setVisibility(View.GONE);
        if (myFavorites.size()>7){
            button06.setVisibility(View.VISIBLE);
            button06.setText(myFavorites.get(7).getTitle());
        }
        else button06.setVisibility(View.GONE);
        if (myFavorites.size()>8){
            button07.setVisibility(View.VISIBLE);
            button07.setText(myFavorites.get(8).getTitle());
        }
        else button07.setVisibility(View.GONE);
        if (myFavorites.size()>9){
            button08.setVisibility(View.VISIBLE);
            button08.setText(myFavorites.get(9).getTitle());
        }
        else button08.setVisibility(View.GONE);
        if (myFavorites.size()>10) {
            button09.setVisibility(View.VISIBLE);
            button09.setText(myFavorites.get(10).getTitle());
        }
        else button09.setVisibility(View.GONE);
    }

    @Override
    public void onClick(View v) {
        int id = v.getId();

        switch (id){
            case R.id.button00:
            case R.id.button10:
                myFavorites.get(0).setTitle("네이버 뉴스");
                tempStack.clear();
                tempStack.push(Arrays.asList("https://m.news.naver.com/", "map_init"));
                myFavorites.get(0).setBackStack(tempStack);
                break;

            case R.id.button01:
                myFavorites.get(0).setTitle(myFavorites.get(2).getTitle());
                myFavorites.get(0).setBackStack(myFavorites.get(2).getBackStack());
                break;

            case R.id.button02:
                myFavorites.get(0).setTitle(myFavorites.get(3).getTitle());
                myFavorites.get(0).setBackStack(myFavorites.get(3).getBackStack());
                break;

            case R.id.button03:
                myFavorites.get(0).setTitle(myFavorites.get(4).getTitle());
                myFavorites.get(0).setBackStack(myFavorites.get(4).getBackStack());
                break;

            case R.id.button04:
                myFavorites.get(0).setTitle(myFavorites.get(5).getTitle());
                myFavorites.get(0).setBackStack(myFavorites.get(5).getBackStack());
                break;

            case R.id.button05:
                myFavorites.get(0).setTitle(myFavorites.get(6).getTitle());
                myFavorites.get(0).setBackStack(myFavorites.get(6).getBackStack());
                break;

            case R.id.button06:
                myFavorites.get(0).setTitle(myFavorites.get(7).getTitle());
                myFavorites.get(0).setBackStack(myFavorites.get(7).getBackStack());
                break;

            case R.id.button07:
                myFavorites.get(0).setTitle(myFavorites.get(8).getTitle());
                myFavorites.get(0).setBackStack(myFavorites.get(8).getBackStack());
                break;

            case R.id.button08:
                myFavorites.get(0).setTitle(myFavorites.get(9).getTitle());
                myFavorites.get(0).setBackStack(myFavorites.get(9).getBackStack());
                break;

            case R.id.button09:
                myFavorites.get(0).setTitle(myFavorites.get(10).getTitle());
                myFavorites.get(0).setBackStack(myFavorites.get(10).getBackStack());
                break;

            case R.id.button11:
                System.out.println("HomeMenu.java - button11 Clicked");
                myFavorites.get(0).setTitle("네이버 쇼핑");
                tempStack.clear();
                tempStack.push(Arrays.asList("https://m.shopping.naver.com/", ""));
                myFavorites.get(0).setBackStack(tempStack);
                break;

            case R.id.button12:
                System.out.println("HomeMenu.java - button12 Clicked");
                myFavorites.get(0).setTitle("네이버 스포츠");
                tempStack.clear();
                tempStack.push(Arrays.asList("https://m.sports.naver.com/", "map_init"));
                myFavorites.get(0).setBackStack(tempStack);
                break;

            case R.id.button13:
                myFavorites.get(0).setTitle("네이버 연예");
                tempStack.clear();
                tempStack.push(Arrays.asList("https://m.entertain.naver.com/", ""));
                myFavorites.get(0).setBackStack(tempStack);
                break;

            default:
                myFavorites.get(0).setTitle("blank");
                tempStack.clear();
                tempStack.push(Arrays.asList("blank", "blank"));
                myFavorites.get(0).setBackStack(tempStack);
                break;
        }

        Intent intent = new Intent(this, MainActivity.class);
        gson = new Gson();
        myFavoritesToString = gson.toJson(myFavorites);
        intent.putExtra("favorite", myFavoritesToString);
        intent.putExtra("isLogin", "login");
        startActivityForResult(intent, 1111);
    }
}
