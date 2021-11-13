package com.lukas.display.model;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import com.lukas.display.form.GeneralForm;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.io.Writer;
import java.lang.reflect.Modifier;
import java.nio.file.Files;
import java.nio.file.Paths;

public class User {

    transient Logger logger = LoggerFactory.getLogger(User.class);

    private String iCalString;
    private float lat;
    private float lon;

    transient Gson gson;

    public static final String FILE = "data.dis";

    public User() {
        gson = new GsonBuilder().setPrettyPrinting().excludeFieldsWithModifiers(Modifier.TRANSIENT, Modifier.STATIC).create();
    }

    public String getiCalString() {
        return iCalString;
    }

    public float getLat() {
        return lat;
    }

    public float getLon() {
        return lon;
    }

    public void update(GeneralForm form) {
        this.lon = form.getLon();
        this.lat = form.getLat();
        this.iCalString = form.getiCal();
        save();
    }

    private boolean save() {
        try {
            Writer writer = Files.newBufferedWriter(Paths.get(FILE));
            gson.toJson(this, writer);
            writer.close();
            logger.info("Successfully saved user data:\n" + gson.toJson(this));
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
