package com.lukas.display.model;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;

public class User {

    Logger logger = LoggerFactory.getLogger(User.class);

    private String iCalString;
    private float lat;
    private float lon;

    Gson gson;

    public static final String FILE = "data.dis";

    public User() {
        gson = new GsonBuilder().setPrettyPrinting().create();
    }

    public boolean save() {
        try {
            gson.toJson(this, new FileWriter(FILE));
            logger.info("Successfully saved user data");
            return true;
        } catch (IOException e) {
            logger.warn("Failed to store user data: " + e.getMessage());
            return false;
        }
    }

    /**
     * Load a user from memory
     *
     * @return Returns the user profile or null if none exists
     */
    public static User load() {
        try {
            User result = new Gson().fromJson(new FileReader(FILE), User.class);
            System.out.println(result);
            return result;
        } catch (IOException e) {
            return null;
        }
    }

    @Override
    public String toString() {
        return "User{" +
                "iCalString='" + iCalString + '\'' +
                ", lat=" + lat +
                ", lon=" + lon +
                '}';
    }
}
