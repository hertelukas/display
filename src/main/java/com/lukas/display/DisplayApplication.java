package com.lukas.display;

import com.lukas.display.model.User;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class DisplayApplication {

    private static User user;
    private static boolean initialized;

    public static void main(String[] args) {
        SpringApplication.run(DisplayApplication.class, args);


        user = User.load();
        initialized = user != null;

    }

    public static boolean isInitialized() {
        return initialized;
    }

    public static void setUser(User user) {
        DisplayApplication.user = user;
        user.save();
    }
}
