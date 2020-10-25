package com.example.ands;

import android.os.Parcel;

import java.util.Stack;

public class FavoriteList{

    private String title;
    private Stack backStack;

    protected FavoriteList(Parcel in) {
    }

    public FavoriteList(String _title, Stack _backStack){
        this.title = _title;
        this.backStack = _backStack;
    }

    public String getTitle() {
        return title;
    }

    public void setTitle(String _title) {
        this.title = _title;
    }

    public Stack getBackStack() { return backStack; }

    public void setBackStack(Stack _backStack) { this.backStack = _backStack; }
}
